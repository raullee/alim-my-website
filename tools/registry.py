# -*- coding: utf-8 -*-
"""
ALIM legislation registry.

The curated list of instruments relevant to the Malaysian arts scene, mapped onto
the structure the ALIM board adopted on 20 September 2026:

  OBJECTIVES  socio | ip | freedom
  SEGMENTS    visual | music | film | performing | literature | fashion |
              digital | museum | content | others

`act` numbers are verified against the live AGC catalogue by tools/harvest.py.
Anything with kind != "federal_act" is not on LOM and is described + linked, not mirrored.
"""

OBJECTIVES = {
    "socio":   {"n": 1, "label": "Socio-economic rights",
                "blurb": "Getting paid, getting a contract, getting home safe: the law that governs "
                         "an arts career as work."},
    "ip":      {"n": 2, "label": "Intellectual property rights",
                "blurb": "Owning, licensing and enforcing what you make."},
    "freedom": {"n": 3, "label": "Artistic freedom",
                "blurb": "The law that decides what may be made, shown, published, performed "
                         "or said, and what happens when the state says no."},
}

SEGMENTS = {
    "visual":     "Visual arts",
    "music":      "Music",
    "film":       "Film & TV",
    "performing": "Performing arts",
    "literature": "Literature, writing & publishing",
    "fashion":    "Fashion & craft",
    "digital":    "Digital & media",
    "museum":     "Museum & archiving",
    "content":    "Content creation",
    "others":     "Everything else",
}

ALL = list(SEGMENTS.keys())
MAKERS = ["visual", "music", "film", "performing", "literature", "fashion", "digital", "content"]

# ---------------------------------------------------------------------------
# tier 1 = every artist should know it exists
# tier 2 = bites a specific segment or situation
# tier 3 = background / occasionally decisive
# ---------------------------------------------------------------------------

