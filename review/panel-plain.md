# ALIM.my — plain-language & access review

Reviewed: `enhanced/` (live source), and the generated legislation library via its sources
`tools/build.py`, `tools/scenarios.py`, `tools/registry.py`. Library rebuilt with
`python3 tools/build.py` (65 instrument pages + 19 scenario pages + index) and read as rendered.
Skipped as undeployed: `enhanced/cases/`, `lawyers/`, `register/`, `structure/`, `mockup-v3.html`.

Companion seat: `review/panel-copy.md` (voice & craft). This report does not repeat it. Where a
fix it already proposes also solves an access problem, I say so and move on.

---

## VERDICT

**The writing is good; the library's reading level is not, and its colour badges fail contrast in
both themes.** This site currently serves the gallery administrator and fails the batik maker. The
marketing pages and the five guides are written at a genuinely accessible level; the legislation
library is written at a different one, and nothing warns the reader when they cross between them.

The three changes that would most increase how many people this helps:

1. **Cut the step `point` paragraphs to one idea per sentence.** 56 authored sentences run 28 words
   or longer, and they sit in `lg-step p` at 14.5px — the exact place a frightened person reads on a
   phone. The single worst is 46 words. This is the biggest barrier on the site, bigger than jargon.
2. **Fix the objective badges.** White text on riso green renders at **2.56:1** in light mode and
   **2.59:1** in dark. That is a WCAG AA failure at any size, on the library's primary colour-coding
   device, which also **relies on colour alone** to carry the three objectives.
3. **Link the library to the guides.** The plain-English definitions this library needs already
   exist on this site: `A license lets the client use it; an assignment transfers ownership
   forever` is sitting in `understanding-contracts/` while `release-track` uses `assignment` cold.
   Measured: **the library contains zero links to any guide, and two of the guides contain zero
   links to the library.** Cross-linking them is one field on `SCENARIOS` and it fixes more jargon
   than any rewrite would.

Close behind, and cheaper than all three: **surface the Bahasa Malaysia Act titles properly.** The
library already holds them for 57 of 65 entries and already searches them, but renders them as
11px uppercase letter-spaced monospace on Act pages only. One CSS class and two template lines puts
`Akta Hak Cipta 1987` in readable serif on every card and search result.

---

## THE FIVE READERS

**The 24-year-old DJ in KL, phone, 2am, night shut down.** He gets further than I expected. If he
lands on the library and types "shut down" or taps the `Stopped, raided, shut down or arrested`
card, the page opens with a lede that speaks to him, and **`Talk to someone at ALIM →` sits right
under the role chips** (`build.py` `help_line`, gated to this scenario). That is the single best
access decision in the whole build; protect it. Where he falls off: the chain that follows is
**eleven steps** of Acts, and step 06 tells him `Seditious tendency, with intention expressly
irrelevant.` with nothing after it. At 2am that reads as "it doesn't matter what I meant, I'm
finished." He also arrives via the **home page**, which opens on `The ALIM Dossier · § 01 ·
Manifesto · Filed from Kuala Lumpur` — editorial furniture, not a door. On a 390px screen he scrolls
through a ticker, a nav and a masthead before anything tells him where to go.

**The batik maker in Kelantan, Malay first, slow English.** She does not get what she needs. The
site is English-only prose; `Fashion & craft` is a chip she must read in English to find. The
library **does** hold the Bahasa Malaysia Act titles and **does** print them — but as
`AKTA HAKCIPTA 1987` in 11px uppercase letter-spaced monospace in `--ink-3`, which is the least
legible typographic treatment on the entire site, applied to the one string that would let her
recognise where she is. They appear on Act pages only, never on a card, a search result or a step.
She also meets 28-to-46-word sentences with three subordinate clauses. She falls off on the first
one.

**The documentary maker who has had a lawyer's letter and is frightened.** He finds the right page
fast; `Shoot and screen a film or documentary` is one of nineteen cards and the title is literal.
Then the site does him active harm. The lede and the watch line tell him `possession alone is an
offence` and `A finished unapproved cut sitting on your drive is already inside the offence.` There
is no sentence anywhere near it telling him what not to do. **The obvious action for a frightened
person reading that at night is to delete the footage**, which destroys his film and, if a letter
has already arrived, may be far worse than the offence he is afraid of. See MISLEADING.

**The illustrator not paid for three months who does not know the word "forum".** He is served
better than any other reader here, and the `unpaid` lede is the best access writing on the site:
`Being owed money is common, and it is fixable more often than people expect.` He falls off at the
`watch` line, which is the one he most needs: `Sending a civil letter of demand when you had a free
statutory forum wastes the cheapest route you had.` He does not know what a forum is, does not know
what statutory means, and `letter of demand` is not defined anywhere. He is told he has wasted
something without being told what he had.

**The gallery administrator who needs the right answer for a collector today.** She is the reader
this site currently serves best, and she is the only one who can use the framework matrix. She gets
`Selling the object is not selling the copyright, and the commission clause decides who owned it in
the first place` and `Section 26(2) is the clause that quietly transfers ownership of commissioned
work` — precise, fast, citable. Her friction is mechanical, not linguistic: on a phone the 12-column
matrix is a silent horizontal scroll she will never discover, and when she filters by role the steps
she filtered out drop to **1.88:1 contrast** and become unreadable even though she may need them.

---

## SENTENCES TO SIMPLIFY

56 authored sentences run 28 words or longer. These are the ones that sit where fear or money is.

### `tools/scenarios.py` :: `arrested` step06 (act-15)
- **NOW:** `Seditious tendency, with intention expressly irrelevant.`
- **PROBLEM:** Not too long; too short and too cold. Four words of statute with no subject, no verb
  the reader owns, and a phrase (`intention expressly irrelevant`) that a frightened person reads as
  "nothing I say can help me." It is the single most alarming string on the site.
- **BETTER:** `Under this Act what you meant does not form part of the offence, so arguing that you never intended anything is not the defence people expect. That makes the exact words used, and what was actually said or shown, the ground you fight on. Do not try to work this one out alone.`

### `tools/scenarios.py` :: `documentary`.watch
- **NOW:** `Section 6 of the Film Censorship Act catches possession. A finished unapproved cut sitting on your drive is already inside the offence.`
- **PROBLEM:** Accurate, and the obvious next action it invites is destroying the material. Nothing
  tells the reader not to.
- **BETTER:** `Section 6 of the Film Censorship Act catches possession, so a finished unapproved cut sitting on your drive is already inside the offence. Do not delete it and do not hand it over. Destroying material once a complaint or a letter has arrived makes things worse, not better. Talk to someone first.`

### `tools/scenarios.py` :: `stage-show` step07 (act-872) — 45 words
- **NOW:** `That means a written service agreement setting out the service, the rate and the payment method, payment within seven days where the agreement says nothing, no termination without just cause or excuse, conciliation before the Director General for Industrial Relations, and the Gig Workers Tribunal.`
- **PROBLEM:** One sentence, six separate rights, two institutions and a term of art
  (`conciliation`) nobody has defined. Nothing is retained at 14.5px on a phone.
- **BETTER:** `That gives your cast and crew five things. A written agreement saying what the work is, what it pays and how. Payment within seven days if the agreement does not say. No termination without a proper reason. A free meeting run by the Director General for Industrial Relations to try to settle it. And if that fails, the Gig Workers Tribunal.`

### `tools/scenarios.py` :: `unpaid` step02 (act-872) — 44 words
- **NOW:** `It reaches you two ways: any service you provide through a platform, or, even with no platform involved, any service listed in the Schedule; acting, film production crew, singing, musicianship, composing, lyric writing, make-up, hair, styling, photography and videography are all listed by name.`
- **PROBLEM:** The eleven-item list is the good news and it is buried behind a colon, a semicolon and
  a double negative construction (`even with no platform involved`).
- **BETTER:** `You are covered two ways. Either you took the work through a platform, or your kind of work is named in the Schedule, with no platform needed at all. The Schedule names acting, film crew, singing, playing, composing, lyric writing, make-up, hair, styling, photography and videography.`

### `tools/scenarios.py` :: `unpaid`.watch
- **NOW:** `Work out which of the four you were before you write the first letter. Sending a civil letter of demand when you had a free statutory forum wastes the cheapest route you had.`
- **PROBLEM:** Three undefined terms in one clause (`civil`, `letter of demand`, `statutory forum`)
  on the page whose whole promise is that some routes are free. Tells the reader he lost something
  without telling him what.
- **BETTER:** `Work out which of the four you were before you send anything. Some of these give you a free government body that will hear the complaint for you. If you go straight to a lawyer's demand letter instead, you have paid for the expensive route when a free one was open.`

