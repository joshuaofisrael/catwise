#!/usr/bin/env python3
"""Generates _src/toxic-to-cats.html (the toxic plant and household item checker).
Edit ENTRIES, set REVIEWED, run this, then python3 _build.py. Only add entries with a reputable source."""
import re, os
REVIEWED = "2026-10-08"; REVIEWED_H = "8 October 2026"
A = "https://www.aspca.org/pet-care/animal-poison-control/toxic-and-non-toxic-plants/"
C = "https://www.vet.cornell.edu/departments-centers-and-institutes/cornell-feline-health-center/health-information/feline-health-topics/"
S = {
 "FDA": ("FDA lily warning", "https://www.fda.gov/animal-veterinary/animal-health-literacy/lovely-lilies-and-curious-cats-dangerous-combination"),
 "UCD": ("UC Davis", "https://healthtopics.vetmed.ucdavis.edu/health-topics/feline/lily-toxicity-cats"),
 "CORL": ("Cornell", C + "common-cat-hazards"),
 "CORP": ("Cornell", C + "poisons"),
 "CORF": ("Cornell", C + "feeding-your-cat"),
 "PPHL": ("Pet Poison Helpline", "https://www.petpoisonhelpline.com/poison/lilies/"),
 "PPHO": ("Pet Poison Helpline", "https://www.petpoisonhelpline.com/uncategorized/essential-oils-cats/"),
 "PPHP": ("Pet Poison Helpline", "https://www.petpoisonhelpline.com/poison/potpourri-liquid/"),
 "ASPO": ("ASPCA essential oils", "https://www.aspca.org/news/essentials-essential-oils-around-pets"),
 "ASPF": ("ASPCA foods", "https://www.aspca.org/pet-care/animal-poison-control/people-foods-avoid-feeding-your-pets"),
 "ICC": ("International Cat Care", "https://icatcare.org/articles/permethrin-poisoning"),
}
def asp(slug): return ("ASPCA", A + slug)
E, T, M, N = "Emergency", "Toxic", "Caution", "Non toxic"
CALL = "<b>Call your vet or a pet poison helpline now.</b> "
# (anchor, name, also known as, group, level, explanation, [sources])
ENTRIES = [
 ("true-lilies", "True lilies: Easter, tiger, Asiatic, Stargazer and Oriental lilies", "Lilium species and hybrids, common in bouquets", "Cut flowers", E,
  "Can cause fatal kidney failure. Every part is toxic, including pollen and vase water; licking a few pollen grains off the fur can be enough. Cats are the only species known to be affected.", ["FDA", "UCD", asp("easter-lily"), "PPHL", "CORL"]),
 ("daylily", "Daylily", "Hemerocallis", "Garden plants", E, "Causes kidney failure in cats, like true lilies.", ["UCD", asp("daylily"), "FDA"]),
 ("lily-of-the-valley", "Lily of the valley", "Convallaria majalis; not a true lily", "Garden plants", E,
  "Affects the heart: irregular heartbeat, low blood pressure, disorientation, coma or seizures.", [asp("lily-valley"), "UCD"]),
 ("peace-lily", "Peace lily", "Spathiphyllum; not a true lily", "Houseplants", T,
  "Does not cause kidney failure, but causes intense mouth irritation, drooling, vomiting and difficulty swallowing.", [asp("peace-lily"), "UCD"]),
 ("calla-lily", "Calla lily", "Zantedeschia; not a true lily", "Cut flowers", T,
  "Does not cause kidney failure, but causes intense mouth irritation, drooling, vomiting and difficulty swallowing.", [asp("calla-lily"), "UCD"]),
 ("tulip", "Tulip", "bulb is most toxic", "Cut flowers", T, "Vomiting, depression, diarrhea, drooling. The bulb contains the most toxin.", [asp("tulip"), "CORL"]),
 ("daffodil", "Daffodil", "Narcissus", "Cut flowers", T, "Vomiting, drooling, diarrhea; large amounts can cause convulsions, low blood pressure, tremors and heart rhythm problems. Bulbs are the most poisonous part.", [asp("daffodil")]),
 ("hyacinth", "Hyacinth", "", "Cut flowers", T, "Intense vomiting, diarrhea (sometimes with blood), depression and tremors.", [asp("hyacinth")]),
 ("iris", "Iris", "", "Cut flowers", T, "Drooling, vomiting, lethargy, diarrhea. The rhizomes (roots) are most toxic.", [asp("iris")]),
 ("chrysanthemum", "Chrysanthemum", "mums", "Cut flowers", T, "Vomiting, diarrhea, drooling, incoordination, skin irritation.", [asp("chrysanthemum")]),
 ("amaryllis", "Amaryllis", "", "Cut flowers", T, "Vomiting, depression, diarrhea, abdominal pain, drooling, loss of appetite, tremors.", [asp("amaryllis"), "CORL"]),
 ("hydrangea", "Hydrangea", "", "Cut flowers", T, "Vomiting, depression, diarrhea.", [asp("hydrangea"), "CORL"]),
 ("carnation", "Carnation", "Dianthus", "Cut flowers", M, "Mild stomach upset and mild skin irritation.", [asp("carnation")]),
 ("sweet-william", "Sweet William", "Dianthus barbatus", "Cut flowers", M, "Mild stomach upset and mild skin irritation.", [asp("sweet-william"), "CORL"]),
 ("babys-breath", "Baby's breath", "Gypsophila", "Cut flowers", M, "Mild vomiting and diarrhea if eaten.", [asp("babys-breath"), "CORL"]),
 ("rose", "Rose", "", "Cut flowers", N, "Listed as non toxic to cats by the ASPCA. Thorns can still injure.", [asp("rose")]),
 ("golden-pothos", "Golden pothos", "devil's ivy, Epipremnum", "Houseplants", T, "Intense burning and irritation of the mouth, drooling, vomiting, difficulty swallowing.", [asp("golden-pothos")]),
 ("philodendron", "Philodendron", "including split leaf philodendron", "Houseplants", T, "Mouth pain and swelling, drooling, vomiting, difficulty swallowing.", [asp("philodendron-pertusum"), "CORL"]),
 ("dieffenbachia", "Dieffenbachia", "dumb cane", "Houseplants", T, "Intense mouth irritation, drooling, vomiting, difficulty swallowing.", [asp("dieffenbachia")]),
 ("snake-plant", "Snake plant", "mother in law's tongue, Sansevieria", "Houseplants", T, "Nausea, vomiting, diarrhea.", [asp("snake-plant")]),
 ("aloe", "Aloe", "aloe vera", "Houseplants", T, "Vomiting, lethargy, diarrhea.", [asp("aloe")]),
 ("jade-plant", "Jade plant", "Crassula", "Houseplants", T, "Vomiting, depression, incoordination.", [asp("jade-plant")]),
 ("kalanchoe", "Kalanchoe", "", "Houseplants", T, "Vomiting, diarrhea; rarely abnormal heart rhythm.", [asp("kalanchoe")]),
 ("english-ivy", "English ivy", "Hedera helix", "Houseplants", T, "Vomiting, abdominal pain, drooling, diarrhea. Leaves are more toxic than berries.", [asp("english-ivy")]),
 ("cyclamen", "Cyclamen", "", "Houseplants", T, "Drooling, vomiting, diarrhea; large amounts of the tubers can cause heart rhythm problems, seizures and death.", [asp("cyclamen")]),
 ("poinsettia", "Poinsettia", "", "Houseplants", M, "Irritates the mouth and stomach and may cause vomiting; the ASPCA says its toxicity is generally overrated.", [asp("poinsettia"), "CORL"]),
 ("spider-plant", "Spider plant", "Chlorophytum comosum", "Houseplants", N, "Listed as non toxic to cats by the ASPCA.", [asp("spider-plant")]),
 ("boston-fern", "Boston fern", "", "Houseplants", N, "Listed as non toxic to cats by the ASPCA.", [asp("boston-fern")]),
 ("african-violet", "African violet", "", "Houseplants", N, "Listed as non toxic to cats by the ASPCA.", [asp("african-violet")]),
 ("areca-palm", "Areca palm", "", "Houseplants", N, "Listed as non toxic to cats by the ASPCA.", [asp("areca-palm")]),
 ("sago-palm", "Sago palm", "cycad", "Garden plants", E, "Vomiting, bleeding problems, liver damage and liver failure; can be fatal.", [asp("sago-palm")]),
 ("foxglove", "Foxglove", "Digitalis", "Garden plants", E, "Heart rhythm problems, vomiting, diarrhea, weakness, heart failure; can be fatal.", [asp("foxglove"), "CORL"]),
 ("oleander", "Oleander", "", "Garden plants", E, "Drooling, abdominal pain, diarrhea, depression; can be fatal.", [asp("oleander")]),
 ("azalea", "Azalea", "Rhododendron", "Garden plants", E, "Vomiting, diarrhea, weakness and heart failure.", [asp("azalea")]),
 ("holly", "Holly", "", "Garden plants", T, "Vomiting, diarrhea, depression. Leaves and berries are low toxicity.", [asp("holly"), "CORL"]),
 ("mistletoe", "Mistletoe (American)", "", "Garden plants", T, "Vomiting, diarrhea; rarely low blood pressure, breathing difficulty and slow heart rate.", [asp("mistletoe-american"), "CORL"]),
 ("catnip", "Catnip", "", "Garden plants", M, "Safe for most cats in small amounts, but the ASPCA notes it can cause vomiting and diarrhea.", [asp("catnip")]),
 ("essential-oils", "Concentrated essential oils: tea tree, wintergreen, sweet birch, citrus, pine, ylang ylang, peppermint, cinnamon, pennyroyal, clove, eucalyptus", "aromatherapy oils, diffuser oils", "Essential oils and fragrance", E,
  "Cats cannot break down some compounds in essential oils well. Exposure on the skin, from walking through spills or from grooming can cause drooling, vomiting, tremors, wobbliness, breathing difficulty, low body temperature and liver failure. The ASPCA notes as few as seven or eight drops of concentrated tea tree oil can cause problems. Never apply essential oils to a cat.", ["PPHO", "ASPO"]),
 ("liquid-potpourri", "Liquid potpourri", "simmering potpourri", "Essential oils and fragrance", T, "Can cause chemical burns to the lips, tongue, gums and throat; cats are particularly sensitive.", ["PPHP", "PPHO"]),
 ("permethrin", "Dog flea and tick spot ons containing permethrin", "", "Household and medicines", E, "Highly toxic to cats: twitching, seizures and death. Use only products made for cats.", ["ICC", "CORP"]),
 ("painkillers", "Human painkillers: acetaminophen (paracetamol), ibuprofen, aspirin", "", "Household and medicines", E, "Among the most common causes of cat poisoning. Never give a human medicine unless your vet prescribes it.", ["CORP"]),
 ("antifreeze", "Antifreeze", "ethylene glycol", "Household and medicines", E, "A frequent cause of cat poisoning when spilled and licked up.", ["CORP"]),
 ("rodenticides", "Rat and mouse poison", "rodenticides", "Household and medicines", E, "A frequent cause of cat poisoning.", ["CORP"]),
 ("bleach", "Bleach and household cleaners", "", "Household and medicines", T, "Among the most frequently identified causes of cat poisoning.", ["CORP"]),
 ("lead", "Lead", "dust or chips from old paint", "Household and medicines", T, "Listed by Cornell, citing the ASPCA, among the most frequently identified causes of cat poisoning; mainly found in older homes.", ["CORP"]),
 ("onion-garlic", "Onion, garlic, chives", "including powders", "Foods", T, "Stomach upset and red blood cell damage leading to anemia; the ASPCA notes cats are more susceptible than dogs.", ["ASPF"]),
 ("chocolate-caffeine", "Chocolate, coffee, caffeine", "", "Foods", T, "Vomiting, diarrhea, abnormal heart rhythm, tremors, seizures. Darker chocolate is more dangerous.", ["ASPF", "CORP"]),
 ("grapes-raisins", "Grapes and raisins", "", "Foods", T, "Listed by Cornell among human foods that can severely harm cats.", ["CORP"]),
 ("xylitol", "Xylitol", "sugar free gum and sweets", "Foods", T, "Listed by Cornell among human foods that can severely harm cats.", ["CORP"]),
 ("alcohol-dough", "Alcohol and raw yeast dough", "", "Foods", T, "Vomiting, incoordination, breathing problems, coma; dough also releases alcohol and gas in the stomach.", ["ASPF"]),
 ("milk", "Milk and dairy", "", "Foods", M, "Many cats are lactose intolerant: diarrhea and stomach upset.", ["CORF", "ASPF"]),
]
GROUPS = ["Cut flowers", "Houseplants", "Garden plants", "Essential oils and fragrance", "Household and medicines", "Foods"]
CLS = {E: "v", T: "v", M: "m", N: "h"}
assert len({e[0] for e in ENTRIES}) == len(ENTRIES)