REGISTRY = [

# ============================== IP ==========================================
dict(act="332", obj=["ip"], seg=ALL, tier=1,
     why="The single most important statute for anyone who makes anything in Malaysia. It decides "
         "what counts as a protected work, who owns it first, how long it lasts, what a licence "
         "has to look like to be valid, and what you can do when someone takes it. Malaysia has "
         "no copyright registration system: protection is automatic on fixation, and the Voluntary "
         "Notification system is evidence, not title.",
     keys=["Works eligible for copyright", "Infringements",
           "Nature of copyright in literary, musical or artistic works, films and sound recordings", "Duration of copyright in literary, musical or artistic works", "First ownership of copyright",
           "Assignment, licences and testamentary disposition", "Moral rights", "Nature of performers’ right"],
     watch="Section 26(2) is the clause that quietly transfers ownership of commissioned work and "
           "work made in the course of employment. It can be contracted out of; most artists never "
           "do. Section 27 requires assignments and exclusive licences to be in writing.",
     also=["P.U. (A) 159/2012", "P.U. (A) 212/2012"]),

dict(act="815", obj=["ip"], seg=["fashion", "visual", "music", "digital", "content", "others"], tier=1,
     why="Brand names, logos, band names, label names, festival names, clothing labels. Registration "
         "gives a monopoly in the registered classes; without it you are left with passing off, which "
         "is slower and harder to prove. The 2019 Act also brought Malaysia into the Madrid Protocol, "
         "so a Malaysian mark can be extended abroad from one filing.",
     keys=["Acts amounting to infringement of registered trademark", "Absolute grounds for refusal of registration", "Relative grounds for refusal of registration",
           "Rights conferred by registered trademark", "Action for infringement",
           "Assignment, etc., of registered trademark", "Licensing of registered trademark", "Collective marks", "Certification marks"],
     watch="Replaced the Trade Marks Act 1976 (Act 175) from 27 December 2019. Non-use for three "
           "years exposes a registration to revocation."),

dict(act="552", obj=["ip"], seg=["fashion", "visual", "digital", "others"], tier=2,
     why="Protects the look of a mass-produced article: the shape of a chair, the cut and ornament of "
         "a garment, jewellery, packaging, a product's form. Registration is required, and novelty is "
         "destroyed by disclosure anywhere in the world before you file, so file before you show. "
         "There is no grace period for showing your own work; the only six-month exception is an "
         "official exhibition or a disclosure someone else made unlawfully.",
     keys=["Registrable industrial design", "Novelty", "Rights of owner are personal property",
           "Period of registration", "Infringement proceedings"],
     watch="Overlaps awkwardly with copyright. Section 7(6) of the Copyright Act, which used to do "
           "this work, has been deleted. Two provisions replace it: s.7(5) removes copyright in a "
           "design actually registered under industrial design law, and s.13B cuts copyright back "
           "to twenty-five years from the end of the year articles made to the work were first "
           "marketed, where the owner industrially exploited it. Designers routinely fall into "
           "this gap."),

dict(act="291", obj=["ip"], seg=["digital", "others", "fashion"], tier=3,
     why="Rarely the arts' first port of call, but it matters for makers who invent: instrument and "
         "pedal builders, textile and materials processes, stage and lighting rigs, and the hardware "
         "side of interactive and immersive work.",
     keys=["Patentable inventions", "Right to a patent", "Rights of owner of patent", "Duration of patent",
           "Utility innovation"],
     watch="Absolute novelty: any public disclosure, including an exhibition or a demo, before filing "
           "destroys patentability."),

dict(act="836", obj=["ip", "socio"], seg=["fashion", "visual", "others"], tier=2,
     why="The instrument for craft and heritage products tied to a place. Songket, batik, pua kumbu, "
         "Sarawak and Sabah craft traditions, regional foodstuffs. It protects a collective, "
         "place-based reputation rather than one producer's brand, which is the right shape for "
         "craft communities.",
     keys=["Grounds for refusal of registration of geographical indication", "Right to use registered "
           "geographical indication", "Right of use of producer", "Rights conferred under registered geographical indication"],
     watch="Replaced the Geographical Indications Act 2000 (Act 602) on 18 March 2022."),

dict(act="606", obj=["ip"], seg=["music", "film"], tier=3,
     why="Licensing and marking regime for the manufacture of optical discs. Legacy now, but still "
         "the live instrument for physical CD, vinyl-adjacent and DVD replication runs, and it is "
         "the statute behind piracy enforcement against pressing plants.",
     keys=["Licence to manufacture optical discs", "Optical discs to be marked with manufacturer’s code", "Maintenance of records", "Power of enforcement"]),

dict(act="730", obj=["ip", "socio"], seg=["fashion", "visual", "others"], tier=3,
     why="Makes it an offence to apply a false trade description to goods. In practice it is the "
         "consumer-protection sibling of trademark law and the route enforcement takes against "
         "counterfeit merchandise.",
     keys=["False trade description", "Offences by body corporate", "Power to enter premises and inspect and seize goods and documents"]),

# ============================ ARTISTIC FREEDOM ==============================
dict(act="FEDCON", kind="constitution", obj=["freedom", "socio"], seg=ALL, tier=1,
     short="Federal Constitution", title_en="Federal Constitution of Malaysia",
     title_bm="Perlembagaan Persekutuan",
     url="https://lom.agc.gov.my/federal-constitution.php",
     why="Article 10(1)(a) guarantees freedom of speech and expression, and Article 10(2)(a) lets "
         "Parliament restrict it on grounds including security, public order and morality. Every "
         "censorship and speech statute below is an exercise of that power, so every challenge to "
         "one starts here. Article 5 (liberty), Article 8 (equality) and Article 13 (property) do "
         "the rest of the constitutional work in arts cases.",
     keys=["Article 5 - Liberty of the person", "Article 8 - Equality",
           "Article 10 - Freedom of speech, assembly and association",
           "Article 13 - Rights to property", "Article 11 - Freedom of religion",
           "Ninth Schedule - Legislative lists"],
     watch="The Ninth Schedule is why there is no single national answer on entertainment licensing, "
           "Syariah offences or local by-laws: those sit on the State List."),

dict(act="588", obj=["freedom"], seg=["digital", "content", "music", "film", "literature", "visual"], tier=1,
     why="The statute that governs everything published online in Malaysia. Section 233 (improper use "
         "of network facilities: offensive, indecent, obscene or menacing content, and content sent "
         "with intent to annoy) is the provision most often used against artists, critics and "
         "commentators, and it was amended with heavier penalties in 2024.",
     keys=["Improper use of network facilities or network service, etc",
           "Prohibition on provision of offensive content", "Licensing of network facilities, network services and applications services", "Content Forum",
           "Applicable voluntary industry code", "General duty of licensees"],
     watch="Section 211 and s.233 are the live risk. Section 3(3) says nothing in the Act shall be "
           "construed as permitting censorship of the Internet; read it against s.233 before relying "
           "on it. The Content Code made under s.213 is the operative standard for most platforms.",
     also=["Malaysian Communications and Multimedia Content Code"]),

dict(act="866", obj=["freedom", "socio"], seg=["digital", "content", "literature", "visual"], tier=1,
     why="The newest and least-tested speech instrument. It imposes duties on licensed service "
         "providers to deal with defined harmful content, which in practice means platform takedowns "
         "rather than prosecutions. For artists the exposure is not a charge but silent removal, and "
         "removal is much harder to appeal than a charge is to defend.",
     keys=["Duty to implement measures to mitigate risk of exposure to harmful content", "Duty to establish mechanism for making priority harmful content inaccessible", "Duty to make available mechanism for reporting harmful content",
           "Power to issue directions", "Report to Commission on harmful content"],
     watch="In force from 1 January 2026. Almost no case law. Watch how 'harmful content' is read "
           "against satire, documentary and performance."),

dict(act="620", obj=["freedom"], seg=["film", "content", "digital"], tier=1,
     why="No film may be distributed, exhibited or possessed in Malaysia unless the Board of Film "
         "Censors has approved it. That includes short films, documentaries, music videos and, on "
         "the Board's own reading, material screened at festivals and in galleries. Approval is the "
         "gate; classification is the tariff.",
     keys=["Unapproved film or film-publicity material", "Decision of the Board",
           "Appeal Committee", "Submission of film for censorship", "Obscene film", "Appointment of Enforcement Officers"],
     watch="Section 6 catches possession, not just exhibition. The Appeal Committee under s.16 is "
           "the first real remedy and is chronically under-used by filmmakers.",
     also=["P.U. (A) 6/2023"]),

dict(act="244", obj=["freedom", "socio"], seg=["film", "content"], tier=2,
     short="FINAS Act 1981",
     why="Establishes FINAS and, through the licensing provisions, makes it an offence to carry on "
         "film production, distribution or exhibition without a licence. This is the provision that "
         "has been used against independent documentary makers, and it is the most-criticised "
         "barrier to entry in Malaysian film.",
     keys=["Functions of the Perbadanan", "Activity or combination of activities to be licensed", "Offence to contravene any of the provisions of this Part"],
     watch="The licensing requirement is the contested part. Track any amendment; reform has been "
           "promised repeatedly."),

dict(act="301", obj=["freedom"], seg=["literature", "visual", "content"], tier=1,
     why="Printing presses need a licence and publications need a permit, both at the Minister's "
         "absolute discretion, and the Minister may prohibit a publication outright. Zines, art "
         "books, catalogues, comics and independent presses all sit inside this Act whether or not "
         "they think of themselves as publishers.",
     keys=["Licence to use printing press", "Offence to print, import, publish, etc., newspaper without permit",
           "Undesirable publications", "Undesirable publications", "Offences"],
     watch="Section 7 is the prohibition power and has been used against books and graphic novels. "
           "The 2012 amendment removed annual renewal and the finality clause, so the Minister's "
           "decision is now judicially reviewable. That is the opening."),

dict(act="15", obj=["freedom"], seg=ALL, tier=1,
     why="Criminalises words with a seditious tendency, including bringing hatred or contempt "
         "against a ruler or government, and questioning the entrenched matters. Intent is expressly "
         "irrelevant. Performance, lyrics, stand-up, visual satire and social posts have all been "
         "charged under it.",
     keys=["Seditious tendency", "Offences", "Legal proceedings", "Legal proceedings"],
     watch="Repeal has been announced more than once and has not happened. Section 3(3) removes "
           "intention as a defence, which is what makes it so dangerous to satire."),

dict(act="286", obj=["freedom", "socio"], seg=ALL, tier=1,
     why="Cuts both ways for the arts: it is the statute used against critics, reviewers, "
         "documentary makers and commentators, and it is also the statute an artist uses when "
         "someone destroys their reputation. Justification, fair comment and qualified privilege "
         "are the defences that matter to criticism.",
     keys=["Justification", "Fair comment", "Qualified privilege of newspapers", "Apology in mitigation of damages",
           "Apology in mitigation of damages", "Limitation of privilege at elections"],
     watch="Section 8 requires notice of intention to rely on justification or fair comment in some "
           "circumstances. Malaysia has no serious-harm threshold, so the bar to suing is low."),

dict(act="574", obj=["freedom"], seg=ALL, tier=1,
     short="Penal Code",
     why="The general criminal law, and the home of the provisions most often turned on artists: "
         "obscenity (ss.292 to 294, which reach obscene objects, books, drawings and songs or "
         "recitations in public), wounding religious feelings (s.298 and s.298A), and statements "
         "conducing to public mischief (s.505).",
     keys=["Sale, etc., of obscene books, etc", "Sale, etc., of obscene objects or documents to young person",
           "Obscene songs", "Uttering words, etc., with deliberate intent to wound the religious feelings of any person",
           "Causing, etc., disharmony, disunity, or feelings of enmity, hatred or ill will on grounds of religion", "Statements conducing to public mischief",
           "Criminal intimidation", "Intentional insult with intent to provoke a breach of the peace"],
     watch="Section 294(a) reaches an obscene song, ballad or words in or near a public place. It is "
           "the busking and stand-up provision."),

dict(act="593", obj=["freedom", "socio"], seg=ALL, tier=1,
     short="Criminal Procedure Code",
     why="What is supposed to happen to you between being stopped and being charged. Section 28A "
         "is the one to know: you must be told the grounds of your arrest, and you may contact a "
         "relative and a lawyer of your choice and consult that lawyer out of hearing of the "
         "police. Section 117 governs how long you can be held before a magistrate has to extend "
         "it. The rest of the Code is the machinery of bail, search, seizure and charge.",
     keys=["Person arrested to be informed of grounds of arrest",
           "Arrest how made", "Search of place entered by person sought to be arrested",
           "Procedure when investigation cannot be completed within twenty-four hours",
           "When police may require attendance of witnesses", "Bailable and non-bailable offences"],
     watch="Read s.28A together with s.28A(8), not on its own. Subsection (8) lets the police "
           "delay your access to a lawyer where it would interfere with evidence or with the "
           "arrest of someone else, so a refusal at the counter can be lawful. Knowing only the "
           "right and not the exception is how people conclude the police are acting illegally "
           "when they are not, and it makes the situation worse. Ask for the grounds in writing, "
           "say you want a lawyer, and say nothing else."),

dict(act="336", obj=["freedom", "socio"], seg=["music", "performing", "visual"], tier=2,
     why="The busking statute. Begging and public nuisance offences here, read with local council "
         "by-laws, are how street performance is actually policed. Whether a busker is performing or "
         "soliciting alms is the whole question, and it is decided on the street.",
     keys=["Begging", "Public nuisance", "Obstruction", "Penalty"],
     watch="The real rules are municipal: DBKL, MBPJ and each local authority license busking "
           "separately under the Local Government Act 1976."),

dict(act="736", obj=["freedom"], seg=ALL, tier=2,
     why="Governs any assembly, which on the authorities' reading can include a performance, a "
         "gathering, a vigil or a participatory work in a public place. Notice requirements and "
         "prohibitions on assemblies at prohibited places are the operative parts.",
     keys=["Notification of assembly", "Restrictions and conditions",
           "Designated place of assembly", "Power to compound offences"],
     watch="The Federal Court struck down s.9(5) as unconstitutional in 2021; the notification "
           "requirement in s.9(1) survives."),

dict(act="88", obj=["freedom"], seg=["film", "literature", "content", "digital"], tier=3,
     why="Matters to documentary, investigative and archival work. A document classified as an "
         "official secret carries a mandatory custodial sentence, and the Minister's certificate is "
         "conclusive as to classification, so there is no route to argue the material was innocuous.",
     keys=["Wrongful communication, etc. of official secret", "Wrongful communication, etc. of official secret", "Penalty for making or assisting in making false declaration", "Certificate by a public officer to be conclusive evidence"]),

dict(act="563", obj=["freedom", "socio"], seg=["digital", "content"], tier=3,
     why="Unauthorised access and modification of computer material. Relevant to net art, glitch and "
         "hacking-adjacent practice, to anyone scraping or archiving, and to artists whose accounts "
         "or work are compromised.",
     keys=["Unauthorized access to computer material", "Unauthorized modification of the contents of any computer",
           "Wrongful communication", "Presumption"]),

# ============================ SOCIO-ECONOMIC ================================
dict(act="136", obj=["socio"], seg=ALL, tier=1,
     why="Every commission, gig, residency, publishing deal, sync licence and band agreement is a "
         "contract, and this is the Act that decides whether one exists, what it means and what "
         "happens when it is broken. Read with the Copyright Act for any deal touching rights.",
     keys=["Communication, acceptance and revocation of proposals", "What agreements are contracts",
           "Agreements void for uncertainty", "Agreement in restraint of trade void", "Power to set aside contract induced by undue influence",
           "“Misrepresentation”", "Contingent contracts",
           "(1) Compensation for loss or damage caused by breach of contract (2) Compensation for failure to discharge obligation resembling those created by contract", "Compensation for loss or damage",
           "Agency"],
     watch="Section 28 makes agreements in restraint of trade void, which is why most exclusivity "
           "clauses in Malaysian artist and management agreements are weaker than they look."),

dict(act="137", obj=["socio"], seg=ALL, tier=3,
     why="The remedies statute that sits behind Contracts Act claims: specific performance, "
         "injunctions, rescission and rectification. It is what you reach for when damages are not "
         "enough, which in arts disputes is often, because the thing you want is the work back or "
         "the show stopped.",
     keys=["Cases in which specific performance enforceable", "Contracts not specifically enforceable Discretion of the Court",
           "Rescission for mistake", "Principles of rectification", "Injunction when refused"]),

dict(act="265", obj=["socio"], seg=ALL, tier=1,
     why="Since the 2022 amendments took effect on 1 January 2023 the Act covers all employees "
         "regardless of wage, with some provisions capped. It matters enormously to arts workers "
         "because the line between employee and freelancer decides whether any of it applies: "
         "notice, leave, maternity, paternity, sick pay, and the right to complain to the Labour "
         "Department instead of suing.",
     keys=["Contracts of service not to restrict rights of employees to join, participate in or organize trade unions", "Time of payment of wages", "Rest day", "Hours of work and working at night", "Annual leave",
           "Sick leave", "Length of eligible period and entitlement to maternity allowance", "Paternity leave",
           "Termination, lay-off and retirement benefits", "Discrimination in employment",
           "Flexible working arrangement", "Inquiry into complaints of sexual harassment"],
     watch="Labelling someone a freelancer does not make them one. Control, integration and mutuality "
           "decide it, and the Labour Court looks at substance."),

dict(act="872", obj=["socio"], seg=ALL, tier=1,
     why="The first Malaysian statute written for people who are not employees, and in large part "
         "an arts statute. Its Schedule names the work directly: acting, film production crew, "
         "singers, musicians, composers, lyricists, make-up artists, hair stylists, stylists, "
         "interpreters, translators, transcribers, journalists, stringers, photographers and "
         "videographers. If that is what you do, you are a gig worker under this Act whether or "
         "not a platform is involved. It gives you a written service agreement, payment within "
         "seven days where the agreement is silent, no termination without just cause, free "
         "conciliation before the Director General for Industrial Relations, and a Tribunal.",
     keys=["Service agreement", "Rights of gig worker", "Deactivation under service agreement, etc",
           "Rights of gig worker", "Conciliation proceedings", "Jurisdiction and power of Tribunal",
           "Matters to be decided by Tribunal under Self-Employment Social Security"],
   watch="Two things the page cannot show you. First, s.33 gives the Tribunal power to make "
           "any award it thinks just and appropriate, including consequential loss, with no "
           "monetary ceiling written into it; small claims stops dead at RM5,000. Second, "
           "s.36(3) bars advocates and solicitors from appearing at all, but s.36(2)(b) lets a "
           "gig worker be represented by an official of a gig workers' association or by a "
           "family member. A gig workers' association means one registered under the Societies "
           "Act 1966, so a company limited by guarantee cannot be one. You have to reach the "
           "Tribunal through conciliation first; you cannot file there directly.",
     also=["P.U. (A) 143/2026", "P.U. (A) 144/2026", "P.U. (A) 146/2026"],
     internal="/resources/gig-workers-act-2025/"),

dict(act="789", obj=["socio"], seg=ALL, tier=1,
     why="The self-employed social security scheme administered by PERKESO. This is the only "
         "realistic injury and disability cover for a freelance artist, and contribution is the "
         "difference between a broken wrist being an inconvenience and being the end of a career.",
     keys=["Self-employed insured person who has more than one contribution", "Registration and contribution", "Self-employment injury",
           "Permanent disablement benefit", "Dependants' benefit", "Medical benefit"],
     watch="Coverage is by declared sector under the First Schedule; check that the artist's activity "
           "is a listed self-employment before assuming cover."),

dict(act="4", obj=["socio"], seg=ALL, tier=2,
     why="SOCSO for employees. Relevant to arts organisations, venues, galleries and production "
         "companies as employers, and to any artist who is in truth an employee.",
     keys=["Disablement benefit", "Contributions", "Disablement benefit",
           "Invalidity pension", "Benefits"]),

dict(act="452", obj=["socio"], seg=ALL, tier=2,
     why="EPF. The 2024 introduction of voluntary contribution routes for the self-employed made "
         "this newly relevant to freelance artists, who otherwise reach fifty with no retirement "
         "asset but a catalogue.",
     keys=["Rate of contributions", "Payment for withdrawal", "Rate of contributions", "Offences by body corporate"]),

dict(act="177", obj=["socio"], seg=ALL, tier=2,
     why="Unfair dismissal. Section 20 is the route for an arts worker dismissed without just cause "
         "or excuse, and the claim goes to the Industrial Court, not the civil courts. It also "
         "governs recognition of trade unions, which matters if arts workers ever organise.",
     keys=["Representations on dismissals", "Reference of complaint to Industrial Court", "Recognition of trade "
           "unions", "Collective agreements", "Trade disputes"],
     watch="Sixty days from dismissal to file under s.20. Miss it and the claim is gone."),

dict(act="262", obj=["socio"], seg=ALL, tier=3,
     why="Registration and regulation of trade unions. The statute any future arts or performers' "
         "union or guild would have to be built inside.",
     keys=["Necessity for registration", "Liability in contract", "Membership of trade union",
           "Application of funds"]),

dict(act="840", obj=["socio"], seg=ALL, tier=1,
     why="Creates a Tribunal for Anti-Sexual Harassment open to complaints outside the employment "
         "relationship. For the arts that is decisive: the harm in this sector usually happens "
         "between a freelancer and a gatekeeper who is not their employer, which left the Employment "
         "Act route unavailable.",
     keys=["Establishment of Tribunal", "Notice of complaint of sexual harassment",
           "Exclusion of jurisdiction of court", "Award of Tribunal", "Criminal penalty for failure to comply with award"],
     watch="Remedies are an apology, compensation up to the statutory cap and a fine. It is not a "
           "criminal route; the Penal Code remains separate."),

dict(act="514", obj=["socio"], seg=["performing", "film", "music", "visual"], tier=2,
     why="Applies to every workplace, which includes a set, a stage, a rigging plot, a workshop and "
         "a studio. The 2022 amendments extended coverage and made it an offence for a principal to "
         "ignore the safety of contractors' workers, which is how most crew are engaged.",
     keys=["General duties of employers", "General duties of employees at work", "Safety and health officer",
           "Duty to conduct and implement risk assessment", "Notification of accidents, dangerous occurrence, occupational poisoning and occupational diseases, and inquiry", "Functions of safety and health committee"],
     watch="Duties now reach the principal, not just the direct employer. Producers cannot "
           "subcontract the risk away."),

dict(act="611", obj=["socio"], seg=["film", "performing", "music", "content"], tier=2,
     why="Child performers. Anyone casting, filming or staging a child, and anyone putting a child on "
         "a channel, is inside this Act. It also carries the reporting duties that apply if a child "
         "on a production is at risk.",
     keys=["Meaning of child in need of care and protection", "Duty of member of the family", "Offences",
           "Court For Children may order placement detention, etc., to extend beyond the date child attains the age of eighteen years"]),

dict(act="350", obj=["socio"], seg=["film", "performing", "music", "content"], tier=2,
     why="The specific permission regime for employing children and young persons, including in "
         "public entertainment. A child's appearance in a film, show or paid performance needs to be "
         "squared with this Act, and the parent's consent is not the whole answer.",
     keys=["Employment connected with public entertainment", "Employment in which children and young persons may be engaged",
           "Hours of work of children", "Penalty"],
     watch="Public entertainment is separately regulated here; do not rely on a parental release "
           "alone for a paid child performer."),

dict(act="599", obj=["socio"], seg=["fashion", "visual", "music", "content", "others"], tier=2,
     why="Applies to artists as sellers, which any merch table, print drop or online store makes you. "
         "The e-commerce regulations impose mandatory disclosure of identity and terms on an online "
         "seller, and the Tribunal for Consumer Claims is a cheap route both for and against you.",
     keys=["Misleading conduct", "False representation and other misleading conduct in relation to land", "Implied guarantee as to acceptable quality",
           "Right of redress", "Establishment of the Tribunal for Consumer Claims"],
     watch="The Consumer Protection (Electronic Trade Transactions) Regulations 2012 require an "
           "online seller to display name, registration number and address. Most artist stores do not."),

dict(act="658", obj=["socio"], seg=ALL, tier=3,
     why="Makes electronic contracts, signatures and records legally effective. This is the answer "
         "to whether a deal done over WhatsApp or a licence signed with a typed name is binding: "
         "usually yes.",
     keys=["Legal recognition of electronic message", "Formation and validity of contract",
           "Signature", "Retention of document"],
     watch="It does not apply to instruments that must be under seal, and it is expressly excluded "
           "for wills, trusts and powers of attorney."),

dict(act="378", obj=["socio"], seg=ALL, tier=2,
     why="Instruments have to be stamped to be admissible in evidence. An assignment of copyright, a "
         "management agreement or a commission contract that has never been stamped can be shut out "
         "of court at the worst possible moment, and the penalty for late stamping grows.",
     keys=["Instruments chargeable with duty", "Penalty for late stamping",
           "Instruments not duly stamped inadmissible in evidence", "Penalty for late stamping",
           "Adjudication and assessment as to proper stamp"],
     watch="Section 52 is the admissibility bar. It is curable by paying duty plus penalty, but only "
           "before you need the document."),

dict(act="53", obj=["socio"], seg=ALL, tier=2,
     why="Two provisions dominate arts practice. Section 4 and the badges of trade decide whether an "
         "artist's income is taxable business income. Section 109A imposes a 15 per cent withholding "
         "on payments to non-resident public entertainers, which is the rule that catches every "
         "promoter booking a foreign act and every Malaysian act performing abroad.",
     keys=["Classes of income on which tax is chargeable", "Classes of income on which tax is chargeable", "Deductions not allowed",
           "Application of sections 109 and 110 to income derived by a public entertainer",
           "Deduction of tax from interest or royalty in certain cases", "Double taxation arrangements"],
     watch="Section 109A withholding is the promoter's liability, not the artist's, and failure to "
           "deduct makes the promoter personally liable plus a 10 per cent increase."),

dict(act="807", obj=["socio"], seg=ALL, tier=3,
     why="Service tax reaches a number of arts-adjacent supplies once the registration threshold is "
         "crossed, and the scope has been widened repeatedly, most recently in 2025. Relevant to "
         "agencies, venues, production services and digital services.",
     keys=["Imposition and scope of service tax", "Application for registration", "Taxable service", "Imported taxable services"],
     watch="Thresholds and the taxable-services list change by order almost every year. Check the "
           "current First Schedule, not a remembered figure."),

dict(act="155", obj=["socio"], seg=ALL, tier=2,
     why="Foreign artists performing in Malaysia and Malaysian artists hosting them. A performance is "
         "work, so a social visit pass is the wrong pass, and the correct route is a Professional "
         "Visit Pass with PUSPAL clearance for foreign performers.",
     keys=["Entry into or departure from Malaysia", "Director General’s power to prohibit entry, or cancel any Pass or Permit", "Prohibited immigrants", "Offences",
           "Employing a person who is not in possession of a valid Pass"],
     watch="PUSPAL approval is a separate administrative gate under the Ministry of Communications "
           "and is usually the binding constraint on timelines, not the pass itself.",
     also=["PUSPAL"]),

dict(act="709", obj=["socio", "freedom"], seg=["digital", "content", "museum", "others"], tier=2,
     why="Applies to anyone processing personal data commercially: a mailing list, a ticketing "
         "database, a gallery's collector records, an archive of interviews, a documentary's release "
         "forms. The 2024 amendments added mandatory breach notification and a data protection "
         "officer requirement, both in force in 2025.",
     keys=["General Principle", "Notice and Choice Principle", "Disclosure Principle",
           "Security Principle", "Retention Principle", "Data Integrity Principle",
           "Access Principle", "Non-compliance with code of practice", "Compliance with data access request",
           "Right of access to personal data"],
     watch="Breach notification and the DPO obligation are new and are being enforced. Most arts "
           "organisations have neither."),

dict(act="254", obj=["socio"], seg=ALL, tier=3,
     why="Six years for contract and tort. Unpaid invoices, unaccounted royalties and infringement "
         "claims all die on this clock, and arts disputes are slow to surface because the artist "
         "finds out late.",
     keys=["Had masa tindakan mengenai kontrak dan tort dan tindakan lain yang tertentu", "Hak tindakan terakru dalam hal penyewaan tertentu",
           "Pelanjutan tempoh had masa dalam hal ketidakupayaan", "Penangguhan tempoh had masa dalam hal fraud atau kesilapan"],
     watch="Section 29 postpones time where the claim is concealed by fraud, which is the usual "
           "argument when royalties were never reported."),

dict(act="646", obj=["socio"], seg=ALL, tier=3,
     why="Most arts contracts that contain a dispute clause point at AIAC arbitration. This Act "
         "decides whether that clause bites, whether a court must stay proceedings, and how an award "
         "is enforced or set aside.",
     keys=["Definition and form of arbitration agreement", "Arbitration agreement and substantive claim before court", "Power of arbitral tribunal to order interim measures",
           "Application for setting aside", "Court-ordered interim measures"]),

dict(act="300", obj=["socio", "ip"], seg=ALL, tier=3,
     why="Copyright lasts fifty years past the author's death, so it is an estate asset. This Act "
         "governs intestate distribution for non-Muslims and decides who inherits a catalogue when "
         "an artist dies without a will.",
     keys=["Law regulating distribution", "Trusts in favour of issue and other classes of relatives of intestate", "Application"],
     watch="For Muslim estates, faraid under state law governs instead. Either way, an artist with "
           "a catalogue and no will leaves a rights problem behind."),

# ======================= ORGANISATIONS, MUSEUMS, HERITAGE ===================
dict(act="777", obj=["socio"], seg=ALL, tier=2,
     why="The vehicle statute. Sdn Bhd for a production company or label, and the company limited by "
         "guarantee in s.45 for an arts non-profit. It is the form ALIM intends to take.",
     keys=["Types of companies", "Prohibition on companies limited by guarantee with a share capital",
           "Company limited by guarantee", "Duties and responsibilities of directors", "Register of members", "Constitution of a company"],
     watch="A CLBG needs the Minister's licence under s.45 to drop 'Berhad', and it cannot pay "
           "dividends. That is the trade-off for the charitable form."),

dict(act="832", obj=["socio", "freedom"], seg=ALL, tier=2,
     why="The other vehicle for an arts collective: a registered society. Cheaper and faster than a "
         "CLBG, but the Registrar has wide powers over registration, rules and dissolution, which is "
         "a live freedom-of-association issue for politically engaged arts groups.",
     keys=["Application for registration", "Power of the Minister to declare a society unlawful", "Powers of Registrar",
           "Cancellation and suspension", "Penalty on office-bearer, etc., of an unlawful society"],
     watch="This is the 2021 revised reprint of the Societies Act 1966 (formerly Act 335)."),

dict(act="743", obj=["socio"], seg=ALL, tier=3,
     why="The LLP is the practical middle form for a small studio, collective or production "
         "partnership: limited liability without the full compliance weight of a company.",
     keys=["Formation of limited liability partnerships", "Limited liability of partners", "Limited liability partnership agreement",
           "Registration of limited liability partnerships", "Registration of conversion"]),

dict(act="135", obj=["socio"], seg=ALL, tier=3,
     why="Bands, collectives and studios that never signed anything are usually partnerships by "
         "operation of law, with joint and several liability and default profit-sharing they never "
         "agreed to. This Act supplies the terms they did not write.",
     keys=["Definition of partnership", "Relations of partners to persons dealing with them",
           "Liability of partners", "Dissolution"],
     watch="Section 26 splits profits equally in the absence of agreement. Most band disputes are "
           "this section arriving uninvited."),

dict(act="200", obj=["socio"], seg=ALL, tier=3,
     why="Public fundraising, street collections and house-to-house appeals need a licence. Relevant "
         "to benefit gigs, community arts fundraising and any collection taken for a cause.",
     keys=["House to house and street collections to be licensed", "Regulations", "Penalties"]),

dict(act="645", obj=["freedom", "socio"], seg=["museum", "visual", "others"], tier=2,
     why="Heritage listing, national heritage objects, and controls on the export and alteration of "
         "heritage items. It reaches artists working with heritage material and sites, conservators, "
         "and any museum or archive acquiring or lending.",
     keys=["National Heritage Register", "Designation of heritage site",
           "Sale or disposal of heritage object", "Export of heritage object", "Conservation and preservation of National Heritage",
           "Offence"],
     watch="Declaration constrains what an owner may do with their own property, and objects can be "
           "caught on export without anyone realising they were listed."),

dict(act="629", obj=["socio"], seg=["museum", "literature", "film"], tier=2,
     why="Governs public records, their transfer to the National Archives and their disposal. Central "
         "to any archival arts practice, to researchers seeking access, and to the question of what "
         "can lawfully be copied or exhibited from a public collection.",
     keys=["Public records to be surrendered on demand", "Transfer of public records to National Archives", "Disposal of public records",
           "Access to public archives", "Functions of the Director General"]),

dict(act="724", obj=["socio", "freedom"], seg=["visual", "museum"], tier=2,
     why="Constitutes the National Art Gallery's governing board and its statutory functions. The "
         "instrument behind national collection decisions, acquisition and the public visual arts "
         "infrastructure artists deal with.",
     keys=["Establishment of the National Visual Arts Development Board", "Functions of the Board", "The Fund", "Exchange of works of visual arts"],
     watch="Repealed and replaced the National Art Gallery Act 1959 (Act 516)."),

dict(act="653", obj=["socio"], seg=["performing", "music", "visual"], tier=3,
     why="Establishes ASWARA, the national academy for arts, culture and heritage. Relevant to arts "
         "education, accreditation and the public training pipeline.",
     keys=["Establishment of the Akademi Seni Budaya dan Warisan Kebangsaan", "Powers of the Akademi", "The Board of Directors", "Students"]),

dict(act="493", obj=["freedom", "socio"], seg=["music", "performing", "film"], tier=2,
     why="The entertainment licensing statute for the Federal Territory of Kuala Lumpur. A public "
         "performance, a gig, a club night or a ticketed show in KL needs a licence under it, and "
         "the conditions attached are where content control actually happens in live music.",
     keys=["Requirement for licence", "Revocation of licence",
           "Duration of licence", "Compounding of offences"],
     watch="Outside KL the equivalent power sits in state entertainment enactments and local "
           "authority by-laws. There is no single national rule."),

dict(act="171", obj=["freedom", "socio"], seg=["music", "performing", "visual", "fashion"], tier=2,
     why="The source of local authority power to make by-laws, which is where busking permits, "
         "hawker and stall licences for craft markets, street art rules, and licensing of public "
         "places actually live. If an artist is being moved on, it is usually a by-law under this "
         "Act doing it.",
     keys=["By-laws", "Licences", "Control of public place, etc", "General power to make by-laws"],
     watch="By-laws are made per local authority and are not on the federal portal. DBKL, MBPJ and "
           "each council publish separately."),

dict(act="103", obj=["socio"], seg=["music", "performing", "film"], tier=3,
     why="Entertainments duty on paid admissions, levied at state level. It is a real line item on a "
         "ticketed show's budget and is frequently missed by first-time promoters.",
     keys=["Duty chargeable in respect of each person", "Exemption", "Penalties"],
     watch="Administered by the states, with exemption practice varying. Check the state, not the Act."),

dict(act="92", obj=["socio"], seg=ALL, tier=1,
     short="Subordinate Courts Act 1948",
     why="There is no Small Claims Act in Malaysia; people look for one and do not find it. The "
         "small claims procedure runs in the Magistrates' Court, whose civil jurisdiction comes "
         "from this Act, under Order 93 of the Rules of Court 2012. The limit is RM5,000, you file "
         "on Form 198, and you appear in person: an advocate does not represent you. For an artist "
         "owed a few thousand ringgit by a client, this is usually the cheapest and fastest route "
         "there is, and it is the one most people never hear about.",
     keys=["Civil jurisdiction of Magistrates' Court", "Sessions Court civil jurisdiction",
           "Jurisdiction of Magistrates' Courts", "Transfer of proceedings"],
     watch="The no-lawyer rule cuts both ways. It is what makes small claims cheap, and it is why "
           "you cannot bring counsel if the other side turns up well prepared. Above RM5,000 you "
           "are out of it and into an ordinary Magistrates' or Sessions Court claim, so think "
           "before you round a RM5,400 invoice up rather than down.",
     internal="/small-claim-drafter/"),

dict(act="91", obj=["socio"], seg=ALL, tier=3,
     why="Which court, what it can order, and what can be appealed. Background, but it decides "
         "whether a claim is worth bringing at all.",
     keys=["Jurisdiction of the High Court", "Appeals to the Court of Appeal",
           "Powers of the Federal Court"]),

dict(act="67", obj=["socio"], seg=ALL, tier=3,
     why="Imports English common law and equity where there is no local statute, which is how "
         "passing off, breach of confidence and much of the law an artist relies on got here.",
     keys=["Application of U.K. common law, rules of equity and statutes", "Damages in respect of personal injury",
           "Power of Courts to award interest on debts and damages"]),

# ================= NOT ON LOM: described and linked, not mirrored ===========
dict(kind="industry_code", id="cmcf-content-code",
     short="Content Code", title_en="Malaysian Communications and Multimedia Content Code",
     issuer="Communications and Multimedia Content Forum of Malaysia (CMCF)",
     url="https://www.cmcf.my/content-code/",
     obj=["freedom"], seg=["film", "digital", "content", "music", "literature"], tier=1,
     why="Registered under s.213 of the Communications and Multimedia Act 1998, so compliance is a "
         "defence and it is the operative standard applied to online and broadcast content in "
         "Malaysia. In day-to-day terms it does more work than the Act itself: it is what platforms, "
         "broadcasters and advertisers actually apply when they decide whether your work goes out.",
     keys=["Part 2 - General prohibitions", "Indecent content", "Obscene content",
           "Violence", "Bad language", "Advertising", "Complaints procedure"],
     watch="Not on the AGC portal because it is an industry code, not legislation. That is exactly "
           "the gap this library exists to close."),

dict(kind="guideline", id="puspal",
     short="PUSPAL", title_en="PUSPAL guidelines for foreign artistes",
     issuer="Central Agency for the Application for Filming and Performance by Foreign Artistes",
     url="https://puspal.komunikasi.gov.my/",
     obj=["freedom", "socio"], seg=["music", "performing", "film"], tier=2,
     why="Every foreign performer and every foreign film crew shooting in Malaysia needs PUSPAL "
         "clearance before the immigration pass issues. The guidelines also carry the dress and "
         "conduct conditions imposed on foreign acts, which are a live artistic-freedom issue and "
         "are not found in any statute.",
     keys=["Application timelines", "Supporting documents", "Conditions of approval",
           "Dress and conduct guidelines"],
     watch="Administrative, not statutory. Conditions change without amendment or gazetting, which is "
           "why they need to be tracked here."),

dict(kind="state_enactment", id="state-entertainment",
     short="State entertainment enactments",
     title_en="State entertainment and places of entertainment enactments and by-laws",
     obj=["freedom", "socio"], seg=["music", "performing", "film", "visual"], tier=1,
     url="https://lom.agc.gov.my/",
     why="Entertainment licensing sits on the State List, so outside Kuala Lumpur the rules that "
         "decide whether a show can happen are state enactments and local authority by-laws, none of "
         "which are on the federal portal. Selangor, Penang, Johor, Sabah and Sarawak each differ, "
         "and Sarawak and Sabah have separate immigration control on top.",
     keys=["Licensing of places of public entertainment", "Conditions and hours",
           "Local authority by-laws", "Revocation"],
     watch="This is the single largest gap in any Malaysian legal resource for the arts, including "
           "this one. Building it out state by state is a standing ALIM research task."),

dict(kind="state_enactment", id="syariah-criminal",
     short="Syariah criminal enactments",
     title_en="State Syariah criminal offences enactments",
     obj=["freedom"], seg=ALL, tier=1,
     url="https://lom.agc.gov.my/",
     why="Each state has its own Syariah criminal offences enactment, applying to Muslims, and these "
         "reach performance, dress, conduct and content. For Muslim artists they operate in parallel "
         "with everything else on this page, and a work cleared federally can still be actionable in "
         "a state Syariah court.",
     keys=["Insulting or bringing into contempt the religion of Islam",
           "Indecent acts in public place", "Khalwat", "Dress", "Offences relating to performance"],
     watch="Not federal legislation and not on the AGC portal. Jurisdictional limits are set by the "
           "Ninth Schedule and by the Syariah Courts (Criminal Jurisdiction) Act 1965 (Act 355)."),

dict(kind="treaty", id="berne",
     short="Berne Convention",
     title_en="Berne Convention for the Protection of Literary and Artistic Works",
     issuer="WIPO", url="https://www.wipo.int/treaties/en/ip/berne/",
     obj=["ip"], seg=ALL, tier=2,
     why="Malaysia acceded in 1990. Berne is why a Malaysian work is automatically protected in every "
         "other member state without registration or formality, and why a foreign work is protected "
         "here. It is the answer to 'do I need to register my copyright overseas'.",
     keys=["Article 5 - National treatment and no formalities",
           "Article 6bis - Moral rights", "Article 7 - Term of protection",
           "Article 9 - Right of reproduction"]),

dict(kind="treaty", id="wppt",
     short="WPPT", title_en="WIPO Performances and Phonograms Treaty",
     issuer="WIPO", url="https://www.wipo.int/treaties/en/ip/wppt/",
     obj=["ip"], seg=["music", "performing"], tier=2,
     why="The international floor for performers' and producers' rights, and the source of the "
         "performers' rights provisions inserted into the Copyright Act 1987. It is the basis for a "
         "performer's economic and moral rights in a fixed performance.",
     keys=["Article 5 - Moral rights of performers",
           "Article 6 - Economic rights in unfixed performances",
           "Article 15 - Right to remuneration for broadcasting and communication to the public"]),

dict(kind="treaty", id="marrakesh",
     short="Marrakesh Treaty",
     title_en="Marrakesh Treaty to Facilitate Access to Published Works for Persons Who Are Blind, "
              "Visually Impaired or Otherwise Print Disabled",
     issuer="WIPO", url="https://www.wipo.int/treaties/en/ip/marrakesh/",
     obj=["ip", "socio"], seg=["literature", "museum"], tier=3,
     why="The basis for the authorised entity exceptions in Malaysian copyright law, which let "
         "accessible-format copies be made and shared without the rightholder's permission. Relevant "
         "to publishers, libraries and any arts organisation asked about accessibility.",
     keys=["Article 4 - National law limitations and exceptions",
           "Article 5 - Cross-border exchange of accessible format copies"]),

dict(kind="collecting", id="cmos",
     short="Collecting societies",
     title_en="Malaysian collective management organisations (MACP, PPM, RPM)",
     issuer="Declared licensing bodies under the Copyright Act 1987",
     url="https://www.myipo.gov.my/",
     obj=["ip", "socio"], seg=["music", "performing"], tier=1,
     why="Public performance and broadcast of music in Malaysia is licensed through declared "
         "licensing bodies, and there is more than one because there is more than one right in a "
         "recording. MACP licenses the musical work for composers and publishers, PPM licenses the "
         "sound recording for record companies, and RPM collects the performers' equitable "
         "remuneration. A venue, festival or broadcaster needs to deal with each of them, and a "
         "songwriter or performer who is not a member collects nothing from any of them.",
     keys=["Licensing body declaration", "Tariffs", "Distribution rules",
           "Copyright Tribunal reference"],
     watch="Check that the body invoicing you currently holds a declaration before you pay. A "
           "declaration runs for two years and must be renewed, operating without one is an offence "
           "under s.27A(8), and both PRISM and MRM kept issuing invoices after losing theirs. "
           "Disputes about a licensing scheme or the terms of a licence go to the Copyright "
           "Tribunal rather than the civil courts.",
     also=["P.U. (A) 159/2012", "P.U. (A) 212/2012"]),
]

# Subsidiary legislation pulled in by `also` on the acts above.
SUBSIDIARY = {
    "P.U. (A) 159/2012": "Copyright (Licensing Body) Regulations 2012",
    "P.U. (A) 212/2012": "Copyright (Copyright Tribunal) Regulations 2012",
    "P.U. (A) 62/2022":  "Copyright (Voluntary Notification) (Amendment) Regulations 2022",
    "P.U. (A) 6/2023":   "Film Censorship (Classification of Film) Regulations 2023",
    "P.U. (A) 143/2026": "Gig Workers (Social Security) Regulations 2026",
    "P.U. (A) 144/2026": "Gig Workers (Gig Workers Tribunal) Regulations 2026",
    "P.U. (A) 145/2026": "Gig Workers (Compounding of Offences) Regulations 2026",
    "P.U. (A) 146/2026": "Gig Workers (Conciliation Proceedings) Regulations 2026",
}
