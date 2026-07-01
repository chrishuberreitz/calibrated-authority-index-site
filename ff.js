/* =============================================================================
   ff.js — Feature-Flag engine for the Calibrated Authority Index redesign-v2
   -----------------------------------------------------------------------------
   A tiny, dependency-free, page-agnostic flag system. Each redesign move is a
   flag that can be toggled independently so the new layer can be A/B'd against
   the current single-screen canvas.

   SOURCES OF TRUTH (in priority order)
     1. URL query param  ?ff=...   (see grammar below)
     2. The DEFAULTS declared on each flag in FLAGS, below.

   ?ff GRAMMAR (comma-separated tokens)
     ?ff=none                      -> every flag OFF
     ?ff=all                       -> every flag ON
     ?ff=default | defaults        -> the documented default set
     ?ff=record-cards,cite-blocks  -> EXACT set: only these ON, the rest OFF
     ?ff=+hover-annotations        -> start from DEFAULTS, then ADD this one
     ?ff=-numbered-sections        -> start from DEFAULTS, then REMOVE this one
     ?ff=no-numbered-sections      -> same as -numbered-sections
     ?ff=record-cards,+in-the-news -> EXACT set {record-cards}, then add one
   Bare names define an exact set; +/-/no- deltas mutate the base (defaults, or
   the exact set if any bare names are present).

   PUBLIC API (window.FF)
     FF.on(name)   -> boolean: is this flag active right now?
     FF.list()     -> array of active flag names
     FF.all        -> the FLAGS registry (defaults, labels, descriptions)
     FF.set(names) -> navigate to ?ff=<exact set> (reloads the page)

   SIDE EFFECTS
     - Adds `ff-on` + `ff-<flag>` classes to <html> immediately (pre-paint), so
       CSS can gate on any flag without waiting for JS render.
     - On DOMContentLoaded, mounts a floating "flags" panel (bottom-left) for
       live toggling — the compare tool. Production-hidden: opt in with ?ffpanel=1.
   ========================================================================== */