### `tools/scenarios.py` :: `run-organisation` step06 (act-265) — 46 words, the longest on the site
- **NOW:** `Since 1 January 2023 the First Schedule covers any person who has entered into a contract of service, whatever they earn; above RM4,000 a month only a short list drops away, being the overtime rate, rest day and public holiday pay, shift allowance and termination benefits.`
- **PROBLEM:** 46 words, a semicolon splice, `contract of service` undefined, and the crucial
  RM4,000 threshold is stated as a subtraction from a list the reader has not been shown.
- **BETTER:** `Since 1 January 2023 the Employment Act covers anyone employed under a contract of service, whatever they are paid. If they earn more than RM4,000 a month, most of it still applies. Only five things drop away: the overtime rate, rest day pay, public holiday pay, shift allowance and termination benefits.`

### `tools/scenarios.py` :: `management-deal`.lede — money case, highest risk
- **NOW:** `What you assign you do not get back, and the clause that looks like a life sentence is often void anyway.`
- **PROBLEM:** `often void anyway` is an invitation to ignore a signed clause. See MISLEADING.
- **BETTER:** `What you assign you do not get back. And the clause that looks like a life sentence is often weaker than it reads, though that is a fight to have with advice, not a reason to walk away on your own.`

### `tools/scenarios.py` :: `brand-deal` step09 (act-872) — 42 words
- **NOW:** `If you are shooting stills or video, Schedule item 9 of the Gig Workers Act 2025 lists photographers and videographers, so the brand itself is a contracting entity and the protections apply directly; you do not need a platform in the chain.`
- **BETTER:** `If you are shooting stills or video, the Gig Workers Act 2025 names photographers and videographers in its Schedule. That makes the brand the one on the hook, so the protections apply to you directly. No agency or platform needs to be involved.`

### `tools/scenarios.py` :: `dj-club-night` step11 (act-514) — 43 words
- **NOW:** `Since 1 June 2024 the 2022 amendments can put the duty on you as principal, so long as you are directing how the work is done; leaving the method entirely to the crew's own employer is what takes you outside that particular duty.`
- **PROBLEM:** `as principal` is undefined here and at seven other places, and the second clause is a
  double negative dressed as a positive.
- **BETTER:** `Since 1 June 2024 the safety duty can land on you, the person running the night, and not only on the crew's own employer. It lands on you if you are telling them how to do the work. If you leave the method entirely to their employer, that particular duty is not yours.`

### `tools/scenarios.py` :: `merch-online` step03 (act-552) — 39 words
- **NOW:** `Novelty is destroyed by disclosure anywhere in the world before you file, and there is no grace period for showing your own work; the only six-month exception is for an official exhibition or a disclosure someone else made unlawfully.`
- **PROBLEM:** `Novelty is destroyed by disclosure` is the passive abstract voice at the exact moment
  the reader needs a rule of conduct.
- **BETTER:** `File before you show it to anyone, anywhere. Once the design has been shown in public, even by you, it is no longer new and you cannot register it. There are only two exceptions, both six months: an official exhibition, or someone else leaking it without permission.`

### `tools/registry.py` :: `REGISTRY[15].why` (Penal Code) — 44 words
- **NOW:** `The general criminal law, and the home of the provisions most often turned on artists: obscenity (ss.292 to 294, which reach obscene objects, books, drawings and songs or recitations in public), wounding religious feelings (s.298 and s.298A), and statements conducing to public mischief (s.505).`
- **PROBLEM:** A nested parenthesis inside a colon-list, and `statements conducing to public
  mischief` is a statutory phrase reproduced with no translation.
- **BETTER:** `The general criminal law. Three parts of it are the ones most often turned on artists. Obscenity, ss.292 to 294, which reach obscene objects, books, drawings, and songs or recitations performed in public. Wounding religious feelings, s.298 and s.298A. And s.505, spreading statements likely to cause public alarm or set groups against each other.`

### `tools/registry.py` :: `REGISTRY[8].why` (CMA) — 40 words
- **NOW:** `Section 233 (improper use of network facilities: offensive, indecent, obscene or menacing content, and content sent with intent to annoy) is the provision most often used against artists, critics and commentators, and it was amended with heavier penalties in 2024.`
- **BETTER:** `Section 233 is the provision most often used against artists, critics and commentators, and the penalties got heavier in 2024. It covers content that is offensive, indecent, obscene or menacing, and content sent with intent to annoy. It is written broadly enough to reach an ordinary post.`

### `tools/build.py` :: the library disclaimer, paragraph 2
- **NOW:** `Subsidiary legislation, state enactments and local authority by-laws may also apply to your situation and are largely outside this library.`
- **PROBLEM:** `Subsidiary legislation` appears here and nowhere else, undefined, in the one
  paragraph every reader is meant to take seriously.
- **BETTER:** `Rules made under an Act, state laws and council by-laws may also apply to you, and most of those are outside this library.`

### `tools/scenarios.py` :: `exhibit-sell-art` step08 (act-53)
- **NOW:** `Whether your sales are taxable business income turns on the badges of trade, not on whether you call yourself a business.`
- **PROBLEM:** `badges of trade` is a term of art with no plain equivalent, used three more times,
  never once explained. The sentence tells the reader the test exists and withholds it.
- **BETTER:** `Whether your sales are taxable business income does not depend on what you call yourself. LHDN looks at how you actually operate: how often you sell, whether you buy to resell, how you market, and how long you hold work before selling it. Lawyers call these the badges of trade.`

