# -*- coding: utf-8 -*-
"""
The intelligence layer over the ALIM legislation registry.

Two things live here:

  SCENARIOS   real-world things people in the arts actually do, each resolved
              into the ordered chain of instruments that bite, with a note on
              what each one does *in that situation* and which role it lands on.
              This is the layer that answers "I am DJing a club night" — a
              question no section heading in any Act contains.

  ALIASES     the words people actually type, mapped onto instruments. "MCMC"
              has to find the Communications and Multimedia Act; "233", "MACP",
              "PDPA", "unfair dismissal" and "sync" all have to land somewhere.

Every `ref` is validated against the live registry by tools/build.py, so a typo
here fails the build rather than shipping a dead link.
"""

# ---------------------------------------------------------------------------
# What people type -> what it should find.  Lower-case; matched on whole words
# or word prefixes, never as a raw substring (that is how "dj" once matched
# "a-dj-acent" three times and found nothing real).
# ---------------------------------------------------------------------------
ALIASES = {
    "act-332": ["copyright", "hak cipta", "moral rights", "fair dealing", "infringement",
                "royalties", "ownership", "licence", "licensing", "assignment", "performers",
                "performer rights", "bootleg", "remix", "sample", "sampling", "mashup",
                "public performance", "sync", "synchronisation", "plagiarism", "stolen",
                "credit", "attribution", "orphan works", "derivative", "song", "lyrics",
                "artwork", "my work", "stole", "copied", "no permission"],
    "act-815": ["trademark", "trade mark", "brand", "logo", "band name", "artist name",
                "label name", "passing off", "madrid", "myipo", "tm"],
    "act-552": ["industrial design", "design registration", "product design", "pattern"],
    "act-291": ["patent", "invention", "utility innovation"],
    "act-836": ["geographical indication", "songket", "batik", "pua kumbu", "craft", "heritage craft"],
    "act-606": ["optical disc", "cd", "dvd", "pressing", "replication", "piracy"],
    "act-730": ["trade description", "counterfeit", "fake goods", "misdescription"],
    "fedcon": ["constitution", "perlembagaan", "article 10", "free speech", "freedom of expression",
               "fundamental liberties", "human rights"],
    "act-588": ["mcmc", "cma", "communications and multimedia", "233", "s233", "section 233",
                "online", "internet", "social media", "post", "posting", "platform",
                "offensive content", "cyber", "suruhanjaya komunikasi"],
    "act-866": ["online safety", "harmful content", "takedown", "take down", "removal",
                "platform duty", "osa", "act 866", "mcmc", "removed", "deleted",
                "suspended account", "banned online"],
    "act-620": ["censorship", "lpf", "film censorship", "classification", "banned",
                "board of film censors", "penapisan", "screening", "cut"],
    "act-244": ["finas", "film licence", "shooting licence", "production licence",
                "perbadanan kemajuan filem"],
    "act-301": ["pppa", "printing press", "publication permit", "publishing permit",
                "banned book", "printing presses and publications", "kdn"],
    "act-15": ["sedition", "hasutan", "seditious"],
    "act-286": ["defamation", "libel", "slander", "fitnah", "reputation", "review",
                "bad review", "criticism"],
    "act-574": ["penal code", "kanun keseksaan", "obscene", "obscenity", "298a", "505",
                "religious feelings", "indecent", "criminal", "292", "294"],
    "act-336": ["minor offences", "busking", "busker", "begging", "public nuisance", "street"],
    "act-736": ["assembly", "protest", "gathering", "vigil", "himpunan", "peaceful assembly"],
    "act-88": ["official secrets", "osa 1972", "classified", "leak", "whistle"],
    "act-563": ["computer crimes", "hacking", "unauthorised access", "scraping", "hacked"],
    "act-136": ["contract", "kontrak", "agreement", "breach", "consideration", "restraint of trade",
                "exclusivity", "nda", "terms", "deal", "verbal agreement", "whatsapp agreement"],
    "act-137": ["specific relief", "injunction", "rescission", "rectification", "stop order"],
    "act-265": ["employment", "employee", "wages", "leave", "maternity", "paternity", "notice",
                "termination", "overtime", "rest day", "labour", "buruh", "jtk"],
    "act-872": ["gig worker", "gig", "platform worker", "freelance", "freelancer", "deactivation",
                "eaduan", "act 872", "grab", "rider"],
    "act-789": ["perkeso self employed", "self employment social security", "socso self employed",
                "injury cover", "freelance insurance"],
    "act-4": ["socso", "perkeso", "employment injury", "invalidity"],
    "act-452": ["epf", "kwsp", "provident fund", "retirement"],
    "act-177": ["industrial relations", "unfair dismissal", "dismissal", "sacked", "fired",
                "section 20", "industrial court", "reinstatement"],
    "act-262": ["trade union", "union", "kesatuan", "guild", "organise"],
    "act-840": ["sexual harassment", "harassment", "gangguan seksual", "tribunal",
                "misconduct", "me too", "abuse"],
    "act-514": ["osha", "safety", "occupational safety", "accident", "rigging", "crew safety",
                "dosh", "risk assessment"],
    "act-611": ["child", "minor", "child protection", "kanak-kanak"],
    "act-350": ["child performer", "child actor", "young person", "child employment"],
    "act-599": ["consumer protection", "refund", "online seller", "ecommerce", "e-commerce",
                "misleading", "tribunal for consumer claims", "ttpm", "shop", "store"],
    "act-658": ["electronic commerce", "electronic signature", "esign", "digital signature",
                "email contract", "whatsapp contract"],
    "act-378": ["stamp duty", "stamping", "setem", "stamp", "adjudication", "lhdn stamp"],
    "act-53": ["income tax", "tax", "withholding", "109a", "public entertainer", "lhdn",
               "cukai", "badges of trade", "deductions"],
    "act-807": ["service tax", "sst", "sales and service tax", "taxable service"],
    "act-155": ["immigration", "visa", "work permit", "professional visit pass", "pvp",
                "foreign artist", "imigresen", "pass"],
    "act-709": ["pdpa", "personal data", "data protection", "privacy", "mailing list",
                "database", "breach notification", "dpo", "consent"],
    "act-254": ["limitation", "time bar", "too late", "six years", "deadline"],
    "act-646": ["arbitration", "aiac", "dispute resolution", "arbitrate"],
    "act-300": ["distribution act", "intestate", "estate", "inheritance", "died", "death",
                "succession", "catalogue estate"],
    "act-777": ["companies act", "sdn bhd", "clbg", "company limited by guarantee",
                "incorporate", "ssm", "directors duties", "berhad"],
    "act-832": ["societies", "society", "ros", "persatuan", "register a society", "collective"],
    "act-743": ["llp", "limited liability partnership", "plt"],
    "act-135": ["partnership", "band agreement", "collective agreement", "joint venture"],
    "act-200": ["fundraising", "street collection", "donation", "benefit gig", "charity"],
    "act-645": ["national heritage", "heritage", "warisan", "heritage site", "conservation",
                "listed building", "artefact"],
    "act-629": ["national archives", "archive", "arkib", "public records", "records"],
    "act-724": ["national art gallery", "balai seni", "visual arts board", "national collection"],
    "act-653": ["aswara", "arts education", "akademi seni"],
    "act-493": ["entertainment licence", "kl entertainment", "dbkl", "club licence",
                "venue licence", "place of entertainment"],
    "act-171": ["local government", "by-law", "bylaw", "council", "mbpj", "mbsa", "mbsj",
                "licence hawker", "noise", "operating hours", "premises"],
    "act-103": ["entertainments duty", "ticket duty", "admission duty"],
    "act-91": ["courts", "jurisdiction", "appeal", "high court"],
    "act-92": ["small claims", "small claim", "small claims court", "magistrates court",
               "magistrate", "form 198", "order 93", "sue", "suing", "take them to court",
               "claim under 5000", "rm5000", "cheap court", "no lawyer"],
    "act-67": ["civil law", "common law", "damages", "interest"],
    "cmcf-content-code": ["content code", "cmcf", "content forum", "advertising standards",
                          "broadcast standards", "mcmc", "self regulation"],
    "puspal": ["puspal", "foreign artiste", "filming permit", "foreign performer clearance"],
    "state-entertainment": ["state licence", "selangor", "penang", "johor", "sabah", "sarawak",
                            "state enactment", "entertainment enactment"],
    "syariah-criminal": ["syariah", "shariah", "jakim", "jais", "religious offence", "khalwat"],
    "berne": ["berne", "international copyright", "overseas protection", "wipo"],
    "wppt": ["wppt", "performers treaty", "neighbouring rights"],
    "marrakesh": ["marrakesh", "accessible format", "braille", "print disabled", "accessibility"],
    "cmos": ["macp", "prism", "rpm", "collecting society", "collective management",
             "performing rights", "licensing body", "royalty collection", "ppm",
             "public performance licence", "blanket licence"],
}


