#!/usr/bin/env python3
"""Build the MAHUS multi-page site (white ink on black) into website/.

Run:  python3 _build.py
Emits the light (white) version at website/ root — website/index.html …
website/contact.html — and the black version in website/black/.
Shared assets (styles.css, site.js, favicon.svg, img/, data/) live in
website/ itself.
34 designs + 195 lines are pulled from website/data/*.json.
"""
import json, os, html, io

HERE = os.path.dirname(os.path.abspath(__file__))
D = lambda p: os.path.join(HERE, p)

DESIGNS = json.load(open(D("data/designs.json"), encoding="utf-8"))
LINES = json.load(open(D("data/lines195.json"), encoding="utf-8"))
assert len(DESIGNS) == 34 and len(LINES) == 195

WA = "919592364304"
WALINK = "https://wa.me/" + WA
WAFLAT = "95923-64304"
EMAIL = "mahusenterprises@gmail.com"

# ---- theme pass -------------------------------------------------------
# P          asset prefix — both versions sit one level down from the
#            shared assets (styles.css, site.js, img/, favicon.svg)
# HTML_ATTR  data-theme hook for the light pass
P = "../"
HTML_ATTR = ""


def set_theme(theme):
    global HTML_ATTR, TOGGLE_PREFIX, TOGGLE_TXT, TOGGLE_ARIA, P
    if theme == "light":
        HTML_ATTR = ' data-theme="light"'
        P = ""
        TOGGLE_PREFIX, TOGGLE_TXT, TOGGLE_ARIA = (
            "black/", "BLACK", "Switch to the black version")
    else:
        HTML_ATTR = ""
        P = "../"
        TOGGLE_PREFIX, TOGGLE_TXT, TOGGLE_ARIA = (
            "../", "WHITE", "Switch to the white version")


NAV = [
    ("index.html", "Home"),
    ("size-chart.html", "Size Chart"),
    ("blank-tee.html", "Blank Tee"),
    ("pricing.html", "Pricing"),
    ("hoodies.html", "Hoodies"),
    ("order.html", "Order"),
    ("polo.html", "Polo"),
    ("about.html", "About"),
    ("contact.html", "Contact"),
]

SPECS = [
    ("Unisex", "One cut, everyone"),
    ("Round neck", "Classic crew"),
    ("Oversized", "Relaxed, dropped shoulder"),
    ("Black colour", "One colourway only"),
    ("Ribbed collar", "Holds its shape"),
    ("240 GSM", "Grams per square metre"),
    ("100% cotton", "No synthetics"),
    ("Thick / heavyweight / durable", "Built to last"),
    ("White font on black tee", "Or a plain black tee"),
    ("Images in colour", "Full-colour prints"),
]

# Hoodie Specifications.pdf — 21 rows set as twelve lines
HOODIE_SPECS = [
    ("Black", "Hoodie colour — white print"),
    ("Unisex", "One cut, everyone"),
    ("420 GSM", "Grams per square metre"),
    ("100% cotton heavy fleece", "Thick, substantial, cozy"),
    ("About 800 grams", "Most hoodies are 600–700 g"),
    ("Relaxed oversized", "Dropped shoulders · streetwear fit"),
    ("Full sleeve", "Pullover or zip — both possible"),
    ("Winter weight", "Excellent warmth · cold weather"),
    ("DTF print or embroidery", "Both can be provided"),
    ("Chest or back print", "Your line, your image, your logo"),
    ("XS to 7XL", "Chest 36 to 56 inches"),
    ("Built to last", "Quality fabric and stitching"),
]


def esc(s):
    return html.escape(s, quote=True)


def shell(title, desc, active, body, extra_head=""):
    nav = "\n      ".join(
        '<a href="%s"%s>%s</a>' % (h, ' class="on"' if h == active else "", esc(t))
        for h, t in NAV
    )
    pages = " · ".join('<a href="%s">%s</a>' % (h, esc(t)) for h, t in NAV)
    return """<!DOCTYPE html>
<html lang="en"%s>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>%s</title>
  <meta name="description" content="%s">
  <link rel="icon" type="image/svg+xml" href="%sfavicon.svg">
  <link rel="stylesheet" href="%sstyles.css">%s
</head>
<body>

  <header class="hud">
    <div class="hud-l">
      <a class="logo" href="index.html">MAHUS</a>
      <span class="tag">CUSTOM OVERSIZED TEES / REV 1.1</span>
    </div>
    <nav>
      %s
    </nav>
    <a class="themebtn" href="%s" aria-label="%s">&#9680; %s</a>
    <a class="cta-wa" href="%s">%s</a>
  </header>

%s

  <footer class="foot">
    <div>
      <p class="logo">MAHUS</p>
      <p class="fine">Your line. Your image. your imagination. One black heavyweight tee, printed to order in white ink or full colour. First revision of the website — to be re-cut next year.</p>
    </div>
    <div>
      <p class="fh">Order</p>
      <a class="btn btn-wa" href="%s">WHATSAPP %s</a>
      <p class="fh">Email</p>
      <p class="fine"><a href="mailto:%s">%s</a></p>
    </div>
    <div>
      <p class="fh">Pages</p>
      <p class="fine">%s</p>
    </div>
  </footer>
  <div class="legal">
    <span>MAHUS · mahus.in</span>
    <span>UPI QR live · gateway to follow</span>
    <span>WhatsApp %s</span>
  </div>

  <script src="%ssite.js"></script>
</body>
</html>
""" % (
        HTML_ATTR, esc(title), esc(desc), P, P, extra_head,
        nav, TOGGLE_PREFIX + active, TOGGLE_ARIA, TOGGLE_TXT,
        WALINK, WAFLAT,
        body,
        WALINK, WAFLAT, EMAIL, EMAIL,
        pages,
        WAFLAT,
        P,
    )


