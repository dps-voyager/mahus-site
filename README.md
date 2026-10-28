# MAHUS — live website (rev 1.1)

Multi-page site built from the client's final direction (`samples/05-mach10/`)
and their brief **To Do_For Website_5.0.docx**, using the artwork in
**Images for Darshan.zip**. Hoodie content from **Mahus HOODIES writeup.pdf**
and **Hoodie Specifications.pdf**.

**Theme:** black background, white type, mach10's technical grid + condensed
display face. No blue or yellow — emphasis is done by inversion (white block,
black text). WhatsApp green appears only on WA buttons.

**Two versions, one folder:** every page is generated twice — into `black/`
(white ink on black) and `light/` (`data-theme="light"`, black ink on white).
The HUD toggle (`◐ WHITE` / `◐ BLACK`) switches between the same page in the
other version; both are kept in step by the dual build below.

## Pages

| File | Brief tab | What it does |
|---|---|---|
| `index.html` | Home | Hero ("Your line / Your image / Your imagination"), 10 specifications beside the client's `00_…` artwork, horizontal carousel of **all 34 designs** (client's PNGs, in the order sent), vertical list of **all 195 lines** with a live filter, three price entry points |
| `size-chart.html` | Tab 2 | XS to 7XL — chest 36→56 inches, length 26→36, plus the supplied "How to measure" image |
| `blank-tee.html` | Tab 3 | Blank tee ₹600 — chest-size checkboxes (40/42/44/46 only), quantity, live invoice, order via WhatsApp |
| `pricing.html` | Tab 4 | Blank ₹600 / front ₹1,000 / front + back ₹1,100, with a configurator: print side, your line, chest sizes, quantity. Bulk orders priced on request |
| `hoodies.html` | — | 420 GSM hoodie — specs beside the hoodie drawing (incl. ~800 g weight, XS–7XL), pricing ₹1,800 blank / ₹2,150 with a print / ₹2,500 front + back, chest & back print photos, comparison table (MAHUS vs Brand X vs Brand Y), good-to-know notes |
| `order.html` | Tab 5 | WhatsApp + phone, UPI QR with VPA and amount, 4-step flow, buyer-details form that composes the WhatsApp message |
| `polo.html` | Tab 6 | Black polo — also customised; sizing/pricing flagged as not yet final |
| `about.html` | — | Founder block (Akaljot Singh, IIT Delhi '98) from `notes1.rtf`; long-form story still to come |
| `contact.html` | — | WhatsApp 95923-64304 · call · mahusenterprises@gmail.com |

## Files

```
website/
├── black/                      the 9 pages, black version (generated)
├── light/                      the 9 pages, white version (generated)
├── styles.css                  dark tokens in :root + [data-theme="light"] overrides
├── site.js                     line filter, strip arrows, order calculators, WhatsApp composer
├── favicon.svg
├── _build.py                   regenerates both versions (shared header/footer/nav)
├── data/
│   ├── designs.json            34 designs: file + caption
│   └── lines195.json           195 lines, extracted verbatim from Suggestions_Ideas.docx
└── img/
    ├── designs/d01–d34.png     the client's 34 PNGs, renamed 01–34
    ├── hero-spec.png           "00_ Your Line Your Image…" (home, left of specs)
    ├── hoodie.svg              hoodie technical drawing (hoodies page)
    ├── hoodie-chest.jpg        production photo — chest print, front
    ├── hoodie-back.jpg         production photo — full-colour back print
    ├── size-chart.png          "How to measure" graphic (from Size Chart.pdf)
    ├── upi-qr.svg              UPI QR — placeholder pattern
    └── tee.svg
```

## Regenerating

Content is data-driven, so a changed list does not mean hand-editing HTML:

```bash
cd website
python3 _build.py      # rebuilds all 9 pages in BOTH versions (black/ + light/)
```

To change the design catalogue, edit `data/designs.json` (and drop any new PNG
into `img/designs/`). To change the line library, edit `data/lines195.json`.

## Viewing

```bash
cd website && python3 -m http.server 8899
# http://localhost:8899/black/index.html    black version (default)
# http://localhost:8899/light/index.html    white version
```

Any static host works — there is no build step at serve time.

## Behaviour

* **Theme toggle** (HUD, every page) — jumps to the same page in the other
  version: `black/index.html` ⇄ `light/index.html`, same anchor preserved.
* **Line filter** (home) — filters the 195 lines as you type, with a live count.
* **Design strip** — horizontal scroll with snap; ← → buttons page it.
* **Order calculators** (blank tee + pricing) — unit × qty, live invoice, and a
  validation line ("Please tick a chest size", "type your line…"). The WhatsApp
  button stays disabled until the order is valid, then opens a pre-filled
  message with print side, copy, chest sizes, qty and value.
* **Buyer form** (order) — composes the same WhatsApp message; nothing is stored.

## Placeholders to swap before launch

| Item | Where | Note |
|---|---|---|
| UPI QR | `img/upi-qr.svg`, order page | Pattern, not a scannable code — client said the real QR arrives this week |
| UPI ID | `order.html` | `mahus@okhdfcbank` — confirm the real VPA |
| About matter | `about.html` | Founder block in; long-form story still to be sent by client |
| Polo sizing & pricing | `polo.html` | Deliberately marked "not finalised" |
