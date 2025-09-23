from Alphabet import Alphabet, BoundaryMarker, ContextFreeRule, CDRule, ParallelRewriter, VoicingBlock, rewrite
import pynini as pn
from pynini.lib import rewrite, pynutil

# -----------
# The model
# -----------
class CzechG2P:
    def __init__(self):
        # phones (final alphabet)
        phones = {
            "a","á","b","c","č","C","Č","d","ď","e","é","f","g","h","X","i","í","j","k","l",
            "m","M","n","N","ň","o","ó","p","r","ř","Ř","s","š","t","ť","u","ú","v","z","ž","E","-","#",
            ".",",","!","?",":",";"," "
        }
        # graphs (input alphabet)
        lowercase = set("abcdefghijklmnopqrstuvwxyz")
        czech_lower = {"á","é","ě","í","ó","ú","ů","ý","č","ř","ď","ť","ň","š","ž"}
        uppercase = {c.upper() for c in lowercase}
        czech_upper = {c.upper() for c in czech_lower}
        graphs = lowercase | czech_lower | uppercase | czech_upper | {" ", ".",",","!","?",";",":"}

        self.alpha = Alphabet(graphs=graphs, phones=phones, specials=set())
        self.boundary = BoundaryMarker("#")

        # helper sets
        self.V = pn.union("a","á","e","é","i","í","o","ó","u","ú","ů","y","ý")
        self.BPFV = pn.union("b","p","f","v")
        self.I_OR_LONG_I = pn.union("i","í")

        # obstruent classes
        self.ZPS = {"b","d","ď","g","z","ž","h","C","Č","Ř"}   # voiced
        self.NPS = {"p","t","ť","k","s","š","X","c","č","ř"}   # voiceless

        # build pipeline
        self.rewrite_fst = self._build_pipeline()

    def _build_pipeline(self) -> pn.Fst:
        SIGMA = self.alpha.SIGMA
        PR = ParallelRewriter(self.alpha)

        ALL_MARKERS = {
            "α","β","γ","δ","ε","ζ","η",
            "θ","ι",
            "κdě","κtě","κně","κmě",
            "λd","λt","λn",
            "¤","§","©","«","µ","¶","¥",
        }
        # in __init__ or _build_pipeline:
        self.alpha.add_markers(*ALL_MARKERS)

        # --- Base context-free rewrites (slide (2)) ---
        PR.add_cf("α", "ch", "X")
        PR.add_cf("β", "ů",  "ú")
        PR.add_cf("γ", "w",  "v")
        PR.add_cf("δ", "q",  "kv")
        PR.add_cf("ε", "x",  "ks")
        PR.add_cf("ζ", "y",  "i")
        PR.add_cf("η", "ý",  "í")

        # --- Slabikotvorné j: i→ij / _ V (slide (3)) ---
        # mark when i is followed by a vowel
        PR.add_cd("θ", "i", "ij", "", self.V)

        # --- ě after b/p/f/v → je (slide (4)) ---
        PR.add_cd("ι", "ě", "je", self.BPFV, "")

        # --- dě,tě,ně,mě → ďe,ťe,ňe,mňe (slide (4)) ---
        for (src, dst) in [("dě","ďe"),("tě","ťe"),("ně","ňe"),("mě","mňe")]:
            PR.add_cf("κ" + src, src, dst)

        # --- d/t/n → ď/ť/ň / _ i|í (slide (4)) ---
        for (src, dst) in [("d","ď"),("t","ť"),("n","ň")]:
            PR.add_cd("λ" + src, src, dst, "", self.I_OR_LONG_I)

        # --- Voicing block (slides (5)) ---
        voicing = VoicingBlock(self.alpha, self.ZPS, self.NPS).build()

        # Compose: base (parallel) then voicing (parallel)
        base = PR.build()
        return (base @ voicing).optimize()

    # API
    def apply(self, text: str) -> str:
        inp = self.boundary.mark(text)
        out = rewrite.one_top_rewrite(inp, self.rewrite_fst)
        return self.boundary.unmark(out)


# ---------------
# Quick smoke test
# ---------------
if __name__ == "__main__":
    g2p = CzechG2P()
    tests = [
        "chata", "kůň", "wow", "quark", "xenon", "byl dým",
        "marie", "biologie",
        "běh", "pěna", "věc", "fě",
        "dě", "těžký", "nějak", "město",
        "dik", "dívka", "ticho", "tíž", "nikdy", "nízko",
        "hrad", "vůz", "Radka", "drozd", "kdo", "keř", "břicho",
        "kresba", "leckde",
    ]
    for s in tests:
        print(s)
        print(f"{s} -> {g2p.apply(s)}")