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
      "@media(max-width:600px){#sc-consent .sc-box{flex-direction:column;align-items:stretch;text-align:left;}#sc-consent .sc-actions{width:100%;}#sc-consent .sc-actions button{flex:1;}}",
      "#sc-adblock{position:fixed;left:0;right:0;top:0;z-index:9999998;padding:14px;font-family:'Inter','Segoe UI',system-ui,sans-serif;}",
      "#sc-adblock .ab-box{max-width:600px;margin:0 auto;display:flex;align-items:center;gap:14px;background:rgba(21,29,44,.98);border:1px solid #2a3446;border-radius:16px;padding:16px 18px;box-shadow:0 24px 60px rgba(0,0,0,.55);backdrop-filter:blur(14px);}",
      "#sc-adblock .ab-icon{flex:0 0 auto;width:44px;height:44px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;background:linear-gradient(135deg,#4facfe,#2563eb);color:#fff;box-shadow:0 6px 16px rgba(79,172,254,.35);}",
      "#sc-adblock .ab-text{flex:1 1 auto;color:#cbd2e0;font-size:13px;line-height:1.45;min-width:120px;}",
      "#sc-adblock .ab-text strong{color:#fff;font-weight:700;display:block;margin-bottom:2px;font-size:14.5px;}",
      "#sc-adblock .ab-actions{flex:0 0 auto;display:flex;gap:8px;align-items:center;}",
      "#sc-adblock button{font-family:'Inter','Segoe UI',system-ui,sans-serif;font-weight:700;font-size:13px;border-radius:11px;padding:10px 16px;cursor:pointer;transition:transform .15s,box-shadow .15s,background .15s,border-color .15s;line-height:1;white-space:nowrap;}",
      "#sc-adblock .ab-ok{background:linear-gradient(135deg,#22c55e,#16a34a);color:#fff;border:1px solid transparent;box-shadow:0 6px 16px rgba(34,197,94,.35);}",
      "#sc-adblock .ab-later{background:rgba(255,255,255,.04);color:#e6e9ef;border:1px solid #3b4a63;box-shadow:none;}",
      "#sc-adblock .ab-later:hover{background:#1f2937;color:#fff;border-color:#4facfe;}",
      "@media(max-width:600px){#sc-adblock .ab-box{flex-direction:column;align-items:stretch;text-align:left;}#sc-adblock .ab-actions{width:100%;}#sc-adblock .ab-actions button{flex:1;}}"
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
    el.querySelector('#sc-consent-ok').onclick=function(){try{localStorage.setItem(CONSENT_KEY,'1');}catch(e){}el.remove();};
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
    // Banner invoke.js must load synchronously (no async) for the iframe ad to render.
    var s = document.createElement('script');
    s.src = 'https://www.highrevenueformat.com/'+key+'/invoke.js';
    s.setAttribute('data-cfasync','false');
    el.appendChild(s);
  };

  function initBanners(){
    var slots = document.querySelectorAll('[data-adsterra]');
    for(var i=0;i<slots.length;i++) window.adsterra.activateBanner(slots[i]);
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

  // ---- Adblock detection + friendly notice ----
  var AB_KEY = 'switchere_ab_asked';

  function abWasAsked(){
    try { return sessionStorage.getItem(AB_KEY) === '1'; } catch(e){ return false; }
  }
  function abMarkAsked(){
    try { sessionStorage.setItem(AB_KEY, '1'); } catch(e){}
  }

  // Bait: create a decoy ad container. Adblockers hide/remove elements matching
  // ad-like class names (.ad-slot, .adsbox, [class*="ad-"], #ad-banner, etc.).
  function adBlockDetected(){
    // PRIMARY, most reliable signal: did a real Adsterra banner actually render?
    // Adsterra invoke.js injects an <iframe> (or <ins>) into each [data-adsterra]
    // slot when it runs. If at least one real ad rendered, ads are NOT being blocked
    // for this user -> never show the notice (avoid false positives / annoying players).
    var slots = document.querySelectorAll('[data-adsterra]');
    var realAdRendered = false;
    for(var i=0;i<slots.length;i++){
      var sl = slots[i];
      if(sl.querySelector('iframe') || sl.querySelector('ins')){
        realAdRendered = true;
        break;
      }
    }
    // Also consider a global ad iframe (popunder/socialbar may add their own).
    if(!realAdRendered){
      var anyAd = document.querySelector('iframe[src*="highrevenueformat"], iframe[src*="profitableratecpmnetwork"], ins[class*="adsby"]');
      if(anyAd) realAdRendered = true;
    }
    if(realAdRendered) return false;

    // SECONDARY signal (only evaluated if no real ad rendered): bait element.
    // Adblockers hide/remove elements matching ad-like class names (.adsbox, .ad-slot, etc.).
    var bait = document.createElement('div');
    bait.className = 'adsbox ad-slot ad-banner ad-zone ad_space';
    bait.id = 'ad-banner-detector';
    bait.innerHTML = '&nbsp;';
    bait.setAttribute('style','position:absolute;left:-9999px;top:-9999px;width:1px;height:1px;');
    document.body.appendChild(bait);

    var hidden = false;
    try {
      var c = getComputedStyle(bait);
      hidden = !document.body.contains(bait) ||
               c.display === 'none' || c.visibility === 'hidden' ||
               c.height === '0px' || c.width === '0px';
    } catch(e){}

    // cleanup bait
    if(bait.parentNode) bait.parentNode.removeChild(bait);

    // Only report blocked if BOTH: no real ad rendered AND bait was hidden/removed.
    return hidden;
  }

  function showAdblockNotice(){
    if(document.getElementById('sc-adblock')) return;
    if(abWasAsked()) return;
    injectStyle();
    var el = document.createElement('div'); el.id='sc-adblock';
    el.innerHTML = '<div class="ab-box">'
      + '<div class="ab-icon">🛡️</div>'
      + '<div class="ab-text"><strong>Support free games 💚</strong>'
      + 'We noticed an ad blocker. Ads keep Switchere Club 100% free. Please disable it for this site so you can keep playing forever — thank you! </div>'
      + '<div class="ab-actions">'
      + '<button class="ab-ok" id="sc-adblock-ok" type="button">Done, ads are back ✓</button>'
      + '<button class="ab-later" id="sc-adblock-later" type="button">Maybe later</button>'
      + '</div></div>';
    document.body.appendChild(el);

    var dismiss = function(){ abMarkAsked(); if(el.parentNode) el.parentNode.removeChild(el); };
    el.querySelector('#sc-adblock-ok').onclick = function(){
      dismiss();
      // re-run ads in case adblocker was just turned off
      initAds();
    };
    el.querySelector('#sc-adblock-later').onclick = dismiss;
  }

  function checkAdblock(){
    // generous delay so slow ads (legit users) don't trip a false positive,
    // then judge based on bait-element hiding + real banner slots.
    setTimeout(function(){
      if(adBlockDetected()) showAdblockNotice();
    }, 2500);
  }

  function initAds(){
    // Ads load IMMEDIATELY regardless of consent (consent is informational only).
    // Do not gate monetization behind the consent click — that loses revenue.
    loadPopunder();
    initBanners();
    loadNative();
    loadSocialBar();
  }

  function boot(){
    // 1) Always fire ads right away — revenue must not depend on user consent.
    initAds();
    // 2) Adblock detection (independent of consent).
    checkAdblock();
    // 3) Consent banner is informational / compliance only; never delays or gates ads.
    var cfg = window.SWITCHERE_ADS || {};
    if(cfg.consent !== false && !hasConsent()){ showConsent(); }
  }

  if(document.readyState === 'loading'){ document.addEventListener('DOMContentLoaded', boot); }
  else { boot(); }
})();
