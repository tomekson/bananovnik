const CACHE = 'bananovnik-v9.85';
const CORE = ['./', './index.html', './manifest.json', './favicon.svg', './icon-180.png'];
const TEST_FILES = ['./tests/pravo-v-praxi.json', './tests/belbin.json', './tests/inovace.json', './tests/manazerska-ekonomie.json', './tests/komunikace.json', './tests/management.json', './tests/management-stare.json', './tests/manazerske-dovednosti.json', './tests/anglicky-jazyk.json', './tests/projektove-rizeni.json'];

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
function networkRequest(req) {
  if (req.method !== 'GET' || new URL(req.url).origin !== self.location.origin) return req;
  if (req.mode === 'navigate') return new Request(req.url, { cache: 'no-cache', credentials: 'same-origin' });
  return new Request(req, { cache: 'no-cache' });
}

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(networkRequest(e.request)).then(res => {
      const clone = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, clone));
      return res;
    }).catch(() => caches.match(e.request))
  );
});