# ---------------------------------------------------------------- fragments

def designs_strip():
    cards = []
    for d in DESIGNS:
        cards.append(
            '        <figure class="dcard">\n'
            '          <div class="dmedia"><img src="%s" alt="Design %02d — %s" loading="lazy"></div>\n'
            '          <figcaption class="dmeta"><span class="i">%02d</span><span class="c">%s</span></figcaption>\n'
            '        </figure>'
            % (P + d["src"], d["i"], esc(d["cap"]), d["i"], esc(d["cap"]))
        )
    return (
        '    <div class="strip-wrap">\n'
        '      <div class="strip">\n' + "\n".join(cards) + '\n      </div>\n'
        '      <div class="arrows">\n'
        '        <button type="button" data-strip-prev aria-label="Scroll designs left">&#8592;</button>\n'
        '        <button type="button" data-strip-next aria-label="Scroll designs right">&#8594;</button>\n'
        '      </div>\n'
        '    </div>'
    )


def lines_list():
    rows = []
    for L in LINES:
        t = "<br>".join(esc(x) for x in L["text"].split("\n"))
        rows.append(
            '        <div class="ln"><span class="n">%03d</span><span class="t">%s</span></div>'
            % (L["n"], t)
        )
    return "\n".join(rows)


def spec_list():
    return "\n".join(
        '        <li><span class="n">%02d</span><span class="t">%s<em>%s</em></span></li>'
        % (i + 1, esc(t), esc(s))
        for i, (t, s) in enumerate(SPECS)
    )


def hoodie_spec_list():
    return "\n".join(
        '        <li><span class="n">%02d</span><span class="t">%s<em>%s</em></span></li>'
        % (i + 1, esc(t), esc(s))
        for i, (t, s) in enumerate(HOODIE_SPECS)
    )


def size_chips(name="chest"):
    return "\n".join(
        '            <label class="chip"><input type="checkbox" name="%s" value="%d"><span>%d</span></label>'
        % (name, c, c)
        for c in (40, 42, 44, 46)
    )


# ---------------------------------------------------------------- pages

def page_index():
    body = """
  <section class="hero">
    <p class="blink">&#9679; Now taking orders — 240 GSM tees · 420 GSM hoodies · white ink · colour images</p>
    <h1>Your line.<br>Your image.<br><span>Your imagination.</span></h1>
    <p class="lede"><b>Product — Customised oversized tees.</b> One black heavyweight round-neck, printed to order. Pick a line from our 195, send your own image, or take the blank shirt as it is.</p>
    <div class="cta">
      <a class="btn btn-hi" href="blank-tee.html">ORDER A BLANK TEE — ₹600</a>
      <a class="btn" href="pricing.html">PRINTED FROM ₹1,000</a>
    </div>
  </section>

  <section class="sec" id="specs">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>THE SHIRT</b></p>
        <h2>Specifications</h2>
      </div>
      <p class="note">Ten points, no fine print. Everything below is what you get on every piece.</p>
    </div>
    <div class="specsplit">
      <figure class="spec-art">
        <img src="%simg/hero-spec.png" alt="Your line, your image, your imagination — printed in white on black">
        <figcaption>Your line · your image · your imagination</figcaption>
      </figure>
      <ul class="specs">
%s
      </ul>
    </div>
  </section>

  <section class="sec sec-alt strip-sec" id="designs">
    <div class="sec-head">
      <div>
        <p class="ey">02 / <b>THE CATALOGUE</b></p>
        <h2>34 designs</h2>
      </div>
      <p class="note">Scroll sideways through the full parade — exactly in the order we sent them. White ink sits on the black shirt; colour images print in full colour.</p>
    </div>
%s
  </section>

  <section class="sec" id="lines">
    <div class="sec-head">
      <div>
        <p class="ey">03 / <b>OUR SUGGESTIONS</b></p>
        <h2>195 lines</h2>
      </div>
      <p class="note">Every line we have, in order. Type in the box to filter, then pick one when you order — it prints in white, centre chest.</p>
    </div>
    <div class="lnbar">
      <input class="lnfilter" id="lnFilter" type="search" placeholder="Filter 195 lines…" autocomplete="off">
      <span class="lncount" id="lnCount">195 / 195 LINES</span>
    </div>
    <div class="lines">
%s
    </div>
  </section>

  <section class="sec" id="hoodies">
    <div class="sec-head">
      <div>
        <p class="ey">04 / <b>NEW</b></p>
        <h2>Hoodies</h2>
      </div>
      <p class="note">Heavy fleece for the winter — same idea as the tee, heavier cloth. Black, unisex, printed or embroidered to order.</p>
    </div>
    <div class="grid2">
      <div class="panel panel-hi">
        <p class="lab lab-w">420 GSM pullover hoodie</p>
        <p class="price"><small>₹</small>1,800</p>
        <p class="fine bd">100%% cotton heavy fleece, relaxed oversized with dropped shoulders, full sleeve, about 800 g. ₹350 extra for a print front or back; embroidery priced to the design.</p>
        <p style="margin:18px 0 0"><a class="btn btn-hi btn-block" href="hoodies.html">SEE THE HOODIES</a></p>
      </div>
      <div class="panel">
        <p class="lab">Why 420 GSM</p>
        <p class="fine" style="font-size:13px;line-height:1.8">Most hoodies are 200–320 GSM. Ours is 420 — a much warmer layer for North Indian winters. Need it sooner? A 400 GSM version sits as ready stock in M, L and XL, out in 7–10 days.</p>
        <p style="margin:18px 0 0"><a class="btn btn-block" href="hoodies.html#compare">HOW WE COMPARE</a></p>
      </div>
    </div>
  </section>

  <section class="sec sec-alt">
    <div class="sec-head">
      <div>
        <p class="ey">05 / <b>WHAT NEXT</b></p>
        <h2>Three ways in</h2>
      </div>
    </div>
    <div class="grid3">
      <div class="panel">
        <p class="lab">Blank</p>
        <p class="price"><small>₹</small>600</p>
        <p class="fine">Plain black oversized tee. Pick your chest size, pay by UPI QR.</p>
        <p style="margin:18px 0 0"><a class="btn btn-block" href="blank-tee.html">BLANK TEE</a></p>
      </div>
      <div class="panel">
        <p class="lab">Front printed</p>
        <p class="price"><small>₹</small>1,000</p>
        <p class="fine">One of our 195 lines, or your own words, printed in white on the front.</p>
        <p style="margin:18px 0 0"><a class="btn btn-block" href="pricing.html">SEE PRICING</a></p>
      </div>
      <div class="panel">
        <p class="lab">Front + back</p>
        <p class="price"><small>₹</small>1,100</p>
        <p class="fine">Front print, and back too if you want both. Full colour on black.</p>
        <p style="margin:18px 0 0"><a class="btn btn-hi btn-block" href="order.html">HOW TO ORDER</a></p>
      </div>
    </div>
    <p class="fine" style="margin-top:26px">Ordering multiple pieces? The price can come down — <a href="contact.html">contact us</a> to know more.</p>
  </section>
""" % (P, spec_list(), designs_strip(), lines_list())
    return shell(
        "MAHUS — Customised Oversized Tees",
        "MAHUS prints your line, your image, your imagination on a 240 GSM black oversized tee. 34 designs, 195 lines, plain black from ₹600 — and 420 GSM hoodies from ₹1,800.",
        "index.html", body,
    )


