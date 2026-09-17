"""Register of real New Zealand receiving organisations, research programmes,
and published evidence.

CONVENTION — read this before adding entries.

Every fact in `accepts`, `region` and `scale` is taken from the source in
`source_url`. Where an intake spec or commercial term is not published, the
field says so rather than carrying a plausible-looking number. This is
deliberate: these are real organisations, and inventing "min 18% dry solids"
for a named company is the kind of detail that survives into a slide deck and
then embarrasses someone.

`last_checked` is the date a human opened the source URL and confirmed the
entry. Anything older than about six months should be re-checked before a
demo — this sector reorganises constantly. The four Crown Research Institutes
merged into one entity in July 2025, and at least one company in this file has
already changed its trading name.

Fields:
  kind        processor | collector | funder | council
  accepts     material types, from the source
  intake      known constraints, or an explicit "not published"
  terms       commercial basis, or an explicit "not published"
"""

# --------------------------------------------------------------------------
# Tier 2 — organisations that can receive material
# --------------------------------------------------------------------------

APPROVED_ORGS = [
    {
        "id": "ORG-ECOGAS",
        "name": "Ecogas",
        "kind": "processor",
        "region": "Reporoa, central North Island; Christchurch facility in development",
        "accepts": (
            "Source-separated food waste from council kerbside collections and "
            "commercial and industrial food producers, for anaerobic digestion"
        ),
        "scale": (
            "Around 75,000 t/yr at Reporoa. New Zealand's first and only "
            "commercial-scale AD facility. Christchurch site planned at 100,000 t/yr"
        ),
        "intake": "Not published — source-separated feedstock, contact to confirm suitability",
        "terms": "Not published — gate fee basis, confirm directly",
        "outputs": "Biomethane injected to the national gas network, digestate biofertiliser, CO2",
        "source_url": "https://ecogas.co.nz/",
        "last_checked": None,
    },
    {
        "id": "ORG-ECOSTOCK",
        "name": "Eco Stock Supplies",
        "kind": "processor",
        "region": "Wiri, South Auckland. Collections Auckland and Waikato; transport arranged nationally",
        "accepts": (
            "Surplus and out-of-spec food from growers, manufacturers, transporters "
            "and retailers, processed into supplementary stock feed. Will de-package "
            "liquid, frozen, bulk and retail product"
        ),
        "scale": "Capacity over 200 t/day; contracts with 140+ food manufacturers and suppliers",
        "intake": (
            "REGULATED. Feed use sits under MPI rules, and the Biosecurity (Meat and "
            "Food Waste for Pigs) Regulations 2005 prohibit feeding pigs uncooked meat "
            "or food that has contacted uncooked meat. Confirm before assuming any "
            "stream is feed-eligible"
        ),
        "terms": "Not published — collection cost offset against recovered feed value",
        "outputs": "Dairy stock feed supplement; packaging recovered separately",
        "source_url": "https://www.ecostock.co.nz/",
        "last_checked": None,
    },
    {
        "id": "ORG-LIVINGEARTH",
        "name": "Living Earth",
        "kind": "processor",
        "region": "Auckland and Christchurch",
        "accepts": "Green waste, food waste and wood waste for composting",
        "scale": (
            "Describes itself as New Zealand's largest organic waste processor; "
            "over 2 million tonnes processed across roughly 30 years"
        ),
        "intake": (
            "Batches tested on and offsite for micro- and macro-contaminants, nutrient "
            "value, maturity and growth performance — contamination will be detected"
        ),
        "terms": "Not published — owned by Waste Management NZ; commercial arrangement",
        "outputs": "BioGro-certified compost and soil mixes; Toitū carbonreduce certified",
        "source_url": "https://www.livingearth.co.nz/",
        "last_checked": None,
    },
    {
        "id": "ORG-ENVIROFERT",
        "name": "Envirofert",
        "kind": "processor",
        "region": "Tuakau. Receives from Auckland, Waikato and Bay of Plenty",
        "accepts": (
            "Green waste, cropping wastes, pre-consumer and factory food waste, "
            "separated post-consumer waste. Also runs a consented industrial cleanfill"
        ),
        "scale": "One of the largest composting facilities in New Zealand",
        "intake": "Fully consented for organic waste. Does not accept small residential loads",
        "terms": "Not published — collections via approved contractors",
        "outputs": "Compost and blends for horticultural growers, farmers and landscapers",
        "source_url": "https://www.envirofert.co.nz/waste-recycling/",
        "last_checked": None,
    },
    {
        "id": "ORG-ENVIROFERT-C",
        "name": "Envirofert Central",
        "kind": "processor",
        "region": "Feilding. Serves Whanganui, Rangitīkei, Manawatū and Horowhenua",
        "accepts": (
            "Agricultural residues, pre-consumer and industrial by-products, "
            "separated post-consumer food waste, and green waste"
        ),
        "scale": "Not published",
        "intake": "Does not accept small residential or personal loads",
        "terms": "Not published",
        "outputs": "Compost for orchards, vegetable plots, pasture, maize and arable",
        "source_url": "https://www.envirofertcentral.com/",
        "last_checked": None,
    },
    {
        "id": "ORG-REVITAL",
        "name": "Revital Group",
        "kind": "processor",
        "region": "New Plymouth, Cambridge and Mount Maunganui",
        "accepts": "Organic waste for composting and vermicomposting",
        "scale": "Over 50,000 t/yr of BioGro-certified compost and vermicast produced",
        "intake": (
            "Case by case — each of the three sites accepts different quantities "
            "and different material types"
        ),
        "terms": "Not published",
        "outputs": "BioGro-certified compost and vermicast",
        "source_url": "https://revital.co.nz/",
        "last_checked": None,
    },
    {
        "id": "ORG-WORMSRUS",
        "name": "WormsRus",
        "kind": "processor",
        "region": "Auckland; in-situ systems deployable on site",
        "accepts": "Food waste for vermicomposting, including in-situ systems at the point of waste",
        "scale": (
            "Around 550 t/yr — the largest worm farm operation in New Zealand, "
            "but small next to the composters and digesters in this register"
        ),
        "intake": "Not published — small-volume operation, scale-limited",
        "terms": "Not published — an EcoStock division",
        "outputs": "Worm castings; red tiger worms sold and distributed",
        "source_url": "https://sustainable.org.nz/circular-economy-directory/solutions/eco-stock-supplies-ltd/",
        "last_checked": None,
    },
    {
        "id": "ORG-MDC",
        "name": "Marlborough District Council — solid waste",
        "kind": "council",
        "region": "Marlborough",
        "accepts": (
            "Not a receiver. Commissions and part-funds work on regional waste "
            "streams — ran a Waste Minimisation Fund-backed grape marc research "
            "project with Massey University"
        ),
        "scale": "Region produces up to 65,000 t of grape marc annually",
        "intake": "N/A",
        "terms": "Project funding via central government Waste Minimisation Fund grants",
        "outputs": "Research, consenting guidance, regional diversion targets",
        "source_url": "https://www.marlborough.govt.nz/",
        "last_checked": None,
    },
]