# ---------------------------------------------------------------------------
# Scenarios.  steps = (instrument id, [roles it lands on], what it does here)
# ---------------------------------------------------------------------------
SCENARIOS = [

dict(
  id="dj-club-night", title="DJ a club night",
  lede="You are playing other people's recordings to a paying room. Three separate licences, "
       "one venue licence, a state layer, and a tax nobody budgets for.",
  segments=["music", "performing"], objectives=["ip", "socio", "freedom"],
  aliases=["dj", "djing", "deejay", "dj set", "spin", "spinning", "decks", "turntable",
           "club", "club night", "nightclub", "rave", "party", "set", "residency", "selector",
           "techno", "house music", "open format", "gig", "night", "promoter", "bar", "festival"],
  roles={"dj": "I am the DJ", "promoter": "I am the promoter", "venue": "I am the venue"},
  steps=[
    ("cmos", ["venue", "promoter"],
     "Playing recorded music to a paying room engages three separate claims held by three "
     "separate bodies: MACP for the musical work, PPM for the sound recording, and RPM for the "
     "performers on it. A room holding one of the three is under-licensed, and the liability "
     "lands on whoever put the night on."),
    ("act-332", ["dj", "promoter", "venue"],
     "Public performance and communication to the public are acts the copyright owner controls. "
     "Your own edits, bootlegs and mashups are derivative works: making one is a permission, "
     "playing it is a second, releasing it is a third."),
    ("act-493", ["venue", "promoter"],
     "In Kuala Lumpur the premises needs an entertainment licence, and the conditions attached to "
     "it are where hours and content are actually controlled. The licence, not a statute, is "
     "usually what a shutdown is based on."),
    ("state-entertainment", ["venue", "promoter"],
     "Outside KL the same power sits in state enactments and council by-laws, and they differ by "
     "state. Confirm the licensing position before you confirm the date."),
    ("act-171", ["venue", "promoter"],
     "Operating hours, amplified noise and premises licensing come from local authority by-laws "
     "made under this Act. If you are being moved on or closed early, this is usually why."),
    ("act-103", ["promoter"],
     "Entertainments duty is charged on payments for admission. In the Federal Territories it "
     "runs under the Entertainments Duty Act 1953, where the Collector is the Minister of "
     "Finance and the rate is set by resolution of the Dewan Rakyat. Outside the Federal "
     "Territories each state has its own entertainment duty enactment and its own rate and "
     "exemptions, so confirm which one you are under before you price the ticket. Either way it "
     "is a real line on a ticketed show's budget and first-time promoters leave it out."),
    ("act-53", ["promoter"],
     "Book a non-resident DJ and the withholding under s.109A is yours, not the artist's. The "
     "rate is 15 per cent of the gross under Part II of Schedule 1, you deduct on paying or "
     "crediting and you must account for it and pay it to the Director General within one "
     "month. Miss it and s.109(2) adds a further 10 per cent and makes the whole thing a debt "
     "payable forthwith. If you book through a company the debt is the company's, but s.75A "
     "makes any director who controls twenty per cent or more of the shares jointly and "
     "severally liable for it, which in a two-person promoter company is everybody."),
    ("act-155", ["promoter"],
     "A performance is work, so a foreign DJ needs the right pass. A social visit pass is the "
     "wrong pass and the exposure runs to the person who brought them in."),
    ("puspal", ["promoter"],
     "Foreign performers also need PUSPAL clearance before the immigration pass issues, and that "
     "is usually the binding constraint on your timeline, not the pass itself."),
    ("act-136", ["dj", "promoter", "venue"],
     "The booking is a contract whether or not anyone signed anything. Section 28 makes "
     "agreements in restraint of trade void, and Malaysian courts do not soften a restraint for "
     "reasonableness the way English courts do; if it is a restraint it is simply void. But the "
     "section bites on what happens **after** the deal ends. A radius clause that stops you "
     "playing another room in the weeks after this show is squarely in its sights. An "
     "exclusivity that only binds you while the booking is on foot is not: in Polygram Records "
     "v Hillary Ang the High Court upheld exactly that kind of in-term exclusive against a "
     "band. Treat the post-term restriction as the weak one and the in-term one as real."),
    ("act-514", ["venue", "promoter"],
     "** `Since 1 June 2024 the safety duty can land on you, the person running the night, and "
     "not only on the crew's own employer. It lands on you if you are telling them how to do "
     "the work. If you leave the method entirely to their employer, that particular duty is not "
     "yours."),
    ("act-840", ["dj", "promoter", "venue"],
     "The Tribunal takes complaints from outside an employment relationship, which is exactly the "
     "shape harm takes in nightlife: a freelancer and a gatekeeper who is not their employer."),
    ("act-574", ["dj"],
     "Section 294(b) reaches whoever, **to the annoyance of others**, sings, recites or utters "
     "any obscene song, ballad or words in or near any public place. Annoyance to somebody is "
     "part of the offence, not background, and it is the first thing to test. The maximum is "
     "three months' imprisonment, a fine, or both."),
    ("act-807", ["promoter", "venue"],
     "Once past the registration threshold, event and related services can be taxable. The list "
     "is widened by order most years, so check the current schedule rather than a remembered figure."),
  ],
  watch="The single most common failure is the room assuming one licence covers the music. It "
        "does not. MACP, PPM and RPM are three separate bodies collecting on three separate "
        "rights, and each sets its own tariff.",
  related=["post-set-online", "foreign-artist", "arrested"]),

dict(
  id="post-set-online", title="Post a set, reel or performance video",
  lede="Uploading is reproduction and communication to the public, and then four separate speech "
       "regimes sit on top of it.",
  segments=["music", "content", "digital", "film"], objectives=["ip", "freedom"],
  aliases=["upload", "post", "posting", "video", "reel", "reels", "youtube", "instagram", "tiktok",
           "mixcloud", "soundcloud", "boiler room", "livestream", "live stream", "stream",
           "set video", "content", "clip", "vlog", "podcast", "shorts", "mcmc", "233",
           "section 233", "takedown", "taken down", "removed", "reported", "online",
           "social media", "viral", "caption", "comment"],
  roles={"creator": "I posted it", "organiser": "I ran the event", "subject": "I am in it"},
  steps=[
    ("act-332", ["creator", "organiser"],
     "A recorded set or a reel with music in it contains other people's recordings and "
     "compositions. Uploading is both reproduction and communication to the public, which is why "
     "content matching pulls sets down even when nobody complained."),
    ("cmos", ["creator", "organiser"],
     "A licence the venue holds for the room does not travel with the video. Platform-level "
     "licensing covers some uses and not others, and never covers a full recorded set."),
    ("act-588", ["creator"],
     "Section 233 is the provision most often used against people who post. It reaches content "
     "that is obscene, indecent, false, menacing or grossly offensive in character, sent with "
     "intent to annoy, abuse, threaten, harass, or commit an offence involving fraud or "
     "dishonesty against, any person. The Communications and Multimedia (Amendment) Act 2025 "
     "(Act A1743) took effect on 11 February 2025; it raised the maximum to a fine of RM500,000 "
     "or two years or both, but it also raised the threshold from 'offensive' to 'grossly "
     "offensive' and wrote in Explanations that say satire, parody and clearly fictional work "
     "are not 'false', that artistic or anatomical depiction of the body is not obscene or "
     "indecent, and that a good-faith statement of fact or opinion is not grossly offensive. In "
     "February 2026 the Federal Court in Government of Malaysia v Heidy Quah Gaik Li kept the "
     "words 'offensive' and 'annoy' in the section but read it down: it reaches communications "
     "intended to cause harm, and anger or discontent provoked by political or controversial "
     "expression is protected speech, not harm. The consolidated text we host predates all of "
     "this. This is the MCMC route."),
    ("cmcf-content-code", ["creator"],
     "The Content Code is prepared by the Content Forum, which the Commission designates under "
     "s.212, and it is registered by the Commission under s.95 of the Communications and "
     "Multimedia Act. Once registered, s.98(2) makes compliance with it a defence to any "
     "prosecution, action or proceeding about a matter the code deals with, for a person who is "
     "subject to the code. Section 98(1) also says compliance is not compulsory. Day to day the "
     "Code does more work than the Act: it is the standard platforms, broadcasters and "
     "advertisers actually apply when they decide whether your work goes out."),
    ("act-866", ["creator", "subject"],
     "In force from 1 January 2026. Your exposure here is not a charge, it is silent removal by a "
     "platform acting on a statutory duty, and a removal is far harder to appeal than a charge is "
     "to defend."),
    ("act-620", ["creator"],
     "The Film Censorship Act does not apply to what you put on the internet. Section 2(3) says "
     "the Act is not to be construed as permitting the censorship of any film transmitted over "
     "the internet or an intranet. The moment the same work moves offline, into a screening, a "
     "gallery, a festival or physical copies, Board approval becomes the gate and the Board "
     "reads 'film' widely enough to catch shorts, music videos and festival material. Online, "
     "your exposure is s.233 and the Online Safety Act, not the Board."),
    ("act-709", ["creator", "organiser"],
     "Filming the room means processing other people's personal data. Since 1 June 2025 you "
     "must notify the Commissioner of a personal data breach as soon as practicable and no "
     "later than 72 hours after it happens, and then tell the affected people within 7 days of "
     "notifying the Commissioner where the breach causes or is likely to cause them significant "
     "harm. Note the trigger: the 72 hours runs from the breach happening, not from you finding "
     "out about it, and if you miss it you have to give the Commissioner a written explanation "
     "with supporting evidence. There is no size threshold on that duty. The data protection "
     "officer duty is different: it only bites if you process the personal data of 20,000 or "
     "more people, the sensitive personal data of 10,000 or more, or your core activity is "
     "regular and systematic monitoring. Almost no individual artist will reach that."),
    ("act-286", ["creator", "subject"],
     "What you say over the top, or in the caption, is publication. It also cuts the other way: "
     "this is your statute if someone destroys your reputation in a post."),
    ("fedcon", ["creator"],
     "Article 10(1)(a) is the right every statute above restricts, and Article 10(2)(a) is the "
     "power they are made under. Every challenge to a takedown or a charge starts here."),
  ],
  watch="Removal and prosecution are different problems with different cures. Most artists prepare "
        "for the charge that rarely comes and have no plan for the takedown that does.",
  related=["dj-club-night", "brand-deal", "documentary"]),

dict(
  id="busking", title="Busk or perform in the street",
  lede="The rule that decides whether you can play is almost always your own council's by-law, "
       "and nobody publishes those in one place. Below is the federal layer, and where to go "
       "for the council layer.",
  segments=["music", "performing", "visual"], objectives=["freedom", "socio"],
  aliases=["busk", "busking", "busker", "street performance", "street performer", "street",
           "public performance", "pasar seni", "central market", "sidewalk", "pavement",
           "street musician", "perform in public"],
  roles={"performer": "I am performing", "organiser": "I am organising it"},
  steps=[
    ("act-171", ["performer", "organiser"],
     "The permit is a by-law made by the local council under this Act. DBKL, MBPJ and every other "
     "local authority licence busking separately and publish separately, so there is no national "
     "answer and none of it is on the federal portal."),
    ("act-336", ["performer"],
     "Section 27(c) is the begging provision and it is sharper than buskers expect: it catches "
     "soliciting alms whether or not there is any pretence of singing, playing or performing. "
     "The noise route is s.13, though s.13(3) lets the Chief Police Officer give permission. "
     "Whether you are performing or soliciting alms is the whole question and it gets settled "
     "on the street, not in a court. This Act reaches Peninsular Malaysia only; Sabah and "
     "Sarawak have their own."),
    ("act-574", ["performer"],
     "Section 294(b) reaches whoever, **to the annoyance of others**, sings, recites or utters "
     "any obscene song, ballad or words in or near any public place. Annoyance to somebody is "
     "part of the offence, not background, and it is the first thing to test. The maximum is "
     "three months' imprisonment, a fine, or both."),
    ("cmos", ["performer"],
     "Performing other people's songs in public is a public performance. Enforcement against "
     "buskers is rare, but the right is real and organised street programmes get asked."),
    ("act-736", ["performer", "organiser"],
     "A crowd that forms around you can be characterised as an assembly. Section 9(1) still "
     "asks an organiser to notify the police five days ahead, but the offence of not doing so, "
     "s.9(5), was struck down as unconstitutional by the Federal Court on 1 July 2025 in Amir "
     "Hariri bin Abd Hadi v Public Prosecutor. The duty survives; the criminal penalty for "
     "breaching it does not. The consolidated text we host predates that ruling and still "
     "prints the offence."),
    ("state-entertainment", ["performer", "organiser"],
     "Some states require an entertainment licence even for unamplified street performance."),
    ("fedcon", ["performer"],
     "Article 10 is the backstop when a by-law written for hawkers is turned on expression."),
  ],
  watch="This is the clearest example of the gap in every Malaysian legal resource for the arts: "
        "the operative rule is a council by-law nobody publishes centrally.",
  related=["arrested", "stage-show", "mural"]),

dict(
  id="release-track", title="Release and distribute a track",
  lede="Ownership, registration and the two separate rights in every recording.",
  segments=["music"], objectives=["ip", "socio"],
  aliases=["release", "distribute", "distribution", "spotify", "apple music", "distrokid",
           "tunecore", "single", "album", "ep", "master", "streaming", "label", "put out",
           "drop a track", "isrc", "upc"],
  roles={"artist": "I am the artist", "label": "I am the label"},
  steps=[
    ("act-332", ["artist", "label"],
     "Two rights live in every release: the composition and the sound recording, often owned by "
     "different people. Section 26 gives first ownership and s.26(2) quietly moves it for "
     "commissioned work and work made in employment. Section 27(3) is stricter than most people "
     "assume: no assignment and no licence of any kind, exclusive or not, has effect unless it "
     "is in writing. Copyright itself arises automatically on fixation with no registration, "
     "but Voluntary Notification under s.26A puts your claim on a public register and a "
     "certified extract is prima facie evidence in court."),
    ("cmos", ["artist", "label"],
     "Register with MACP as a writer and RPM as a performer, or you collect nothing from public "
     "performance and broadcast no matter how heavily you are played. If you own the master, "
     "PPM is a third registration."),
    ("act-815", ["artist", "label"],
     "The artist name and the label name. Registration gives a monopoly in the registered classes; "
     "without it you are left with passing off, which is slower and harder to prove."),
    ("berne", ["artist", "label"],
     "You are protected in every member state automatically, with no registration or formality. "
     "That is the answer to whether you need to register your copyright overseas."),
    ("wppt", ["artist"],
     "The international floor for performers' and producers' rights, and the source of the "
     "performers' rights provisions in the Copyright Act."),
    ("act-136", ["artist", "label"],
     "Splits, producer points, the distribution deal and the label agreement are all contract. "
     "Section 28 makes restraint of trade void, which weakens most exclusivity."),
    ("act-378", ["artist", "label"],
     "Stamp within thirty days of execution. Late stamping costs you the unpaid duty plus, "
     "under s.47A, RM50 or ten per cent of the deficient duty (whichever is greater) if you fix "
     "it within three months of the deadline, and RM100 or twenty per cent (whichever is "
     "greater) after that. Since 1 January 2026 most arts agreements fall in Phase 1 of the "
     "stamp duty self-assessment system, which means you assess and pay through MyTax yourself "
     "and can be audited on it afterwards. LHDN has waived certain 2026 penalties for getting "
     "the self-assessed return wrong, but that waiver does not touch late stamping, so an old "
     "unstamped agreement is still a full-penalty problem."),
    ("act-53", ["artist", "label"],
     "The increase is not the worst of it. Section 39(1)(q) disallows the whole fee as a "
     "deduction if the tax was not withheld and paid over, and you only get the deduction back "
     "by paying the tax and the ten per cent increase. On a six-figure fee that turns a "
     "five-figure problem into a six-figure one. The Director General can remit the increase "
     "for good cause under s.109(3A), but do not plan on it."),
    ("act-606", ["label"],
     "This licenses the plant, not you. Anyone manufacturing optical discs without a licence "
     "commits an offence, so check your replicator holds a current one before you place a CD or "
     "DVD order. It does not touch vinyl or cassette, which are not optical media."),
  ],
  watch="Most Malaysian artists are members of nothing. The recording can be everywhere and the "
        "public performance money stays unclaimed because no one registered the work.",
  related=["sync-licence", "management-deal", "dj-club-night"]),

dict(
  id="sync-licence", title="Licence a song for an ad, film or game",
  lede="Two permissions, usually from two different owners, and a blanket licence is neither of them.",
  segments=["music", "film", "digital"], objectives=["ip", "socio"],
  aliases=["sync", "synchronisation", "synchronization", "licence a song", "license a song",
           "ad music", "commercial", "soundtrack", "game music", "film music", "tv music",
           "master use", "publishing"],
  roles={"artist": "I own the music", "buyer": "I want to use the music"},
  steps=[
    ("act-332", ["artist", "buyer"],
     "Section 27(3) requires every licence to be in writing, exclusive or not, so a sync agreed "
     "in conversation has no effect at all."),
    ("cmos", ["buyer"],
     "A blanket public performance licence from MACP, PPM or RPM is not a sync licence and "
     "never has been. Sync is negotiated directly with the owners."),
    ("act-136", ["artist", "buyer"],
     "Term, territory, media, exclusivity and the most-negotiated clause of all: what happens on "
     "renewal."),
    ("act-378", ["artist", "buyer"],
     "Stamp within thirty days of execution. Late stamping costs you the unpaid duty plus, "
     "under s.47A, RM50 or ten per cent of the deficient duty (whichever is greater) if you fix "
     "it within three months of the deadline, and RM100 or twenty per cent (whichever is "
     "greater) after that. Since 1 January 2026 most arts agreements fall in Phase 1 of the "
     "stamp duty self-assessment system, which means you assess and pay through MyTax yourself "
     "and can be audited on it afterwards. LHDN has waived certain 2026 penalties for getting "
     "the self-assessed return wrong, but that waiver does not touch late stamping, so an old "
     "unstamped agreement is still a full-penalty problem."),
    ("act-53", ["artist", "buyer"],
     "The increase is not the worst of it. Section 39(1)(q) disallows the whole fee as a "
     "deduction if the tax was not withheld and paid over, and you only get the deduction back "
     "by paying the tax and the ten per cent increase. On a six-figure fee that turns a "
     "five-figure problem into a six-figure one. The Director General can remit the increase "
     "for good cause under s.109(3A), but do not plan on it."),
    ("act-815", ["artist"],
     "Use of your artist name in the credit or the campaign is a separate question from use of the "
     "music."),
    ("berne", ["artist"],
     "National treatment means a Malaysian work is protected in the buyer's territory without "
     "formality."),
  ],
  watch="The two-rights problem is where almost every Malaysian sync falls over: a brand clears "
        "the recording from a label and never clears the song from the writers.",
  related=["release-track", "management-deal", "brand-deal"]),

dict(
  id="documentary", title="Shoot and screen a film or documentary",
  lede="Approval is the gate, a FINAS licence is the price of admission, and possession alone "
       "is an offence.",
  segments=["film", "content"], objectives=["freedom", "ip", "socio"],
  aliases=["film", "documentary", "doc", "shoot", "shooting", "filming", "screening", "festival",
           "short film", "cinema", "feature", "crew", "production", "premiere", "director"],
  roles={"filmmaker": "I am making it", "exhibitor": "I am showing it"},
  steps=[
    ("act-620", ["filmmaker", "exhibitor"],
     "No film may be distributed, exhibited or possessed unless the Board has approved it, and "
     "s.6 catches possession, not only exhibition. Festival and gallery screenings are inside it "
     "on the Board's own reading. The Appeal Committee is the first real remedy and filmmakers "
     "barely use it."),
    ("act-244", ["filmmaker"],
     "FINAS licensing makes it an offence to carry on film production, distribution or exhibition "
     "without a licence. This is the provision that has been used against independent documentary "
     "makers and it is the most-criticised barrier to entry in Malaysian film."),
    ("act-332", ["filmmaker"],
     "Archive footage, stills, music and the interview release you did not get. Clear it before "
     "the edit lock, not after."),
    ("act-709", ["filmmaker"],
     "Filming the room means processing other people's personal data. Since 1 June 2025 you "
     "must notify the Commissioner of a personal data breach as soon as practicable and no "
     "later than 72 hours after it happens, and then tell the affected people within 7 days of "
     "notifying the Commissioner where the breach causes or is likely to cause them significant "
     "harm. Note the trigger: the 72 hours runs from the breach happening, not from you finding "
     "out about it, and if you miss it you have to give the Commissioner a written explanation "
     "with supporting evidence. There is no size threshold on that duty. The data protection "
     "officer duty is different: it only bites if you process the personal data of 20,000 or "
     "more people, the sensitive personal data of 10,000 or more, or your core activity is "
     "regular and systematic monitoring. Almost no individual artist will reach that."),
    ("act-88", ["filmmaker"],
     "A document classified as an official secret carries a mandatory custodial sentence and the "
     "Minister's certificate is conclusive as to classification, so there is no route to argue the "
     "material was innocuous."),
    ("act-286", ["filmmaker"],
     "Justification, fair comment and qualified privilege are the defences that matter to "
     "investigative work, and Malaysia has no serious-harm threshold, so the bar to suing you is low."),
    ("act-155", ["filmmaker"],
     "Foreign crew are working, not visiting."),
    ("puspal", ["filmmaker"],
     "Foreign filming needs PUSPAL clearance, and the conditions attached are administrative rather "
     "than statutory, so they change without any amendment being gazetted."),
    ("act-514", ["filmmaker"],
     "A set is a workplace. Since 1 June 2024, when the 2022 amendments came into force, the "
     "duty can reach the principal and not just the crew's direct employer, but only where the "
     "principal directs the manner in which the work is carried out. Independent of that, every "
     "employer, self-employed person and principal must now carry out a risk assessment for the "
     "place of work and act on it."),
    ("act-301", ["exhibitor"],
     "Programmes, catalogues and accompanying publications sit under a different regime again."),
  ],
  watch="** `Section 6 of the Film Censorship Act catches possession, so a finished unapproved "
        "cut sitting on your drive is already inside the offence. Do not delete it and do not "
        "hand it over. Destroying material once a complaint or a letter has arrived makes "
        "things worse, not better. Talk to someone first.",
  related=["post-set-online", "arrested", "stage-show"]),

dict(
  id="exhibit-sell-art", title="Exhibit and sell your work",
  lede="Selling the object is not selling the copyright, and the commission clause decides who "
       "owned it in the first place.",
  segments=["visual", "fashion", "museum"], objectives=["ip", "socio"],
  aliases=["exhibition", "exhibit", "gallery", "show", "art fair", "sell art", "commission",
           "commissioned", "print", "painting", "sculpture", "collector", "artwork", "consignment",
           "illustration", "illustrator", "portrait"],
  roles={"artist": "I am the artist", "gallery": "I am the gallery or buyer"},
  steps=[
    ("act-332", ["artist", "gallery"],
     "Selling the physical work is not selling the copyright, and s.25 moral rights survive the "
     "sale. The trap is s.26(2): commissioned work and work made in the course of employment moves "
     "ownership unless you contract out of it, and almost nobody does."),
    ("act-136", ["artist", "gallery"],
     "Consignment, commission percentage, insurance while held, and what happens when the gallery "
     "closes owing you for sold work."),
    ("act-552", ["artist"],
     "If you industrially produce and market articles made to your own artistic work, section "
     "13B limits copyright in that work to twenty-five years from the end of the year the "
     "articles are first marketed. And if the design is registered under industrial design law, "
     "section 7(5) removes copyright in it altogether. Registration under this Act is the "
     "protection designers are meant to be relying on, and they fall into this gap constantly."),
    ("act-599", ["artist", "gallery"],
     "You are a seller. Implied guarantees, misleading conduct and the Tribunal for Consumer Claims "
     "all apply, and the Tribunal is cheap enough to be used against you."),
    ("act-378", ["artist", "gallery"],
     "Stamp within thirty days of execution. Late stamping costs you the unpaid duty plus, "
     "under s.47A, RM50 or ten per cent of the deficient duty (whichever is greater) if you fix "
     "it within three months of the deadline, and RM100 or twenty per cent (whichever is "
     "greater) after that. Since 1 January 2026 most arts agreements fall in Phase 1 of the "
     "stamp duty self-assessment system, which means you assess and pay through MyTax yourself "
     "and can be audited on it afterwards. LHDN has waived certain 2026 penalties for getting "
     "the self-assessed return wrong, but that waiver does not touch late stamping, so an old "
     "unstamped agreement is still a full-penalty problem."),
    ("act-645", ["artist", "gallery"],
     "Heritage objects can be caught on export without anyone realising they were listed, and "
     "declaration constrains what an owner may do with their own property."),
    ("act-709", ["gallery"],
     "Filming the room means processing other people's personal data. Since 1 June 2025 you "
     "must notify the Commissioner of a personal data breach as soon as practicable and no "
     "later than 72 hours after it happens, and then tell the affected people within 7 days of "
     "notifying the Commissioner where the breach causes or is likely to cause them significant "
     "harm. Note the trigger: the 72 hours runs from the breach happening, not from you finding "
     "out about it, and if you miss it you have to give the Commissioner a written explanation "
     "with supporting evidence. There is no size threshold on that duty. The data protection "
     "officer duty is different: it only bites if you process the personal data of 20,000 or "
     "more people, the sensitive personal data of 10,000 or more, or your core activity is "
     "regular and systematic monitoring. Almost no individual artist will reach that."),
    ("act-53", ["artist"],
     "** `Whether your sales are taxable business income does not depend on what you call "
     "yourself. LHDN looks at how you actually operate: how often you sell, whether you buy to "
     "resell, how you market, and how long you hold work before selling it. Lawyers call these "
     "the badges of trade."),
  ],
  watch="Section 26(2) is the clause that quietly transfers ownership of commissioned work. Read it "
        "before you accept the commission, not after you see it reprinted.",
  related=["mural", "merch-online", "archive"]),

dict(
  id="mural", title="Paint a mural or install work in public space",
  lede="Your copyright survives on someone else's wall. What the owner may then do to it is the fight.",
  segments=["visual"], objectives=["ip", "freedom", "socio"],
  aliases=["mural", "street art", "graffiti", "public art", "wall", "installation", "site specific",
           "paint a wall", "commission a mural"],
  roles={"artist": "I am the artist", "commissioner": "I commissioned it"},
  steps=[
    ("act-171", ["artist", "commissioner"],
     "Permission comes from the local authority under a by-law made under this Act, and the council "
     "can require removal. Get the permission in writing before the first coat."),
    ("act-332", ["artist", "commissioner"],
     "Copyright in the mural is yours even though the wall is not. Section 25 moral rights, "
     "including integrity, are where the argument lands when a wall is painted over or altered."),
    ("act-645", ["artist", "commissioner"],
     "On or near a declared heritage site, what may be done to the fabric is controlled and the "
     "penalty falls on whoever did it."),
    ("act-574", ["artist"],
     "Section 298A on causing religious disharmony also reaches public imagery, and it is the "
     "heaviest of these: a minimum of two years' imprisonment, with the Criminal Procedure "
     "Code's discharge and good-behaviour-bond routes expressly shut off. Raise its "
     "constitutionality early. The Supreme Court held in Mamat bin Daud v Government of "
     "Malaysia [1988] 1 MLJ 119 that s.298A is in substance a law about religion, which is a "
     "State matter, and so beyond Parliament's power. It has never been repealed and it is "
     "still charged. Note the limit of the argument: the reasoning turns on Parliament "
     "legislating for the States, so it is at its strongest outside the Federal Territories and "
     "weakest in Kuala Lumpur, Putrajaya and Labuan, where Parliament does legislate on State "
     "subjects."),
    ("act-336", ["artist"],
     "The everyday enforcement route is s.15(2), defacing property, not public nuisance, and it "
     "is heavier than people expect: up to a year inside or a fine of RM1,000. This Act reaches "
     "Peninsular Malaysia only."),
    ("act-136", ["artist", "commissioner"],
     "The commission agreement should say who owns the copyright, whether it can be altered or "
     "removed, and who is liable if the council objects."),
    ("fedcon", ["artist"],
     "Article 10 when the objection is to the content rather than the paint."),
  ],
  watch="Commissioners routinely assume that paying for a mural buys the copyright and the right to "
        "alter it. Section 26(2) may give them the first; s.25 does not give them the second.",
  related=["exhibit-sell-art", "busking", "arrested"]),

dict(
  id="publish-book", title="Publish a book or zine",
  lede="Printing needs a licence, publishing needs a permit, and the Minister can prohibit the "
       "result outright.",
  segments=["literature", "visual"], objectives=["freedom", "ip", "socio"],
  aliases=["book", "zine", "publish", "publishing", "publisher", "isbn", "print", "printing",
           "self publish", "novel", "poetry", "comic", "graphic novel", "anthology", "catalogue",
           "manuscript", "author"],
  roles={"author": "I wrote it", "publisher": "I am publishing it"},
  steps=[
    ("act-301", ["publisher", "author"],
     "The 2012 amendment did not delete s.13A, which is still headed 'Minister's decision "
     "final'. What it removed were the words that had barred any court from questioning the "
     "decision at all, along with the Minister's 'absolute discretion' over licences and "
     "permits and the twelve-month expiry that forced annual renewal. A refusal, revocation or "
     "suspension can now be taken to court on ordinary administrative law grounds. Note the "
     "limits: s.13A only ever covered licence and permit decisions, and the prohibition power "
     "in s.7(1) is still expressed to be exercisable in the Minister's absolute discretion."),
    ("act-332", ["author", "publisher"],
     "Section 27(3) requires every assignment and every licence to be in writing, exclusive or "
     "not, and a publishing deal is usually an exclusive licence. Anything you let a publisher "
     "do that is not in the written grant is not licensed."),
    ("act-286", ["author", "publisher"],
     "Memoir, reportage and anything naming a living person. Justification and fair comment are "
     "the defences; there is no serious-harm threshold here."),
    ("act-15", ["author", "publisher"],
     "Seditious tendency, with intention expressly irrelevant under s.3(3). That is what makes it "
     "dangerous to satire."),
    ("act-574", ["author", "publisher"],
     "Section 298A on causing religious disharmony also reaches public imagery, and it is the "
     "heaviest of these: a minimum of two years' imprisonment, with the Criminal Procedure "
     "Code's discharge and good-behaviour-bond routes expressly shut off. Raise its "
     "constitutionality early. The Supreme Court held in Mamat bin Daud v Government of "
     "Malaysia [1988] 1 MLJ 119 that s.298A is in substance a law about religion, which is a "
     "State matter, and so beyond Parliament's power. It has never been repealed and it is "
     "still charged. Note the limit of the argument: the reasoning turns on Parliament "
     "legislating for the States, so it is at its strongest outside the Federal Territories and "
     "weakest in Kuala Lumpur, Putrajaya and Labuan, where Parliament does legislate on State "
     "subjects."),
    ("act-378", ["author", "publisher"],
     "Stamp within thirty days of execution. Late stamping costs you the unpaid duty plus, "
     "under s.47A, RM50 or ten per cent of the deficient duty (whichever is greater) if you fix "
     "it within three months of the deadline, and RM100 or twenty per cent (whichever is "
     "greater) after that. Since 1 January 2026 most arts agreements fall in Phase 1 of the "
     "stamp duty self-assessment system, which means you assess and pay through MyTax yourself "
     "and can be audited on it afterwards. LHDN has waived certain 2026 penalties for getting "
     "the self-assessed return wrong, but that waiver does not touch late stamping, so an old "
     "unstamped agreement is still a full-penalty problem."),
    ("marrakesh", ["publisher"],
     "The basis for the accessible-format exceptions, which is the answer when a library or a "
     "reader asks."),
    ("berne", ["author"],
     "Automatic protection in every member state, no formality required."),
    ("act-53", ["author"],
     "Advances and royalties are income; the badges of trade decide the character."),
  ],
  watch="Section 7 of the Printing Presses and Publications Act is the prohibition power and it has "
        "been used against books and graphic novels. Reviewability is the remedy people forget they now have.",
  related=["exhibit-sell-art", "arrested", "archive"]),

dict(
  id="stage-show", title="Stage a play, gig or live show",
  lede="Two sets of performing rights, a venue licence, a duty on admissions, and the question of "
       "what your cast actually are.",
  segments=["performing", "music"], objectives=["socio", "ip", "freedom"],
  aliases=["theatre", "theater", "play", "stage", "production", "rehearsal", "musical", "dance",
           "show", "concert", "live show", "ticketed", "venue", "cast", "crew", "run of show"],
  roles={"producer": "I am producing", "performer": "I am performing", "venue": "I am the venue"},
  steps=[
    ("act-332", ["producer"],
     "The script and the music are separate permissions from separate owners, and a performing "
     "licence for one is not a licence for the other."),
    ("cmos", ["producer", "venue"],
     "Live and recorded music in the show engages the public performance rights administered by "
     "MACP and PPM, and the performers' remuneration collected by RPM."),
    ("act-493", ["producer", "venue"],
     "In Kuala Lumpur the venue needs an entertainment licence and the conditions attached are "
     "where content control actually happens."),
    ("state-entertainment", ["producer", "venue"],
     "Outside KL, state enactments and council by-laws, which differ."),
    ("act-103", ["producer"],
     "Entertainments duty is charged on payments for admission. Two reliefs in the Act itself "
     "are worth knowing: s.4(2) halves the rate where all the performers are actually present "
     "and performing and the bill is a stage play, ballet, music performance, lecture, "
     "recitation, variety, circus, travelling show or sport; and s.4(3)(a) exempts a stage "
     "play, ballet or traditional dance, music performance, lecture or recitation altogether "
     "where the Collector is satisfied it is put on by a non-profit society, institution or "
     "committee or that it is amateur. Note s.4(3)(b): pay any performer, instructor, producer, "
     "manager, conductor or adviser and it stops being amateur. Check which enactment applies "
     "to your state, because the collecting regime outside the Federal Territories is a state "
     "one."),
    ("act-265", ["producer", "performer"],
     "Whether the cast and crew are employees decides notice, leave, sick pay and which forum hears "
     "a complaint. Calling someone a freelancer does not make them one: control, integration and "
     "mutuality decide it."),
    ("act-872", ["performer"],
     "** `That gives your cast and crew five things. A written agreement saying what the work "
     "is, what it pays and how. Payment within seven days if the agreement does not say. No "
     "termination without a proper reason. A free meeting run by the Director General for "
     "Industrial Relations to try to settle it. And if that fails, the Gig Workers Tribunal."),
    ("act-350", ["producer"],
     "Employment connected with public entertainment is separately regulated where a child is "
     "involved, and a parental release is not the whole answer."),
    ("act-611", ["producer"],
     "The Child Act 2001 does not make a producer a mandatory reporter; that duty sits on "
     "doctors, family members and paid child care providers, and a chaperone or tutor you "
     "engage and pay is a child care provider. What reaches the producer is s.31: it is an "
     "offence for a person having the care of a child to neglect or abuse the child, or to "
     "permit it, with up to twenty years' imprisonment. Appoint a named, paid chaperone and "
     "record who had care of the child at every point."),
    ("act-514", ["producer", "venue"],
     "Rigging, get-in, get-out and crowd. Since 1 June 2024 the duty can reach the principal, "
     "not just the crew's own employer, where the principal directs how the work is done; and "
     "every principal must in any event conduct a risk assessment under s.18B."),
    ("act-840", ["producer", "performer"],
     "The Tribunal reaches conduct outside an employment relationship, which is how most theatre "
     "and music engagements are structured."),
    ("act-574", ["performer", "producer"],
     "Section 298A on causing religious disharmony also reaches public imagery, and it is the "
     "heaviest of these: a minimum of two years' imprisonment, with the Criminal Procedure "
     "Code's discharge and good-behaviour-bond routes expressly shut off. Raise its "
     "constitutionality early. The Supreme Court held in Mamat bin Daud v Government of "
     "Malaysia [1988] 1 MLJ 119 that s.298A is in substance a law about religion, which is a "
     "State matter, and so beyond Parliament's power. It has never been repealed and it is "
     "still charged. Note the limit of the argument: the reasoning turns on Parliament "
     "legislating for the States, so it is at its strongest outside the Federal Territories and "
     "weakest in Kuala Lumpur, Putrajaya and Labuan, where Parliament does legislate on State "
     "subjects."),
  ],
  watch="The employment question is upstream of everything. Get it wrong and you have also got the "
        "safety duty, the harassment forum and the tax treatment wrong.",
  related=["dj-club-night", "foreign-artist", "unpaid"]),

dict(
  id="merch-online", title="Sell merch, prints or downloads online",
  lede="The moment you take money online you are a seller, and there is a disclosure rule almost "
       "no artist store complies with.",
  segments=["fashion", "visual", "content", "music"], objectives=["socio", "ip"],
  aliases=["merch", "merchandise", "shop", "store", "online store", "tshirt", "t-shirt", "hoodie",
           "print sales", "ecommerce", "e-commerce", "shopify", "dropship", "sell online",
           "bandcamp", "etsy", "stripe", "checkout"],
  roles={"seller": "I am selling", "buyer": "I am buying"},
  steps=[
    ("act-599", ["seller", "buyer"],
     "The Consumer Protection (Electronic Trade Transactions) Regulations 2024 replaced the "
     "2012 Regulations on 25 December 2024, and the transition period ended on 24 June 2025. If "
     "you sell online you must display your name or business name, your registration number if "
     "you have one, your contact details including address, email and telephone, a description "
     "and the price of what you are selling, the payment methods, the estimated delivery terms "
     "and your returns and refund policy. The Regulations also require the information to be "
     "given in Bahasa Malaysia, with other languages allowed alongside it; KPDN suspended "
     "enforcement of that language rule in June 2025 and has not set a new date, but the rule "
     "itself has not been revoked. Most artist stores display none of this. Implied guarantees "
     "and the Tribunal for Consumer Claims apply either way, and the Tribunal can hear claims "
     "up to RM50,000."),
    ("act-815", ["seller"],
     "Your mark, and theirs. Putting someone else's logo on a shirt is the fastest route to a "
     "letter you cannot answer."),
    ("act-552", ["seller"],
     "** `File before you show it to anyone, anywhere. Once the design has been shown in "
     "public, even by you, it is no longer new and you cannot register it. There are only two "
     "exceptions, both six months: an official exhibition, or someone else leaking it without "
     "permission."),
    ("act-730", ["seller"],
     "Counterfeit merchandise carrying a registered mark is prosecuted under Part XV of the "
     "Trademarks Act 2019, not under the trade description order route, which was repealed. The "
     "Trade Descriptions Act still reaches false claims about the goods themselves, such as "
     "origin, maker or composition, and that cuts in both directions."),
    ("act-332", ["seller"],
     "Artwork, photographs and fonts on the product. The licence you bought for a font often does "
     "not cover merchandise."),
    ("act-658", ["seller", "buyer"],
     "Electronic contracts and signatures are legally effective, so your checkout terms bind."),
    ("act-709", ["seller"],
     "Filming the room means processing other people's personal data. Since 1 June 2025 you "
     "must notify the Commissioner of a personal data breach as soon as practicable and no "
     "later than 72 hours after it happens, and then tell the affected people within 7 days of "
     "notifying the Commissioner where the breach causes or is likely to cause them significant "
     "harm. Note the trigger: the 72 hours runs from the breach happening, not from you finding "
     "out about it, and if you miss it you have to give the Commissioner a written explanation "
     "with supporting evidence. There is no size threshold on that duty. The data protection "
     "officer duty is different: it only bites if you process the personal data of 20,000 or "
     "more people, the sensitive personal data of 10,000 or more, or your core activity is "
     "regular and systematic monitoring. Almost no individual artist will reach that."),
    ("act-807", ["seller"],
     "Selling physical merch is selling goods, so the tax to look at first is sales tax under "
     "the Sales Tax Act 2018, not service tax. Sales tax bites on goods manufactured here by a "
     "registered manufacturer and on imports; if you buy in finished stock and resell it you "
     "are usually outside it, and if you have goods made to order ask whether the "
     "contract-manufacture rules catch you. Service tax under the Service Tax Act 2018 only "
     "matters if you are supplying a taxable service, and the rate and the registration "
     "threshold both depend on which service it is, so check the current schedule against RMCD "
     "rather than a remembered figure."),
    ("act-777", ["seller"],
     "The vehicle you sell through, and whether you chose one at all."),
    ("act-53", ["seller"],
     "Business income, deductions, and the badges of trade."),
  ],
  watch="The e-commerce disclosure regulations are the quiet one. They are cheap to comply with and "
        "they are the first thing a complaint will point at.",
  related=["exhibit-sell-art", "brand-deal", "run-organisation"]),

dict(
  id="management-deal", title="Sign a management, label or agency deal",
  lede="** `What you assign you do not get back. And the clause that looks like a life sentence "
       "is often weaker than it reads, though that is a fight to have with advice, not a reason "
       "to walk away on your own.",
  segments=["music", "performing", "content", "literature"], objectives=["socio", "ip"],
  aliases=["contract", "management", "manager", "label deal", "agency", "sign", "signing",
           "deal", "agreement", "360 deal", "exclusive", "commission", "review my contract",
           "terms", "publishing deal", "record deal", "should i sign", "before signing",
           "band agreement", "band", "splits", "royalty split", "partnership agreement"],
  roles={"artist": "I am the artist", "counterparty": "I am the manager or label"},
  steps=[
    ("act-136", ["artist", "counterparty"],
     "Section 28 makes agreements in restraint of trade void, and there is no reasonableness "
     "discretion in Malaysia; a restraint is either outside the section or it is void. The "
     "section reaches post-term restrictions, so a clause stopping you signing elsewhere for "
     "two years after the deal ends is vulnerable. It does not reach exclusivity that only "
     "operates while the deal is running: Polygram Records v Hillary Ang upheld an in-term "
     "exclusive recording covenant against a band. A post-term commission on income from deals "
     "done during the term is a payment obligation rather than a restraint, so do not assume "
     "s.28 kills it; negotiate a sunset instead. Sections 15, 16 and 20 cover coercion, undue "
     "influence and mistake if you need to set the contract aside."),
    ("act-332", ["artist", "counterparty"],
     "Section 27(3) requires every assignment and every licence to be in writing, exclusive or "
     "not. Understand exactly what is assigned, for how long, and whether it reverts."),
    ("act-378", ["artist", "counterparty"],
     "Stamp it. Section 52 keeps an unstamped instrument out of evidence, but the proviso to "
     "s.52(1) lets the court admit it on payment of the duty and the s.47A penalty, and s.51 "
     "lets the document be impounded and stamped mid-case. So the defect is curable even at "
     "trial; it is just expensive, embarrassing and it hands the other side a delay. Stamp "
     "within thirty days of execution and none of this arises."),
    ("act-137", ["artist"],
     "Damages are often not the remedy you want. Rescission, rectification and injunctions are "
     "here, and in arts disputes what you want is usually the work back or the deal undone."),
    ("act-254", ["artist"],
     "Six years for contract, and s.29 postpones time where the claim was concealed by fraud, "
     "which is the usual argument when royalties were never reported."),
    ("act-646", ["artist", "counterparty"],
     "An arbitration clause decides where the fight happens and whether a court must stay "
     "proceedings. Most Malaysian arts contracts point at AIAC without anyone reading it."),
    ("act-177", ["artist"],
     "If you were in truth an employee rather than a contracting artist, s.20 of the Industrial "
     "Relations Act 1967 is the route: written representations to the Director General for "
     "Industrial Relations, not to the Industrial Court, within sixty days of the dismissal. "
     "There is no wage ceiling on who counts as a workman, and this route runs throughout "
     "Malaysia."),
    ("act-872", ["artist"],
     "The Gig Workers Act 2025 already names actors, film crew, singers, musicians, composers, "
     "lyricists, make-up artists, stylists, photographers and videographers in its Schedule, so "
     "those artists are covered whether or not a platform is involved. Dancers, visual artists, "
     "writers, theatre directors, stage crew and DJs are not in the Schedule, and s.110 lets "
     "the Minister add them by order. That is where ALIM should be pushing. Note too that a gig "
     "worker cannot also be an employee; the Act's definition of service agreement expressly "
     "excludes a contract of service or of employment."),
  ],
  watch="Never sign an assignment where a licence would do. An assignment moves ownership; a licence "
        "lends it back on terms and ends.",
  related=["release-track", "unpaid", "sync-licence"]),

dict(
  id="foreign-artist", title="Bring a foreign artist into Malaysia",
  lede="Two gates, one tax, and the administrative one is the constraint on your timeline.",
  segments=["music", "performing", "film"], objectives=["socio", "freedom"],
  aliases=["foreign artist", "foreign artiste", "international act", "booking", "tour", "visa",
           "work permit", "foreign dj", "foreign band", "overseas artist", "import an act",
           "professional visit pass"],
  roles={"promoter": "I am the promoter", "artist": "I am the visiting artist"},
  steps=[
    ("puspal", ["promoter", "artist"],
     "PUSPAL clearance comes before the immigration pass, and it is administered by the "
     "Ministry of Communications through the ePUSPAL system. Two things about the sequence "
     "catch promoters out. First, PUSPAL will not release the approval letter until the "
     "withholding tax on the artist's fee has been paid, so the tax is a gate on the clearance, "
     "not a problem for later. Second, its dress and conduct conditions are a live artistic "
     "freedom issue that appears in no statute and changes without any amendment being "
     "gazetted, so check the current guidance rather than last year's."),
    ("act-155", ["promoter", "artist"],
     "A performance is work. The correct route is a Professional Visit Pass; a social visit pass is "
     "the wrong pass and the liability reaches the person who engaged them."),
    ("act-53", ["promoter"],
     "Book a non-resident DJ and the withholding under s.109A is yours, not the artist's. The "
     "rate is 15 per cent of the gross under Part II of Schedule 1, you deduct on paying or "
     "crediting and you must account for it and pay it to the Director General within one "
     "month. Miss it and s.109(2) adds a further 10 per cent and makes the whole thing a debt "
     "payable forthwith. If you book through a company the debt is the company's, but s.75A "
     "makes any director who controls twenty per cent or more of the shares jointly and "
     "severally liable for it, which in a two-person promoter company is everybody."),
    ("act-493", ["promoter"],
     "The venue's entertainment licence and its conditions."),
    ("state-entertainment", ["promoter"],
     "Outside KL, the state enactment, and in Sabah and Sarawak a separate immigration control on top."),
    ("act-103", ["promoter"],
     "Entertainments duty on the admissions."),
    ("act-136", ["promoter", "artist"],
     "The booking agreement, the rider, the cancellation terms and who carries the visa risk."),
    ("act-514", ["promoter"],
     "Production safety, with the duty reaching you as principal."),
  ],
  watch="Budget the withholding into the fee from the first email. Renegotiating 15 per cent after "
        "the artist has agreed a net figure is where these deals die.",
  related=["dj-club-night", "stage-show", "documentary"]),

dict(
  id="brand-deal", title="Take a brand deal as a creator",
  lede="Advertising standards reach you personally, and the brand's terms usually take the copyright "
       "in what you made.",
  segments=["content", "digital", "fashion"], objectives=["socio", "ip", "freedom"],
  aliases=["brand deal", "sponsorship", "sponsored", "influencer", "ugc", "paid partnership",
           "endorsement", "affiliate", "collab", "collaboration", "advertorial", "kol"],
  roles={"creator": "I am the creator", "brand": "I am the brand or agency"},
  steps=[
    ("act-599", ["creator", "brand"],
     "Misleading conduct and false representation reach an endorsement. Saying you use something "
     "you do not is inside this Act, not just inside a platform policy."),
    ("cmcf-content-code", ["creator", "brand"],
     "The advertising parts of the Content Code apply to this work, and under s.98(2) of the "
     "Communications and Multimedia Act compliance with the registered Code is a defence to any "
     "prosecution or proceeding about a matter the Code covers. Check first whether you are a "
     "person subject to the Code; the defence is expressed to run only to those who are.\" ---"),
    ("act-332", ["creator", "brand"],
     "Who owns the content you made. The brand's standard terms usually take it outright, when a "
     "licence limited by term, territory and media would do."),
    ("act-136", ["creator", "brand"],
     "Usage period, exclusivity, approvals, kill fee and whitelisting. Category exclusivity "
     "that runs only for the campaign term is ordinarily enforceable; it is the tail after the "
     "campaign ends that s.28 of the Contracts Act attacks, so price the tail or cut it."),
    ("act-588", ["creator"],
     "What you post in the campaign is still inside s.233."),
    ("act-866", ["creator"],
     "Platform duties mean a campaign can be removed without anyone charging anyone."),
    ("act-815", ["creator", "brand"],
     "Your handle and your name as marks, and their marks in your content."),
    ("act-709", ["creator", "brand"],
     "Filming the room means processing other people's personal data. Since 1 June 2025 you "
     "must notify the Commissioner of a personal data breach as soon as practicable and no "
     "later than 72 hours after it happens, and then tell the affected people within 7 days of "
     "notifying the Commissioner where the breach causes or is likely to cause them significant "
     "harm. Note the trigger: the 72 hours runs from the breach happening, not from you finding "
     "out about it, and if you miss it you have to give the Commissioner a written explanation "
     "with supporting evidence. There is no size threshold on that duty. The data protection "
     "officer duty is different: it only bites if you process the personal data of 20,000 or "
     "more people, the sensitive personal data of 10,000 or more, or your core activity is "
     "regular and systematic monitoring. Almost no individual artist will reach that."),
    ("act-872", ["creator"],
     "** `If you are shooting stills or video, the Gig Workers Act 2025 names photographers and "
     "videographers in its Schedule. That makes the brand the one on the hook, so the "
     "protections apply to you directly. No agency or platform needs to be involved."),
    ("act-53", ["creator"],
     "Payment in kind is still income. Gifted product has a value."),
  ],
  watch="Read the intellectual property clause before the fee. A perpetual worldwide assignment for "
        "a one-month campaign is the standard opening position and it is negotiable.",
  related=["post-set-online", "merch-online", "management-deal"]),

dict(
  id="run-organisation", title="Run an arts organisation or collective",
  lede="A collective that never chose a vehicle is already a partnership, with liabilities it never "
       "agreed to.",
  segments=["others", "visual", "performing", "museum"], objectives=["socio", "freedom"],
  aliases=["ngo", "non profit", "nonprofit", "collective", "society", "company", "clbg",
           "organisation", "organization", "register", "incorporate", "funding", "grant",
           "committee", "board", "constitution", "ssm", "ros"],
  roles={"founder": "I am setting it up", "officer": "I run it"},
  steps=[
    ("act-135", ["founder", "officer"],
     "Bands, collectives and studios that never signed anything are partnerships by operation of "
     "law, with joint and several liability and a default equal profit split they never agreed to. "
     "Section 26 arrives uninvited in most band disputes."),
    ("act-777", ["founder"],
     "Section 45 company limited by guarantee is the non-profit form. It needs the Minister's "
     "licence to drop 'Berhad' and it cannot pay dividends; that is the trade-off for the "
     "charitable shape."),
    ("act-832", ["founder"],
     "A registered society is cheaper and faster, but the Registrar has wide powers over "
     "registration, rules and dissolution, which is a live freedom of association issue for "
     "politically engaged arts groups."),
    ("act-743", ["founder"],
     "The limited liability partnership is the practical middle form for a small studio or "
     "production partnership."),
    ("act-200", ["officer"],
     "If you are appealing to the public for money door to door, or soliciting in a street or "
     "other public place, that is a 'collection' under the House to House and Street "
     "Collections Act 1947 and it needs a licence from the Chief Police Officer for the area, "
     "or the Inspector-General across Peninsular Malaysia. Promoting an unlicensed collection "
     "carries a fine up to RM5,000 or two years' imprisonment or both. Selling tickets to a "
     "benefit gig is not a collection and neither is an online crowdfunder, but passing a "
     "bucket at a public event is exactly what the Act is aimed at. The machinery in the Act is "
     "Peninsular; check your state position in Sabah and Sarawak."),
    ("act-265", ["officer"],
     "** `Since 1 January 2023 the Employment Act covers anyone employed under a contract of "
     "service, whatever they are paid. If they earn more than RM4,000 a month, most of it still "
     "applies. Only five things drop away: the overtime rate, rest day pay, public holiday pay, "
     "shift allowance and termination benefits."),
    ("act-514", ["officer"],
     "As an occupier and a principal."),
    ("act-840", ["officer"],
     "A complaints route now exists that does not depend on an employment relationship. Have a "
     "policy before you need one."),
    ("act-709", ["officer"],
     "Filming the room means processing other people's personal data. Since 1 June 2025 you "
     "must notify the Commissioner of a personal data breach as soon as practicable and no "
     "later than 72 hours after it happens, and then tell the affected people within 7 days of "
     "notifying the Commissioner where the breach causes or is likely to cause them significant "
     "harm. Note the trigger: the 72 hours runs from the breach happening, not from you finding "
     "out about it, and if you miss it you have to give the Commissioner a written explanation "
     "with supporting evidence. There is no size threshold on that duty. The data protection "
     "officer duty is different: it only bites if you process the personal data of 20,000 or "
     "more people, the sensitive personal data of 10,000 or more, or your core activity is "
     "regular and systematic monitoring. Almost no individual artist will reach that."),
    ("act-53", ["officer"],
     "Tax-exempt status is not automatic and is separate from the vehicle you chose."),
  ],
  watch="Choose the vehicle before you take the first grant. Retrofitting a CLBG around money "
        "already received is the expensive way round.",
  related=["unpaid", "merch-online", "archive"]),

dict(
  id="unpaid", title="Chase an unpaid fee or invoice",
  lede="Being owed money is common, and it is fixable more often than people expect. Where you "
       "go to get it depends on what you were on that job: employee, freelancer, gig worker or "
       "seller. Some of those routes are free and don't need a lawyer.",
  segments=["others", "music", "visual", "performing", "content", "film", "literature", "fashion"],
  objectives=["socio"],
  aliases=["unpaid", "not paid", "invoice", "late payment", "owe", "owed", "debt", "chase",
           "chasing", "wont pay", "won't pay", "will not pay", "money", "fee", "payment",
           "outstanding", "non payment", "ghosted", "client", "customer", "never paid",
           "small claims", "letter of demand", "lod", "refuses to pay", "withholding payment"],
  roles={"freelancer": "I was a freelancer", "employee": "I was an employee",
         "gig": "I worked through a platform", "seller": "I sold something"},
  steps=[
    ("act-136", ["freelancer", "seller"],
     "The contract exists even if nothing was signed: a WhatsApp thread and a delivered job is a "
     "contract. Section 74 gives compensation for loss caused by the breach."),
    ("act-872", ["gig"],
     "** `You are covered two ways. Either you took the work through a platform, or your kind "
     "of work is named in the Schedule, with no platform needed at all. The Schedule names "
     "acting, film crew, singing, playing, composing, lyric writing, make-up, hair, styling, "
     "photography and videography."),
    ("act-265", ["employee"],
     "If you were in truth an employee, the Labour Department is the cheap route: the Director "
     "General can hear a wages dispute under s.69 of the Employment Act 1955 and order payment "
     "with no cap on the amount. It is an alternative to suing, not a bar on it, so you keep "
     "the civil claim if you would rather have it. In Sabah and Sarawak the Employment Act does "
     "not apply; the equivalent route is the Labour Department under the Labour Ordinance of "
     "Sabah or of Sarawak. Labelling you a freelancer does not make you one."),
    ("act-177", ["employee"],
     "For dismissal rather than unpaid wages the route is s.20 of the Industrial Relations Act "
     "1967. You file written representations with the Director General for Industrial "
     "Relations, at the Industrial Relations Department office nearest the place you worked, "
     "within sixty days of the dismissal. You do not file at the Industrial Court. If "
     "conciliation fails the Director General must refer the case to the Industrial Court "
     "himself; since 1 January 2021 that is no longer a Ministerial discretion. Miss the sixty "
     "days and the Director General cannot entertain you at all."),
    ("act-92", ["freelancer", "seller"],
     "There is no Small Claims Act, which is why you cannot find one. The small claims procedure "
     "sits in Order 93 of the Rules of Court 2012 and runs in the Magistrates' Court under this "
     "Act. Up to RM5,000, you file on Form 198 and you appear yourself; no advocate represents "
     "either side. For most unpaid arts invoices this is the cheapest route there is. ALIM has a "
     "guide to it."),
    ("act-599", ["seller"],
     "The Tribunal for Consumer Claims is cheap and fast and does not need a lawyer. It cuts both "
     "ways: a client can use it on you."),
    ("act-378", ["freelancer", "seller"],
     "Stamp it. Section 52 keeps an unstamped instrument out of evidence, but the proviso to "
     "s.52(1) lets the court admit it on payment of the duty and the s.47A penalty, and s.51 "
     "lets the document be impounded and stamped mid-case. So the defect is curable even at "
     "trial; it is just expensive, embarrassing and it hands the other side a delay. Stamp "
     "within thirty days of execution and none of this arises."),
    ("act-254", ["freelancer", "employee", "seller"],
     "Six years for contract and tort. Section 29 postpones time where the claim was concealed by "
     "fraud, which is the argument when royalties were never reported."),
    ("act-137", ["freelancer"],
     "When money is not the remedy you want and you need the work back or the use stopped."),
    ("act-646", ["freelancer"],
     "If the agreement has an arbitration clause, that is where this goes, not to court."),
  ],
  watch="** `Work out which of the four you were before you send anything. Some of these give "
        "you a free government body that will hear the complaint for you. If you go straight to "
        "a lawyer's demand letter instead, you have paid for the expensive route when a free "
        "one was open.",
  related=["management-deal", "stage-show", "run-organisation"]),

dict(
  id="arrested", title="Stopped, raided, shut down or arrested",
  lede="This is a frightening place to be, and it usually has more give in it than it feels "
       "like. Most of these turn on a licence condition or a council by-law rather than the "
       "speech offence everyone assumes, and that changes what you can do next.",
  segments=["music", "performing", "visual", "film", "literature", "content"],
  objectives=["freedom"],
  aliases=["arrest", "arrested", "police", "raid", "raided", "remand", "bail", "shut down",
           "shutdown", "stopped", "detained", "charged", "investigation", "statement",
           "summons", "seized", "banned", "ditahan", "cancelled", "closed down", "warned",
           "complaint against me", "reported to police", "gig", "show", "event",
           "venue", "club", "performance"],
  roles={"artist": "I am the artist", "organiser": "I am the organiser"},
  steps=[
    ("fedcon", ["artist", "organiser"],
     "Article 5 on liberty and Article 10 on expression. Article 5(3) is the one that bites in the "
     "first hour: you must be told the grounds of your arrest and allowed to consult a lawyer of "
     "your choice. Every restriction below is an exercise of the Article 10(2) power, and every "
     "challenge to one starts here."),
    ("act-593", ["artist", "organiser"],
     "Section 28A is the provision to know by heart. You must be told why you are being arrested, "
     "and you may contact a relative and a lawyer and speak to that lawyer out of police hearing. "
     "Read it with s.28A(8), which lets the police delay that access where it would interfere with "
     "evidence or with arresting someone else, so a refusal can be lawful and arguing otherwise at "
     "the counter makes things worse. Section 117 is the limit on how long you can be held before "
     "a magistrate has to extend it. Ask for the grounds, ask for a lawyer, then stop talking."),
    ("act-493", ["organiser"],
     "In practice a shutdown is usually enforced through the venue's entertainment licence and its "
     "conditions, not through a speech offence. That matters, because the remedy is different."),
    ("act-171", ["organiser"],
     "Council by-laws on hours, noise and premises are the other common basis."),
    ("act-588", ["artist"],
     "Section 233 is the provision most often used over something posted."),
    ("act-574", ["artist"],
     "Section 298A on causing religious disharmony also reaches public imagery, and it is the "
     "heaviest of these: a minimum of two years' imprisonment, with the Criminal Procedure "
     "Code's discharge and good-behaviour-bond routes expressly shut off. Raise its "
     "constitutionality early. The Supreme Court held in Mamat bin Daud v Government of "
     "Malaysia [1988] 1 MLJ 119 that s.298A is in substance a law about religion, which is a "
     "State matter, and so beyond Parliament's power. It has never been repealed and it is "
     "still charged. Note the limit of the argument: the reasoning turns on Parliament "
     "legislating for the States, so it is at its strongest outside the Federal Territories and "
     "weakest in Kuala Lumpur, Putrajaya and Labuan, where Parliament does legislate on State "
     "subjects."),
    ("act-15", ["artist"],
     "** `Under this Act what you meant does not form part of the offence, so arguing that you "
     "never intended anything is not the defence people expect. That makes the exact words "
     "used, and what was actually said or shown, the ground you fight on. Do not try to work "
     "this one out alone."),
    ("act-736", ["organiser"],
     "If it was characterised as an assembly rather than a performance."),
    ("act-620", ["artist", "organiser"],
     "For anything screened, remembering that possession alone is inside s.6."),
    ("act-301", ["artist"],
     "For anything printed or published."),
    ("syariah-criminal", ["artist"],
     "For Muslim artists a state Syariah enactment runs in parallel with all of the above, and work "
     "cleared federally can still be actionable there."),
    ("act-88", ["artist"],
     "If documents are involved and the classification question arises."),
  ],
  watch="Get the exact provision cited, in writing, before you argue anything. Half of these "
        "situations turn out to be a licensing decision that is reviewable rather than an offence "
        "that has to be defended.",
  related=["busking", "documentary", "post-set-online"]),

dict(
  id="someone-used-my-work", title="Someone used your work without asking",
  lede="Before anything else, check that you own it. Most of these come apart on ownership "
       "rather than on the copying, and s.26(2) of the Copyright Act is usually why. Once "
       "that's settled, the question is whether this is infringement, passing off, or neither.",
  segments=["visual", "music", "film", "literature", "fashion", "content", "digital", "performing"],
  objectives=["ip", "socio"],
  aliases=["stolen", "stole", "copied", "copy", "took my song", "used my song", "used my work",
           "took my work", "plagiarism", "plagiarised", "plagiarized", "ripped off", "rip off",
           "infringement", "infringed", "without permission", "no credit", "uncredited",
           "reposted", "repost", "bootleg", "fake", "song", "my work", "my art", "my design",
           "someone used", "passing off", "counterfeit", "knock off", "artwork", "art",
           "design", "photo", "image", "illustration", "track", "beat", "painting"],
  roles={"owner": "I made the work", "accused": "I have been accused"},
  steps=[
    ("act-332", ["owner", "accused"],
     "Copyright arises without registration, but there is a register: Voluntary Notification "
     "under s.26A puts your claim on the Register of Copyright, and a certified extract is "
     "prima facie evidence of ownership admissible in court. If you never notified, your "
     "evidence is files, dates and drafts, and a statutory declaration of ownership under "
     "section 42."),
    ("act-815", ["owner", "accused"],
     "If what was taken is a name, a logo or a get-up rather than a work, this is trademark "
     "territory, or passing off if you never registered. Different test, different remedy."),
    ("act-552", ["owner"],
     "If it is the shape or ornament of a mass-produced article, registration under this Act is "
     "the protection. Check section 13B of the Copyright Act first: twenty-five years after "
     "articles made to the work were first marketed, the copyright you were relying on no "
     "longer stops copying."),
    ("act-136", ["owner", "accused"],
     "If there was ever a brief, a quote or a deal, the stronger claim is often breach of contract "
     "rather than infringement. It is easier to prove and the damages are easier to calculate."),
    ("act-137", ["owner"],
     "An injunction to stop the use is usually what you actually want, and damages are usually "
     "not enough. This is the Act that gives it."),
    ("cmos", ["owner"],
     "If the use is music being performed or broadcast, the practical route is usually the "
     "licensing body and its tariff rather than a claim of your own. A dispute about a "
     "licensing scheme or the terms of a licence goes to the Copyright Tribunal; your own "
     "infringement action under section 37 is not displaced by it."),
    ("act-588", ["owner"],
     "For online use, the platform takedown route, and s.233 where the use is abusive rather than "
     "commercial."),
    ("act-866", ["owner"],
     "Platform duties give a second removal route that does not need a court."),
    ("act-730", ["owner"],
     "Where the copy is being sold as goods under your registered mark, the criminal route is "
     "Part XV of the Trademarks Act 2019, enforced by the Ministry of Domestic Trade. If the "
     "falsity is about the goods rather than the mark, the Trade Descriptions Act 2011 applies "
     "instead. Both carry criminal penalties."),
    ("act-286", ["owner", "accused"],
     "If the use also misrepresents you or damages your reputation, that is a separate claim with "
     "its own defences."),
    ("act-378", ["owner"],
     "Stamp within thirty days of execution. Late stamping costs you the unpaid duty plus, "
     "under s.47A, RM50 or ten per cent of the deficient duty (whichever is greater) if you fix "
     "it within three months of the deadline, and RM100 or twenty per cent (whichever is "
     "greater) after that. Since 1 January 2026 most arts agreements fall in Phase 1 of the "
     "stamp duty self-assessment system, which means you assess and pay through MyTax yourself "
     "and can be audited on it afterwards. LHDN has waived certain 2026 penalties for getting "
     "the self-assessed return wrong, but that waiver does not touch late stamping, so an old "
     "unstamped agreement is still a full-penalty problem."),
    ("act-254", ["owner"],
     "Six years from when the cause of action accrued, which for infringement is the date of "
     "the infringing act, not the date you found out. Section 29 only postpones time where the "
     "claim is based on the other side's fraud, where they concealed the claim by fraud, or "
     "where you are seeking relief from a mistake. Simply not knowing is not enough, so "
     "date-stamp your discovery and take advice early rather than assuming the clock has not "
     "started."),
  ],
  watch="Send nothing before you have settled ownership. A letter of demand from someone who turns "
        "out not to own the work is worse than silence, and s.26(2) means that happens often.",
  related=["release-track", "sync-licence", "exhibit-sell-art"]),

dict(
  id="archive", title="Archive, conserve or exhibit heritage material",
  lede="Listing constrains the owner, export catches the unaware, and copyright outlives everyone "
       "who could give permission.",
  segments=["museum", "visual", "literature", "film"], objectives=["socio", "ip", "freedom"],
  aliases=["archive", "archiving", "museum", "heritage", "conservation", "conserve", "collection",
           "records", "artefact", "artifact", "preservation", "oral history", "digitise",
           "digitize", "repatriation"],
  roles={"archivist": "I hold the material", "researcher": "I want access"},
  steps=[
    ("act-645", ["archivist", "researcher"],
     "The National Heritage Register, declaration of sites and objects, and controls on export and "
     "alteration. Declaration constrains what an owner may do with their own property, and objects "
     "get caught on export without anyone realising they were listed."),
    ("act-629", ["archivist", "researcher"],
     "Public records, their transfer and disposal, and the access provisions. This decides what may "
     "lawfully be copied or exhibited from a public collection."),
    ("act-332", ["archivist"],
     "Term depends on what the item is. Literary, musical and artistic works run for the "
     "author's life plus fifty years. Sound recordings, films and broadcasts run fifty years "
     "from the year after publication, fixation or broadcast, with no reference to anyone's "
     "death. Most archive material is still in copyright and often has no traceable owner, so "
     "duration and first ownership are the two questions, and you must ask them per item."),
    ("act-300", ["archivist"],
     "When a non-Muslim artist dies intestate in Peninsular Malaysia or Sarawak, the "
     "Distribution Act 1958 decides who inherits the catalogue and therefore who can now give "
     "you permission; s.6 sets the shares between spouse, issue and parents. The Act does not "
     "apply in Sabah, which has its own succession law, and by s.2 it does not apply to the "
     "estate of a Muslim at all. A Muslim artist's estate is distributed under faraid, and the "
     "people who can licence the work are those named in the sijil faraid issued by the Syariah "
     "court. Establish which regime you are in before you write to anyone."),
    ("marrakesh", ["archivist"],
     "The basis for making and sharing accessible-format copies without the rightholder's permission."),
    ("act-709", ["archivist"],
     "Filming the room means processing other people's personal data. Since 1 June 2025 you "
     "must notify the Commissioner of a personal data breach as soon as practicable and no "
     "later than 72 hours after it happens, and then tell the affected people within 7 days of "
     "notifying the Commissioner where the breach causes or is likely to cause them significant "
     "harm. Note the trigger: the 72 hours runs from the breach happening, not from you finding "
     "out about it, and if you miss it you have to give the Commissioner a written explanation "
     "with supporting evidence. There is no size threshold on that duty. The data protection "
     "officer duty is different: it only bites if you process the personal data of 20,000 or "
     "more people, the sensitive personal data of 10,000 or more, or your core activity is "
     "regular and systematic monitoring. Almost no individual artist will reach that."),
    ("act-724", ["archivist"],
     "The statutory framework behind national collection acquisition and disposal."),
    ("act-88", ["researcher"],
     "Classified material, where the Minister's certificate is conclusive."),
  ],
  watch="The orphan works problem has no clean Malaysian solution. Document your diligent search "
        "before you publish, because that record is the only mitigation available.",
  related=["exhibit-sell-art", "publish-book", "documentary"]),
]
