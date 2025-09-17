# core_g2p_cz.py
import re
import pynini as pn
from pynini.lib import rewrite

# a list of supported phones for the output
phones = {
    "a", "á",
    "b",
    "c", "č", "C", "Č", # C = dz; Č = dž
    "d", "ď",
    "e", "é",
    "f",
    "g",
    "h", "X",          # X = ch
    "i", "í",
    "j",
    "k",
    "l",
    "m", "M",
    "n", "N", "ň",
    "o", "ó",
    "p",
    "r", "ř", "Ř",          # Ř = voiced ř
    "s", "š",
    "t", "ť",
    "u", "ú",
    "v",
    "z", "ž",
    "E",               # neutrální samohláska
    "-"                # ticho
}

# basic czech alphabet ---------------------------------------------------------
lowercase = set("abcdefghijklmnopqrstuvwxyz")
czech_lower = {"á","é","ě","í","ó","ú","ů","ý","č","ř","ď","ť","ň","š","ž"}

uppercase    = {c.upper() for c in lowercase}
czech_upper  = {c.upper() for c in czech_lower}

graphs = (
        lowercase | czech_lower |
        uppercase | czech_upper |
        {" ", ".",",","!","?",";",":"}
)
# -----------------------------------------------------------------------------


# rules -----------------------------------------------------------------------

# helper sets for rules
vowel_set = pn.union("a","á","e","é","i","í","o","ó","u","ú","ů","y","ý")
bpfv = pn.union("b","p","f","v")
i_or_long_i = pn.union("i", "í")

# Voiced obstruents (ZPS). Use Ř (voiced ř) here.
ZPS = {"b","d","ď","g","z","ž","h","C","Č","Ř"}  # v handled separately, see r_v_final
# Voiceless obstruents (NPS).
NPS = {"p","t","ť","k","s","š","X","c","č","ř"}

# --- maps (voiced <-> voiceless) ---
devoice_pairs = {
    "b":"p","d":"t","ď":"ť","g":"k",
    "z":"s","ž":"š","h":"X","C":"c","Č":"č","Ř":"ř"
}
voice_pairs = {v:k for k,v in devoice_pairs.items()}

DEVOICE = pn.string_map(list(devoice_pairs.items()))
VOICE   = pn.string_map(list(voice_pairs.items()))

VOICE_MAP = pn.string_map([
    ("p","b"), ("t","d"), ("ť","ď"), ("k","g"),
    ("s","z"), ("š","ž"), ("X","h"), ("c","C"), ("č","Č"), ("ř","Ř"),
])

