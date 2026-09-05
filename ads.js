(function () {
  var CONSENT_KEY = 'switchere_consent';
  function hasConsent(){ try { return localStorage.getItem(CONSENT_KEY) === '1'; } catch(e){ return false; } }
  function injectStyle(){
    if (document.getElementById('sc-consent-style')) return;
    var css = [
      "#sc-consent{position:fixed;left:0;right:0;bottom:0;z-index:999999;padding:14px;font-family:'Inter',system-ui,sans-serif;}",
      "#sc-consent .sc-box{max-width:760px;margin:0 auto;display:flex;align-items:center;gap:16px;background:linear-gradient(135deg,#151d2c,#1a2334);border:1px solid #263048;border-radius:16px;padding:18px 20px;box-shadow:0 20px 50px rgba(0,0,0,.5);backdrop-filter:blur(12px);}",
      "#sc-consent .sc-icon{flex:0 0 auto;width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;background:linear-gradient(135deg,#22c55e,#16a34a);}",
      "#sc-consent .sc-text{flex:1 1 320px;color:#e6e9ef;font-size:13.5px;line-height:1.55;}",
      "#sc-consent .sc-text strong{color:#fff;font-weight:700;}",
      "#sc-consent .sc-text a{color:#4facfe;text-decoration:underline;font-weight:600;}",
      "#sc-consent .sc-actions{flex:0 0 auto;display:flex;gap:8px;flex-wrap:wrap;}",
      "#sc-consent button{font-family:'Inter',system-ui,sans-serif;font-weight:600;font-size:13.5px;border-radius:10px;padding:10px 18px;cursor:pointer;transition:transform .15s,box-shadow .15s,background .15s;border:1px solid transparent;}",
      "#sc-consent button:hover{transform:translateY(-1px);}",
      "#sc-consent .sc-accept{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;box-shadow:0 6px 16px rgba(34,197,94,.3);}",
      "#sc-consent .sc-accept:hover{box-shadow:0 8px 22px rgba(34,197,94,.45);}",
      "#sc-consent .sc-decline{background:transparent;color:#cbd2e0;border:1px solid #3b4a63;}",
      "#sc-consent .sc-decline:hover{background:#1f2937;color:#fff;border-color:#4facfe;}",
      "@media(max-width:560px){#sc-consent .sc-box{flex-direction:column;align-items:flex-start;}#sc-consent .sc-actions{width:100%;}#sc-consent .sc-actions button{flex:1;}}"
    ].join("");
    var s = document.createElement('style'); s.id='sc-consent-style'; s.textContent=css; document.head.appendChild(s);
  }
  function showConsent() {
    if (document.getElementById('sc-consent')) return;
    injectStyle();
    var el = document.createElement('div'); el.id='sc-consent';
    el.innerHTML = '<div class="sc-box">'
      + '<div class="sc-icon">🍪</div>'
      + '<div class="sc-text"><strong>We value your privacy</strong> — Switchere Club uses cookies and third-party advertising to stay free. Read our <a href="/privacypolicy.html">Privacy Policy</a>.</div>'
      + '<div class="sc-actions"><button class="sc-accept" id="sc-consent-ok">Accept</button><button class="sc-decline" id="sc-consent-no">Decline</button></div>'
      + '</div>';
    document.body.appendChild(el);
    el.querySelector('#sc-consent-ok').onclick=function(){try{localStorage.setItem(CONSENT_KEY,'1');}catch(e){}el.remove();initAds();};
    el.querySelector('#sc-consent-no').onclick=function(){try{localStorage.setItem(CONSENT_KEY,'0');}catch(e){}el.remove();};
  }
  function injectScriptAt(el,src,async){var s=document.createElement('script');s.src=src;if(async)s.async='async';s.setAttribute('data-cfasync','false');el.appendChild(s);}
  function injectScriptHead(src,async){var s=document.createElement('script');s.src=src;if(async)s.async='async';s.setAttribute('data-cfasync','false');document.head.appendChild(s);}
  window.adsterra=window.adsterra||{};
  window.adsterra.activateBanner=function(el){
    if(!el||el.dataset.loaded)return; el.dataset.loaded='1';
    var key=el.getAttribute('data-key'); var w=parseInt(el.getAttribute('data-w')||'300',10); var h=parseInt(el.getAttribute('data-h')||'250',10);
    if(!key)return; el.innerHTML='';
    var os=document.createElement('script'); os.text="atOptions={'key':'"+key+"','format':'iframe','height':"+h+",'width':"+w+",'params':{}};"; el.appendChild(os);
    injectScriptAt(el,'https://www.profitableratecpmnetwork.com/'+key+'/invoke.js',true);
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