### `enhanced/resources/understanding-contracts/index.html` :: WhatsApp clause — money case
- **NOW:** `Under the Electronic Commerce Act 2006 and the Contracts Act 1950, electronic communications (including WhatsApp messages) can form a valid contract if the essential elements are present: offer, acceptance, consideration, and intention to create legal relations.`
- **PROBLEM:** 36 words, and the most useful fact for this audience (your WhatsApp thread may
  already be a contract) is buried in the middle behind two Act citations, then followed by four
  untranslated doctrinal terms.
- **BETTER:** `Your WhatsApp messages can be a contract. Under the Electronic Commerce Act 2006 and the Contracts Act 1950, a deal done over chat or email counts, so long as the basics are there: one side offered, the other accepted, something of value was promised both ways, and you both meant it to be binding.`

### `enhanced/resources/understanding-contracts/index.html` :: unconscionability
- **NOW:** `Check for unconscionability -- Under Malaysian contract law, terms that are grossly unfair may be voidable, especially if there was unequal bargaining power`
- **PROBLEM:** `unconscionability` is the hardest word on the whole site and it leads the sentence.
  It is also the shakiest claim; Malaysian law reaches grossly unfair terms through undue influence
  (s.16 Contracts Act) and related doctrines rather than a general unconscionability ground, so the
  plain rewrite is also the more accurate one.
- **BETTER:** `Check for terms that are grossly one-sided. Where one side had far more bargaining power, Malaysian law may let the weaker side get out of the deal, most often through the undue influence rules in s.16 of the Contracts Act 1950.`

### The rest of `enhanced/` largely passes, and should be left alone
A clean sweep of the authored prose in `enhanced/` (`page-lede`, `.prose`, `.card p`, `.a`, `.hint`)
returns only **9 sentences at 28 words or longer, against 56 in the library sources**, and most of
those 9 are bullet lists in `understanding-contracts` that only read as long sentences when the
markup is stripped. **The marketing site and the guides are written at a materially easier reading
level than the library.** That gap is the finding: a reader moves from `Free, plain-language legal
knowledge for Malaysia's creative communities` straight into 46-word statutory summaries with no
warning that the register has changed. `enhanced/resources/gig-workers-act-2025/` in particular is
the reading level the library should be aiming at.

### Already good; leave alone
- `unpaid`.lede, in full. Best plain-language writing on the site.
- `arrested`.lede and `arrested`.watch (`Get the exact provision cited, in writing, before you argue
  anything.`) — a concrete action a frightened person can take in the next five minutes.
- `mural` step02, `someone-used-my-work`.watch, `foreign-artist`.watch, and the short steps generally
  (`Council by-laws on hours, noise and premises are the other common basis.`). Short steps are the
  strongest writing here; the fix is to make the long ones look like these.

---

## JARGON TABLE

Counted as the terms actually appear in `tools/scenarios.py`, `tools/registry.py` and
`tools/build.py`, then checked against `enhanced/resources/` and `enhanced/faq/`.

**The important correction: the guides already define most of these, and define them well.** The
library does not, and the two halves of the site do not link to each other.

- `enhanced/resources/understanding-contracts/` contains the single best gloss on the site:
  `A license lets the client use it; an assignment transfers ownership forever.` It also glosses
  moral rights (`the right to be credited as the creator and to object to distortion of your work.
  These moral rights exist even if you assign copyright`) and Small Claims Tribunal
  (`fast and no lawyer needed`).
- `enhanced/resources/copyright-basics/` has a whole `Fair Dealing` section.
- `enhanced/resources/gig-workers-act-2025/` puts conciliation in sequence
  (`If conciliation fails, your case goes to the Tribunal`) and carries the fact that most matters:
  `Lawyers cannot represent at the Tribunal. Section 38 prohibits advocates`.

**So the defect is not missing definitions; it is that they are unreachable from where the jargon
is used.** Measured: **the legislation library contains zero links to any guide** (0 hits for
`understanding-contracts`, `copyright-basics`, `freelancer-protections`,
`performing-artist-rights`, `gig-workers-act` across `legislation/index.html`, the scenario pages,
the Act pages and all of `build.py`/`scenarios.py`). In the other direction,
`copyright-basics` and `understanding-contracts` contain **zero links to the library**. A reader
who meets `assignment` cold in `release-track` step01 is four unguided clicks from the sentence
that explains it.

| Term | Where it appears | Keep or replace | Plainest accurate wording | Explain at first use? |
|---|---|---|---|---|
| **consolidated** / consolidation | 6× — staleness warning, Act page meta (`build.py:447`), disclaimer, `How this library is kept honest` | **Split.** Replace in the red warning box; keep in the disclaimer and provenance card, where precision is the point | Warning: `this copy of the Act`. Provenance: keep `consolidated`, add `(the AGC's tidied-up version with all amendments folded in)` once | **Yes**, once, in the provenance card |
| **subsidiary legislation** | 3× — all in the disclaimer | **Replace.** No reader needs the category name | `rules made under an Act` | No, once replaced |
| **assignment** / assign | 14× across 7 library scenarios; 12× in understanding-contracts | **Keep.** It is the difference between losing a copyright forever and lending it, and no shorter word carries that | The guide already nails it: `A license lets the client use it; an assignment transfers ownership forever.` Use that string verbatim at first use in the library | **Yes — highest priority of all.** `management-deal`.watch also glosses it well, but far too late |
| **exclusive licence** | 1× in the library (`publish-book` step02); 2× in freelancer-protections | **Keep** | `an exclusive licence (you keep the copyright, but only they may use it, and not even you)` | Yes |
| **tribunal** | 25× in the library, the most common term; 21× across the guides, where it is glossed (`fast and no lawyer needed`) | **Keep.** It is the name of the actual body | Reuse `a cheap, informal court where you normally appear yourself, without a lawyer`. For the Gig Workers Tribunal specifically, surface the guide's fact that **s.38 prohibits advocates appearing** | **Yes.** This is good news the library is failing to deliver |
| **forum** | 3× (`stage-show`.watch, `stage-show` step06, `unpaid`.watch) | **Replace outright.** The illustrator reader does not have this word and it carries no precision a plainer phrase loses | `which body hears the complaint` / `where you go to be heard` | N/A |
| **restraint of trade** | 3× | **Keep the term, change the surrounding claim.** See MISLEADING | `a clause stopping you working for others (lawyers call this restraint of trade)` | Yes |
| **passing off** | 5× | **Keep.** It is a distinct cause of action with no synonym | `passing off (suing because they traded on your name or look, even though you never registered a trademark)` | **Yes.** Currently appears in `someone-used-my-work`.lede, the first screen a wronged artist sees, cold |
| **intestate** | 2× (`archive` step04, `REGISTRY[42].why`) | **Replace.** Pure Latin with an exact English equivalent | `without a will` — `REGISTRY[42].why` already writes `dies without a will` in the same sentence as `intestate distribution`, so the site proves my point | N/A |
| **principal** | 8×, all in safety-duty steps | **Replace in body, keep in the citation.** A musician reads "principal" as a school head or a loan amount | `the person running the job` / `whoever is directing the work` | N/A once replaced |
| **conciliation** | 5× in the library; 2× in gig-workers-act-2025, in sequence (`If conciliation fails, your case goes to the Tribunal`) | **Replace in the library.** No precision is lost and the plain version is the selling point | `a free meeting run by the government to try to settle it before anyone goes to a tribunal` | N/A |
| **adjudication** | **0×** anywhere, library or guides. Good; do not introduce it | — | — | — |
| **injunction** | 3× | **Keep.** No substitute | `an injunction (a court order telling them to stop)` — `someone-used-my-work` step05 already says `to stop the use`, so only `REGISTRY[21].why` and `management-deal` step04 need the gloss | Yes |
| **rescission** | 2× (`management-deal` step04, `REGISTRY[21].why`) | **Replace.** The site already writes the plain version in the very next clause: `what you want is usually the work back or the deal undone` | `undoing the deal` | N/A |
| **fair dealing** | **0× in the library**, but `copyright-basics` has a whole `Fair Dealing` section | **Add to the library and link out.** Its absence from `documentary` and `post-set-online` is a real gap; the critic and the documentary maker both need it | `fair dealing (the narrow exceptions that let you use someone's work for criticism, review, news or research)` | Yes — and link to the guide that already covers it |
| **moral rights** | 8× in the library; also 4× in understanding-contracts and 5× in copyright-basics, **where it is properly explained** | **Keep.** Statutory term, s.25 Copyright Act | Reuse the guide's own wording: `the right to be credited as the creator and to object to distortion of your work. These moral rights exist even if you assign copyright` | **Yes.** `mural` and `exhibit-sell-art` both turn on it and neither explains it or links out |
| **badges of trade** | 4× | **Keep as the label, add the test.** Currently the site names a test and withholds its content | See SENTENCES, `exhibit-sell-art` step08 | **Yes** |
| **withholding** | 11× | **Replace the bare noun, keep `withholding tax` where it is the name** | `the 15% the payer must hold back and send to LHDN` | **Yes.** `foreign-artist`.watch already gives the practical rule; the gloss belongs at first use in `dj-club-night` step07 |
| **stamping** / stamped | 5× | **Keep.** It is the actual procedure and its name | `stamped (a duty you pay at LHDN to make the document usable in court)` | **Yes.** `REGISTRY[35].why` explains the consequence beautifully but never says what stamping *is* |
| **equitable remuneration** | 1× (`REGISTRY[64].why`) | **Replace.** `equitable` here means a statutory share, not fairness, and a lay reader will read it as "fair pay" | `the performers' share, which RPM collects for them` | N/A |
| **contracting entity** | 2× (`stage-show` step07, `brand-deal` step09) | **Replace.** Statutory drafting, not a term anyone needs | `the one legally on the hook for paying you` | N/A |