def src_html(keys):
    out = []
    for k in keys:
        l, u = S[k] if isinstance(k, str) else k
        out.append(f'<a href="{u}" rel="noopener">{l}</a>')
    return ", ".join(out)

rows = []
for g in GROUPS:
    rows.append(f'<tr class="grp"><th colspan="4" id="{re.sub("[^a-z]+","-",g.lower()).strip("-")}">{g}</th></tr>')
    for a, n, aka, grp, lvl, ex, src in [e for e in ENTRIES if e[3] == g]:
        call = CALL if lvl != N else ""
        q = (n + " " + aka + " " + g).lower().replace('"', "")
        rows.append(f'<tr id="{a}" data-q="{q}" data-g="{g}"><td><b>{n}</b>' + (f'<br><span class="sci">{aka}</span>' if aka else "") +
                    f'<br><a class="sci" href="#{a}">#{a}</a></td><td class="{CLS[lvl]}">{lvl}</td><td>{call}{ex}</td>'
                    f'<td>{src_html(src)}<br><span class="sci">Reviewed {REVIEWED}</span></td></tr>')
n = len(ENTRIES)
jump = " · ".join(f'<a href="#{re.sub("[^a-z]+","-",g.lower()).strip("-")}">{g}</a>' for g in GROUPS)
page = f'''title: Is This Plant or Household Item Toxic to Cats? Lily Safe Checker | MeowWise
description: Check {n} cut flowers, houseplants, garden plants, essential oils and household products for toxicity to cats. Lilies first: deadly even as pollen or vase water.
h1: Is this plant or household item toxic to cats?
label: Toxic plant and household checker
group: tool
updated: {REVIEWED}
related: blog/are-lilies-poisonous-to-cats.html, health.html, kittens.html, nutrition.html, myths.html
source: ASPCA Animal Poison Control Center: Toxic and non toxic plants list | https://www.aspca.org/pet-care/animal-poison-control/toxic-and-non-toxic-plants
source: US FDA: Lovely Lilies and Curious Cats: A Dangerous Combination | {S["FDA"][1]}
source: UC Davis School of Veterinary Medicine: Lily Toxicity in Cats | {S["UCD"][1]}
source: Pet Poison Helpline: Lilies | {S["PPHL"][1]}
source: Pet Poison Helpline: Essential Oils and Cats | {S["PPHO"][1]}
source: Pet Poison Helpline: Liquid Potpourri Is Toxic to Cats | {S["PPHP"][1]}
source: ASPCA: The Essentials of Essential Oils Around Pets | {S["ASPO"][1]}
source: Cornell Feline Health Center: Poisons | {S["CORP"][1]}
source: Cornell Feline Health Center: Common Cat Hazards | {S["CORL"][1]}
source: International Cat Care: Permethrin poisoning | {S["ICC"][1]}
source: ASPCA: People foods to avoid feeding your pets | {S["ASPF"][1]}
---
<p class="lead"><b>If your cat has touched or eaten anything marked Emergency, Toxic or Caution below, call your vet or a pet poison helpline now.</b> The most dangerous plants for cats are true lilies and daylilies: a nibble of a leaf, pollen licked off the fur or a drink of vase water can cause fatal kidney failure. Search {n} common cut flowers, houseplants, garden plants, essential oils, household products and foods below; every entry has its own link and lists the sources it relies on.</p>
<p class="meta">Last reviewed <time datetime="{REVIEWED}">{REVIEWED_H}</time>. Only items we can source to the ASPCA, Cornell Feline Health Center, International Cat Care, Pet Poison Helpline, UC Davis or the FDA are included.</p>
<section class="card warn" id="what-to-do"><h2>Call your vet or a pet poison helpline now</h2><ol>
<li><b>Call</b> your vet or an emergency vet. In the US you can also call the ASPCA Animal Poison Control Center on (888) 426-4435 or Pet Poison Helpline on (855) 764-7661 (both charge a fee).</li>
<li><b>Keep the plant, packaging or a photo</b> to show the vet, and keep the cat away from it.</li>
<li><b>Do not</b> make your cat vomit or give home remedies unless a vet tells you to.</li>
<li><b>If there is pollen, oil or liquid on the fur,</b> stop the cat grooming it off if you safely can, and tell the vet.</li></ol></section>
<section class="card warn" id="lilies"><h2>Lilies: the number one plant danger for cats</h2>
<p><b>Call your vet or a pet poison helpline now if your cat has had any contact with a true lily or daylily.</b></p>
<ul><li><b>Which lilies:</b> true lilies (<i>Lilium</i>: Easter, tiger, Asiatic, Stargazer, Oriental and many bouquet hybrids) and daylilies (<i>Hemerocallis</i>).</li>
<li><b>How little:</b> a small bite of leaf or petal, a few pollen grains licked off the fur, or water from the vase (FDA).</li>
<li><b>How fast:</b> vomiting, drooling and low energy within 0 to 12 hours, kidney damage at 12 to 24 hours, kidney failure within 24 to 72 hours. If treatment is delayed by 18 hours or more, kidney failure is generally irreversible (FDA).</li>
<li><b>Only cats:</b> dogs that eat lilies may get an upset stomach but do not develop kidney failure.</li>
<li><b>Not true lilies:</b> peace lilies and calla lilies irritate the mouth but do not cause kidney failure; lily of the valley affects the heart.</li></ul>
<p>Safest rule: no lilies in a home with cats, and check every bouquet. Full guide: <a href="/blog/are-lilies-poisonous-to-cats.html">are lilies poisonous to cats?</a></p></section>
<section class="card" id="checker"><h2>Toxicity checker</h2>
<label for="q"><b>Search:</b></label> <input id="q" type="search" placeholder="e.g. tulip, pothos, tea tree, bleach" autocomplete="off" style="max-width:420px">
<p class="jump"><b>Jump to:</b> {jump}</p>
<p class="sci" id="count" aria-live="polite"></p>
<div class="tablewrap"><table id="tox"><thead><tr><th>Item</th><th>Risk</th><th>What to do and what it can cause</th><th>Sources</th></tr></thead><tbody>
{"".join(rows)}
</tbody></table></div>
<p class="note">Risk levels: <b>Emergency</b>: potentially fatal, go to a vet now. <b>Toxic</b>: can cause significant illness, get advice now. <b>Caution</b>: usually mild stomach or skin upset, but still call for advice. <b>Non toxic</b>: listed as non toxic to cats by the ASPCA, though eating any plant can cause minor stomach upset. Not listed does not mean safe: check the full <a href="https://www.aspca.org/pet-care/animal-poison-control/toxic-and-non-toxic-plants" rel="noopener">ASPCA plant list</a> or ask your vet. For foods, see also <a href="/nutrition.html#avoid">foods to avoid</a>.</p></section>
<section class="card faq" id="faq"><h2>Toxic plants and cats: FAQ</h2>
<h3>What is the most poisonous plant for cats?</h3>
<p>True lilies (such as Easter, tiger, Asiatic and Stargazer lilies) and daylilies are among the most dangerous, because a tiny amount, even pollen or vase water, can cause fatal kidney failure. Sago palm, foxglove, oleander, azalea and lily of the valley can also be fatal.</p>
<h3>Can lily pollen or vase water really harm a cat?</h3>
<p>Yes. The US FDA warns that licking a few pollen grains off the fur or drinking water from a vase holding lilies can cause fatal kidney failure in cats.</p>
<h3>Are peace lilies poisonous to cats?</h3>
<p>Peace lilies are not true lilies and do not cause kidney failure, but the ASPCA lists them as toxic to cats because they cause intense mouth irritation, drooling, vomiting and difficulty swallowing.</p>
<h3>Are essential oil diffusers safe for cats?</h3>
<p>Use caution. Pet Poison Helpline explains that cats have difficulty breaking down some compounds in essential oils, and oils such as tea tree, wintergreen, citrus, pine, peppermint, cinnamon, clove and eucalyptus are known to poison cats. Never apply oils to a cat, keep bottles out of reach and clean up spills.</p>
<h3>Which houseplants are safe for cats?</h3>
<p>The ASPCA lists spider plant, Boston fern, African violet and areca palm, among many others, as non toxic to cats. Check any new plant on the ASPCA list before bringing it home.</p>
<h3>What should I do if my cat ate a toxic plant?</h3>
<p>Call your vet or a pet poison helpline now, and keep the plant or a photo of it. Do not make your cat vomit or give home remedies unless a vet tells you to.</p>
</section>
<script>(function(){{var q=document.getElementById("q"),rows=[].slice.call(document.querySelectorAll("#tox tbody tr[data-q]")),gr=[].slice.call(document.querySelectorAll("#tox tbody tr.grp")),c=document.getElementById("count");function run(){{var t=q.value.trim().toLowerCase(),n=0,seen={{}};rows.forEach(function(r){{var ok=!t||r.getAttribute("data-q").indexOf(t)>-1;r.hidden=!ok;if(ok){{n++;seen[r.getAttribute("data-g")]=1}}}});gr.forEach(function(g){{g.hidden=!!t&&!seen[g.textContent]}});c.textContent=n+" of "+rows.length+" items shown"}}q.addEventListener("input",run);run()}})();</script>
'''
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "_src", "toxic-to-cats.html"), "w").write(page)
print("entries", n)
