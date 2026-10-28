/* MAHUS — site behaviour (white ink on black) */
(function () {
  "use strict";

  var WA = "919592364304";

  function $ (s, r) { return (r || document).querySelector(s); }
  function $$ (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); }
  function rupee (n) { return "₹" + n.toLocaleString("en-IN"); }

  /* ---------- 34-design strip: arrow paging ---------- */
  $$(".strip-wrap").forEach(function (wrap) {
    var strip = $(".strip", wrap);
    var prev = $("[data-strip-prev]", wrap);
    var next = $("[data-strip-next]", wrap);
    if (!strip) return;
    function step () { return Math.max(220, strip.clientWidth * 0.8); }
    if (prev) prev.addEventListener("click", function () { strip.scrollBy({ left: -step(), behavior: "smooth" }); });
    if (next) next.addEventListener("click", function () { strip.scrollBy({ left: step(), behavior: "smooth" }); });
  });

  /* ---------- 195 lines: live filter ---------- */
  var lnFilter = $("#lnFilter");
  if (lnFilter) {
    var rows = $$(".ln");
    var count = $("#lnCount");
    var total = rows.length;
    function apply () {
      var q = lnFilter.value.trim().toLowerCase();
      var shown = 0;
      rows.forEach(function (r) {
        var hit = !q || $(".t", r).textContent.toLowerCase().indexOf(q) !== -1;
        r.hidden = !hit;
        if (hit) shown++;
      });
      if (count) count.textContent = shown + " / " + total + " LINES";
    }
    lnFilter.addEventListener("input", apply);
    apply();
  }

  /* ---------- order calculators ---------- */
  var calc = $("[data-calc]");
  if (calc) {
    var mode = calc.getAttribute("data-calc");          // "blank" | "custom"
    var priceOf = mode === "blank" ? { "600": 600 } : { "1000": 1000, "1100": 1100 };

    function readPrice () {
      var el = $("input[name='print']:checked", calc);
      return el ? parseInt(el.value, 10) : 0;
    }
    function readSizes () {
      return $$("input[name='chest']:checked", calc).map(function (i) { return i.value; });
    }
    function readQty () {
      var el = $("input[name='qty']", calc);
      var v = el ? parseInt(el.value, 10) : 1;
      return isNaN(v) || v < 1 ? 1 : v;
    }
    function readPrintCopy () {
      var el = $("input[name='printcopy']", calc);
      return el ? el.value.trim() : "";
    }

    function render () {
      var unit = readPrice();
      var sizes = readSizes();
      var qty = readQty();
      var gross = unit * qty;
      var copy = readPrintCopy();

      var set = function (sel, txt) { var n = $(sel, calc); if (n) n.textContent = txt; };
      set(".out-unit", rupee(unit));
      set(".out-qty", String(qty));
      set(".out-sizes", sizes.length ? sizes.join(" · ") : "Select chest size");
      set(".out-gross", rupee(gross));
      set(".out-invoice", rupee(gross));
      set(".out-copy", copy ? "“" + copy + "”" : (mode === "blank" ? "Plain black tee" : "Type your line"));

      var err = $(".calc-error", calc);
      var go = $("[data-pay]", calc);
      var problems = [];
      if (!unit) problems.push("choose a print option");
      if (!sizes.length) problems.push("tick a chest size");
      if (mode === "custom" && unit === 1000 && !copy) problems.push("type your line for the front print");
      if (err) err.textContent = problems.length ? "Please " + problems.join(", ") + "." : "";
      if (go) {
        go.disabled = problems.length > 0;
        go.setAttribute("href", problems.length ? "" :
          "https://wa.me/" + WA + "?text=" + encodeURIComponent(
            "MAHUS order\n" +
            (mode === "blank" ? "Blank black oversized tee" : "Customised oversized tee") + "\n" +
            "Print: " + (mode === "blank" ? "none (plain)" : (unit === 1000 ? "front" : "front + back")) + "\n" +
            (copy ? "Copy: " + copy + "\n" : "") +
            "Chest: " + sizes.join(", ") + "\n" +
            "Qty: " + qty + "\n" +
            "Value: " + rupee(gross) + "\n" +
            "Name:\nMobile:"
          ));
      }
      var payA = $("[data-pay-label]", calc);
      if (payA) payA.textContent = "Pay " + rupee(gross) + " by UPI";
    }

    calc.addEventListener("change", render);
    calc.addEventListener("input", render);
    render();
  }

  /* ---------- buyer form -> WhatsApp ---------- */
  var bf = $("#buyerForm");
  if (bf) {
    bf.addEventListener("submit", function (e) {
      e.preventDefault();
      var v = function (n) { var el = bf.elements[n]; return el ? el.value.trim() : ""; };
      var msg =
        "MAHUS order\n" +
        "Name: " + v("name") + "\n" +
        "Mobile: " + v("mobile") + "\n" +
        (v("email") ? "Email: " + v("email") + "\n" : "") +
        (v("address") ? "Address: " + v("address") + "\n" : "") +
        (v("notes") ? "Notes: " + v("notes") + "\n" : "");
      window.open("https://wa.me/" + WA + "?text=" + encodeURIComponent(msg), "_blank", "noopener");
    });
  }
})();