**Also undefined in the library and not on the brief's list, but as blocking:** `letter of demand`
(defined nowhere in the library, though `performing-artist-rights` and `freelancer-protections` use
it 8× between them and build a tool around it), `prima facie evidence`, `just cause or excuse`, `contract of service` (vs contract *for* services — the whole
employee/freelancer distinction turns on a one-word difference the site never flags),
`get-up`, `novelty`, `mandatory reporter`, `specific performance`, `rectification`,
`seditious tendency`, `statements conducing to public mischief`, `Director General for Industrial
Relations`.

**Concrete recommendation — cheaper than I first thought, because the writing already exists.**
Do not write a glossary page; nobody reading at 2am will open one. Do two things instead:

1. **Add a `terms` dict to `registry.py`** mapping each term to a one-line gloss **plus the guide
   that already explains it**, and render it as a `<dfn>` with a dotted underline on **first
   occurrence per page only**. Lift the wording verbatim from the guides where it exists; it is
   better than anything new. Twelve terms covers everything above: assignment, licence, tribunal,
   passing off, moral rights, stamping, withholding, injunction, principal, conciliation, badges of
   trade, contract of service. Six of the twelve already have a gloss written.
2. **Cross-link the two halves of the site.** Every scenario page should carry a
   `Read the plain-English guide →` line pointing at the matching guide (`management-deal` and
   `brand-deal` → understanding-contracts; `someone-used-my-work`, `release-track`, `mural`,
   `exhibit-sell-art` → copyright-basics; `unpaid` → freelancer-protections and
   gig-workers-act-2025; `stage-show`, `dj-club-night` → performing-artist-rights). This is a
   one-field addition to `SCENARIOS` and it converts the guides from orphans into the library's
   reading level.

---

## BILINGUAL

**The site is English-only and its audience is not.** The batik maker reader is not an edge case;
Kelantan, Terengganu and the craft and heritage segments are squarely in ALIM's stated remit, and
Malaysian legislation is authoritative in Bahasa Malaysia.

**What already exists.** `title_bm` is harvested (`tools/harvest.py:292`), stored on every entry,
indexed for search (`build.py:1223` tokenises `title_bm`, so **typing `hakcipta` or `hasutan` in
the search box already works** — this is genuinely good and nobody is told about it), and rendered
on Act pages at `build.py:467`.

**What is wrong with how it is surfaced.**

1. It renders through `class="label"`, which is `font-size:11px; letter-spacing:.16em;
   text-transform:uppercase; color:var(--ink-3)` — so `Akta Hakcipta 1987` displays as
   `AKTA HAKCIPTA 1987` in 11px letter-spaced monospace. That is the hardest-to-read styling in the
   stylesheet, applied to the string a Malay-first reader is scanning for. It reads as a filing
   code, not as a title.
2. It appears on the **Act page only**. Not on the 65 cards in `The full list`, not in search
   results, not in the `lg-step h4` chain, not in `Related situations`. The reader has to already be
   in the right place before the recognition aid appears.
3. **57 of the 65 entries carry a `title_bm`, and all 57 render it**, so coverage is good; this is
   purely a presentation and placement problem. (The 8 without one are the non-Act entries: the
   collecting societies, the industry code and the state/by-law placeholders.)

**The one concrete cheap improvement I recommend** (not a translation, one template change):

**Render the BM title as ordinary text under the English title in the search results and on every
card, and stop uppercasing it on the Act page.** Change `build.py:467` from `class="label"` to a
new `class="lg-bm"` and add:

```
.lg-bm{ font-family:'Literata',Georgia,serif; font-size:15px; color:var(--ink-2);
  margin-top:4px; }
```

then emit the same `lg-bm` line inside the card template at `build.py:649` and in the JS search
result renderer (the `tt` index already carries the tokens, so the data is present client-side).
Cost: one CSS rule and two template lines. Effect: `Akta Hak Cipta 1987` becomes findable and
recognisable at every point of contact, in a serif at 15px, rather than shouted at 11px in one
place. Add one line to the search placeholder or the `Try` chips: a `hakcipta` chip alongside
`Act 332`, which advertises that BM search works.

**Beyond Act titles**, the highest-recognition BM terms for this audience, in order, are
**hak cipta** (copyright), **akta** (Act), **seksyen** (section), **mahkamah** (court),
**fitnah** (defamation), **hasutan** (sedition), **lesen** (licence), **undang-undang kecil**
(by-law). Two of these are already carried free by the Act titles (`Akta Hasutan 1948`,
`Akta Hakcipta 1987`) the moment the rendering above lands. For the rest, the cheapest addition is
a BM word in parentheses on the **segment chips and the three objective labels only** — eleven
strings in `registry.py`, no prose touched: `Fashion & craft / Fesyen & kraf`,
`Music / Muzik`, `Artistic freedom / Kebebasan seni`. That is the recognition layer; it is not a
translation and does not imply one exists.

