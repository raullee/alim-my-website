# ALIM.my — copy review (voice & craft seat)

Reviewed: `enhanced/` (all pages in the brief), plus the generated legislation library via its
sources `tools/build.py`, `tools/scenarios.py`, `tools/registry.py`. Library rendered with
`python3 tools/build.py` and read in context (`legislation/index.html`,
`legislation/doing/*/index.html`, `legislation/<act>/index.html`).

---

## VERDICT

The marketing site is publication-worthy and in places genuinely good; the legislation library is
not, because its furniture was written for a board and its scenario ledes were written for rhythm.
Three changes carry most of the fix: **(1)** replace the library's first-screen bar
`Provision of legal resources` and rewrite the Resources card that the client flagged, which is
also factually wrong (it says 18 situations; there are 19); **(2)** warm the three pages a
frightened person actually lands on — the `arrested` scenario lede, the `unpaid` lede and the
Get Help page lede — none of which currently speak to the reader at all; **(3)** retire
`instruments` / `objectives` / `creative segments` / `order of operations` from every
reader-facing label, keeping them only where they are terms of art.

Em dashes: **zero** in the copy under review. That part is already clean.

---

## THE HOUSE VOICE

Derived from the pages that are working: the home hero, `resources/`, the instrument pages, the
`gig-workers-act-2025` guide.

1. **Short declaratives, then one longer sentence that earns its length.** "Know your rights."
   "No retainer. No PR." "A guide can only take you so far."
2. **Concrete nouns from the reader's life, not from the statute book.** "DJing a club night",
   "busking", "a client won't pay", "a takedown threat". Never "creative segments", never
   "stakeholders".
3. **Second person, and the reader is the subject of the sentence.** "Know what you are signing."
   "What this does to artists." Where a line has no "you" in it, ask whether it should.
4. **Confident understatement instead of adjectives.** "This is most of what we do: pressure
   resolved before it ever becomes a case." No "powerful", no "comprehensive", no "seamless".
5. **The site admits what it does not know, and that is a voice feature.** "What is deliberately
   not here yet", "the pages here say so rather than pretend otherwise". Protect this; it is the
   reason a lawyer's site sounds trustworthy rather than salesy.
6. **British spelling, sentence case in headings, `·` as the separator, no em dashes, semicolons
   where a dash is tempting.** En dashes in date and time ranges (12–14 June) are correct and stay.
7. **Contractions: YES, in direct address.** The live pages already do it exactly right and the
   pattern is consistent enough to be a rule. Contract when speaking *to* the reader ("Tell us
   what's going on and we'll match you", "wherever you're based", "if that's easiest for you",
   "the legal cover they're routinely denied", and the search placeholder "client won't pay").
   Keep the full form only where the negation *is* the point and the uncontracted form lands
   harder: "It does not." / "Most artist stores display none of it." The legislation library
   currently uses **no** contractions anywhere in its furniture, which is the single biggest
   reason it sounds like a different, colder organisation. Fix that and half the "AI scripted"
   complaint goes away.
8. **Say the frightening thing plainly and immediately offer a person.** The disclaimer's closing
   move — "If you have a live problem, talk to us." — is the template.

---

## REWRITES

Priority order. Exact current strings given for find-and-replace.

> **Applying the library edits.** Every string below lives in a `.py` file, not in the generated
> HTML; editing `legislation/*/index.html` directly is wasted work because `python3 tools/build.py`
> overwrites it. Note also that most `lede`, `why` and `watch` values in `scenarios.py` and
> `registry.py` are **implicitly concatenated across two or three source lines**, so match on the
> whole value rather than on one line. Rebuild after every change.


---

### A. LEGISLATION LIBRARY — HERO AND HEADINGS

#### `enhanced/resources/index.html` (line 90) :: the card the client flagged
- **NOW:**
  `Start from what you are actually doing. 18 situations, from DJing a club night to busking, posting a set or chasing an unpaid fee, each resolved into the exact chain of law that reaches it, in order, and filtered by whether you are the artist, the promoter or the venue. Behind them sit 65 instruments sourced from the Attorney General&rsquo;s Chambers and mapped onto ALIM&rsquo;s three objectives and ten creative segments.`
- **PROBLEM:** Four separate tells in one paragraph — the hollow "actually"; a sentence with three
  stacked subordinate clauses ("each resolved into…, in order, and filtered by…"); the forbidden
  "whether you are a X or a Y"; and a closing sentence lifted straight from a board deck
  ("mapped onto ALIM's three objectives and ten creative segments"). It is also **factually wrong**:
  there are 19 scenarios, not 18.
- **BETTER:**
  `Start with what you&rsquo;re doing. DJing a club night, busking, posting a set, chasing a fee that never came: 19 situations, each one laid out as the laws that reach it, in the order they reach you. Say which one you are, artist, promoter or venue, and the list narrows to your part. The 65 laws and codes behind it come straight from the Attorney General&rsquo;s Chambers, and every page says how old the text is.`

#### `tools/build.py` line 695 :: library hero bar
- **NOW:** `      <span class="bar">Provision of legal resources</span>`
- **PROBLEM:** The first three words on the library's first screen, and they are grant-application
  language. Nobody has ever said "provision of legal resources" out loud. Worse, it is passive and
  institutional at the exact moment a reader is deciding whether this site is for them.