def page_size_chart():
    rows = "\n".join(
        '        <tr><th>%s</th><td>%d</td><td>%d</td></tr>' % (s, c, l)
        for s, c, l in (
            ("XS", 36, 26), ("S", 38, 27), ("M", 40, 28), ("L", 42, 29),
            ("XL", 44, 30), ("2XL", 46, 31), ("3XL", 48, 32), ("4XL", 50, 33),
            ("5XL", 52, 34), ("6XL", 54, 35), ("7XL", 56, 36),
        )
    )
    body = """
  <section class="hero">
    <p class="blink">&#9679; Tab 2 — view size chart</p>
    <h1>Size<br><span>chart.</span></h1>
    <p class="lede">Chest sizes with lengths only. Measure once, order once. The shirt is oversized by design — if you want a closer fit, go one chest size down.</p>
  </section>

  <section class="sec">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>MEASUREMENTS</b></p>
        <h2>Chest &amp; length</h2>
      </div>
      <p class="note">Flat measurement, in inches — the full run, XS to 7XL.</p>
    </div>
    <div class="specsplit" style="align-items:start">
      <table class="chart">
        <thead><tr><th>Size</th><th>Chest (inches)</th><th>Length (inches)</th></tr></thead>
        <tbody>
%s
        </tbody>
      </table>
      <div class="panel">
        <p class="lab">How to measure</p>
        <p class="fine" style="font-size:13px;line-height:1.8">
          <b>Chest:</b> measure around your upper body just under the arms, across the shoulder blades, holding the tape firm and level.<br><br>
          <b>Length:</b> measure from the shoulder area up to the bottom part of your t-shirt, usually just below your waistline. Snug, but not too tight or too loose.
        </p>
      </div>
    </div>
  </section>

  <section class="sec sec-alt">
    <div class="sec-head">
      <div>
        <p class="ey">02 / <b>REFERENCE</b></p>
        <h2>How to measure</h2>
      </div>
      <p class="note">The chart we were sent — same two points, every size from XS to 7XL.</p>
    </div>
    <figure class="howto" style="margin:0">
      <img src="%simg/size-chart.png" alt="How to measure chest and length on a t-shirt">
    </figure>
    <p style="margin:26px 0 0"><a class="btn btn-hi" href="blank-tee.html">PICK YOUR SIZE →</a></p>
  </section>
""" % (rows, P)
    return shell(
        "Size Chart — MAHUS",
        "MAHUS size chart: XS to 7XL — chest 36 to 56 inches, length 26 to 36 inches, plus how to measure.",
        "size-chart.html", body,
    )