# --------------------------------------------------------------------------
# Tier 3 — research programmes and funders
# --------------------------------------------------------------------------

RESEARCHERS = [
    {
        "id": "RES-BPA",
        "name": "Bioresource Processing Alliance",
        "unit": "MBIE-funded; partners AgResearch, Scion, Plant & Food Research, Callaghan Innovation",
        "focus": (
            "Co-funds industry-led R&D that adds value to low-value biological "
            "by-products from forestry, marine, agricultural, horticultural, animal "
            "and microbiological streams. Exists for precisely this problem"
        ),
        "route_in": (
            "Applications must be submitted by a BPA R&D partner or a New Zealand "
            "university, not by the business directly. Contact the BPA first and they "
            "will match-make to a research group. Quarterly funding rounds"
        ),
        "terms": (
            "Projects from about $5,000 to $500,000, most under $150,000. Industry "
            "cash and in-kind co-funding expected, typically 25–50% cash"
        ),
        "source_url": "https://bioresourceprocessing.co.nz/working-with-us/",
        "last_checked": None,
    },
    {
        "id": "RES-BRI-MARC",
        "name": "Waste to Treasure — high-value products from grape marc",
        "unit": "Bragato Research Institute with University of Auckland, AUT, Scion, University of Canterbury",
        "focus": (
            "Transforming the entire grape marc stream into high-value products for "
            "food, pharmaceutical, building and fine chemical applications, and "
            "producing valorisation models transferable to other horticultural streams"
        ),
        "route_in": "Via Bragato Research Institute, Marlborough Research Centre, Blenheim",
        "terms": "Co-design approach with industry, consumer and community stakeholders",
        "source_url": "https://bri.co.nz/2025/11/14/high-value-products-derived-from-grape-marc/",
        "last_checked": None,
    },
    {
        "id": "RES-UOA-BIOPROCESS",
        "name": "Grape marc to medium-chain organic acids",
        "unit": "Chemical and Materials Engineering, University of Auckland, with Bragato Research Institute",
        "focus": (
            "Engineering bioprocesses that convert the organic-rich residue left after "
            "bioactive extraction into medium-chain organic acids such as caproic acid, "
            "for uses including stock feed"
        ),
        "route_in": "Two-year project funded through the New Zealand Wine Futures Fund; approach via BRI",
        "terms": "Not published",
        "source_url": "https://bri.co.nz/2024/08/26/turning-grape-marc-into-value/",
        "last_checked": None,
    },
    {
        "id": "RES-BSI-PINE",
        "name": "Turning pine waste into premium proteins",
        "unit": "Bioeconomy Science Institute — Drs David Hooks and Scott Knowles",
        "focus": (
            "Precision fermentation converting softwood forestry residues, normally "
            "discarded or burned, into fermentation feedstocks via chemoenzymatic "
            "methods, then into specialty proteins using engineered yeast"
        ),
        "route_in": "Five-year, $10.4m Endeavour Fund programme; approach via Bioeconomy Science Institute",
        "terms": "Publicly funded programme; industry partnership basis not published",
        "source_url": "https://www.bioeconomyscience.co.nz/",
        "last_checked": None,
    },
    {
        "id": "RES-SCION-KIWI",
        "name": "Kiwifruit waste into high-end materials",
        "unit": "Scion (now part of Bioeconomy Science Institute), with Materially Kiwi",
        "focus": (
            "Developing high-value materials from rejected kiwifruit. Working technical "
            "constraints are sugar content, flexibility and durability, and water "
            "resistance — a useful illustration that feedstock chemistry, not demand, "
            "is usually the blocker"
        ),
        "route_in": "Via Bioeconomy Science Institute or the Bioresource Processing Alliance",
        "terms": "$60,000 from the industry partner plus $180,000 from the BPA",
        "source_url": "https://www.scionresearch.com/news-and-events/news/2025-news-and-media-releases/turning-kiwifruit-waste-into-high-end-materials",
        "last_checked": None,
    },
    {
        "id": "RES-MASSEY-MARC",
        "name": "Grape marc stabilisation and reuse",
        "unit": "Massey University, commissioned by Marlborough District Council",
        "focus": (
            "Turning grape marc into a stable, reusable and marketable product. Found "
            "that marc can be ensiled and stored as silage, and that leachate can be "
            "diluted for summer irrigation"
        ),
        "route_in": "Via Massey University or Marlborough District Council solid waste team",
        "terms": "Waste Minimisation Fund grant, roughly $128,000–$170,000",
        "source_url": "https://www.rnz.co.nz/news/in-depth/440979/the-environmental-hangover-from-nz-s-winemaking",
        "last_checked": None,
    },
]