**Do not** half-translate the legal prose. A partial BM version of a legal explanation is worse
than none, because a reader will rely on the half they can read. If ALIM ever does translate, the
19 scenario titles and ledes are the right first 19 strings, and nothing else.

---

## MOBILE (390px)

### 1. The sticky search bar is hidden behind the sticky nav. Critical.

`#nav{ position:sticky; top:0; z-index:50 }` (alim.css:189) and
`.lg-tools{ position:sticky; top:0; z-index:30 }` (`build.py` EXTRA_CSS) **both stick to `top:0`,
and the tools bar has the lower z-index.** Once the page scrolls, `.lg-tools` slides underneath a
translucent, `backdrop-filter:blur(14px)` nav. The nav is roughly 66px tall (38px controls +
14px×2 padding). `.lg-tools` is roughly 124px tall, and its first child is the search input at
18–70px — **so the search field is almost entirely behind the nav whenever it is stuck**, which is
exactly when a user reaches for it.

- **Fix:** give the nav a height custom property and offset the tools bar:
  `#nav{ --nav-h:66px }` then `.lg-tools{ top:var(--nav-h,66px); z-index:40; }`. Raising the
  z-index alone is not enough; it would then cover the nav.

### 2. Two stacked stickies eat 190px of a 390×844 viewport

Nav 66px + tools 124px = **190px, about 23% of the screen, before browser chrome**. On an iPhone SE
(375×667) with Safari chrome it is closer to 35%. The reader sees roughly four lines of legal text
at a time.

- **Fix:** collapse `.lg-tools` on scroll to the search field alone and move the three chip rows
  behind a `Filters` disclosure on narrow viewports:
  `@media(max-width:600px){ .lg-tools .lg-chiprow{ display:none } .lg-tools details[open] .lg-chiprow{ display:flex } }`.

### 3. Tap targets under 44px (WCAG 2.5.5 / 2.5.8)

Computed from the declared padding, font-size and border:

| Element | Declared | Rendered height | Verdict |
|---|---|---|---|
| `.lg-chip` | `font-size:11px; padding:6px 11px; border:1.5px` | **≈28px** | **FAIL.** The main filter control, and there are 19 of them |
| `.lg-tab` | `font-size:11px; padding:12px 18px` | **≈37px** | **FAIL** |
| `.navcta` | `font-size:11px; padding:11px 16px` | **≈35px** | **FAIL.** This is `Get Legal Help →`, the site's primary conversion target |
| `#theme-toggle`, `#nav-toggle` | `width:38px; height:38px` | **38px** | **FAIL** |
| `.lg-search` | `font-size:16px; padding:15px 44px 15px 16px` | ≈52px | PASS, and `font-size:16px` correctly prevents iOS zoom-on-focus. Good |
| `#mobile-nav a` | `font-size:13px; padding:14px 28px` | ≈44px | PASS, exactly |
| `.lg-cell` | `padding:16px 6px; font-size:15px` | ≈50px tall | PASS height; width may fall under 44px in narrow columns |

- **Fix:** one rule, no visual change on desktop:
  `@media(pointer:coarse){ .lg-chip{ padding:11px 13px } .lg-tab{ padding:15px 18px } .navcta{ padding:15px 16px } #theme-toggle,#nav-toggle{ width:44px; height:44px } }`

### 4. Undiscoverable horizontal scroll, three places

- **`.lg-chiprow`** (`build.py:780–782`): `display:flex; overflow-x:auto; flex-wrap:nowrap` on the
  `Objective`, `Segment` and `Depth` rows. Ten segment chips at ~100px each is ~1000px of content in
  a 334px content box (390 − 2×28 `padding-inline`). **No scrollbar on iOS, no fade, no snap.** A
  reader sees `Visual arts · Music · Film &…` and has no reason to believe there are seven more.
  Note the scenario pages use `.lg-wrapchips` (`flex-wrap:wrap`) for the same job and it works
  fine — **the fix is to use `.lg-wrapchips` on the index too**, at least under 600px.
- **`.lg-matrixscroll`** (`build.py:109`): the 12-column grid, with `thead th{ min-width:78px }`, is
  ~1000px wide. Sticky `tbody th` at `left:0` helps orientation but nothing signals the scroll. Add
  a right-edge fade:
  `.lg-matrixscroll{ background:linear-gradient(to left,var(--paper-3),transparent 24px) right/24px 100% no-repeat }`
  and, per ACCESSIBILITY, `tabindex="0"` so it can be reached by keyboard at all.
- **`.lg-tabs`**: three tabs, fits at 390px. No action.

### 5. Body text under 14px

`@media(max-width:600px)` in EXTRA_CSS only adjusts two grid templates; **no font sizes are raised
for mobile anywhere in either stylesheet.**

| Selector | Size | Content it carries |
|---|---|---|
| `.lg-roleb` | **9.5px** | `I am the artist` / `I am the organiser` — the role badge on every step |
| `.lg-ink` | **10px** | the objective badges |
| `.lg-prov .lg-provtag` | **10px** | provenance status |
| `.label` | **11px** + `.16em` letter-spacing, uppercase | section labels, the `Narrow it down` prompt, **and the Bahasa Malaysia Act titles** |
| `.lg-card .lg-meta`, `.lg-step .lg-ref` | **11px** | `Act 332` and step counts |
| `.lg-matrix` | **13px** | every number in the grid |
| `.lg-prov p` | **13px** | provenance prose |
| `.lg-notice p` | **13.5px** | **the legal disclaimer** |
| `.lg-warn` | **14px** | **the staleness warning — the most safety-critical text in the library** |
| `.lg-step p` | **14.5px** | every substantive legal explanation |

- **Fix:** `@media(max-width:600px){ .lg-step p,.lg-sec{ font-size:16px } .lg-warn,.lg-notice p,.lg-prov p{ font-size:15px } .lg-roleb{ font-size:11px } .lg-ink,.lg-provtag{ font-size:11px } }`
  The 9.5px role badge is indefensible at any breakpoint; raise it globally.

### 6. Live rendering bug: double-escaped ampersand

`tools/registry.py:34` reads `"digital": "Digital &amp; media",` but `build.py` escapes through
`E()`, so the page renders the literal string **`Digital &amp; media`**. Confirmed in
`legislation/index.html` lines 250 and 269 and in four scenario pages:
`<th>Digital &amp;amp; media</th>`.

- **Fix:** `tools/registry.py:34` → `"digital":    "Digital & media",` (plain ampersand; `E()`
  handles the escaping). Check the same for any other label carrying an entity.

### 7. Nav row crowding at 390px

`#nav .row` is `display:flex; gap:18px` holding the wordmark, theme toggle, `Get Legal Help →`
(`white-space:nowrap`, ~130px) and the menu button, inside `.wrap{ padding-inline:28px }` = 334px of
space. Wordmark ~70px + 38 + 130 + 38 + 3 gaps at 18px = **330px**. It fits by 4px, which means it
will overflow the moment the font falls back to a system monospace before JetBrains Mono loads.