def page_blank_tee():
    body = """
  <section class="hero">
    <p class="blink">&#9679; Tab 3 — blank t-shirt</p>
    <h1>Blank<br><span>black tee.</span></h1>
    <p class="lede">The shirt as it is — nothing printed on it. 240 GSM, 100%% cotton, oversized, ribbed collar. <b>₹600 per piece.</b> Choose your chest size, choose a quantity, pay by UPI QR or send the order on WhatsApp.</p>
  </section>

  <section class="sec" data-calc="blank">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>CONFIGURE</b></p>
        <h2>Build the order</h2>
      </div>
      <p class="note">Only four chest sizes in stock for the blank: 40, 42, 44 and 46. See the <a href="size-chart.html">size chart</a> for lengths.</p>
    </div>

    <div class="grid2">
      <div class="panel">
        <p class="lab lab-w">Chest size — tick every size you need</p>
        <div class="chips">
%s
        </div>

        <p class="lab lab-w" style="margin-top:30px">Quantity</p>
        <label class="field"><b>Pieces</b><input type="number" name="qty" min="1" max="99" value="1" inputmode="numeric"></label>

        <p class="lab lab-w" style="margin-top:24px">Price</p>
        <label class="opt"><input type="radio" name="print" value="600" checked><span><b>Blank black tee</b><i>₹600 per piece</i></span></label>

        <p class="fine">Want something printed on it instead? That is the <a href="pricing.html">printed tee</a>. Ordering multiple pieces — the price can come down, <a href="contact.html">contact us</a> to know more.</p>
      </div>

      <div class="sum">
        <p class="lab lab-w">Order summary</p>
        <dl>
          <dt>Print</dt><dd>None — plain</dd>
          <dt>Chest</dt><dd class="out-sizes">Select chest size</dd>
          <dt>Unit</dt><dd class="out-unit">₹600</dd>
          <dt>Qty</dt><dd class="out-qty">1</dd>
          <dt>Gross</dt><dd class="out-gross">₹600</dd>
        </dl>
        <p class="inv"><span>Invoice value</span><b class="out-invoice">₹600</b></p>
        <p class="calc-error" role="status"></p>
        <a class="btn btn-wa btn-block" data-pay href="%s">SEND ORDER ON WHATSAPP</a>
        <p class="fine">Or pay straight by UPI — the QR is on the <a href="order.html">order page</a>. Prefer to talk it through first? WhatsApp us on %s.</p>
      </div>
    </div>
  </section>

  <section class="sec sec-alt">
    <div class="sec-head">
      <div>
        <p class="ey">02 / <b>QUESTIONS</b></p>
        <h2>Before you order</h2>
      </div>
    </div>
    <div class="grid3">
      <div class="panel"><p class="lab">Which sizes?</p><p class="fine" style="font-size:13px;line-height:1.8">Only 40, 42, 44 and 46 in the blank tee. Each has a fixed length — 28, 29, 30 and 31 inches respectively.</p></div>
      <div class="panel"><p class="lab">How many?</p><p class="fine" style="font-size:13px;line-height:1.8">Any quantity — and on multiple pieces the price can decline. Order on WhatsApp and we confirm the total and the dispatch date before you pay.</p></div>
      <div class="panel"><p class="lab">How to pay?</p><p class="fine" style="font-size:13px;line-height:1.8">Scan the UPI QR on the order page, or send the order on WhatsApp and we will share payment details there.</p></div>
    </div>
  </section>
""" % (size_chips(), WALINK, WAFLAT)
    return shell(
        "Blank Tee — MAHUS",
        "Plain black MAHUS oversized tee, 240 GSM, ₹600 per piece. Chest 40/42/44/46, order on WhatsApp or pay by UPI QR.",
        "blank-tee.html", body,
    )


