(function () {
  var CONSENT_KEY = 'switchere_consent';
  function hasConsent(){ try { return localStorage.getItem(CONSENT_KEY) === '1'; } catch(e){ return false; } }
  function showConsent() {
    if (document.getElementById('sc-consent')) return;
    var el = document.createElement('div'); el.id='sc-consent';
    el.innerHTML = '<div class="sc-consent-box"><div class="sc-consent-text">We use cookies and third-party advertising to keep Switchere Club free. <a href="/privacypolicy.html">Privacy Policy</a>.</div><div class="sc-consent-actions"><button id="sc-consent-ok" class="sc-btn sc-btn-primary">Accept</button><button id="sc-consent-no" class="sc-btn">Decline</button></div></div>';
    el.style.cssText='position:fixed;left:0;right:0;bottom:0;z-index:99999;padding:12px;';
    el.querySelector('.sc-consent-box').style.cssText='max-width:720px;margin:0 auto;background:#0e1420;color:#e6e9ef;border:1px solid #2a3446;border-radius:14px;padding:16px 18px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;box-shadow:0 8px 30px rgba(0,0,0,.35);font-family:system-ui,sans-serif;font-size:14px;';
    el.querySelector('.sc-consent-text').style.cssText='flex:1 1 300px;line-height:1.5;';
    el.querySelector('.sc-consent-text a').style.cssText='color:#7dd3fc;text-decoration:underline;';
    el.querySelector('.sc-btn').style.cssText='padding:9px 16px;border-radius:8px;border:1px solid #3b4a63;background:transparent;color:#e6e9ef;cursor:pointer;font-size:14px;';
    el.querySelector('.sc-btn-primary').style.cssText='padding:9px 16px;border-radius:8px;border:none;background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;cursor:pointer;font-size:14px;font-weight:600;';
    el.querySelector('#sc-consent-ok').onclick=function(){try{localStorage.setItem(CONSENT_KEY,'1');}catch(e){}el.remove();initAds();};
    el.querySelector('#sc-consent-no').onclick=function(){try{localStorage.setItem(CONSENT_KEY,'0');}catch(e){}el.remove();};
    document.body.appendChild(el);
  }
  function injectScriptAt(el,src,async){var s=document.createElement('script');s.src=src;if(async)s.async='async';s.setAttribute('data-cfasync','false');el.appendChild(s);}
  function injectScriptHead(src,async){var s=document.createElement('script');s.src=src;if(async)s.async='async';s.setAttribute('data-cfasync','false');document.head.appendChild(s);}
  window.adsterra=window.adsterra||{};
  window.adsterra.activateBanner=function(el){
    if(!el||el.dataset.loaded)return; el.dataset.loaded='1';
    var key=el.getAttribute('data-key'); var w=parseInt(el.getAttribute('data-w')||'300',10); var h=parseInt(el.getAttribute('data-h')||'250',10);
    if(!key)return; el.innerHTML='';
    var os=document.createElement('script'); os.text="atOptions={'key':'"+key+"','format':'iframe','height':"+h+",'width':"+w+",'params':{}};"; el.appendChild(os);
    injectScriptAt(el,'https://www.highrevenueformat.com/'+key+'/invoke.js',true);
  };
  function initBanners(){
    var slots=document.querySelectorAll('[data-adsterra]');
    if(!('IntersectionObserver' in window)){slots.forEach(function(el){window.adsterra.activateBanner(el);});return;}
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){window.adsterra.activateBanner(e.target);io.unobserve(e.target);}});},{rootMargin:'250px'});
    slots.forEach(function(el){io.observe(el);});
  }
  function loadNative(){injectScriptHead('https://pl31197007.profitableratecpmnetwork.com/688c523c4b27897a1e1c95831a8f3ee7/invoke.js',true);}
  function loadSocialBar(){injectScriptHead('https://pl31196891.profitableratecpmnetwork.com/f5/86/c5/f586c502f00f0adba9d308c986acd3b6.js',false);}
  var POP_KEY='switchere_popunder';
  function loadPopunder(){try{var last=parseInt(localStorage.getItem(POP_KEY)||'0',10);var now=Date.now();if(now-last<120000)return;localStorage.setItem(POP_KEY,String(now));}catch(e){}injectScriptHead('https://pl31196890.profitableratecpmnetwork.com/8d/43/b2/8d43b22f6dc3a21677534e70935c81ac.js',true);}
  function initAds(){if(!hasConsent())return;loadPopunder();initBanners();loadNative();loadSocialBar();}
  function boot(){var cfg=window.SWITCHERE_ADS||{};if(cfg.consent===false){initAds();return;}if(!hasConsent()){showConsent();return;}initAds();}
  if(document.readyState==='loading'){document.addEventListener('DOMContentLoaded',boot);}else{boot();}
})();