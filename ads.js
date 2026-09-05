(function () {
  var CONSENT_KEY = 'switchere_consent';
  var POP_KEY = 'switchere_popunder';
  var NATIVE_CONTAINER = 'container-688c523c4b27897a1e1c95831a8f3ee7';

  function hasConsent(){ try { return localStorage.getItem(CONSENT_KEY) === '1'; } catch(e){ return false; } }

  // ---- Consent UI (modern, matches brand) ----
  function injectStyle(){
    if (document.getElementById('sc-consent-style')) return;
    var css = [
      "#sc-consent{position:fixed;left:0;right:0;bottom:0;z-index:999999;padding:14px;font-family:'Inter','Segoe UI',system-ui,sans-serif;}",
      "#sc-consent .sc-box{max-width:560px;margin:0 auto;display:flex;align-items:center;gap:16px;background:rgba(21,29,44,.98);border:1px solid #2a3446;border-radius:18px;padding:18px 20px;box-shadow:0 24px 60px rgba(0,0,0,.55);backdrop-filter:blur(14px);}",
      "#sc-consent .sc-icon{flex:0 0 auto;width:46px;height:46px;border-radius:13px;display:flex;align-items:center;justify-content:center;font-size:24px;background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;box-shadow:0 6px 16px rgba(34,197,94,.35);}",
      "#sc-consent .sc-text{flex:1 1 auto;color:#cbd2e0;font-size:13px;line-height:1.45;min-width:120px;}",
      "#sc-consent .sc-text strong{color:#fff;font-weight:700;display:block;margin-bottom:2px;font-size:14.5px;}",
      "#sc-consent .sc-text a{color:#4facfe;text-decoration:underline;font-weight:600;}",
      "#sc-consent .sc-text a:hover{color:#7cc4ff;}",
      "#sc-consent .sc-actions{flex:0 0 auto;display:flex;gap:10px;align-items:center;}",
      "#sc-consent button{font-family:'Inter','Segoe UI',system-ui,sans-serif;font-weight:700;font-size:13.5px;border-radius:11px;padding:11px 20px;cursor:pointer;transition:transform .15s,box-shadow .15s,background .15s,border-color .15s;line-height:1;}",
      "#sc-consent button:hover{transform:translateY(-1px);}",
      "#sc-consent button:active{transform:translateY(0);}",
      "#sc-consent .sc-accept{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;border:1px solid transparent;box-shadow:0 6px 16px rgba(34,197,94,.35);}",
      "#sc-consent .sc-accept:hover{box-shadow:0 8px 22px rgba(34,197,94,.5);background:linear-gradient(135deg,#25d264,#17ae4f);}",
      "#sc-consent .sc-decline{background:rgba(255,255,255,.04);color:#e6e9ef;border:1px solid #3b4a63;box-shadow:none;}",
      "#sc-consent .sc-decline:hover{background:#1f2937;color:#fff;border-color:#4facfe;box-shadow:0 4px 14px rgba(79,172,254,.18);}",
      "@media(max-width:600px){#sc-consent .sc-box{flex-direction:column;align-items:stretch;text-align:left;}#sc-consent .sc-actions{width:100%;}#sc-consent .sc-actions button{flex:1;}}"
    ].join("");
    var s = document.createElement('style'); s.id='sc-consent-style'; s.textContent=css; document.head.appendChild(s);
  }

  function showConsent() {
    if (document.getElementById('sc-consent')) return;
    injectStyle();
    var el = document.createElement('div'); el.id='sc-consent';
    el.innerHTML = '<div class="sc-box">'
      + '<div class="sc-icon">🍪</div>'
      + '<div class="sc-text">Cookies & ads keep Switchere Club free. <a href="/privacypolicy.html">Privacy Policy</a></div>'
      + '<div class="sc-actions"><button class="sc-accept" id="sc-consent-ok" type="button">Accept</button><button class="sc-decline" id="sc-consent-no" type="button">Decline</button></div>'
      + '</div>';
    document.body.appendChild(el);
    el.querySelector('#sc-consent-ok').onclick=function(){try{localStorage.setItem(CONSENT_KEY,'1');}catch(e){}el.remove();initAds();};
    el.querySelector('#sc-consent-no').onclick=function(){try{localStorage.setItem(CONSENT_KEY,'0');}catch(e){}el.remove();};
  }

  // ---- script injectors ----
  function injectAt(el,src,async){var s=document.createElement('script');s.src=src;if(async)s.async='async';s.setAttribute('data-cfasync','false');el.appendChild(s);}
  function injectHead(src,async){var s=document.createElement('script');s.src=src;if(async)s.async='async';s.setAttribute('data-cfasync','false');document.head.appendChild(s);}
  function injectBody(src,async){var s=document.createElement('script');s.src=src;if(async)s.async='async';s.setAttribute('data-cfasync','false');document.body.appendChild(s);}

  // ---- Banner (iframe format) — official Adsterra domain is highrevenueformat.com ----
  window.adsterra = window.adsterra || {};
  window.adsterra.activateBanner = function(el){
    if(!el || el.dataset.loaded) return;
    el.dataset.loaded = '1';
    var key = el.getAttribute('data-key');
    var w = parseInt(el.getAttribute('data-w')||'300',10);
    var h = parseInt(el.getAttribute('data-h')||'250',10);
    if(!key) return;
    el.removeAttribute('class');           // drop dashed placeholder styling
    el.style.minHeight = '0';
    el.style.border = 'none';
    el.style.background = 'transparent';
    el.style.textAlign = 'center';
    el.style.overflow = 'visible';
    el.style.margin = '16px auto';
    var os = document.createElement('script');
    os.text = "atOptions={'key':'"+key+"','format':'iframe','height':"+h+",'width':"+w+",'params':{}};";
    el.appendChild(os);
    injectAt(el, 'https://www.highrevenueformat.com/'+key+'/invoke.js', true);
  };

  function initBanners(){
    var slots = document.querySelectorAll('[data-adsterra]');
    if(!('IntersectionObserver' in window)){
      for(var i=0;i<slots.length;i++) window.adsterra.activateBanner(slots[i]);
      return;
    }
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ window.adsterra.activateBanner(e.target); io.unobserve(e.target); } });
    },{ rootMargin:'250px' });
    for(var j=0;j<slots.length;j++) io.observe(slots[j]);
  }

  // ---- Native Banner (official: invoke.js + container div) ----
  function loadNative(){
    if(document.getElementById(NATIVE_CONTAINER)) {
      injectHead('https://pl31197007.profitableratecpmnetwork.com/688c523c4b27897a1e1c95831a8f3ee7/invoke.js', true);
      return;
    }
    var c = document.createElement('div');
    c.id = NATIVE_CONTAINER;
    c.style.cssText = 'max-width:760px;margin:20px auto;';
    // inject container near top of body (after header if present)
    var main = document.querySelector('main') || document.body;
    main.parentNode.insertBefore(c, main);
    injectHead('https://pl31197007.profitableratecpmnetwork.com/688c523c4b27897a1e1c95831a8f3ee7/invoke.js', true);
  }

  // ---- Popunder (official: before </head>) ----
  function loadPopunder(){
    try {
      var last = parseInt(localStorage.getItem(POP_KEY)||'0',10);
      var now = Date.now();
      if(now-last < 120000) return;
      localStorage.setItem(POP_KEY, String(now));
    } catch(e){}
    injectHead('https://pl31196890.profitableratecpmnetwork.com/8d/43/b2/8d43b22f6dc3a21677534e70935c81ac.js', true);
  }

  // ---- Social Bar (official: above </body>) ----
  function loadSocialBar(){
    injectBody('https://pl31196891.profitableratecpmnetwork.com/f5/86/c5/f586c502f00f0adba9d308c986acd3b6.js', false);
  }

  function initAds(){
    if(!hasConsent()) return;
    loadPopunder();
    initBanners();
    loadNative();
    loadSocialBar();
  }

  function boot(){
    var cfg = window.SWITCHERE_ADS || {};
    if(cfg.consent === false){ initAds(); return; }
    if(!hasConsent()){ showConsent(); return; }
    initAds();
  }

  if(document.readyState === 'loading'){ document.addEventListener('DOMContentLoaded', boot); }
  else { boot(); }
})();