- **BETTER:** `      <span class="bar">Know your rights</span>`
  (This is already the site's own line, from `resources/` and the home ticker. Use it.)

#### `tools/build.py` lines 702–705 :: library hero lede
- **NOW:**
  ```
    <p class="page-lede">You do not need to know which Act to look for. Say what you are doing, or
      what has gone wrong, and we will show you the laws that reach it and what each one means for
      you. Everything here comes from the Attorney General's Chambers, and every page tells you how
      current it is.</p>
  ```
- **PROBLEM:** Three balanced pairs in a row ("what you are doing, or what has gone wrong" / "the
  laws that reach it and what each one means for you" / "comes from the AGC, and every page tells
  you"). The content is right; the metronome is what reads as machine-written. No contractions, and
  no offer of a person on the coldest page on the site.
- **BETTER:**
  ```
    <p class="page-lede">You don't need to know which Act to look for. Say what you're doing, or
      what's gone wrong, and we'll show you the laws that reach it, in the order they reach you.
      Everything here is the Attorney General's Chambers' own text, and every page tells you how old
      that text is. If you'd rather talk to a person, that's what <a class="ulink"
      href="{up}get-help/">Get Help</a> is for.</p>
  ```
  (`up` is already in scope in `index_page` via `depth`; if threading it is awkward, use the literal
  `../get-help/` since the library index is one level down.)

#### `tools/build.py` line 1167 :: library `<meta description>`
- **NOW:** `"Start from what you are doing. A searchable library of the Malaysian legislation "`
- **PROBLEM:** Same construction the client rejected. This is the line Google and WhatsApp show.
- **BETTER:** `"Start with what you're doing. A searchable library of the Malaysian law that "`
  (continue: `"reaches artists: copyright, censorship, licensing, employment and heritage, "` /
  `"sourced from the Attorney General's Chambers."`)

#### `tools/build.py` line 587 :: scenario page section bar
- **NOW:** `  <div class="sec-head"><div><span class="bar">Order of operations</span><h2>What reaches you, and in what order</h2></div></div>`
- **PROBLEM:** "Order of operations" is a maths/engineering term and it is redundant — the warm h2
  sitting two inches away already says it in English.
- **BETTER:** `  <div class="sec-head"><div><span class="bar">The chain</span><h2>What reaches you, and in what order</h2></div></div>`

#### `tools/build.py` line 570 :: scenario page dossier bar
- **NOW:** `      <span class="bar">Scenario · {len(sc["steps"])} instruments</span>`
- **PROBLEM:** "Scenario" is a training-exercise word, and the site already uses the warmer
  "situations" two clicks earlier ("Related situations", "19 things people come to us about").
  "Instruments" is board-deck; the page itself numbers them 01, 02, 03, so they are steps.
- **BETTER:** `      <span class="bar">Situation · {len(sc["steps"])} steps</span>`

#### `tools/build.py` line 652 :: scenario cards on the index
- **NOW:** `        f'<p class="lg-meta" style="margin-bottom:8px">{len(s["steps"])} instruments</p>'`
- **BETTER:** `        f'<p class="lg-meta" style="margin-bottom:8px">{len(s["steps"])} steps</p>'`

#### `tools/build.py` line 708 :: hero stat label
- **NOW:** `      <div class="stat"><b>{len(entries)}</b><s>instruments</s></div>`
- **BETTER:** `      <div class="stat"><b>{len(entries)}</b><s>laws &amp; codes</s></div>`

#### `tools/build.py` lines 742–743 :: tab labels
- **NOW:**
  ```
      <button class="lg-tab" role="tab" data-view="framework" aria-selected="false">The framework</button>
      <button class="lg-tab" role="tab" data-view="instruments" aria-selected="false">All instruments</button>
  ```
- **PROBLEM:** "The framework" is deck-speak; "All instruments" is opaque to a musician, for whom
  an instrument is a guitar.
- **BETTER:**
  ```
      <button class="lg-tab" role="tab" data-view="framework" aria-selected="false">The big picture</button>
      <button class="lg-tab" role="tab" data-view="instruments" aria-selected="false">The full list</button>
  ```
  (`data-view` values are internal; leave them alone.)

#### `tools/build.py` lines 752–757 :: framework panel
- **NOW:**
  ```
      <div class="sec-head"><div><span class="bar">Three objectives, ten segments</span>
        <h2>The framework, as a map</h2></div></div>
      <p class="prose" style="margin-bottom:22px">Everything in the library is tagged to the
        objectives it serves and the creative segments it reaches. Every number is a live filter, so
        click one to see what sits behind it.</p>
  ```
- **PROBLEM:** Three deck words in one heading block (objectives, segments, framework), and the
  prose explains the taxonomy before it tells the reader what to do with it.
- **BETTER:**
  ```
      <div class="sec-head"><div><span class="bar">Three aims, ten fields</span>
        <h2>The whole library on one grid</h2></div></div>
      <p class="prose" style="margin-bottom:22px">Every law here is tagged by what it's for and who
        it reaches. The numbers are live filters, so click one to see what's behind it.</p>
  ```

#### `tools/build.py` line 761 :: matrix row header
- **NOW:** `            <tr><th>Instruments per segment</th>{seg_totals}`
- **BETTER:** `            <tr><th>Laws per field</th>{seg_totals}`

#### `tools/build.py` line 759 :: matrix column header
- **NOW:** `          <thead><tr><th style="text-align:left">Objective &#8595; / Segment &#8594;</th>{head_cells}<th>All</th></tr></thead>`
- **BETTER:** `          <thead><tr><th style="text-align:left">Aim &#8595; / Field &#8594;</th>{head_cells}<th>All</th></tr></thead>`

#### `tools/build.py` line 788 :: closing card heading
- **NOW:** `      <h3 style="margin-top:14px">What is deliberately not here yet</h3>`
- **PROBLEM:** "Deliberately" is defensive, and the body paragraph already makes that point far
  better. Shorter and less braced is warmer.
- **BETTER:** `      <h3 style="margin-top:14px">What's not in here yet</h3>`
  (Keep `<span class="bar">Known gap</span>` and both body paragraphs exactly as they are — see
  KEEP AS IS.)

#### `tools/build.py` lines 493 and 594 :: instrument- and scenario-page section labels
- **NOW:** `  <span class="label">Creative segments this reaches</span>`  *(instrument page)*
- **NOW:** `  <span class="label">Creative segments</span>`  *(scenario page)*
- **PROBLEM:** "Creative segments" is market-research vocabulary. The chips underneath say "Music",
  "Film & TV", "Fashion & craft" — the reader can see what they are; the label just needs to be
  human.
- **BETTER:** `  <span class="label">Who this reaches</span>` and `  <span class="label">Who this is for</span>`

#### `tools/build.py` line 1083, in the search JS :: filter count
- **NOW:** `    count.textContent=shown+(shown===1?' instrument':' instruments');`
- **BETTER:** `    count.textContent=shown+(shown===1?' law or code':' laws and codes');`

#### `tools/build.py` lines 981–982, in `renderAnswer` :: answer card meta line
- **NOW:**
  ```
      '<p class="label" style="margin:22px 0 4px">Order of operations · '+
      (role?(shown+' of '+s.steps.length+' apply to you'):(s.steps.length+' instruments'))+'</p>'+
  ```
- **BETTER:**
  ```
      '<p class="label" style="margin:22px 0 4px">In this order · '+
      (role?(shown+' of '+s.steps.length+' apply to you'):(s.steps.length+' steps'))+'</p>'+
  ```
  (`N of M apply to you` is excellent — keep it.)

#### `tools/build.py` line 1036 :: search results heading
- **NOW:** `       '<span class="bar">'+(matched?'Also relevant':'Instruments')+'</span>'+`
- **BETTER:** `       '<span class="bar">'+(matched?'Also relevant':'Laws and codes')+'</span>'+`

#### `tools/build.py` line 330 :: staleness warning
- **NOW:** `            f"This consolidation is {age} years old. Any amendment made since {pretty} is "`
- **PROBLEM:** "Consolidation" is the correct term of art but it is meaningless to a reader who came
  here from Instagram, and it appears inside a red warning box where comprehension matters most.
- **BETTER:** `            f"This copy of the Act is {age} years old. Any amendment made since {pretty} is "`
  (Keep the `<strong>not</strong>` and the AGC link. The precise word "consolidated" survives in the
  next branch and in the disclaimer, which is where it belongs.)

#### `tools/registry.py` line 24 :: artistic freedom blurb
- **NOW:** `                "blurb": "The law that decides what may be made, shown, published, performed "` / `                         "or said; and what happens when the state says no."`
- **PROBLEM:** `; and` is a punctuation error — a semicolon cannot introduce a coordinated fragment.
  (The line is otherwise the best of the three blurbs.)
- **BETTER:** `                         "or said, and what happens when the state says no."`

#### `tools/registry.py` lines 34 and 37 :: two segment labels
- **NOW:** `    "digital":    "Digital entertainment / media",` → **BETTER:** `    "digital":    "Digital &amp; media",`
- **NOW:** `    "others":     "Others",` → **BETTER:** `    "others":     "Everything else",`
  ("Others" on a chip reads like a form field; "Everything else" reads like a person wrote it.)

---

### B. SCENARIO LEDES AND WATCH LINES (`tools/scenarios.py`)

**The set-level diagnosis first, because it matters more than any single line.** Nineteen ledes in a
row are built from the same two moulds: the aphoristic noun-stack ("Two gates, one tax, and…",
"Approval is the gate, a licence is the barrier to entry, and possession alone is an offence.",
"Ownership, registration and the two separate rights in every recording.") and the X-not-Y
antithesis ("Selling the object is not selling the copyright…"). Individually most of them are
good writing. Read as a set — which is exactly how they appear, as nineteen cards on one grid —
the uniformity is the tell. **The fix is not to flatten all nineteen; it is to break the pattern
where it costs the most, which is where the reader is frightened.** Rewrite four. Leave the rest.

Where the antithesis is *earned* — because the law genuinely is the distinction — keep it.
"Selling the object is not selling the copyright" is the whole point of s.26(2) and no other
sentence says it as fast. Where the antithesis is decoration, it goes.

**The 178 step `point` strings are the strongest writing in the whole project and should not be
touched.** They are specific, sectioned, and they tell the reader what actually happens to them.
Do not let a global voice pass near them.

#### `tools/scenarios.py` lines 806–807 :: `arrested` — lede  ← highest priority on the site
- **NOW:** `The basis is usually a licence condition or a by-law, not the speech offence everyone assumes it is.`
- **PROBLEM:** This is read by someone who has just been stopped, raided or arrested, possibly on a
  phone outside a venue. It opens with a categorisation exercise, in the third person, with an
  X-not-Y. There is no "you" in it and nothing to do.
- **BETTER:** `This is a frightening place to be, and it usually has more give in it than it feels like. Most of these turn on a licence condition or a council by-law rather than the speech offence everyone assumes, and that changes what you can do next.`
- **STRUCTURAL, same page:** this is the one page where the disclaimer's "talk to us" is too far
  down. In `scenario_page()` in `tools/build.py`, add a single line immediately after the role chips,
  for this scenario only:
  `<p class="label" style="margin-top:14px"><a class="ulink" href="../../../get-help/">Talk to someone at ALIM &rarr;</a></p>`
  Gate it on `sc["id"] == "arrested"` so it does not become site furniture.

#### `tools/scenarios.py` lines 763–764 :: `unpaid` — lede
- **NOW:** `Which forum you are in depends entirely on what you were: employee, freelancer, gig worker or seller.`
- **PROBLEM:** "Forum" is jargon, and the sentence opens on a legal category rather than on the
  reader's problem, which is that they are out of pocket. It also withholds the best news on the
  page — that several of these routes cost nothing.
- **BETTER:** `Being owed money is common, and it is fixable more often than people expect. Where you go to get it depends on what you were on that job: employee, freelancer, gig worker or seller. Some of those routes are free and don't need a lawyer.`

#### `tools/scenarios.py` lines 851–852 :: `someone-used-my-work` — lede
- **NOW:** `Infringement, passing off, or neither. Ownership is the first question and most claims die on it, not on the copying.`
- **PROBLEM:** Opens on a three-item legal taxonomy, then an X-not-Y, at a moment that is
  personally galling rather than academic. Also buries the reader's actual first action.
- **BETTER:** `Before anything else, check that you own it. Most of these come apart on ownership rather than on the copying, and s.26(2) of the Copyright Act is usually why. Once that's settled, the question is whether this is infringement, passing off, or neither.`

#### `tools/scenarios.py` lines 249–250 :: `busking` — lede
- **NOW:** `Almost none of the rules that decide this are federal, and none of the ones that matter are on the government's legislation portal.`
- **PROBLEM:** Two parallel negatives ("Almost none… and none…"), and it tells the reader what the
  library *lacks* before telling them anything they can use. True, honest, and badly ordered.
- **BETTER:** `The rule that decides whether you can play is almost always your own council's by-law, and nobody publishes those in one place. Below is the federal layer, and where to go for the council layer.`

#### `tools/scenarios.py` line 361 :: `documentary` — lede (low priority)
- **NOW:** `Approval is the gate, a licence is the barrier to entry, and possession alone is an offence.`
- **PROBLEM:** Only the middle clause is off — "barrier to entry" is business-school vocabulary in a
  sentence that is otherwise pure law. The rule of three here is earned; three distinct offences
  are three distinct facts.
- **BETTER:** `Approval is the gate, a FINAS licence is the price of admission, and possession alone is an offence.`

**All other ledes and all nineteen `watch` strings: KEEP.** The watch lines are the best-tuned copy
in the library — "The one people miss" is a perfect label for them, and lines like "Budget the
withholding into the fee from the first email" and "Send nothing before you have settled ownership"
are exactly the register the client asked for.

---

### C. THE REST OF THE SITE

#### `enhanced/get-help/index.html` line 83 :: page lede  ← second-highest priority
- **NOW:** `    <p class="page-lede">Confidential, free legal advice for Malaysia's artists and cultural workers.</p>`
- **PROBLEM:** Accurate, and completely inert. This is the first screen of the page the brief
  identifies as a fear point, and it is a service description rather than a welcome. It also fails
  to answer the fear that actually stops people writing in, which is not cost — it is "I don't know
  how to describe what happened."
- **BETTER:** `    <p class="page-lede">Free, confidential legal help for Malaysia's artists and cultural workers. You don't need to know the legal words for it; just tell us what happened.</p>`

#### `enhanced/faq/index.html` lines 103–106 :: registration question
- **NOW (question):** `        <summary><span class="q-idx">03</span> Is ALIM a registered organization? <span class="q-sign">+</span></summary>`
- **NOW (answer):** `        <div class="a">ALIM is a grassroots initiative run by its co-founders and a volunteer network.</div>`
- **PROBLEM:** The answer does not answer the question. A reader asking this is asking one thing —
  "are you real and are you accountable" — and a sidestep reads as evasion, which is the worst
  possible note for a legal NGO. Also "organization" is the only US spelling in the site's prose.
- **BETTER (question):** `        <summary><span class="q-idx">03</span> Is ALIM a registered organisation? <span class="q-sign">+</span></summary>`
- **BETTER (answer):** `        <div class="a">Not yet. ALIM runs as a grassroots initiative led by its co-founders and a volunteer network of counsel. We intend to incorporate as a company limited by guarantee; that has not happened yet, and no page on this site should be read as saying it has.</div>`

#### `tools/registry.py` line 464 :: `act-777` why string
- **NOW:** `ALIM itself is being incorporated as a CLBG under this Act.`
- **PROBLEM:** The present continuous states that an incorporation is in progress. Per the brief,
  the CLBG is not registered and nothing may say or imply otherwise; "is being incorporated" implies
  filings are live.
- **BETTER:** `It is the form ALIM has chosen for itself, and we have not completed it either.`
  (If the self-deprecation is too much for a legislation page, use the plain version:
  `It is the form ALIM intends to take.`)

#### `enhanced/how-we-can-help/index.html` line 152 :: closing headline
- **NOW:** `    <h2 class="display" style="font-size:clamp(30px,5vw,58px);margin:18px 0 0">Every creative journey deserves legal clarity.</h2>`
- **PROBLEM:** Textbook machine cadence: abstract noun + "deserves" + abstract noun, with "journey"
  doing no work at all. It could be the closing line of any professional services site on earth.
- **BETTER:** `    <h2 class="display" style="font-size:clamp(30px,5vw,58px);margin:18px 0 0">You shouldn't have to guess what you signed.</h2>`

#### `enhanced/our-work/index.html` line 189 :: closing headline
- **NOW:** `    <h2 class="display" style="font-size:clamp(30px,5vw,58px);margin:18px 0 0">Join us in building a fairer creative ecosystem.</h2>`
- **PROBLEM:** "Ecosystem" is a deck word and it appears three times across the site. Nothing in the
  sentence is specific to ALIM.
- **BETTER:** `    <h2 class="display" style="font-size:clamp(30px,5vw,58px);margin:18px 0 0">Come and build this with us.</h2>`

#### `enhanced/join-us/index.html` line 83 :: page lede
- **NOW:** `    <p class="page-lede">Help build a fairer creative ecosystem in Malaysia. Donate, volunteer, or spread the word.</p>`
- **BETTER:** `    <p class="page-lede">Help make legal help normal for Malaysian artists. Donate, volunteer, or tell someone who needs us.</p>`

#### `enhanced/join-us/index.html` line 121 :: section bar
- **NOW:** `      <div><span class="bar">For organizations</span><h2>Partner With Us</h2></div>`
- **PROBLEM:** US spelling, in a document that writes "organisations" on the neighbouring page.
- **BETTER:** `      <div><span class="bar">For organisations</span><h2>Partner with us</h2></div>`

#### `enhanced/our-work/index.html` line 103 :: Instagram card
- **NOW:** `        <p>Follow our journey on @artxlawmas.</p>`
- **PROBLEM:** "Journey" is the tell; the sentence also says "follow" twice with the card's own
  heading.
- **BETTER:** `        <p>Panels, sessions, and what we're working on.</p>`

#### `enhanced/about-alim/index.html` line 230 :: FAQ 03
- **NOW:** `        <div class="a"><p>Volunteer your time or expertise, partner with us as an organisation, donate once our donation channel opens, or simply spread the word to artists who need us.</p></div>`
- **PROBLEM:** "Simply" is a hollow intensifier and it makes the last option sound like the small
  one, which is backwards — word of mouth is how most of these clinics actually get found.
- **BETTER:** `        <div class="a"><p>Volunteer your time or expertise, partner with us as an organisation, donate once our donation channel opens, or tell the artists who need us that we exist.</p></div>`

#### `enhanced/mission/index.html` line 83 :: page lede
- **NOW:** `    <p class="page-lede">The principles that guide everything we do at ALIM.</p>`
- **PROBLEM:** Generic filler; true of every organisation that has ever had a values page.
- **BETTER:** `    <p class="page-lede">Six commitments we wrote down so we can be held to them.</p>`

#### `enhanced/mission/index.html` line 96 :: pillar 02 description
- **NOW:** `<p>Build mutual literacy between the creative and legal worlds so each speaks the other's language.</p>`
- **PROBLEM:** "Mutual literacy" is the jargon; the rest of the sentence is good.
- **BETTER:** `<p>Help each side learn the other's language, so artists stop being talked past and lawyers stop guessing.</p>`
- *(Keep the six pillar names — Empower, Foster Understanding, Encourage Harmony, Promote
  Appreciation, Preserve, Disrupt with Intent. They are charter language, not marketing copy, and
  editing them is a governance decision rather than a copy one.)*

#### `enhanced/get-help/index.html` line 106 :: section bar
- **NOW:** `      <div><span class="bar">Our expertise</span><h2>What We Can Help With</h2></div>`
- **PROBLEM:** "Our expertise" is a small brag on a page whose whole job is to lower the barrier,
  and the rest of the site never boasts.
- **BETTER:** `      <div><span class="bar">What we see most</span><h2>What we can help with</h2></div>`

#### `enhanced/request-consultation/index.html` line 82 :: page lede
- **NOW:** `    <p class="page-lede">Fill in the details below and submit. All consultations are free and confidential; we respond within 48 hours.</p>`
- **PROBLEM:** "Fill in the details below and submit" is form-instruction language on a page whose
  form is visible anyway; it wastes the only warm sentence available above the fold.
- **BETTER:** `    <p class="page-lede">Tell us what's going on. It's free, it's confidential, and we reply within 48 hours.</p>`

#### `enhanced/resources/understanding-contracts/index.html` (line 198) :: guide lede
- **NOW:** `    <p class="page-lede">A comprehensive, interactive guide for Malaysia's artists and creatives. Learn to read a contract, negotiate the terms that matter, and protect yourself under Malaysian law.</p>`
- **PROBLEM:** "Comprehensive" is a hollow intensifier and an implicit overclaim; "artists and
  creatives" says the same thing twice; "Learn to X, Y and Z" is the rule of three used as filler.
- **BETTER:** `    <p class="page-lede">How to read a contract before you sign it, and what Malaysian law gives you when one goes wrong. Written for artists, not for lawyers.</p>`

#### `enhanced/resources/performing-artist-rights/index.html` (line 187) :: guide lede
- **NOW:** `    <p class="page-lede">Your comprehensive guide to performing in Malaysia. Venue contracts, fair pay, legal protections, and what to do when things go wrong.</p>`
- **BETTER:** `    <p class="page-lede">Venue contracts, getting paid what you agreed, and what to do when a gig goes wrong. For anyone who performs in Malaysia, at any level.</p>`

#### `enhanced/resources/copyright-basics/index.html` line 249 :: guide lede
- **NOW:** `    <p class="page-lede">Everything Malaysian creatives need to know about protecting their work under the Copyright Act 1987. Interactive guide · 7 sections · ~15 min read.</p>`
- **PROBLEM:** "Everything … need to know" is an overclaim a law NGO cannot support, and the
  sentence describes the document rather than the reader's problem.
- **BETTER:** `    <p class="page-lede">What you own the moment you make something, how long you own it, and what to do when someone takes it. Seven sections, about fifteen minutes.</p>`

#### `enhanced/resources/performing-artist-rights/index.html` line 424 :: section bar
- **NOW:** `<span class="bar">Two sides of the coin</span>` (above `<h2>Rights vs responsibilities</h2>`)
- **PROBLEM:** Dead cliché, and the h2 beside it already carries the idea.
- **BETTER:** `<span class="bar">Both directions</span>`

#### `enhanced/resources/freelancer-protections/index.html` lines 370–371 :: closing heading
- **NOW:** `<span class="bar">Need a person?</span>` + `<h2 ...>Need personalised help?</h2>`
- **PROBLEM:** The bar is excellent and the h2 undoes it — "personalised" is the machine word, and
  the two lines ask the same question twice. The other two guides already close with the right line.
- **BETTER:** keep the bar, and change the h2 to match the house: `A guide can only take you so far.`

#### `enhanced/terms-of-service/index.html` line 92 :: clause 2
- **NOW:** `        <li><strong>No attorney-client relationship.</strong> Using this site or attending a consultation does not, by itself, create a solicitor-client relationship.</li>`
- **PROBLEM:** The heading says "attorney-client" (US) and the sentence beneath it says
  "solicitor-client" (Malaysian). On a legal page, a jurisdiction mismatch in consecutive clauses is
  a credibility defect, not a style one.
- **BETTER:** `        <li><strong>No solicitor-client relationship.</strong> Using this site or attending a consultation does not, by itself, create a solicitor-client relationship.</li>`

#### `tools/build.py` lines 1062–1064, no-result state :: empty search
- **NOW:** `      'Nothing in the library matches <strong>'+esc(raw)+'</strong>. This library is federal legislation plus the codes and treaties around '+ 'it; state entertainment enactments and council by-laws are the known gap. Try one of these, '+ 'or tell us what happened.'`
- **PROBLEM:** The middle sentence explains ALIM's scoping methodology at the precise moment the
  reader has failed to find help. The first and last sentences are right; the middle needs to be
  about them, not about us.
- **BETTER:** `      'Nothing in the library matches <strong>'+esc(raw)+'</strong>. It might be a state enactment or a council by-law; those are the big gap here, and nobody publishes them in one place. Try one of these, or just tell us what happened.'`
  (Keep `Ask ALIM directly →` exactly as it is.)

#### `tools/build.py` lines 778–779 :: filter empty state
- **NOW:** `      <p id="empty" hidden class="prose" style="text-align:center;padding:60px 0">Nothing matches` / `        those filters. Clear them and start again.</p>`
- **PROBLEM:** "Start again" tells the reader they wasted their effort. Minor, but it is an
  empty state, which the brief flags.
- **BETTER:** `      <p id="empty" hidden class="prose" style="text-align:center;padding:60px 0">Nothing matches` / `        those filters. Try clearing one of them.</p>`

---

## KEEP AS IS

Copy that is already better than anything I would write. None of this should be touched by a
global voice pass.

- **`enhanced/index.html`, hero:** `ALIM gives Malaysia's artists, musicians, designers, writers and filmmakers the confidential legal cover they're routinely denied. Free advice. Policy advocacy. Education. No retainer. No PR.`
  "No retainer. No PR." is the best four words on the site.
- **`enhanced/index.html`, marginalia:** `Run by volunteer counsel who believe the right to make is worth defending, first in private, then, if pressed, in public.`
- **`enhanced/index.html`, impact story:** `This is most of what we do: pressure resolved before it ever becomes a case.`
- **`enhanced/resources/index.html`:** `Know your rights.` / `Free, plain-language legal knowledge for Malaysia's creative communities. Read a guide, use a tool, or reach out when you need a person.` This is the house voice in one lede; treat it as the reference sample.
- **`enhanced/resources/index.html`:** `A guide can only take you so far.` and `Need specific help?`
- **`enhanced/get-help/index.html`:** `Tell us what's going on and we'll match you with the right volunteer counsel.` and `No. We help remotely across Malaysia, wherever you're based.`
- **`enhanced/how-we-can-help/index.html`:** `Our support is advisory. The decisions, always, are yours.` and `Know what you are signing away before you sign, and what to keep.` and `Representation agreements reviewed for the traps artists rarely see coming.`
- **`enhanced/resources/gig-workers-act-2025/index.html`:** the whole lede, plus `Real teeth: RM50,000 fine + 2 years jail`, `When the portal will not help`, `Before you start, gather:`. This page is the best-written thing on the site.
- **`tools/build.py`, instrument page:** `<span class="bar">Why it matters</span><h2>What this does to artists</h2>` — the single best heading pair in the library.
- **`tools/build.py`, instrument page:** `<span class="bar">In practice</span><h2>Where this one bites</h2>`
- **`tools/build.py`, index:** the search placeholder `What are you doing? Try "DJing", "busking", "client won't pay", "Act 332"`, the tab `What are you doing?`, and `{N} things people come to us about`. These three already do what the client is asking for.
- **`tools/build.py`, index:** the entire `How this library is kept honest` card, both paragraphs. Do not touch a word. The same goes for the two body paragraphs under the gap card.
- **`tools/build.py`, disclaimer:** `This is a reference library, not legal advice.` … `If you have a live problem, talk to us.` The closing clause is the warmth template for the whole library.
- **`tools/scenarios.py`:** all nineteen `watch` strings, and the stamp that labels them,
  `The one people miss`. Also `Send nothing before you have settled ownership.` and
  `Budget the withholding into the fee from the first email.`
- **`tools/scenarios.py`:** all 178 step `point` strings. They are specific, sectioned and
  reader-facing, and they are the reason the library is worth publishing at all.
- **`tools/registry.py`:** the `why` strings throughout, especially `act-332`, `act-378`
  (`can be shut out of court at the worst possible moment`), `act-452` (`who otherwise reach fifty
  with no retirement asset but a catalogue`), `act-789` (`the difference between a broken wrist
  being an inconvenience and being the end of a career`), and `state-entertainment` (`This is the
  single largest gap in any Malaysian legal resource for the arts, including this one.`).
- **`enhanced/mission/index.html`:** `These pillars only stand because people like you hold them up.`
- **`enhanced/privacy/index.html`** and **`terms-of-service/index.html`** generally. Plain,
  short, unpadded, correctly hedged. Only the attorney/solicitor mismatch needs fixing.

---

## GLOSSARY RULINGS

| Term | Ruling | Replacement |
|---|---|---|
| **instrument** | **Split.** Keep as a term of art where the law itself uses it — the Stamp Act entries depend on it (`An assignment of copyright is an instrument`), and changing those would make them wrong. **Replace everywhere it is used as a category noun in navigation, counts and stat labels**, where the reader is a musician for whom an instrument is a guitar. | Stat: `laws & codes`. Filter count: `laws and codes`. Tab: `The full list`. Scenario counts: `steps` (the page numbers them 01…N, so this is also more accurate). Search heading: `Laws and codes`. "Laws" alone is wrong for the 65 — the set includes an industry code, guidelines, treaties and collecting societies — which is why "laws and codes" is the honest plural. |
| **provision of legal resources** | **Replace outright.** Grant-application language, and it is literally the first phrase on the library's first screen. | `Know your rights` (the site's own existing line). |
| **order of operations** | **Replace.** Engineering vocabulary, and redundant next to the h2 that already says it in English. | Section bar: `The chain`. Answer card: `In this order`. |
| **creative segment** | **Keep the taxonomy, replace the label.** The tagging is genuinely useful; "segment" is market research and the reader never needs the word. | Instrument page: `Who this reaches`. Scenario page: `Who this is for`. Matrix header: `Field`. Framework bar: `ten fields`. |
| **objective** | **Keep internally, replace in reader-facing copy.** These are ALIM's three constitutional aims, so the *labels* (Socio-economic rights / Intellectual property rights / Artistic freedom) stay; the *word* "objectives" in furniture goes. | Matrix header: `Aim`. Framework bar: `Three aims`. In the Resources card, cut the taxonomy sentence entirely rather than translating it. |
| **situation** | **Keep, and promote it.** It is the warmest and clearest word in the library, it is already used in `Related situations` and `{N} things people come to us about`, and it is what the client's own brief calls these things. Make it the standard term. | No change. Use it where "scenario" currently appears. |
| **scenario** | **Keep as the internal identifier** (`SCENARIOS`, `doing/<id>/`, `data-view`) — no reader sees those. **Replace at every reader-facing point**, because it reads as a training exercise and because the site already says "situations" elsewhere. This is a consistency fix, not churn. | `Situation` (dossier bar), `Situation` (card `idx` badge on instrument pages and related cards). |

---

## EM DASHES AND OTHER MECHANICAL DEFECTS

### Em dashes — clean sheet in scope

Zero em dashes in any copy string across `enhanced/index.html`, `about-alim/`, `get-help/`,
`our-work/`, `resources/` and all five guide pages, `join-us/`, `faq/`, `mission/`, `privacy/`,
`terms-of-service/`, `request-consultation/`, `sitemap/`, and all of `tools/build.py`,
`tools/scenarios.py`, `tools/registry.py`.

Excluded, correctly, as quoted source:
- `legislation/act-574/index.html` — `54—55. (Deleted by L.N. (N.S.) 1 of 1957)`, harvested from the
  AGC arrangement of sections. Must stay. Same string in `legislation/data/sections.json` and
  `library.json`.

Not copy, no action:
- `tools/scenarios.py:10` — an em dash inside a Python docstring comment. Never rendered.

Outside the brief's page list but flagged for completeness, because these files sit in `enhanced/`
and would fail the rule if they go live:
- `enhanced/lawyers/index.html` — em dashes at lines 6, 102, 156, 197, 199, 253, 280
  (`Counsel Roster — ALIM`, `Senior — willing to mentor`, `Junior — seeking mentorship`, etc.).
- `enhanced/mockup-v3.html` — throughout the ticker and section comments. Mockup only.
- `enhanced/letters/balai-kp.md` — an internal draft, heavy em dash use, and it separately claims
  `Since 2024 … over 120 legal queries … 37 counsel`, which contradicts the live site's
  `Pro bono since 2025`. Reconcile before that letter goes anywhere.

En dashes in date and time ranges (`12–14 June 2026`, `4–6PM`, `October 17–18, 2025`) are correct
typography and are **not** em dashes. Leave them.

### Other mechanical defects

1. **Factual error.** `enhanced/resources/index.html:90` says `18 situations`. The build reports
   19 (`19 scenario pages`). Fixed in the rewrite above.
2. **US spellings in British copy.** `enhanced/join-us/index.html:121` `For organizations`;
   `enhanced/faq/index.html:104` `Is ALIM a registered organization?`. The rest of the site writes
   `organisations`, `recognise`, `favouring`. Both fixed above.
3. **Jurisdiction mismatch.** `enhanced/terms-of-service/index.html`, clause 2:
   `No attorney-client relationship` heading over a `solicitor-client relationship` body. Fixed
   above.
4. **Punctuation.** `tools/registry.py`, `freedom` blurb: `…performed or said; and what happens…`
   — a semicolon cannot introduce a coordinated fragment. Use a comma.
5. **Heading case inconsistency.** The house is sentence case (`How we help`, `Community in
   action`, `The numbers speak`, `Media coverage`, `Useful links`, `How the advice works`). Three
   pages break it into Title Case, and they are the three warmest-intent pages on the site, which
   is exactly where corporate capitalisation does the most damage:
   - `get-help/`: `How It Works`, `What We Can Help With`, `Get In Touch`, and the card headings
     `Reach Out`, `We Connect You`, `Get Support`, `Request a Consultation`, `Email Us`,
     `Instagram DM`, `Frequently Asked Questions`.
   - `about-alim/`: `Our Mission`, `What We Stand For`, `Founding Members`,
     `Partners & Collaborators`, `Frequently Asked`. (Note `Get in Touch` here is sentence case
     while `get-help/` has `Get In Touch` — the same phrase, capitalised two ways, two clicks apart.)
   - `join-us/`: `Ways to Support`, `Partner With Us`, `Making a Difference`, `Spread the Word`.
   Recommend a single pass to sentence case across those three pages. Proper nouns and `FAQ` stay.
6. **Duplicated metaphor.** `enhanced/index.html` — `the movement only stands because people hold
   it up` and `enhanced/mission/index.html` — `These pillars only stand because people like you
   hold them up.` The mission version is better (it has a "you" in it). Recommend cutting the home
   page's trailing clause to `Art should not exist in a legal vacuum. Every creative deserves to
   know their rights.` and letting the mission page own the image.
7. **`ecosystem` x3** (`our-work/` h2, `join-us/` lede, `join-us/` meta description). Two fixed
   above; update the `join-us/` `<meta name="description">` to match its new lede.
8. **Overclaim risk, not copy craft.** The home and Our Work stat rows assert `500+ Creatives
   reached`, `20+ Events & workshops`, `30+ Partner orgs`. The About page lists five partner
   organisations. `30+` is not supportable from anything published on the site and is the kind of
   number a journalist or funder will ask about. Either hold a source for it or soften to
   `Growing` (which `join-us/` already does for its network stat, and which reads fine).
9. **Registration status.** Two strings currently state or imply a status ALIM does not have, both
   rewritten above: the `act-777` `why` string (`ALIM itself is being incorporated as a CLBG`) and
   FAQ 03's non-answer. No other page on the site makes a registration claim — `A non-profit legal
   clinic` and `Independent. Non-profit.` describe how ALIM operates, not a registered status, and
   are safe. The `enhanced/letters/balai-kp.md` draft contains
   `[ALIM letterhead — once CLBG registration complete…]`, which is correctly guarded but should
   not be published as-is.
