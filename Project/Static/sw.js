const CACHE_NAME = 'citymender-v2';
const OFFLINE_REPORTS = 'offline-reports';

// Cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => {
      return cache.addAll([
        '/',
        '/static/css/main.css',
        '/static/js/main.js',
        '/static/js/location-selector.js'
      ]);
    })
  );
});

// Handle fetch with offline fallback
self.addEventListener('fetch', event => {
  // API calls for report submission
  if (event.request.url.includes('/api/reports/') && event.request.method === 'POST') {
    event.respondWith(
      fetch(event.request).catch(() => {
        // Queue for later sync when online
        return caches.match('/offline-success.html');
      })
    );
  }
});

// Background sync for queued reports
self.addEventListener('sync', event => {
  if (event.tag === 'sync-reports') {
    event.waitUntil(syncQueuedReports());
  }
});

async function syncQueuedReports() {
  // Logic to send queued reports when back online
  const db = await openDatabase();
  const reports = await db.getAll(OFFLINE_REPORTS);
  
  for (const report of reports) {
    try {
      await fetch('/api/reports/', {
        method: 'POST',
        body: JSON.stringify(report),
        headers: {'Content-Type': 'application/json'}
      });
      await db.delete(OFFLINE_REPORTS, report.id);
    } catch (error) {
      console.log('Sync failed, will retry:', error);
    }
  }
}