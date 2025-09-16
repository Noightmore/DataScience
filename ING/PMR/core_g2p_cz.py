# core_g2p_cz.py
import pynini as pn
from pynini.lib import rewrite

# ----- Alphabet & helpers -----
# We work in NFC unicode, lowercase input.
V = pn.union("a","á","e","é","i","í","o","ó","u","ú","ů","y","ý")
CONS = pn.union(*list("bcčdďfghjklmnpqrsštťuvwxyzžxwřXČŘC"))  # includes PAC symbols & digraph outputs
SPACE = pn.union(" ", "\t", "\n")
BOUND = pn.accep("#")                  # explicit word boundary marker
SIGMA = pn.union(V, CONS, SPACE, BOUND, ".", ",", "!", "?", ":", ";").closure().optimize()

def mark_boundaries(text: str) -> str:
    # Surround tokens with # … # so we can implement word-final contexts cleanly.
    import re
    # Split on whitespace/punct and re-insert as boundaries.
    text = re.sub(r"\s+", " ", text.strip())
    text = re.sub(r"([.,!?;:])", r" \1 ", text)
    tokens = [t for t in text.split(" ") if t != ""]
    return " ".join([BOUND + t + BOUND if t not in ".,!?;:" else t for t in tokens])

def unmark_boundaries(text: str) -> str:
    return text.replace(BOUND, "")

# ----- Base grapheme→phoneme rules -----
# Pravidla fonetického přepisu (2): ch→X, ů→ú, w→v, q→kv, x→ks, y/ý→i/í.  :contentReference[oaicite:2]{index=2}
r_base = pn.union(
    pn.cdrewrite(pn.cross("ch","X"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("ů","ú"),  "", "", SIGMA),
    pn.cdrewrite(pn.cross("w","v"),  "", "", SIGMA),
    pn.cdrewrite(pn.cross("q","kv"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("x","ks"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("y","i"),  "", "", SIGMA),
    pn.cdrewrite(pn.cross("ý","í"),  "", "", SIGMA),
).optimize()

# Pravidla (3): "slabikotvorné j" — i→ij before a vowel.  :contentReference[oaicite:3]{index=3}
r_j_insertion = pn.cdrewrite(pn.cross("i","ij"), "", V, SIGMA)

# Pravidla (4): ě after b,p,f,v → je; dě→ďe, tě→ťe, ně→ňe; mě→mňe; d/t/n→ď/ť/ň before i,í.  :contentReference[oaicite:4]{index=4}
BPFV = pn.union("b","p","f","v")
r_e_after_bpfv = pn.cdrewrite(pn.cross("ě","je"), BPFV, "", SIGMA)

r_dte_bigram = pn.union(
    pn.cdrewrite(pn.cross("dě","ďe"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("tě","ťe"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("ně","ňe"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("mě","mňe"), "", "", SIGMA),
).optimize()

r_pal_before_i = pn.union(
    pn.cdrewrite(pn.cross("d","ď"), "", pn.union("i","í"), SIGMA),
    pn.cdrewrite(pn.cross("t","ť"), "", pn.union("i","í"), SIGMA),
    pn.cdrewrite(pn.cross("n","ň"), "", pn.union("i","í"), SIGMA),
).optimize()

# Pravidla (6) – spodoba artikulace (place/manner):
# n→N before k,g ; m→M before f,v ; clusters s/z + t/d etc.  :contentReference[oaicite:5]{index=5}
r_place = pn.union(
    pn.cdrewrite(pn.cross("n","N"), "", pn.union("k","g"), SIGMA),
    pn.cdrewrite(pn.cross("m","M"), "", pn.union("f","v"), SIGMA),
    # s,z with t,d (written in the slides via ts→c, ds→c, tš→č, dš→č, dz→C, dž→Č)
    pn.cdrewrite(pn.cross("ts","c"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("ds","c"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("tš","č"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("dš","č"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("dz","C"), "", "", SIGMA),
    pn.cdrewrite(pn.cross("dž","Č"), "", "", SIGMA),
).optimize()

# Pravidla (5) – spodoba znělosti (voicing/devoicing, incl. ř).  :contentReference[oaicite:6]{index=6}
# Define voiced/voiceless obstruent pairs per the slide:
devoice_pairs = {
    "b":"p","d":"t","ď":"ť","g":"k","v":"f","z":"s","ž":"š","h":"X","C":"c","Č":"č","Ř":"ř"
}
voice_pairs = {v:k for k,v in devoice_pairs.items()}
VOICED = pn.union(*voice_pairs.values())       # set of voiced obstruents (targets for devoicing rule)
VOICELESS = pn.union(*voice_pairs.keys())      # set of voiceless obstruents (context for devoicing)
DEVOICE = pn.string_map(devoice_pairs.items())
VOICE   = pn.string_map(voice_pairs.items())

# Treat plain input 'ř' as underlyingly voiced; let devoicing fix it in voiceless context.
r_raise_R = pn.cdrewrite(pn.cross("ř","Ř"), "", "", SIGMA)

# (a) Devoice a voiced obstruent word-finally or before a voiceless obstruent: ZPS → ¬ZPS / _ <#, NPS>.  :contentReference[oaicite:7]{index=7}
r_devoice = pn.cdrewrite(DEVOICE, "", pn.union(BOUND, VOICELESS), SIGMA)

# (b) Voice a voiceless obstruent before a voiced obstruent: NPS → ¬NPS / _ VOICED.  :contentReference[oaicite:8]{index=8}
r_voice = pn.cdrewrite(VOICE, "", VOICED, SIGMA)

# ----- Compose the pipeline with clear precedence -----
# 1) base grapheme rules; 2) j-insertion; 3) ě/bpfv + palatalizations; 4) place/manner; 5) raise Ř; 6) voicing assimilations.
RULE = (r_base @ r_j_insertion @ r_e_after_bpfv @ r_dte_bigram @ r_pal_before_i
        @ r_place @ r_raise_R @ r_voice @ r_devoice).optimize()

def g2p(text: str) -> str:
    s = mark_boundaries(text.lower())
    out = rewrite.one_top_rewrite(s, RULE)
    return unmark_boundaries(out)