def page_pricing():
    body = """
  <section class="hero">
    <p class="blink">&#9679; Tab 4 — pricing</p>
    <h1>Front.<br>Front<br><span>&amp; back.</span></h1>
    <p class="lede">Three prices, that is all. A blank tee is ₹600. Something said or shown on the front takes it to ₹1,000. Add the back as well and it is ₹1,100. Lines print in white; your own image prints in full colour.</p>
  </section>

  <section class="sec">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>THE THREE PRICES</b></p>
        <h2>What it costs</h2>
      </div>
      <p class="note">Per piece. The blank tee underneath is the same 240 GSM black shirt in every case.</p>
    </div>
    <div class="grid3">
      <div class="panel">
        <p class="lab">Blank tee</p>
        <p class="price"><small>₹</small>600</p>
        <p class="fine">Nothing printed on it — plain black 240 GSM oversized tee. See the <a href="blank-tee.html">blank tee</a> page.</p>
      </div>
      <div class="panel panel-hi">
        <p class="lab lab-w">Front only</p>
        <p class="price"><small>₹</small>1,000</p>
        <p class="fine">Some saying, image or line on the front. White ink for text, full colour for images, centre chest.</p>
      </div>
      <div class="panel">
        <p class="lab">Front + back</p>
        <p class="price"><small>₹</small>1,100</p>
        <p class="fine">The front print as above, plus something on the back. ₹100 more, and the back can be different from the front.</p>
      </div>
    </div>
    <p class="fine" style="margin-top:26px">Ordering multiple pieces? Then the price can decline — <a href="contact.html">contact us</a> to know more.</p>
  </section>

  <section class="sec sec-alt" data-calc="custom">
    <div class="sec-head">
      <div>
        <p class="ey">02 / <b>CONFIGURE</b></p>
        <h2>Build the order</h2>
      </div>
      <p class="note">Pick front or front-and-back, type the line you want, tick your chest sizes. The invoice updates as you go.</p>
    </div>

    <div class="grid2">
      <div class="panel">
        <p class="lab lab-w">Print</p>
        <label class="opt"><input type="radio" name="print" value="1000" checked><span><b>Front</b><i>₹1,000</i></span></label>
        <label class="opt"><input type="radio" name="print" value="1100"><span><b>Front + back</b><i>₹1,100</i></span></label>

        <p class="lab lab-w" style="margin-top:30px">What gets printed</p>
        <label class="field"><b>Your line — type it exactly as it should print</b><input type="text" name="printcopy" maxlength="60" placeholder="YOUR LINE HERE" autocomplete="off"></label>
        <p class="fine">Or pick one of our <a href="index.html#lines">195 lines</a>, or send your own image on WhatsApp after ordering.</p>

        <p class="lab lab-w" style="margin-top:30px">Chest size — tick every size you need</p>
        <div class="chips">
%s
        </div>

        <p class="lab lab-w" style="margin-top:30px">Quantity</p>
        <label class="field"><b>Pieces</b><input type="number" name="qty" min="1" max="99" value="1" inputmode="numeric"></label>
      </div>

      <div class="sum">
        <p class="lab lab-w">Order summary</p>
        <dl>
          <dt>Copy</dt><dd class="out-copy" style="max-width:180px;text-align:right">Type your line</dd>
          <dt>Chest</dt><dd class="out-sizes">Select chest size</dd>
          <dt>Unit</dt><dd class="out-unit">₹1,000</dd>
          <dt>Qty</dt><dd class="out-qty">1</dd>
          <dt>Gross</dt><dd class="out-gross">₹1,000</dd>
        </dl>
        <p class="inv"><span>Invoice value</span><b class="out-invoice">₹1,000</b></p>
        <p class="calc-error" role="status"></p>
        <a class="btn btn-hi btn-block" data-pay href="%s">SEND ORDER ON WHATSAPP</a>
        <p class="fine">Paying by UPI instead? The QR is on the <a href="order.html">order page</a> — same value either way.</p>
      </div>
    </div>
  </section>

  <section class="sec">
    <div class="sec-head">
      <div>
        <p class="ey">03 / <b>PRINT</b></p>
        <h2>White ink, colour images</h2>
      </div>
    </div>
    <div class="grid2">
      <div class="panel"><p class="lab">Lines</p><p class="fine" style="font-size:13px;line-height:1.8">Printed in white on the black shirt. Centre chest, roughly ten inches wide. Any of our 195 lines, or your own words.</p></div>
      <div class="panel"><p class="lab">Images</p><p class="fine" style="font-size:13px;line-height:1.8">Your image prints in full colour, same placement. Send the file on WhatsApp after you order and we share a proof before printing.</p></div>
    </div>
  </section>
""" % (size_chips(), WALINK)
    return shell(
        "Pricing — MAHUS",
        "MAHUS printed tees: ₹600 blank, ₹1,000 for a front print, ₹1,100 for front and back. Lines in white ink, images in full colour. Bulk orders priced on request.",
        "pricing.html", body,
    )


def page_order():
    body = """
  <section class="hero">
    <p class="blink">&#9679; Tab 5 — to order</p>
    <h1>Call.<br>WhatsApp.<br><span>Or scan.</span></h1>
    <p class="lede">Two ways to place the order, and both land with us directly. Call or WhatsApp <b>%s</b> — or scan the UPI QR below and send us the screenshot.</p>
    <div class="cta">
      <a class="btn btn-wa" href="%s">WHATSAPP %s</a>
      <a class="btn btn-hi" href="tel:+%s">CALL %s</a>
    </div>
  </section>

  <section class="sec">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>UPI QR</b></p>
        <h2>Scan to pay</h2>
      </div>
      <p class="note">Open any UPI app, scan, and pay the invoice value. Then WhatsApp us the screenshot with your name and mobile number.</p>
    </div>
    <div class="panel panel-hi">
      <div class="qrblock">
        <img class="qr" src="%simg/upi-qr.svg" alt="MAHUS UPI QR code — placeholder, live code to follow">
        <div style="min-width:240px;flex:1">
          <p class="lab lab-w">Pay to</p>
          <p class="upi">mahus@okhdfcbank</p>
          <p class="lab lab-w" style="margin-top:20px">Amount</p>
          <p class="upi" style="font-size:26px" id="upiAmount">₹600</p>
          <p class="fine">Pay the invoice value of whatever you have configured on the <a href="blank-tee.html">blank tee</a> or <a href="pricing.html">pricing</a> page. The QR itself is a placeholder until this week&rsquo;s code from the bank is live.</p>
        </div>
      </div>
      <ol class="steps">
        <li>Configure your tee and note the <b>invoice value</b></li>
        <li>Scan the UPI QR and pay that amount</li>
        <li>WhatsApp the screenshot to <b>%s</b> with your <b>name + mobile number</b></li>
        <li>We reply with the print proof — approve, and it goes to courier</li>
      </ol>
    </div>
  </section>

  <section class="sec sec-alt" id="buyer">
    <div class="sec-head">
      <div>
        <p class="ey">02 / <b>YOUR DETAILS</b></p>
        <h2>Send the order</h2>
      </div>
      <p class="note">Fill this in and it goes straight to our WhatsApp as a ready message. Nothing is stored on this site.</p>
    </div>
    <div class="panel">
      <form id="buyerForm" onsubmit="return false">
        <div class="grid2">
          <label class="field"><b>Name</b><input type="text" name="name" placeholder="Full name" autocomplete="name" required></label>
          <label class="field"><b>Mobile (order reference)</b><input type="tel" name="mobile" placeholder="10-digit mobile" autocomplete="tel" required></label>
          <label class="field"><b>Email</b><input type="email" name="email" placeholder="you@example.com" autocomplete="email"></label>
          <label class="field"><b>Courier address</b><input type="text" name="address" placeholder="House / street / city / PIN" autocomplete="street-address"></label>
        </div>
        <label class="field"><b>Order notes</b><input type="text" name="notes" placeholder="What you are ordering, chest sizes, quantity, anything else"></label>
        <button class="btn btn-wa" type="submit">SEND ON WHATSAPP</button>
        <p class="fine">Or just call %s. We are on WhatsApp through the day.</p>
      </form>
    </div>
  </section>
""" % (WAFLAT, WALINK, WAFLAT, WA, WAFLAT, P, WAFLAT, WAFLAT)
    return shell(
        "Order — MAHUS",
        "Order from MAHUS: call or WhatsApp %s, or scan the UPI QR to pay. Proof shared before printing, PAN-India courier." % WAFLAT,
        "order.html", body,
    )


