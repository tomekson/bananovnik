const CACHE = 'bananovnik-v5.0';
const CORE = ['./', './index.html', './manifest.json', './favicon.svg', './icon-180.png', './tests/index.json'];

self.addEventListener('install', e => {
  e.waitUntil((async () => {
    const cache = await caches.open(CACHE);
    await cache.addAll(CORE);
    const reg = await fetch('./tests/index.json').then(r => r.json());
    const testFiles = reg.tests.map(t => './tests/' + t.file);
    await cache.addAll(testFiles);
    self.skipWaiting();
  })());
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    fetch(e.request).then(res => {
      const clone = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, clone));
      return res;
    }).catch(() => caches.match(e.request))
  );
});