(function () {
  "use strict";

  // -- The flag registry. Edit DEFAULTS here; they are the documented baseline.
  //    `stub:true` marks a flag that is wired but intentionally thin (TODO).
  var FLAGS = {
    "record-cards": {
      default: true,
      label: "Record cards",
      desc: "Per-institution record card with the fixed citation form — date · source · disposition — exposed by default, not behind a tooltip.",
      exemplar: "GBIF specimen record cards + legal case reporters"
    },
    "cite-blocks": {
      default: true,
      label: "Cite-as blocks",
      desc: "A formatted 'Cite as' block shown inline on every entry (instead of hidden behind a copy button).",
      exemplar: "Our World in Data"
    },
    "provenance-dates": {
      default: true,
      label: "Provenance dates",
      desc: "YYYY-MM-DD coded-date + last-seen verification status surfaced on records and the footer.",
      exemplar: "Gwern.net"
    },
    "case-zoom": {
      default: true,
      label: "Case zoom",
      desc: "The aggregate segment view resolves to the individual cases inside each segment — tap a segment to expand its institutions.",
      exemplar: "The Pudding — In Pursuit of Democracy"
    },
    "numbered-sections": {
      default: true,
      label: "Numbered sections",
      desc: "§-numbered zones, each with a one-line abstract under its title.",
      exemplar: "Stanford HAI AI Index"
    },
    "hover-annotations": {
      default: false,
      label: "Hover annotations",
      desc: "Hover an institution name (in the scoreboard zoom) for a preview card — CA · disposition · quote snippet. Desktop/pointer only.",
      exemplar: "Gwern.net"
    },
    "in-the-news": {
      default: false,
      label: "In the news",
      desc: "Citation-velocity panel — external citations of the Index. Reads /citations.json; shows an honest empty state when none are logged (no fabricated data).",
      exemplar: "Atlas of Economic Complexity",
      stub: true
    }
  };

  var NAMES = Object.keys(FLAGS);
  function defaults() { return NAMES.filter(function (n) { return FLAGS[n].default; }); }

  // -- Resolve the active set from ?ff=
  function resolve() {
    var raw = null;
    try { raw = new URLSearchParams(location.search).get("ff"); } catch (e) { raw = null; }
    if (raw == null || raw === "") return defaults();

    var tokens = raw.split(",").map(function (t) { return t.trim(); }).filter(Boolean);
    if (tokens.length === 1) {
      var t0 = tokens[0].toLowerCase();
      if (t0 === "none") return [];
      if (t0 === "all") return NAMES.slice();
      if (t0 === "default" || t0 === "defaults") return defaults();
    }

    var bare = [], adds = [], dels = [];
    tokens.forEach(function (t) {
      if (t[0] === "+") adds.push(t.slice(1));
      else if (t[0] === "-") dels.push(t.slice(1));
      else if (t.toLowerCase().indexOf("no-") === 0) dels.push(t.slice(3));
      else bare.push(t);
    });

    var set = {};
    var base = bare.length ? bare : defaults();
    base.forEach(function (n) { if (FLAGS[n]) set[n] = true; });
    adds.forEach(function (n) { if (FLAGS[n]) set[n] = true; });
    dels.forEach(function (n) { delete set[n]; });
    return Object.keys(set);
  }

  var ACTIVE = resolve();
  var ACTIVE_SET = {};
  ACTIVE.forEach(function (n) { ACTIVE_SET[n] = true; });

  // -- Apply classes to <html> pre-paint so CSS can gate immediately.
  var root = document.documentElement;
  root.classList.add("ff-on");
  ACTIVE.forEach(function (n) { root.classList.add("ff-" + n); });
  root.setAttribute("data-ff", ACTIVE.join(",") || "none");

  // -- Public API
  window.FF = {
    all: FLAGS,
    on: function (name) { return !!ACTIVE_SET[name]; },
    list: function () { return ACTIVE.slice(); },
    set: function (names) {
      var u = new URL(location.href);
      var clean = (names || []).filter(function (n) { return FLAGS[n]; });
      u.searchParams.set("ff", clean.length ? clean.join(",") : "none");
      location.href = u.toString();
    },
    isDefault: function () { return ACTIVE.slice().sort().join(",") === defaults().sort().join(","); }
  };

  // -- The live toggle panel (the "compare" tool). Production-hidden: the panel
  //    is a dev/demo affordance, so it only mounts when explicitly opted in with
  //    ?ffpanel=1. Public visitors get the hard-defaulted flag set, no panel.
  function mountPanel() {
    try { if (new URLSearchParams(location.search).get("ffpanel") !== "1") return; } catch (e) { return; }
    if (document.getElementById("ff-panel-btn")) return;

    var btn = document.createElement("button");
    btn.id = "ff-panel-btn";
    btn.type = "button";
    btn.innerHTML = "&#9873; flags <span class='ff-n'>" + ACTIVE.length + "/" + NAMES.length + "</span>";
    btn.setAttribute("aria-expanded", "false");
    btn.setAttribute("aria-controls", "ff-panel");

    var panel = document.createElement("div");
    panel.id = "ff-panel";
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-label", "Feature flags");

    var rows = NAMES.map(function (n) {
      var f = FLAGS[n];
      return "<label class='ff-row" + (f.stub ? " ff-stub" : "") + "'>" +
        "<input type='checkbox' data-ff='" + n + "'" + (ACTIVE_SET[n] ? " checked" : "") + ">" +
        "<span class='ff-row-main'><span class='ff-row-name'>" + esc(f.label) +
        (f.stub ? " <em>stub</em>" : "") + " <code>" + n + "</code></span>" +
        "<span class='ff-row-desc'>" + esc(f.desc) + "</span>" +
        "<span class='ff-row-ex'>from: " + esc(f.exemplar) + "</span></span></label>";
    }).join("");

    panel.innerHTML =
      "<div class='ff-head'><b>redesign-v2 feature flags</b>" +
      "<span class='ff-default'>" + (window.FF.isDefault() ? "default set" : "custom set") + "</span></div>" +
      "<div class='ff-rows'>" + rows + "</div>" +
      "<div class='ff-actions'>" +
      "<button data-act='default'>defaults</button>" +
      "<button data-act='all'>all on</button>" +
      "<button data-act='none'>all off</button>" +
      "<a href='/FLAGS.md' target='_blank' rel='noopener'>manifest &#8599;</a>" +
      "</div>";

    function toggleOpen() {
      var open = panel.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    }
    btn.addEventListener("click", toggleOpen);

    panel.addEventListener("change", function (e) {
      var cb = e.target.closest("input[data-ff]");
      if (!cb) return;
      var next = NAMES.filter(function (n) {
        var box = panel.querySelector("input[data-ff='" + n + "']");
        return box && box.checked;
      });
      window.FF.set(next);
    });
    panel.addEventListener("click", function (e) {
      var a = e.target.closest("button[data-act]");
      if (!a) return;
      if (a.dataset.act === "default") window.FF.set(defaults());
      else if (a.dataset.act === "all") window.FF.set(NAMES.slice());
      else window.FF.set([]); // none
    });

    document.body.appendChild(btn);
    document.body.appendChild(panel);
  }

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountPanel);
  } else {
    mountPanel();
  }
})();
