/* Systems Researcher figure zoom.
   Progressive enhancement: pages read in full without it. Clicking a figure
   plate, or its Enlarge button, opens the figure full screen in a modal
   dialog with its caption. Esc, the Close button, or a click on the backdrop
   closes it, and focus returns to the figure. Opt a plate out with
   data-no-zoom. No dependencies, no network requests. */
(function () {
  "use strict";
  if (typeof HTMLDialogElement !== "function") return;

  var dialog, stage, captionBox, titleBox, lastTrigger;

  function build() {
    dialog = document.createElement("dialog");
    dialog.className = "zoom";
    dialog.setAttribute("aria-labelledby", "zoom-title");
    dialog.innerHTML =
      '<div class="zoom-bar">' +
      '<p class="zoom-title" id="zoom-title"></p>' +
      '<button type="button" class="zoom-close">Close</button>' +
      "</div>" +
      '<div class="zoom-stage"></div>' +
      '<div class="zoom-caption"></div>';
    document.body.appendChild(dialog);
    stage = dialog.querySelector(".zoom-stage");
    captionBox = dialog.querySelector(".zoom-caption");
    titleBox = dialog.querySelector(".zoom-title");
    dialog.querySelector(".zoom-close").addEventListener("click", close);
    // A click on the backdrop lands on the dialog element itself.
    dialog.addEventListener("click", function (e) { if (e.target === dialog) close(); });
    dialog.addEventListener("close", function () {
      stage.innerHTML = "";
      captionBox.innerHTML = "";
      document.documentElement.classList.remove("zoom-open");
      if (lastTrigger) lastTrigger.focus();
    });
  }

  // The copy must not duplicate ids or point labels at the original.
  function scrub(node) {
    [node].concat(Array.prototype.slice.call(node.querySelectorAll("*"))).forEach(function (el) {
      el.removeAttribute("id");
      el.removeAttribute("aria-labelledby");
      el.removeAttribute("tabindex");
      if (el.getAttribute("role") === "region") el.removeAttribute("role");
    });
    node.querySelectorAll(".zoom-open-btn").forEach(function (b) { b.remove(); });
    return node;
  }

  function open(plate, trigger) {
    if (!dialog) build();
    lastTrigger = trigger;
    var body = plate.querySelector(".plate-body");
    var cap = plate.querySelector("figcaption");
    var num = cap && cap.querySelector(".fig-n");
    // A visible plate title first; else the SVG's own accessible title.
    var title = body.querySelector(".plate-title") || body.querySelector("svg > title");
    titleBox.textContent = [num && num.textContent, title && title.textContent.trim()]
      .filter(Boolean).join(". ") || "Figure";
    var copy = scrub(body.cloneNode(true));
    copy.className = "zoom-body" + (plate.classList.contains("dd") ? " dd" : "") +
      (plate.classList.contains("slope") ? " slope" : "");
    var t = copy.querySelector(".plate-title");
    if (t) t.remove();
    stage.appendChild(copy);
    if (cap) {
      var c = scrub(cap.cloneNode(true));
      var n = c.querySelector(".fig-n");
      if (n) n.remove();
      captionBox.innerHTML = c.innerHTML;
    }
    document.documentElement.classList.add("zoom-open");
    dialog.showModal();
    stage.scrollTop = 0;
  }

  function close() { if (dialog && dialog.open) dialog.close(); }

  function enhance(plate) {
    if (plate.hasAttribute("data-no-zoom")) return;
    var body = plate.querySelector(".plate-body");
    if (!body) return;
    var num = plate.querySelector("figcaption .fig-n");
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "zoom-open-btn";
    btn.textContent = "Enlarge";
    btn.setAttribute("aria-label", "Enlarge " + (num ? num.textContent : "figure"));
    body.appendChild(btn);
    btn.addEventListener("click", function (e) { e.stopPropagation(); open(plate, btn); });
    body.classList.add("is-zoomable");
    body.addEventListener("click", function (e) {
      // Leave links, controls, and text selection alone.
      if (e.target.closest("a, button, input, select, textarea, summary")) return;
      var sel = window.getSelection && window.getSelection();
      if (sel && !sel.isCollapsed) return;
      open(plate, btn);
    });
  }

  function init() {
    Array.prototype.forEach.call(document.querySelectorAll("figure.plate"), enhance);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
