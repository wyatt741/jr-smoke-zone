// JR Smoke Zone - deterministic assistant. No LLM, no API key, no backend.
// Every answer is built from window.JRZ, which build.py emits from the SAME constants
// the pages render. It never quotes a price or claims stock - those route to a call.
(function () {
  var D = window.JRZ; if (!D) return;
  var panel = document.getElementById('cw-panel'),
      bubble = document.getElementById('cw-bubble'),
      log = document.getElementById('cw-log'),
      form = document.getElementById('cw-form'),
      input = document.getElementById('cw-input'),
      wrap = document.getElementById('cw');
  if (!panel || !bubble) return;

  var telLink  = '<a href="tel:' + D.tel + '">' + D.phone + '</a>';
  var mapsLink = '<a href="' + D.maps + '" target="_blank" rel="noopener">get directions</a>';

  // ---- "are you open right now?" from the real per-day hours -------------------
  function parseTime(s) {                       // "9am" -> 9, "10:30pm" -> 22.5
    var m = /^(\d{1,2})(?::(\d{2}))?\s*(am|pm)$/i.exec(s.trim());
    if (!m) return null;
    var h = (+m[1]) % 12;
    if (/pm/i.test(m[3])) h += 12;
    return h + (m[2] ? (+m[2]) / 60 : 0);
  }
  function openNow() {
    var now = new Date(), i = (now.getDay() + 6) % 7;        // Mon=0 .. Sun=6
    var today = (D.days || [])[i]; if (!today) return null;
    var p = today.h.split('-'); if (p.length !== 2) return null;
    var a = parseTime(p[0]), b = parseTime(p[1]);
    if (a === null || b === null) return null;               // unparseable -> just show hours
    var cur = now.getHours() + now.getMinutes() / 60;
    return { open: cur >= a && cur < b, day: today.d, h: today.h };
  }
  function hoursAnswer() {
    var list = D.hours.map(function (r) { return r.d + ' ' + r.h; }).join('<br>');
    var s = openNow(), lead;
    if (!s) lead = 'Here are our hours:';
    else lead = s.open ? "We're <strong>open right now</strong> (" + s.day + ' ' + s.h + ').'
                       : "We're <strong>closed right now</strong>. " + s.day + ' hours are ' + s.h + '.';
    return lead + '<br><br>' + list;
  }

  // ---- intents (first match wins) ----------------------------------------------
  var productLines = function () {
    return D.products.map(function (p) { return '<strong>' + p.title + '</strong> - ' + p.short; }).join('<br>');
  };
  var INTENTS = [
    // price/stock deflect FIRST so "how much is a bong" never hits the product intent
    [/\b(price|prices|pricing|cost|costs|how much|cheap|expensive|deal|deals|sale)\b/i, function () {
      return 'Prices change with stock, so I do not quote them here. Call the shop and they will tell you exactly: ' + telLink + '.';
    }],
    [/\b(in stock|stock|do you have|have any|got any|available|carry a|specific)\b/i, function () {
      return 'I cannot check live stock. Give the shop a call and they will look for you: ' + telLink + '.<br><br>Here is what we carry:<br>' + productLines();
    }],
    [/\b(hour|hours|open|close|closed|closing|opening|today|tonight|time)\b/i, hoursAnswer],
    [/\b(where|address|located|location|direction|directions|find you|parking|map)\b/i, function () {
      return "We're at <strong>" + D.addr + '</strong>.<br><br>You can ' + mapsLink + '.';
    }],
    [/\b(phone|call|number|contact|text|reach)\b/i, function () {
      return 'Call or text ' + telLink + '.<br>Email: <a href="mailto:' + D.email + '">' + D.email + '</a>';
    }],
    [/\b(online|ship|shipping|deliver|delivery|order|website order|buy online)\b/i, function () {
      return 'We do not sell online, it is an in-store shop only. Come see us at ' + D.addr + ' and you can ' + mapsLink + '.';
    }],
    // broad on purpose: age/ID is the compliance question, better over- than under-matched
    // "do you card" = ID check; "do you take card" = payment. Order matters: this runs
    // before the payment intent, so the ID sense wins only on the ID phrasing.
    [/\b(21|18|age|ages|aged|ids?|identification|minors?|underage|carded|carding)\b|how old|old enough|card me|do (?:you|they) card\b/i, function () {
      // phrased to answer both senses directly: "do you card?" (yes) and "how old?" (21)
      return 'Yes, we card. You must be <strong>21+</strong> and show a valid photo ID. Tobacco and vapor products are for adults 21 and over only.';
    }],
    [/\b(brand|brands|puffco|zig|zag|raw|elf bar|elfbar)\b/i, function () {
      return 'Brands we carry include <strong>' + D.brands.join(', ') + '</strong>, plus plenty more on the wall. For a specific item, call ' + telLink + '.';
    }],
    [/\b(vape|vapes|e-?liquid|ejuice|e-?juice|pod|pods|disposable|coil|salt)\b/i, function () {
      return 'Yes - vape devices, pods, disposables, and a big wall of e-liquid. New to it or dialing in a setup, the staff will walk you through it.';
    }],
    [/\b(hookah|shisha|coal|coals|bowl|hose)\b/i, function () {
      return 'We do hookah: full setups plus shisha, hoses, bowls, and coals. Grab a whole kit or just restock.';
    }],
    [/\b(glass|pipe|pipes|chillum|hand pipe)\b/i, function () {
      return 'The glass wall is what regulars come back for - hand pipes and glass across a real range of styles and price points. Best seen in person.';
    }],
    [/\b(bong|bongs|water pipe|rig|rigs|beaker|downstem)\b/i, function () {
      return 'Water pipes and rigs in glass and silicone, plus bowls, downstems, and the small parts that always go missing.';
    }],
    [/\b(cigar|cigars|cutter|lighter|humidor)\b/i, function () {
      return 'Cigars for the casual smoker and the aficionado, plus cutters, lighters, and ashtrays.';
    }],
    [/\b(accessor|grinder|tray|charger|battery|storage|cleaning)\b/i, function () {
      return 'Chargers, batteries, grinders, trays, storage, and cleaning supplies - the catch-all wall.';
    }],
    [/\b(product|products|sell|what do you|carry|inventory|selection)\b/i, function () {
      return 'Here is what we carry:<br>' + productLines();
    }],
    [/\b(card|cards|cash|credit|debit|payment|pay|apple pay)\b/i, function () {
      return 'We accept credit cards. Good to know: ' + D.amenities.join(', ') + '.';
    }],
    [/\b(wheelchair|accessible|accessibility|bike|handicap)\b/i, function () {
      return 'Good to know: ' + D.amenities.join(', ') + '.';
    }],
    [/\b(review|reviews|rate|rating|google review|leave a review|feedback)\b/i, function () {
      return (D.review ? 'Thank you! You can leave us a Google review here: <a href="' + D.review + '" target="_blank" rel="noopener">Review us on Google</a>. It really helps a local shop.'
                       : 'You can find us on Google to leave a review. Thanks for the support!');
    }],
    [/\b(instagram|insta|ig|social|facebook|follow)\b/i, function () {
      return 'We post deals and events on Instagram: <a href="' + D.ig + '" target="_blank" rel="noopener">@jrsmokezone</a>.';
    }],
    [/\b(hi|hey|hello|yo|sup|howdy|good morning|good evening)\b/i, function () {
      return "Hey. Ask me about hours, directions, or what we carry.";
    }],
    [/\b(thank|thanks|thx|appreciate|cheers)\b/i, function () {
      return 'Anytime. Come see us at ' + D.addr + '.';
    }]
  ];

  function answer(text) {
    for (var i = 0; i < INTENTS.length; i++) if (INTENTS[i][0].test(text)) return INTENTS[i][1]();
    return "I am not sure about that one. The staff can help - call " + telLink +
           ', or come by ' + D.addr + '.<br><br>Try asking about <em>hours</em>, <em>directions</em>, or <em>what we carry</em>.';
  }

  // ---- rendering ----------------------------------------------------------------
  // chip text doubles as the question that gets sent, so it must still match an intent
  var CHIPS = ['Hours', 'Where are you located?', 'What do you carry?', 'Do you sell online?'];
  function bubbleEl(html, who) {
    var d = document.createElement('div');
    d.className = 'cw-msg cw-' + who;
    d.innerHTML = html;
    log.appendChild(d); log.scrollTop = log.scrollHeight;
    return d;
  }
  function showChips() {
    var w = document.createElement('div'); w.className = 'cw-chips';
    CHIPS.forEach(function (c) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'cw-chip'; b.textContent = c;
      b.addEventListener('click', function () { w.remove(); send(c); });
      w.appendChild(b);
    });
    log.appendChild(w); log.scrollTop = log.scrollHeight;
  }
  // ---- AI mode (optional) --------------------------------------------------------
  // If D.worker is set (build.py -> window.JRZ.worker), route to the Cloudflare Worker
  // for real AI answers. On any error, fall back to the deterministic answer() above,
  // so the bot always works. History holds committed user/assistant pairs for context.
  var WORKER = (D.worker || '').replace(/\/+$/, '');
  var history = [];
  // escape all five HTML-significant chars: quotes matter because linkify drops URLs into
  // href="..." - an un-escaped " in a jailbroken AI reply could otherwise break out.
  function esc(s) { return s.replace(/[<>&"']/g, function (c) { return { '<': '&lt;', '>': '&gt;', '&': '&amp;', '"': '&quot;', "'": '&#39;' }[c]; }); }
  function linkify(s) {                                     // AI text -> safe HTML with links
    s = s.replace(/\s*—\s*/g, ', ').replace(/–/g, '-');     // no em dashes; en dashes -> hyphens (house style)
    s = esc(s);
    s = s.replace(/\bhttps?:\/\/[^\s<]+/g, function (u) {
      return '<a href="' + u + '" target="_blank" rel="noopener">' + u.replace(/^https?:\/\//, '') + '</a>';
    });
    s = s.replace(/\(?\b\d{3}\)?[\s.\-]?\d{3}[\s.\-]?\d{4}\b/g, function (p) {
      return '<a href="tel:' + p.replace(/[^\d+]/g, '') + '">' + p + '</a>';
    });
    return s.replace(/\n/g, '<br>');
  }
  function typingEl() {
    var t = document.createElement('div');
    t.className = 'cw-typing'; t.innerHTML = '<span></span><span></span><span></span>';
    log.appendChild(t); log.scrollTop = log.scrollHeight; return t;
  }
  function botReply(text) {
    var t = typingEl();
    if (!WORKER) {                                          // no Worker configured -> deterministic
      setTimeout(function () { t.remove(); bubbleEl(answer(text), 'bot'); showChips(); }, 420);
      return;
    }
    var msgs = history.concat([{ role: 'user', content: text }]).slice(-16);
    fetch(WORKER + '/chat', {
      method: 'POST', headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ messages: msgs })
    })
      .then(function (r) { return r.ok ? r.json() : Promise.reject(r.status); })
      .then(function (d) {
        var reply = (d && d.reply) ? String(d.reply) : '';
        if (!reply) return Promise.reject('empty');
        t.remove();
        history.push({ role: 'user', content: text }, { role: 'assistant', content: reply });
        history = history.slice(-16);
        bubbleEl(linkify(reply), 'bot'); showChips();
      })
      .catch(function () { t.remove(); bubbleEl(answer(text), 'bot'); showChips(); });  // AI down -> deterministic
  }
  function send(text) {
    text = (text || '').trim(); if (!text) return;
    var chips = log.querySelector('.cw-chips'); if (chips) chips.remove();
    bubbleEl(esc(text), 'user');
    botReply(text);
  }

  // ---- open / close --------------------------------------------------------------
  var started = false;
  function toggle(open) {
    panel.hidden = !open;
    wrap.classList.toggle('cw--open', open);
    bubble.setAttribute('aria-expanded', open);
    if (open && !started) {
      started = true;
      bubbleEl("Hey, welcome to " + D.biz + ". Ask me about hours, directions, or what we carry.<br><br>" +
               "<strong>" + D.hoursShort + "</strong>", 'bot');
      showChips();
    }
    if (open) setTimeout(function () { input.focus(); }, 80);
  }
  bubble.addEventListener('click', function () { toggle(panel.hidden); });
  document.getElementById('cw-close').addEventListener('click', function () { toggle(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !panel.hidden) toggle(false); });
  form.addEventListener('submit', function (e) { e.preventDefault(); send(input.value); input.value = ''; });
})();
