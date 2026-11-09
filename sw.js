const CACHE_NAME = 'polyglot-riff-studio-v3.4';
const PRECACHE_URLS = [
  './index.html',
  './polyglot_api_client.js',
  './regional_lyric_flashcards.html',
  './polyglot_audio_rhythm_studio_v4_5.html',
  './polyglot_riff_studio_v3_1_atelier_edition.html',
  './czech_register_switcher_widget.html',
  './polyglot_riff_studio_v3_0_neo4j_srs_heatmap.html',
  './polyglot_riff_studio_v1_zero_corporate.html',
  './db/polyglot_fabric.db.json',
  './db/cz_ova.db.json',
  './db/at_vie.db.json',
  './db/ru_ala.db.json',
  './db/en_yyc.db.json',
  './db/es_sot.db.json'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(PRECACHE_URLS).catch(() => {}))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Network-first for API requests
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(req).catch(() => caches.match(req))
    );
    return;
  }

  // Stale-while-revalidate for Studio HTML, JS, and .db.json shards
  event.respondWith(
    caches.match(req).then((cached) => {
      const networkFetch = fetch(req)
        .then((res) => {
          if (res && res.status === 200) {
            const copy = res.clone();
            caches.open(CACHE_NAME).then((c) => c.put(req, copy)).catch(() => {});
          }
          return res;
        })
        .catch(() => cached);
      return cached || networkFetch;
    })
  );
});

