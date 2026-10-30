const CACHE = 'bananovnik-v10.66';
const CORE = ['./', './index.html', './manifest.json', './favicon.svg', './icon-180.png'];
const TEST_FILES = ['./tests/management-lidskych-zdroju.json', './tests/inovace-prednaska-2026-10-17.json', './tests/pravo-v-praxi.json', './tests/belbin.json', './tests/inovace.json', './tests/manazerska-ekonomie.json', './tests/komunikace.json', './tests/management.json', './tests/management-stare.json', './tests/manazerske-dovednosti.json', './tests/anglicky-jazyk.json', './tests/projektove-rizeni.json'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE)
      // cache: 'reload' = stáhnout ze sítě, ne z HTTP cache prohlížeče (GitHub Pages má max-age=600)
      .then(c => c.addAll([...CORE, ...TEST_FILES].map(u => new Request(u, { cache: 'reload' }))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Síť napřed. U vlastních souborů s revalidací (no-cache), aby HTTP cache prohlížeče
// nevracela až 10 minut starou verzi; když síť nejde, odpověď z cache service workeru.
// Při slabém signálu fetch nespadne, ale visí (iOS ho drží desítky sekund a PWA zůstane bílá),
// proto po NETWORK_TIMEOUT ms odpovíme z cache a síťový požadavek jen dál obnoví cache.
const NETWORK_TIMEOUT = 3000;

function networkRequest(req) {
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return req;
  if (req.mode === 'navigate') return new Request(req.url, { cache: 'no-cache', credentials: 'same-origin' });
  return new Request(req, { cache: 'no-cache' });
}

// Testy se načítají s ?v=<verze>, precache je bez parametru: hledáme proto bez query.
// Navigace (i s ?test=… ze sdíleného odkazu) spadne na uložený index.html.
async function fromCache(req) {
  const hit = await caches.match(req, { ignoreSearch: true });
  if (hit) return hit;
  if (req.mode === 'navigate') return (await caches.match('./index.html')) || (await caches.match('./'));
  return undefined;
}

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  // Audio a PDF v media/ jdou rovnou ze sítě: streamování s Range požadavky, desítky MB do cache nepatří.
  if (new URL(req.url).pathname.includes('/media/')) return;
  const network = fetch(networkRequest(req));
  // Uložení do cache doběhne i po odpovědi z cache (timeout); clone dřív, než se tělo přečte.
  e.waitUntil(network.then(res => {
    if (!res.ok || new URL(req.url).origin !== self.location.origin) return;
    const clone = res.clone();
    return caches.open(CACHE).then(c => c.put(req, clone));
  }).catch(() => {}));
  e.respondWith(new Promise(resolve => {
    let done = false;
    const fallback = () => fromCache(req).then(hit => {
      if (done) return;
      if (hit) { done = true; resolve(hit); }
    });
    const timer = setTimeout(fallback, NETWORK_TIMEOUT);
    network.then(res => {
      clearTimeout(timer);
      if (!done) { done = true; resolve(res); }
    }).catch(() => {
      clearTimeout(timer);
      fromCache(req).then(hit => {
        if (done) return;
        done = true;
        resolve(hit || Response.error());
      });
    });
  }));
});