def page_polo():
    body = """
  <section class="hero">
    <p class="blink">&#9679; Tab 6 — black polo t-shirts</p>
    <h1>Black<br>polo.<br><span>Also custom.</span></h1>
    <p class="lede">Black polo t-shirts — and yes, those can be customised too. Same idea: your line, your image, your imagination, printed to order.</p>
    <div class="cta">
      <a class="btn btn-wa" href="%s">ASK ABOUT POLOS ON WHATSAPP</a>
      <a class="btn" href="pricing.html">SEE TEE PRICING</a>
    </div>
  </section>

  <section class="sec">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>POLO PROGRAM</b></p>
        <h2>What we can say now</h2>
      </div>
      <p class="note">The polo line is early. Everything below is confirmed; the rest we will put up as it is decided.</p>
    </div>
    <div class="grid3">
      <div class="panel panel-hi"><p class="lab lab-w">Colour</p><p class="fine" style="font-size:13px;line-height:1.8">Black, same as the round-neck. One colourway.</p></div>
      <div class="panel panel-hi"><p class="lab lab-w">Customisation</p><p class="fine" style="font-size:13px;line-height:1.8">Your line or your image, printed to order — same as the tee.</p></div>
      <div class="panel"><p class="lab">Sizing &amp; pricing</p><p class="fine" style="font-size:13px;line-height:1.8">Not finalised yet. Message us and we will confirm both before you commit to anything.</p></div>
    </div>
    <p style="margin:30px 0 0"><a class="btn btn-wa" href="%s">REGISTER INTEREST — WHATSAPP %s</a></p>
  </section>
""" % (WALINK, WALINK, WAFLAT)
    return shell(
        "Polo — MAHUS",
        "MAHUS black polo t-shirts, also customised with your line or your image. Ask us on WhatsApp.",
        "polo.html", body,
    )


def page_about():
    body = """
  <section class="hero">
    <p class="blink">&#9679; About us</p>
    <h1>One shirt.<br><span>Your words on it.</span></h1>
    <p class="lede">MAHUS makes a single product and lets you say what you want on it. Heavyweight black cotton, white ink for lines, full colour for images, printed to order.</p>
  </section>

  <section class="sec">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>THE STORY</b></p>
        <h2>About MAHUS</h2>
      </div>
      <p class="note">The short version — the long-form story still to be written.</p>
    </div>
    <div class="grid2">
      <div class="panel">
        <p class="lab lab-w">Who makes it</p>
        <p class="fine bd">MAHUS Enterprises is a new apparel venture by <b>Akaljot Singh</b> — B.Tech, Mechanical Engineering, IIT Delhi, class of 1998 — getting premium winter hoodies and customised tees manufactured: black, heavyweight, printed to order.</p>
        <p class="fine bd">This is the first revision of the website. It will be re-cut properly next year — for now, simple and straight to the point.</p>
      </div>
      <div class="panel">
        <p class="lab lab-w">The facts that are already fixed</p>
        <ul class="specs">
          <li><span class="n">01</span><span class="t">One product<em>Customised oversized tees</em></span></li>
          <li><span class="n">02</span><span class="t">One colourway<em>Black, with white ink or colour print</em></span></li>
          <li><span class="n">03</span><span class="t">Printed to order<em>Proof shared before printing</em></span></li>
          <li><span class="n">04</span><span class="t">PAN-India courier<em>Dispatched once you approve the proof</em></span></li>
        </ul>
      </div>
    </div>
  </section>

  <section class="sec sec-alt">
    <div class="sec-head">
      <div>
        <p class="ey">02 / <b>CATALOGUE</b></p>
        <h2>34 designs, 195 lines</h2>
      </div>
      <p class="note">Everything on the site comes from two lists we were given — and they are all up on the home page, in order.</p>
    </div>
    <div class="cta">
      <a class="btn btn-hi" href="index.html#designs">SEE THE 34 DESIGNS</a>
      <a class="btn" href="index.html#lines">READ THE 195 LINES</a>
    </div>
  </section>
"""
    return shell(
        "About — MAHUS",
        "About MAHUS: one black oversized tee, printed to order with your line or your image.",
        "about.html", body,
    )


