// Service worker da PWA do iTOEFL.
//
// Fonte: app/sw.js. O build.py troca __BUILD_VERSION__ por um hash de tudo que
// vai para o pré-cache e grava em artifact/sw.js. Cada build com conteúdo novo
// produz um sw.js diferente, o navegador instala a versão nova em espera e o
// app.js mostra "Nova versão disponível". Só ao clicar em recarregar a nova
// assume (mensagem SKIP_WAITING), para não trocar o site no meio de um estudo.
//
// Estratégias:
// - Arquivos do próprio site (index, páginas legais, manifesto, ícones):
//   pré-cache na instalação, servidos do cache. Funciona offline.
// - Fontes do Google e a biblioteca do Supabase (CDN): cache em tempo de uso
//   (stale-while-revalidate), para o site abrir offline depois da 1ª visita.
// - API do Supabase (login, sync, pagamento), áudio e vídeo: sempre rede,
//   nunca cache. Progresso offline continua indo pro localStorage e o sync
//   empurra quando a conexão volta.

var VERSION = "__BUILD_VERSION__";
var CACHE = "itoefl-" + VERSION;
var RUNTIME = "itoefl-runtime-v1";

// Se um destes faltar no servidor a instalação inteira falha, então a lista
// só tem o que o build.py grava em artifact/ (o smoke test confere). A raiz
// "./" fica de fora de propósito: nem todo servidor devolve o index nela.
var PRECACHE = [
  "./index.html",
  "./termos.html",
  "./privacidade.html",
  "./manifest.json",
  "./icons/icon-192.png",
  "./icons/icon-512.png"
];

var RUNTIME_HOSTS = ["fonts.googleapis.com", "fonts.gstatic.com", "cdn.jsdelivr.net"];

self.addEventListener("install", function(event){
  event.waitUntil(
    caches.open(CACHE).then(function(cache){
      // cache: "reload" ignora o cache HTTP, garante a versão recém-publicada
      return cache.addAll(PRECACHE.map(function(u){ return new Request(u, { cache: "reload" }); }));
    })
  );
});

self.addEventListener("activate", function(event){
  event.waitUntil(
    caches.keys().then(function(keys){
      return Promise.all(keys.map(function(k){
        if(k !== CACHE && k !== RUNTIME && k.indexOf("itoefl-") === 0) return caches.delete(k);
      }));
    }).then(function(){ return self.clients.claim(); })
  );
});

self.addEventListener("message", function(event){
  if(event.data === "SKIP_WAITING") self.skipWaiting();
});

self.addEventListener("fetch", function(event){
  var req = event.request;
  if(req.method !== "GET") return;
  var url = new URL(req.url);

  // mesmo site: cache primeiro (o que está no cache é exatamente a versão
  // deste service worker). ignoreSearch porque a volta do login e do
  // pagamento chega com parâmetros na URL. A raiz da pasta recebe o
  // index.html do cache; outra página fora do cache vai à rede e só cai no
  // index.html se estiver offline.
  if(url.origin === self.location.origin){
    event.respondWith(
      caches.open(CACHE).then(function(cache){
        return cache.match(req, { ignoreSearch: true }).then(function(hit){
          if(hit) return hit;
          if(req.mode !== "navigate") return fetch(req);
          if(url.pathname.slice(-1) === "/"){
            return cache.match("./index.html").then(function(index){ return index || fetch(req); });
          }
          return fetch(req).catch(function(){ return cache.match("./index.html"); });
        });
      })
    );
    return;
  }

  if(RUNTIME_HOSTS.indexOf(url.hostname) !== -1){
    event.respondWith(
      caches.open(RUNTIME).then(function(cache){
        return cache.match(req).then(function(hit){
          var net = fetch(req).then(function(res){
            if(res && (res.ok || res.type === "opaque")) cache.put(req, res.clone());
            return res;
          }).catch(function(){ return hit; });
          return hit || net;
        });
      })
    );
  }
  // demais origens (Supabase, Mercado Pago, YouTube): sem interceptar
});