# --------------------------------------------------------------------------
# Published evidence — what is actually known, with a citation
#
# The tier 3 agent must cite one of these for every application it claims, or
# explicitly return no source. "Nobody in New Zealand has published on this"
# is a real and useful answer, and much better than a confident invention.
# --------------------------------------------------------------------------

EVIDENCE = [
    {
        "id": "EV-MARC-SILAGE",
        "claim": "Grape marc can be ensiled into silage and stored, and leachate diluted for irrigation",
        "maturity": "pilot",
        "caveat": (
            "Uncontrolled marc piles have caused serious harm in Marlborough — "
            "contaminated bores with arsenic at 20x drinking water standards, and "
            "stream loadings above raw sewage. Storage method is not optional"
        ),
        "source_url": "https://www.rnz.co.nz/news/in-depth/440979/the-environmental-hangover-from-nz-s-winemaking",
    },
    {
        "id": "EV-MARC-ETHANOL",
        "claim": "Ethanol for hand sanitiser has been produced from grape marc at trial scale, including from frozen marc",
        "maturity": "pilot",
        "caveat": "Trialled by BRI; the approach was noted as adaptable to apple and pipfruit streams",
        "source_url": "https://bri.co.nz/2022/07/29/hand-sanitiser-from-grape-marc-waste/",
    },
    {
        "id": "EV-MARC-ACIDS",
        "claim": "Post-extraction grape marc residue is a candidate feedstock for medium-chain organic acids such as caproic acid",
        "maturity": "lab only",
        "caveat": "Described as a promising but not fully explored valorisation pathway in New Zealand",
        "source_url": "https://bri.co.nz/2024/08/26/turning-grape-marc-into-value/",
    },
    {
        "id": "EV-FRUIT-AD",
        "claim": "Kiwifruit and apple residues are technically viable anaerobic digestion feedstock for biomethane, with high biodegradability",
        "maturity": "lab only",
        "caveat": (
            "Blends were designed to mitigate acidification; single-stream fruit "
            "waste acidifies. Most such residue is currently composted or landfilled "
            "for logistical rather than technical reasons"
        ),
        "source_url": "https://doi.org/10.3390/resources15030041",
    },
    {
        "id": "EV-KIWI-MATERIAL",
        "claim": "Rejected kiwifruit can be processed into a plastic-free leather alternative at pre-commercial scale",
        "maturity": "pilot",
        "caveat": (
            "High sugar content caramelises if overprocessed; long-term durability "
            "profile still being refined. A pilot factory is planned for Bay of Plenty"
        ),
        "source_url": "https://bioresourceprocessing.co.nz/case-study/kiwileather-innovations-turning-kiwifruit-waste-into-high-performance-plastic-free-vegan-leather/",
    },
    {
        "id": "EV-FOOD-FEED",
        "claim": "Surplus and out-of-spec food is processed into dairy stock feed at commercial scale in New Zealand",
        "maturity": "commercial",
        "caveat": (
            "Feed eligibility is regulated. The Biosecurity (Meat and Food Waste for "
            "Pigs) Regulations 2005 restrict feeding pigs uncooked meat or food that "
            "has contacted it"
        ),
        "source_url": "https://www.ecostock.co.nz/",
    },
    {
        "id": "EV-FOOD-AD",
        "claim": "Source-separated food waste is digested at commercial scale in New Zealand, with biomethane injected into the national gas network",
        "maturity": "commercial",
        "caveat": "Only one commercial-scale AD facility currently operating, at Reporoa — haulage distance dominates viability",
        "source_url": "https://adbioresources.org/newsroom/member-press-release-pasteurisation-plays-crucial-role-in-award-winning-new-zealand-ad-plant/",
    },
    {
        "id": "EV-PINE-PROTEIN",
        "claim": "Softwood forestry residues can be converted to fermentation feedstock and then to specialty proteins via engineered yeast",
        "maturity": "lab only",
        "caveat": "Five-year programme in progress; feedstock availability, manufacturing scale and regulatory pathway all named as open challenges",
        "source_url": "https://www.bioeconomyscience.co.nz/",
    },
    {
        "id": "EV-DIGESTATE-LAND",
        "claim": "Digestate from anaerobic digestion is used as a biofertiliser on land",
        "maturity": "commercial",
        "caveat": (
            "Regulation has historically treated all AD residues as biosolids, which "
            "constrains land application. Check the current position before assuming a route"
        ),
        "source_url": "https://www.biogas.org.nz/documents/resource/Information-Sheets/IS67_Digestate-as-Biofertiliser.pdf",
    },
]


APPROVED_ORG_IDS = {o["id"] for o in APPROVED_ORGS}
RESEARCHER_IDS = {r["id"] for r in RESEARCHERS}
EVIDENCE_IDS = {e["id"] for e in EVIDENCE}