- **Fix:** `@media(max-width:420px){ #nav .row{ gap:10px } .navcta span{ display:none } }`, or drop
  the arrow glyph. Do **not** hide `.navcta` on mobile; it is the only route to a human above the
  fold.

### Already good
`.lg-search` at 16px with a 52px target; `.lg-wrapchips` wrapping correctly on scenario pages; the
`@media(max-width:600px)` narrowing of `.lg-sec` and `.lg-step` grid columns; `@media(hover:none){
#dot{ display:none } }`; the print stylesheet, which strips the sticky furniture properly; and
`@media (prefers-reduced-motion: reduce)` being honoured at all.

---

## ACCESSIBILITY

### Measured contrast ratios — the objective badges (`.lg-ink`)

These are the coloured tags that carry ALIM's three objectives across the whole library
(`tools/build.py:36` `OBJ_INK`, rendered at `build.py:319`). The badge is `color:#F2EBDD` on a riso
background at **10px**, uppercase, letter-spaced.

**Critical: in light mode the badge carries `mix-blend-mode:multiply` (`build.py:89`).** The
declared hex is not what renders. The element is multiplied against paper `#F2EBDD`, so both the
text and the background shift. Measured on the composited result:

| Badge | Light mode (multiply over `#F2EBDD`) | AA | Charter/dark (`mix-blend-mode:normal`) | AA |
|---|---|---|---|---|
| riso green `#00A95C` (socio) | text `rgb(230,217,192)` on `rgb(0,156,80)` = **2.56:1** | **FAIL** (also fails 3:1) | `#F2EBDD` on `#00A95C` = **2.59:1** | **FAIL** (also fails 3:1) |
| riso blue `#0078BF` (ip) | text `rgb(230,217,192)` on `rgb(0,111,166)` = **3.94:1** | **FAIL** | `#F2EBDD` on `#0078BF` = **3.99:1** | **FAIL** |
| riso purple `#765BA7` (freedom) | text `rgb(230,217,192)` on `rgb(112,84,145)` = **4.47:1** | **FAIL** (marginal) | `#F2EBDD` on `#765BA7` = **4.63:1** | **PASS** |

WCAG 2.1 **1.4.3 Contrast (Minimum)**, AA, normal text = 4.5:1. The badge is 10px, so it is
**normal text** in every reading of the spec; there is no large-text exemption available.
**Five of six states fail. Green fails so badly it misses even the 3:1 large-text floor.**

**Fix.** Two options, in order of preference:

- **Darken the three riso inks for this use only** and drop the blend mode. Keeping the riso
  identity while passing AA at 10px on `#F2EBDD` text needs roughly: green `#00753F`, blue
  `#005C92`, purple `#5B4682`. Add these as `--riso-green-ink` / `-blue-ink` / `-purple-ink` and
  point `OBJ_INK` at them, so the bright riso colours survive everywhere else on the site.
- Or invert: keep the bright riso colour as a **1.5px border and text colour on paper**, the way
  `.lg-provtag` already does (`build.py:120`). Note that `riso-green` as *text* on paper is
  **2.59:1** and on `paper-2` is **2.43:1**, so `.lg-provtag[data-tone="good"]` is **also failing
  AA today** and needs the same darkened ink.

### Colour alone (WCAG 1.4.1 Use of Colour)

The badge does carry its label as text (`{E(v['label'])}`), so the objective itself is not
colour-only. **But the framework matrix row headers at `build.py:679` and the legend at
`build.py:692` use the colour as the only link between a row and the badges on a card.** A reader
with deuteranopia sees green and blue badges as near-identical at 10px. Add a one-character prefix
or a distinct shape (e.g. `S ·` `IP ·` `AF ·`) so the mapping survives without colour.

### The role filter's dimming — fails, and it is the worst failure on the site

`build.py` EXTRA_CSS: `.lg-step[data-dim="1"]{ opacity:.34; }`

Measured, composited over paper `#F2EBDD`:

| Dimmed element | Rendered | Ratio | AA |
|---|---|---|---|
| step body (`ink-2` @ .34) | `rgb(180,173,160)` | **1.88:1** | **FAIL** |
| step heading (`ink` @ .34) | `rgb(169,163,152)` | **2.11:1** | **FAIL** |
| step number (`vermillion` @ .34) | `rgb(233,172,156)` | **1.63:1** | **FAIL** |
| charter mode, step body | `rgb(82,77,66)` on `#15120D` | **2.22:1** | **FAIL** |

WCAG **1.4.3**. Nothing here is close. This matters more than the badges because the dimmed steps
are *still real legal content the reader may need* — the role filter says "this probably isn't your
part", not "this is irrelevant". A reader who filters to "artist" and then wants to check what the
venue's duty is cannot read it.

**Fix.** Do not use opacity to de-emphasise text. Either (a) raise to `opacity:.62`, which puts
`ink-2` at about 4.6:1 and just clears AA, or (b) better, keep the text at full contrast and move
the de-emphasis to the container: a `background:var(--paper-2)` and a thinner rule, with the
existing `N of M apply to you` line doing the explanatory work. Option (b) is also more honest.

### Matrix zero-cells

`.lg-cell[data-n="0"]{ color:var(--ink-3); opacity:.4; }` renders `rgb(188,179,164)` on paper =
**1.75:1**. **FAIL, WCAG 1.4.3.** These are `0` digits, so the information loss is small, but they
are inside a `<table>` that a screen reader will read out regardless. Replace the opacity with
`color:var(--ink-3)` alone (**5.25:1**) and let the absence of a link do the de-emphasis, or render
an empty cell with `aria-label="none"`.

### Passing, and worth protecting

- Body prose `ink-2 #3C342A` on paper: **10.31:1**. Excellent.
- `ink #1A1612` on paper: **15.16:1**.
- Pressed chip, paper on ink: **15.16:1**.
- `ink-3 #6B5F4E` labels on paper: **5.25:1** (on `paper-2`: **4.92:1**). Passes, but these are
  10–11px uppercase letter-spaced, which is the hardest thing on the page to read for a
  second-language reader even at passing contrast. See MOBILE.
- Charter mode `ink-2 #C9BFA8` on `#15120D`: **10.23:1**.
- Charter `ink-3 #897E68` on `#15120D`: **4.67:1**. Passes, barely.

### Borderline: the vermillion step numbers and `.lg-num`

`--vermillion #D8311F` on paper = **4.04:1**; on `paper-2` = **3.79:1**; charter on `#15120D` =
**3.90:1**. `.lg-num` is 12px and `.lg-step-n` is 12px, so these are normal text and **all three
FAIL 1.4.3 (needs 4.5:1)**. They are section numbers, so comprehension loss is low, but
`--vermillion-2 #B5261A` is already defined and would fix it at no design cost. Note this also
affects `.idx` and `.dropcap` site-wide, and `::focus-visible{ outline:2px solid var(--vermillion) }`
— the focus ring is a non-text element under **1.4.11 (3:1)**, so at 4.04:1 the focus ring itself is
fine on paper.

### Chips: are they real buttons with state?