def page_contact():
    body = """
  <section class="hero">
    <p class="blink">&#9679; Contact us</p>
    <h1>Talk<br><span>to us.</span></h1>
    <p class="lede">WhatsApp is the fastest. Call if you would rather hear a voice. Email works too — we get to it the same day.</p>
    <div class="cta">
      <a class="btn btn-wa" href="%s">WHATSAPP %s</a>
      <a class="btn btn-hi" href="tel:+%s">CALL %s</a>
      <a class="btn" href="mailto:%s">EMAIL US</a>
    </div>
  </section>

  <section class="sec">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>DETAILS</b></p>
        <h2>Reach MAHUS</h2>
      </div>
    </div>
    <div class="grid3">
      <div class="panel panel-hi">
        <p class="lab lab-w">WhatsApp</p>
        <p class="price" style="font-size:clamp(26px,4vw,38px)">%s</p>
        <p class="fine">Orders, questions, proofs — all on WhatsApp through the day.</p>
        <p style="margin:18px 0 0"><a class="btn btn-wa btn-block" href="%s">OPEN WHATSAPP</a></p>
      </div>
      <div class="panel">
        <p class="lab">Phone</p>
        <p class="price" style="font-size:clamp(26px,4vw,38px)">%s</p>
        <p class="fine">Call the same number if you would rather talk it through.</p>
        <p style="margin:18px 0 0"><a class="btn btn-block" href="tel:+%s">CALL NOW</a></p>
      </div>
      <div class="panel">
        <p class="lab">Email</p>
        <p class="fine" style="font-size:15px;line-height:1.7;margin-top:10px"><a href="mailto:%s">%s</a></p>
        <p class="fine">For anything that needs a file attached, or a longer note.</p>
        <p style="margin:18px 0 0"><a class="btn btn-block" href="mailto:%s">WRITE TO US</a></p>
      </div>
    </div>
  </section>

  <section class="sec sec-alt">
    <div class="sec-head">
      <div>
        <p class="ey">02 / <b>BEFORE YOU WRITE</b></p>
        <h2>Handy links</h2>
      </div>
    </div>
    <div class="cta">
      <a class="btn" href="size-chart.html">SIZE CHART</a>
      <a class="btn" href="blank-tee.html">BLANK TEE — ₹600</a>
      <a class="btn" href="pricing.html">PRICING — ₹1,000 / ₹1,100</a>
      <a class="btn" href="order.html">ORDER &amp; UPI QR</a>
    </div>
  </section>
""" % (WALINK, WAFLAT, WA, WAFLAT, EMAIL, WAFLAT, WALINK, WAFLAT, WA, EMAIL, EMAIL, EMAIL)
    return shell(
        "Contact — MAHUS",
        "Contact MAHUS: WhatsApp and phone %s, email %s." % (WAFLAT, EMAIL),
        "contact.html", body,
    )