def main():
    # full alphabet (Σ)
    # hashtag pro tokenizaci, pro zjisteni word end and word start
    sigma  = pn.union(*(graphs | phones | {"#"})).closure().optimize()
    bound  = pn.accep("#")

    def mark_boundaries(s: str) -> str:
        s = re.sub(r"\s+", " ", s.strip())
        s = re.sub(r"([.,!?;:])", r" \1 ", s)
        toks = [t for t in s.split(" ") if t]
        return " ".join([f"#{t}#" if t not in ".,!?;:" else t for t in toks])

    def unmark_boundaries(s: str) -> str:
        return s.replace("#", "")


    # basic context free rewrite rules
    r_ch   = pn.cdrewrite(pn.cross("ch", "X"), "", "", sigma)  # ch → X
    r_uoh  = pn.cdrewrite(pn.cross("ů",  "ú"), "", "", sigma)  # ů → ú
    r_w    = pn.cdrewrite(pn.cross("w",  "v"), "", "", sigma)  # w → v
    r_q    = pn.cdrewrite(pn.cross("q",  "kv"),"", "", sigma)  # q → kv
    r_x    = pn.cdrewrite(pn.cross("x",  "ks"),"", "", sigma)  # x → ks
    r_y    = pn.cdrewrite(pn.cross("y",  "i"), "", "", sigma)  # y → i
    r_yacu = pn.cdrewrite(pn.cross("ý",  "í"), "", "", sigma)  # ý → í

    # Slabikotvorné j: Jestliže za i následuje jiná samohláska, vloží se mezi i a následující
    # samohlásku j
    # i → ij / _ <SA> “marije”, “mariji”, “bijologije”
    r_slabi_j = pn.cdrewrite(pn.cross("i", "ij"), "", vowel_set, sigma)

    # Následuje-li ě po b, p, f, v, přepisuje se na [je]
    # ě → je / <b, p, f, v> _
    r_je_after_bpfv = pn.cdrewrite(pn.cross("ě","je"), bpfv, "", sigma)

    # Spojení dě, tě, ně, mě přepisujeme na [ďe], [ťe], [ňe], [mňe]
    # dě → ďe / _
    # tě → ťe / _
    # ně → ňe / _
    # ě → ňe / m_
    r_de = pn.cdrewrite(pn.cross("dě","ďe"), "", "", sigma)
    r_te = pn.cdrewrite(pn.cross("tě","ťe"), "", "", sigma)
    r_ne = pn.cdrewrite(pn.cross("ně","ňe"), "", "", sigma)
    r_me = pn.cdrewrite(pn.cross("mě","mňe"), "", "", sigma)

    # Spojení di, ti, ni přepisujeme na [ďi], [ťi], [ňi]
    # d → ď / _<i, í>
    # t → ť / _<i, í>
    # n → ň / _<i, í>
    r_di = pn.cdrewrite(pn.cross("d", "ď"), "", i_or_long_i, sigma)
    r_ti = pn.cdrewrite(pn.cross("t", "ť"), "", i_or_long_i, sigma)
    r_ni = pn.cdrewrite(pn.cross("n", "ň"), "", i_or_long_i, sigma)

    # Pravidla spodoby znělosti
    # Označíme ¬ ZPS jako neznělý protějšek ke znělé souhlásce ZPS,
    # tj ¬ b = p, ¬ d = t, ¬ ď = ť, ¬ g = k, ¬ v = f, ¬ z = s,
    # ¬ ž = š, ¬ h = ch, ¬ C = c, ¬ Č = č, ¬ Ř = ř.
    # podobně ¬ NPS je znělý protějšek k neznělé souhlásce NPS

    voiced_obst    = pn.union(*ZPS)     # triggers for voicing on the right
    voiceless_obst = pn.union(*NPS)     # triggers for devoicing on the right

    # ZPS1 → ¬ ZPS1 / _ < - , NPS, ZPS2 - > „hrad“ → „hrat“, „vůz“ → „vús“,
    # „Radka“ → „ratka“, „drozd“, → „drost“,

    # --- ř baseline: treat plain ř as voiced Ř; devoicing may change it back ---
    r_raise_R = pn.cdrewrite(pn.cross("ř","Ř"), "", "", sigma)

    # Devoice Ř when immediately before a voiceless obstruent (adjacent) …
    r_R_devoice_adj = pn.cdrewrite(pn.cross("Ř","ř"), "", voiced_obst, sigma)

    # …and also when 'i' or 'í' intervenes before a voiceless obstruent (Ř i|í VOICELESS)
    r_R_devoice_iX = pn.cdrewrite(
        pn.cross("Ř","ř"),
        "",
        pn.concat(pn.union("i","í"), voiced_obst),
        sigma
    )

    # --- voicing (NPS -> ZPS) before a voiced obstruent on the right ---
    r_voice   = pn.cdrewrite(VOICE,   "", voiced_obst, sigma)

    # --- devoicing (ZPS -> NPS) before a voiceless obstruent OR word-final (#) ---
    r_devoice = pn.cdrewrite(DEVOICE, "", pn.union(voiceless_obst, "#"), sigma)

    # --- special-case: v -> f only word-final (common Czech, avoids cycles) ---
    r_v_final = pn.cdrewrite(pn.cross("v","f"), "", "#", sigma)

    # Compose these in your pipeline AFTER place/manner assimilation:
    assim_voicing = (r_raise_R @ r_voice @ r_devoice @ r_v_final).optimize()

    # NPS1 → ¬ NPS1 / _ ZPS „kresba → „krezba“, „kdo“ → „gdo“,
    # „leckde“ → „leCgde“,
    # The rule itself: NPS -> voiced / _ ZPS
    r_voice = pn.cdrewrite(VOICE_MAP, "", voiced_obst, sigma)

    # definice pravidel
    base_rules = ((r_ch @ r_uoh @ r_w @ r_q @ r_x @ r_y @ r_yacu @ r_slabi_j
                  @ r_je_after_bpfv @ r_de @ r_te @ r_ne @ r_me @ r_di @ r_ti @ r_ni @ assim_voicing @ r_voice
                   @ r_R_devoice_adj @ r_R_devoice_iX )
                  .optimize())

    def apply_base(text: str, rules) -> str:
        return unmark_boundaries(rewrite.one_top_rewrite(mark_boundaries(text), rules))

    # --- quick demo for context free rules ---
    examples = [
        "chata",    # ch → X
        "kůň",      # ů → ú
        "wow",      # w → v
        "quark",    # q → kv
        "xenon",    # x → ks
        "byl dým",  # y→i, ý→í

        # i -> ij
        "marie",
        "biologie",
        "radnice"

        # Rule: ě → je / <b,p,f,v> _
        "běh",
        "pěna",
        "věc",
        "fě"

        # dě, tě, ně, mě → ďe, ťe, ňe, mňe
        "dě",
        "těžký",
        "nějak",
        "město"
        
        # d, t, n → ď, ť, ň / _ <i, í>
        "dik",
        "dívka",
        "ticho",
        "tíž",
        "nikdy",
        "nízko",
        
        # ZPS/NPS fun
        "hrad", # hrat
        "vůz", # vús
        "Radka", # ratka
        "drozd",  # drost
        "kdo", # gdo
        "keř", # keŘ (voiced ř)
        "břicho", # břiXo (ř devoiced by X)

        # another rule for nps
        "kresba",
        "kdo",
        "leckde",

        # sekvence slov
        "sex kokot hradský hrad buzna buznitá, teplovitost"
    ]
    for s in examples:
        print(f"{s} -> {apply_base(s, base_rules)}")

if __name__ == "__main__":
    main()


# fix Řř
# fix wow -> vof ???????????????????
# fix nikdy -> ňigďi; the rules have to be applied from left to right to prevent this exact scenario
# udelat kod vice modularni a prehledny!!!!!!!!!!!
# napsat vlastni testy dle nouza pravidel, zadny chat gpt!!!!!!

# problemy mohou nastat v poradim v jakem jsou pravidla aplikovana?
# udelat modularni aplikaci pravidel?
