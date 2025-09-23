import re
import unicodedata as ud
import pynini as pn
from pynini.lib import rewrite, pynutil

# ---------------------------
# Alphabet / Sigma management
# ---------------------------
class Alphabet:
    def __init__(self, graphs: set[str], phones: set[str], specials: set[str] | None = None):
        self.graphs = set(graphs)
        self.phones = set(phones)
        self.specials = set(specials or set())
        self._rebuild()

    def add_marker(self, s: str):
        # Add a marker symbol (can be single char or a multi-char token)
        self.specials.add(s)
        self._rebuild()

    def add_markers(self, *marks: str):
        for m in marks: self.add_marker(m)

    @property
    def SIGMA(self) -> pn.Fst:
        return self._sigma

    def _rebuild(self):
        union = self.graphs | self.phones | self.specials
        self._sigma = pn.union(*union).closure().optimize()

# --------------------
# Boundary tokenization
# --------------------
class BoundaryMarker:
    def __init__(self, boundary="#"):
        self.bound = boundary

    def mark(self, s: str) -> str:
        s = re.sub(r"\s+", " ", ud.normalize("NFC", s).strip())
        s = re.sub(r"([.,!?;:])", r" \1 ", s)
        toks = [t for t in s.split(" ") if t]
        return " ".join([f"{self.bound}{t}{self.bound}" if t not in ".,!?;:" else t for t in toks])

    def unmark(self, s: str) -> str:
        return s.replace(self.bound, "")


# -------------
# Rule wrappers
# -------------
class ContextFreeRule:
    """Simple A->B everywhere."""
    def __init__(self, src: str, dst: str):
        self.src, self.dst = src, dst

    def build(self, SIGMA: pn.Fst) -> pn.Fst:
        return pn.cdrewrite(pn.cross(self.src, self.dst), "", "", SIGMA)


class CDRule:
    """Context-dependent A->B / L _ R."""
    def __init__(self, src: str, dst: str, L: pn.Fst | str = "", R: pn.Fst | str = ""):
        self.src, self.dst, self.L, self.R = src, dst, L, R

    def build(self, SIGMA: pn.Fst) -> pn.Fst:
        return pn.cdrewrite(pn.cross(self.src, self.dst), self.L, self.R, SIGMA)

# ----------------------
# Parallel (marker) pass
# ----------------------
class ParallelRewriter:
    """
    Mark → Replace → Clean. Use single-char markers (default) or pass your own.
    """
    def __init__(self, alphabet: Alphabet):
        self.A = alphabet
        self.MARK = pn.accep("")     # inserts markers only
        self.REPLACE = pn.accep("")  # replaces only marked spans
        self.CLEAN = pn.accep("")    # deletes markers at the end
        self._clean_list: list[str] = []

    def _ensure_marker(self, m: str):
        self.A.add_marker(m)
        self._clean_list.append(m)

    def add_cf(self, marker: str, src: str, dst: str):
        """Context-free: mark src, replace with dst."""
        self._ensure_marker(marker)
        SIGMA = self.A.SIGMA
        pre  = pn.cdrewrite(pynutil.insert(marker), "", src, SIGMA)
        post = pn.cdrewrite(pynutil.insert(marker), src, "", SIGMA)
        self.MARK = (self.MARK @ pre @ post).optimize()
        self.REPLACE = (self.REPLACE @ pn.cdrewrite(pn.cross(marker + src + marker, dst), "", "", SIGMA)).optimize()

    def add_cd(self, marker: str, src: str, dst: str, L: pn.Fst | str, R: pn.Fst | str):
        """Context-dependent A->B/L_R: mark focus under L_R, then replace."""
        self._ensure_marker(marker)
        SIGMA = self.A.SIGMA
        pre  = pn.cdrewrite(pynutil.insert(marker), L, src, SIGMA)
        post = pn.cdrewrite(pynutil.insert(marker), L + src, R, SIGMA)
        self.MARK = (self.MARK @ pre @ post).optimize()
        self.REPLACE = (self.REPLACE @ pn.cdrewrite(pn.cross(marker + src + marker, dst), "", "", SIGMA)).optimize()

    def add_map(self, marker: str, mapping: dict[str, str], L: pn.Fst | str, R: pn.Fst | str):
        """
        Mark any single symbol in mapping when L _ R holds, then rewrite by the map.
        Useful for voicing/devoicing families.
        """
        self._ensure_marker(marker)
        SIGMA = self.A.SIGMA
        # Mark: before symbols in domain(mapping) under L _ R
        dom_union = pn.union(*mapping.keys())
        pre  = pn.cdrewrite(pynutil.insert(marker), L, dom_union, SIGMA)
        post = pn.cdrewrite(pynutil.insert(marker), L + dom_union, R, SIGMA)
        self.MARK = (self.MARK @ pre @ post).optimize()
        # Replace: union of per-symbol replacements on the marked token
        repls = [pn.cdrewrite(pn.cross(marker + k + marker, v), "", "", SIGMA) for k, v in mapping.items()]
        self.REPLACE = (self.REPLACE @ pn.union(*repls).optimize()).optimize()

    def build(self) -> pn.Fst:
        # CLEAN: drop all markers we introduced
        SIGMA = self.A.SIGMA
        for m in self._clean_list:
            self.CLEAN = (self.CLEAN @ pn.cdrewrite(pn.cross(m, ""), "", "", SIGMA)).optimize()
        return (self.MARK @ self.REPLACE @ self.CLEAN).optimize()


# -------------------
# Voicing / ř block
# -------------------
class VoicingBlock:
    """Builds the voicing/devoicing + ř behavior as marker-based parallel rules."""
    def __init__(self, alphabet: Alphabet, ZPS: set[str], NPS: set[str]):
        self.A = alphabet
        self.ZPS = set(ZPS)
        self.NPS = set(NPS)

    def build(self) -> pn.Fst:
        SIGMA = self.A.SIGMA
        PR = ParallelRewriter(self.A)

        # Treat plain ř as Ř baseline (context-free)
        PR.add_cf("¤", "ř", "Ř")  # marker char can be anything not in your data

        # Voice: NPS -> ZPS / _ ZPS  (exclude v/f here; handle v final separately if you want)
        voice_map = {
            "p":"b","t":"d","ť":"ď","k":"g",
            "s":"z","š":"ž","X":"h","c":"C","č":"Č","ř":"Ř",
        }
        voiced_trigger = pn.union(*(self.ZPS | {"ř"}))  # ř counts as voiced neighbor
        PR.add_map("§", voice_map, "", voiced_trigger)

        # Devoice: ZPS -> NPS / _ NPS or _ #  (Ř handled separately below to allow special behavior)
        devo_map = {
            "b":"p","d":"t","ď":"ť","g":"k","z":"s","ž":"š","h":"X","C":"c","Č":"č"
        }

        voiceless_trigger = pn.union(*self.NPS)
        # Before voiceless obstruent
        PR.add_map("©", devo_map, "", voiceless_trigger)
        # Word-final (#)
        PR.add_map("«", devo_map, "", "#")

        # ř special devoicing: Ř → ř before NPS (adjacent) and with i/í intervening
        PR.add_cd("µ", "Ř", "ř", "", voiceless_trigger)  # Ř _ NPS
        PR.add_cd("¶", "Ř", "ř", "", pn.concat(pn.union("i","í"), voiceless_trigger))  # Ř i|í _ NPS

        # Optional: v → f / _ #
        PR.add_cd("¥", "v", "f", "", "#")

        return PR.build()