def page_hoodies():
    body = """
  <section class="hero">
    <p class="blink">&#9679; New — 420 GSM heavy fleece hoodies</p>
    <h1>Heavyweight.<br>420 gsm.<br><span>Black.</span></h1>
    <p class="lede"><b>The hoodie.</b> 100%% cotton heavy fleece at 420 GSM — a proper winter layer, not a light one. Unisex, relaxed oversized with dropped shoulders, full sleeve, about 800 g on the scale. Blank at ₹1,800; add a print for ₹350, or embroider to the design.</p>
    <div class="cta">
      <a class="btn btn-hi" href="#pricing">HOODIE PRICING — ₹1,800</a>
      <a class="btn btn-wa" href="%s">ASK ON WHATSAPP</a>
    </div>
  </section>

  <section class="sec" id="specs">
    <div class="sec-head">
      <div>
        <p class="ey">01 / <b>THE HOODIE</b></p>
        <h2>Specifications</h2>
      </div>
      <p class="note">Twenty-one points off the spec sheet, set in twelve lines. This is the cloth we make them from.</p>
    </div>
    <div class="specsplit">
      <figure class="spec-art">
        <img src="%simg/hoodie.svg" alt="Black oversized pullover hoodie in 420 GSM heavy fleece">
        <figcaption>420 GSM · heavy fleece · black</figcaption>
      </figure>
      <ul class="specs">
%s
      </ul>
    </div>
  </section>

  <section class="sec sec-alt" id="pricing">
    <div class="sec-head">
      <div>
        <p class="ey">02 / <b>PRICING</b></p>
        <h2>What it costs</h2>
      </div>
      <p class="note">Per piece. Blank is blank — a print adds ₹350 to it, on the front, the back, or both.</p>
    </div>
    <div class="grid3">
      <div class="panel">
        <p class="lab">Blank hoodie</p>
        <p class="price"><small>₹</small>1,800</p>
        <p class="fine">Plain black 420 GSM pullover, nothing on it.</p>
      </div>
      <div class="panel panel-hi">
        <p class="lab lab-w">With a print</p>
        <p class="price"><small>₹</small>2,150</p>
        <p class="fine">Blank plus one DTF print, front or back — ₹350 more. Less per piece on multiple hoodies.</p>
      </div>
      <div class="panel">
        <p class="lab">Front + back</p>
        <p class="price"><small>₹</small>2,500</p>
        <p class="fine">A print on each side — ₹700 on top of the blank.</p>
      </div>
    </div>
    <div class="grid2" style="margin-top:26px">
      <div class="panel">
        <p class="lab">Chest print — front</p>
        <figure class="howto" style="margin:12px 0 0">
          <img src="%simg/hoodie-chest.jpg" alt="Black hoodie with a small chest print, front view">
        </figure>
      </div>
      <div class="panel">
        <p class="lab">Full-colour print — back</p>
        <figure class="howto" style="margin:12px 0 0">
          <img src="%simg/hoodie-back.jpg" alt="Black hoodie with a large full-colour back print">
        </figure>
      </div>
    </div>
  </section>

  <section class="sec" id="compare">
    <div class="sec-head">
      <div>
        <p class="ey">03 / <b>COMPARISON</b></p>
        <h2>How we compare</h2>
      </div>
      <p class="note">The two we get measured against, on the five points that matter — fabric, price, minimum order, stock and colour.</p>
    </div>
    <div class="tscroll">
      <table class="chart">
        <thead><tr><th>Point</th><th>MAHUS</th><th>Brand X</th><th>Brand Y</th></tr></thead>
        <tbody>
          <tr><th>Fabric</th><td>100%% cotton heavy fleece · 420 GSM</td><td>&ldquo;Rich Cotton&rdquo; — no GSM given</td><td>&ldquo;Poly Cotton&rdquo; blend — no GSM given</td></tr>
          <tr><th>Price</th><td>₹1,800</td><td>₹2,325</td><td>₹1,725</td></tr>
          <tr><th>Minimum order</th><td>1 — when combined orders cross 20</td><td>5</td><td>5</td></tr>
          <tr><th>Stock</th><td>Live now</td><td>200 available — last updated 17.08.2026</td><td>Out of stock</td></tr>
          <tr><th>Colour</th><td>Black</td><td>Charcoal grey</td><td>Black</td></tr>
        </tbody>
      </table>
    </div>
    <p class="fine">MOQ 1 is on the combined order we place with the manufacturer — if your quantity is small or urgent, ask anyway and we will confirm. A 400 GSM version is also ready in M, L and XL.</p>
  </section>

  <section class="sec sec-alt">
    <div class="sec-head">
      <div>
        <p class="ey">04 / <b>GOOD TO KNOW</b></p>
        <h2>Before you order</h2>
      </div>
    </div>
    <div class="grid3">
      <div class="panel"><p class="lab">Pullover or zip</p><p class="fine" style="font-size:13px;line-height:1.8">Both possible. A zip runs about ₹60–70 more and is cut once we know how many zip orders there are — say if you want one.</p></div>
      <div class="panel panel-hi"><p class="lab lab-w">Embroidery or DTF</p><p class="fine" style="font-size:13px;line-height:1.8">Both can be provided. Prints are ₹350 a side; embroidery is quoted per design, stitched instead of printed.</p></div>
      <div class="panel"><p class="lab">Dispatch</p><p class="fine" style="font-size:13px;line-height:1.8">420 GSM: about 20 days from order. Need it sooner? 400 GSM ready stock in M, L and XL — 7 to 10 days.</p></div>
    </div>
    <p class="fine">Something lighter? 300 GSM is supplied for milder winters — indoors around 20°C. Chest sizes XS to 7XL, 36 to 56 inches; send yours in inches, not letters.</p>
    <p style="margin:30px 0 0"><a class="btn btn-wa" href="%s">ORDER A HOODIE — WHATSAPP %s</a></p>
  </section>
""" % (WALINK, P, hoodie_spec_list(), P, P, WALINK, WAFLAT)
    return shell(
        "Hoodies — MAHUS",
        "MAHUS hoodies: 420 GSM 100% cotton heavy fleece pullover, black, unisex, ₹1,800 blank, +₹350 per print. Printed or embroidered to order, MOQ from 1.",
        "hoodies.html", body,
    )


PAGES = {
    "index.html": page_index,
    "size-chart.html": page_size_chart,
    "blank-tee.html": page_blank_tee,
    "pricing.html": page_pricing,
    "hoodies.html": page_hoodies,
    "order.html": page_order,
    "polo.html": page_polo,
    "about.html": page_about,
    "contact.html": page_contact,
}

if __name__ == "__main__":
    # light  -> website/ root  (https://mahus.in/)
    # dark   -> website/black/ (https://mahus.in/black/)
    for theme in ("dark", "light"):
        set_theme(theme)
        outdir = HERE if theme == "light" else D("black")
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        for name, fn in PAGES.items():
            out = os.path.join(outdir, name)
            with io.open(out, "w", encoding="utf-8") as f:
                f.write(fn())
            print("%-5s %-18s %6d bytes" % (theme, name, os.path.getsize(out)))