**Yes, and this is done well.** `.lg-chip` is rendered as a real `<button>` with
`aria-pressed="true"` and a `[aria-pressed="true"]` style that changes **both** background and
colour (15.16:1). A screen reader announces "pressed". **Leave this alone.** Two caveats:

- Some chips render as `<a class="lg-chip">` (the cross-links on instrument and scenario pages).
  Those are correctly links, not buttons; no change needed, but they look identical to the stateful
  filter chips, so a sighted keyboard user cannot tell which will filter and which will navigate.
  Recommend the existing `.lg-chip.lg-alt` dashed border be used consistently for navigational
  chips.
- `.lg-chip:hover` changes `color` and `border-color` only. On touch there is no hover, so the only
  affordance that a chip is interactive is its border. Acceptable.

### Do search results announce to a screen reader?

**No.** This is a real defect. The search in `build.py` writes results into the DOM
(`renderAnswer`, the `count.textContent=...` line) with **no live region**. A blind user types a
query and hears nothing; the page appears not to have responded.

WCAG **4.1.3 Status Messages** (AA). **Fix:** add `role="status" aria-live="polite"
aria-atomic="true"` to the element that holds the count (the `count` node), so it announces
`"12 laws and codes"` on each keystroke-debounced update. Do **not** put the live region on the
results container itself; announcing 12 full cards is worse than silence. The count line is the
right granularity.

Related: the search input has `aria-label`? Check `.lg-search` markup — if it has only a
`placeholder`, that is **1.3.1/4.1.2** and needs a real `<label class="sr-only">` or `aria-label`,
because placeholder text disappears on focus and is not a name.

### Is the grid a real table with headers?

**Yes, and this is genuinely good.** `.lg-matrix` is a `<table>` with `<thead><tr><th>` and
`<tbody><th>` row headers (`build.py:759`, `:679`). A screen reader can navigate it.
Two gaps:

- The `<th>` cells lack `scope="col"` / `scope="row"`. In a two-axis grid, assistive tech guesses.
  **Fix (1.3.1):** add `scope="col"` to the head cells and `scope="row"` to the `tbody th`.
- The table has **no `<caption>`**. Add
  `<caption class="sr-only">Number of laws and codes by aim and field</caption>`.
- The wrapper `.lg-matrixscroll{ overflow-x:auto }` is not keyboard-focusable, so a keyboard-only
  user cannot scroll it. **Fix (2.1.1):** add `tabindex="0"` and `role="region"` with an
  `aria-label` to `.lg-matrixscroll`.

### Other

- `.skip-link` exists and is correctly implemented. Good.
- `#theme-toggle` has `aria-label` and `aria-pressed`. Good.
- `details.lg-fold>summary{ list-style:none }` removes the disclosure triangle. The summary is still
  a real `<summary>` so it remains keyboard-operable and announces expanded state, but sighted
  users lose the only visual cue that it opens. There is a `.q-sign`-style `+` on the FAQ pages;
  the library folds should get the same.
- `mark{ background:rgba(216,49,31,.22) }` on search hits: against `paper-2`, the highlight is a
  background tint only, with `color:inherit`. Text contrast is preserved, which is correct. But the
  highlight itself conveys "this matched" by colour alone. Low severity; a `<mark>` element is
  semantically announced by some screen readers. Leave.

---

## FINDABILITY AND THE FIRST MOMENT

**Landing cold on the home page: no.** The first screen is `The ALIM Dossier · § 01 · Manifesto ·
Filed from Kuala Lumpur · § On purpose`, then `Alim is a legal clinic for Malaysia's creative
communities. Independent. Non-profit.` The dossier conceit is handsome and it costs the reader the
whole first screen. A frightened person in five seconds needs one of two things: *what do I do now*
or *who do I talk to*. The only thing on the mobile first screen that offers either is the 35px
`Get Legal Help →` button in the nav. **Recommend a single line immediately under the hero
paragraph, above the fold:** `Something happened and you need help now? → Get Help` as a real
button, not a `.label`. Nothing else about the home page needs to change.

**Is the fear case reachable fast? From the library, yes. From the home page, no.** The route to
`Stopped, raided, shut down or arrested` is home → Resources → legislation library → scroll the
19-card grid → the card. **Four steps, and the third is a page called "Legislation", which is the
last word a frightened person will click.** The 19 situation cards are the best asset ALIM has built
and they are buried under the most forbidding noun on the site. Recommend surfacing three or four
situation cards directly on `enhanced/resources/index.html` — `Stopped or shut down`,
`Chase an unpaid fee`, `Someone used your work` — linking straight into `legislation/doing/<id>/`.
That is a template change, not new content.

**Is the route to a human visible from inside the library? Yes, and it is done well.** 5 to 7
`get-help` links per page: the nav link, the nav CTA, the mobile nav, the hero lede
(`If you'd rather talk to a person, that's what Get Help is for`), the disclaimer close
(`If you have a live problem, talk to us. It is free and confidential.`), and on the `arrested`
scenario a dedicated `Talk to someone at ALIM →` line directly under the role chips. **That last one
is the single best access decision in the build. It should not stay gated to one scenario.**
Recommend extending `help_line` to at least `arrested`, `documentary`, `unpaid` and
`someone-used-my-work` — the four fear-and-money pages.

**The search box is the real front door and it is better than the navigation.** The placeholder
`What are you doing? Try "DJing", "busking", "client won't pay", "Act 332"` is exactly right, and
the `Try` chips below it are the best onboarding on the site. It also already searches Bahasa
Malaysia Act titles, which nothing tells the reader. Leave the copy alone; fix its position (see
MOBILE 1) so it is actually visible when stuck.

---

## MISLEADING TO A LAY READER

Every sentence below is legally accurate. Each one will be acted on wrongly.

### 1. `tools/scenarios.py` :: `management-deal`.lede — the most dangerous sentence on the site
- **SENTENCE:** `What you assign you do not get back, and the clause that looks like a life sentence is often void anyway.`
- **WHAT A SCARED PERSON DOES:** An artist trapped in a management deal reads `often void anyway`,
  concludes their own clause is void, and stops performing under the contract: takes the competing
  booking, signs elsewhere, stops paying commission. `Often` is doing enormous work that a
  distressed reader will not see. Section 28 of the Contracts Act has express exceptions, a void
  restraint does **not** void the rest of the agreement, and the artist remains bound by every other
  clause. They can be sued for breach on the parts that are perfectly enforceable.
- **FIX:** `What you assign you do not get back. And the clause that looks like a life sentence is often weaker than it reads, but the rest of the agreement usually still binds you, so this is a fight to have with advice rather than a reason to walk away on your own.`

### 2. `tools/scenarios.py` :: `documentary`.watch and `.lede`
- **SENTENCE:** `Section 6 of the Film Censorship Act catches possession. A finished unapproved cut sitting on your drive is already inside the offence.`
- **WHAT A SCARED PERSON DOES:** Deletes the footage. This is the documentary maker in the brief,
  who has already had a lawyer's letter. He destroys years of work, and if any proceeding or
  complaint is live he has turned a censorship exposure into a far worse problem. The site tells him
  the material is incriminating and says nothing at all about what to do with it.
- **FIX:** append to the watch line: `Do not delete it and do not hand it over. Destroying material after a complaint or a letter has arrived makes things worse, not better. Talk to someone first.`

### 3. `tools/scenarios.py` :: `dj-club-night` step10, `release-track` step06, `management-deal` step01
- **SENTENCE:** `Section 28 makes agreements in restraint of trade void, which is why most radius and exclusivity clauses in Malaysian booking agreements are weaker than they read.`
- **WHAT A SCARED PERSON DOES:** The 24-year-old DJ takes the competing booking inside a radius
  clause, because a legal website told him the clause is void. Whether *his* clause falls within
  s.28 is fact-specific; he can still be terminated, still be sued for damages on other grounds, and
  still lose the promoter. `Weaker than they read` is a bargaining observation being read as
  permission.
- **FIX:** `Section 28 makes agreements in restraint of trade void, which is why many radius and exclusivity clauses in Malaysian booking agreements have less force than they appear to. That is a reason to negotiate one, not a reason to ignore one you have already signed.`

### 4. `tools/scenarios.py` :: `arrested` step06 (act-15)
- **SENTENCE:** `Seditious tendency, with intention expressly irrelevant.`
- **WHAT A SCARED PERSON DOES:** Two opposite wrong things, both bad. Either he concludes nothing he
  says can help and gives a full statement to police without counsel because it seems pointless to
  hold back; or he concludes he is already guilty and pleads. The sentence states the most
  frightening feature of the Sedition Act with no context and no next step, on the page for people
  currently in custody.
- **FIX:** see SENTENCES above. The essential addition is the final clause: `Do not try to work this
  one out alone.`

### 5. `tools/scenarios.py` :: `arrested`.lede, in combination with its position
- **SENTENCE:** `This is a frightening place to be, and it usually has more give in it than it feels like. Most of these turn on a licence condition or a council by-law rather than the speech offence everyone assumes, and that changes what you can do next.`
- **WHAT A SCARED PERSON DOES:** Argues at the door. The reassurance is correct and humane, and it
  arrives **before** the one instruction that makes it safe, which is `Get the exact provision cited,
  in writing, before you argue anything` — currently sitting at the bottom of the page after eleven
  Acts. A reader who takes only the lede has been told it is probably just a licensing matter and
  has not been told to say nothing and write things down.
- **FIX:** do not change the lede; **move the watch line above the chain on this scenario.** In
  `scenario_page()`, render `{watch}` before the steps section when `sc["id"] == "arrested"`. This
  is a two-line change and it is the highest-value structural edit in this report.

### 6. `tools/scenarios.py` :: `unpaid` step03 (act-265)
- **SENTENCE:** `If you were in truth an employee, the Labour Department is the cheap route: the Director General can hear a wages dispute under s.69 of the Employment Act 1955 and order payment with no cap on the amount.`
- **WHAT A SCARED PERSON DOES:** The illustrator remembers `no cap on the amount` and forgets
  `if you were in truth an employee`. He files at the Labour Department as a freelancer, waits,
  and is turned away — having possibly let the cheaper Gig Workers route or a limitation period
  run. The conditional is the load-bearing clause and it is first, which is where readers skim.
- **FIX:** `The Labour Department is the cheap route, but only if you were in truth an employee rather than a freelancer. If you were, the Director General can hear a wages dispute under s.69 of the Employment Act 1955 and order payment, with no cap on the amount. If you were not, this door is closed and step 02 is yours instead.`

### 7. `tools/scenarios.py` :: `run-organisation`.lede
- **SENTENCE:** `A collective that never chose a vehicle is already a partnership, with liabilities it never agreed to.`
- **WHAT A SCARED PERSON DOES:** An unfunded arts collective panics and rushes into a registration
  it does not need, or worse, assumes personal liability it does not actually have. A partnership
  under the Partnership Act 1961 requires business carried on **in common with a view of profit**;
  a non-profit collective of artists may well not be one. Stated flatly as `is already a
  partnership`, this is an overclaim against the very readers it addresses.
- **FIX:** `A collective that never chose a vehicle may already be a partnership in law, which would mean liabilities the members never agreed to. Whether it is turns on whether you are carrying on a business for profit, so this is worth checking before you assume either way.`

### 8. `tools/scenarios.py` :: `post-set-online`.watch
- **SENTENCE:** `Most artists prepare for the charge that rarely comes and have no plan for the takedown that does.`
- **WHAT A SCARED PERSON DOES:** Reads `rarely comes` as reassurance and posts. ALIM's own registry
  entry for the same Act says s.233 `is the provision most often used against artists, critics and
  commentators, and it was amended with heavier penalties in 2024`. The two strings contradict each
  other and the reassuring one sits on the page people actually read.
- **FIX:** `Most artists brace for a charge and have no plan at all for the takedown, which is far more likely to be what actually happens. Prepare for both.`

### 9. `tools/build.py` :: the staleness warning
- **SENTENCE:** `This copy of the Act is {age} years old. Any amendment made since {pretty} is not shown.`
- **WHAT A SCARED PERSON DOES:** Concludes the Act is out of date and therefore does not apply to
  him, and stops reading. The warning is about ALIM's *copy*, not about the law's force; a lay reader
  does not hold that distinction. The rewrite from `consolidation` to `copy of the Act` (already
  applied, and correct) makes the ownership of the staleness clearer but does not close this gap.
- **FIX:** add one clause: `This copy of the Act is {age} years old, so any amendment made since {pretty} is not shown here. The Act itself is still in force; it is our copy of the text that may be behind.`

### 10. Interaction, not a sentence: the role filter
- **BEHAVIOUR:** Selecting `I am the artist` dims every other step to `opacity:.34` (**1.88:1**).
- **WHAT A SCARED PERSON DOES:** Reads the dimmed steps as *not applicable to me*. But on
  `dj-club-night` a self-promoting DJ is the artist **and** the organiser, and on `stage-show` a
  producer-performer is both. The filter offers an exclusive choice for a role that is very often
  joint, and then makes the other half unreadable. The `N of M apply to you` counter reinforces the
  false exclusivity.
- **FIX:** allow multiple role chips to be pressed at once (they are already `aria-pressed`
  buttons, so the state model supports it), change the counter to `N of M are about your part`, and
  per ACCESSIBILITY stop using opacity to de-emphasise. Add one line under the chips:
  `Many people are both. Pick both if that is you.`

### Already handled well; do not touch
- `someone-used-my-work`.watch: `A letter of demand from someone who turns out not to own the work
  is worse than silence` — names the wrong action and why. This is the model for every fix above.
- `exhibit-sell-art` step04: `the Tribunal is cheap enough to be used against you` — a two-directional
  warning, rare and valuable.
- `archive`.watch on orphan works: `Document your diligent search before you publish, because that
  record is the only mitigation available` — correctly refuses to promise the documentation makes it
  lawful.
- `foreign-artist`.watch: `Budget the withholding into the fee from the first email` — converts a tax
  rule into a negotiating instruction. Best money-case writing on the site.
- The whole `lg-notice` disclaimer, apart from `Subsidiary legislation`. `Please do not act, or
  decide not to act, on the strength of this page alone` covers the *decide not to act* case, which
  almost no disclaimer does.
