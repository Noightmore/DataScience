# run_translator.py
import sys
import unicodedata as ud
import regex as re
from antlr4 import InputStream, CommonTokenStream
from antlr4.TokenStreamRewriter import TokenStreamRewriter
from ING.PMR.antlr_fun.CzechLexer import CzechLexer
#from CzechLexer import CzechLexer
from ING.PMR.antlr_fun.CzechParser import CzechParser  # generated but not used directly

# ---------- helpers ----------
def nfc(s: str) -> str:
    return ud.normalize("NFC", s)

VOWELS = "aáeéiíoóuúůyý"
VOW = f"[{VOWELS}]"
I_OR_LONG_I = r"[ií]"

# ---------- parallel per-word (your previous pass) ----------
def rewrite_word_parallel(original_word: str) -> str:
    s = nfc(original_word.lower())
    edits = []  # (start, end, repl, prio, tag)

    def add(st, en, rep, pr, tag): edits.append((st, en, rep, pr, tag))

    # Base context-free (prio 50)
    for m in re.finditer(r"ch", s, overlapped=True): add(m.start(), m.end(), "X", 50, "ch→X")
    for i, ch in enumerate(s):
        if ch == "ů": add(i, i+1, "ú", 50, "ů→ú")
        elif ch == "w": add(i, i+1, "v", 50, "w→v")
        elif ch == "q": add(i, i+1, "kv", 50, "q→kv")
        elif ch == "x": add(i, i+1, "ks", 50, "x→ks")
        elif ch == "y": add(i, i+1, "i", 50, "y→i")
        elif ch == "ý": add(i, i+1, "í", 50, "ý→í")

    # i -> ij / _ V (prio 60)
    for m in re.finditer(rf"i(?={VOW})", s, overlapped=True):
        add(m.start(), m.end(), "ij", 60, "i→ij/_V")

    # dě/tě/ně/mě (prio 90)
    for src, dst in (("dě","ďe"),("tě","ťe"),("ně","ňe"),("mě","mňe")):
        for m in re.finditer(re.escape(src), s, overlapped=True):
            add(m.start(), m.end(), dst, 90, f"{src}→{dst}")

    # ě -> je / <b,p,f,v> _ (prio 70)
    for m in re.finditer(r"(?<=[bpfv])ě", s, overlapped=True):
        i = m.start()
        add(i, i+1, "je", 70, "BPFV_ě→je")

    # d/t/n -> ď/ť/ň / _ i|í (prio 80)
    for m in re.finditer(rf"d(?={I_OR_LONG_I})", s, overlapped=True): add(m.start(), m.end(), "ď", 80, "d→ď/_i")
    for m in re.finditer(rf"t(?={I_OR_LONG_I})", s, overlapped=True): add(m.start(), m.end(), "ť", 80, "t→ť/_i")
    for m in re.finditer(rf"n(?={I_OR_LONG_I})", s, overlapped=True): add(m.start(), m.end(), "ň", 80, "n→ň/_i")

    # resolve overlaps
    edits.sort(key=lambda e: (e[0], -(e[1]-e[0]), -e[3]))
    chosen, covered = [], [False]*(len(s)+1)
    for st, en, rep, pr, _ in edits:
        if any(covered[i] for i in range(st, en)): continue
        for i in range(st, en): covered[i] = True
        chosen.append((st, en, rep))

    out, pos = [], 0
    for st, en, rep in sorted(chosen, key=lambda x: x[0]):
        out.append(s[pos:st]); out.append(rep); pos = en
    out.append(s[pos:])
    return "".join(out)

# ---------- voicing/devoicing + ř (parallel over token list) ----------

VOICED_TRIG    = set("bdďgzžhCČ")        # voiced obstruents that trigger voicing
VOICELESS_TRIG = set("ptťksšXcčf")       # voiceless obstruents that trigger devoicing

DEVOICE_MAP = {
    "b":"p","d":"t","ď":"ť","g":"k",
    "z":"s","ž":"š","h":"X","C":"c","Č":"č",
    "Ř":"ř","v":"f"
}
VOICE_MAP   = {
    "p":"b","t":"d","ť":"ď","k":"g",
    "s":"z","š":"ž","X":"h","c":"C","č":"Č",
    "ř":"Ř","f":"v"
}

def _devoice_tail_cluster(s: str) -> str:
    """
    Devoice the entire final obstruent cluster (zd# -> st#).
    EXCEPT: leave Ř untouched (it is handled by its own rules).
    """
    if not s:
        return s
    OBS_ALL = VOICED_TRIG | VOICELESS_TRIG | {"v"}  # Ř/ř excluded!
    i = len(s) - 1
    while i >= 0 and s[i] in OBS_ALL:
        i -= 1
    start = i + 1
    if start >= len(s):
        return s
    tail = list(s[start:])
    for j, ch in enumerate(tail):
        if ch == "v":
            tail[j] = "f"
        else:
            tail[j] = DEVOICE_MAP.get(ch, ch)
    return s[:start] + "".join(tail)

def apply_voicing_parallel(words: list[str]) -> list[str]:
    base = words[:]  # frozen snapshot
    out = []

    for idx, s in enumerate(base):
        edits = []

        def add_char(pos, rep, pr, tag): edits.append((pos, rep, pr, tag))

        # NOTE: removed the old "baseline prefer voiced Ř" — per your rules,
        # ř changes ONLY when one of (34)–(37) matches; otherwise it stays ř.

        # within-word assimilation
        for i in range(len(s) - 1):
            a, b = s[i], s[i+1]

            # ----- R E G R E S S I V E   A S S I M I L A C E  -----
            # (34) ř → ř / _ ZPS   (before a voiced obstruent, keep ř)
            if a == "ř" and b in VOICED_TRIG:
                add_char(i, "ř", 80, "ř→ř / _ ZPS (34)")
            # (35) ř → Ř / _ NPS   (before a voiceless obstruent, make Ř)
            if a == "ř" and b in VOICELESS_TRIG:
                add_char(i, "Ř", 80, "ř→Ř / _ NPS (35)")

            # ----- N O R M Á L N Í   Z N Ě L O S T N Í   S P O D O B A  -----
            # Keep your general voicing/devoicing rules for OTHER consonants
            if a in VOICE_MAP and b in VOICED_TRIG:
                add_char(i, VOICE_MAP[a], 40, "voice")
            if a in DEVOICE_MAP and b in VOICELESS_TRIG:
                add_char(i, DEVOICE_MAP[a], 45, "devoice")

        # ----- P R O G R E S S I V N Í   A S S I M I L A C E  -----
        # (36) ř → ř / ZPS _    (after a voiced obstruent, keep ř)
        # (37) ř → Ř / NPS _    (after a voiceless obstruent, make Ř)
        for i in range(1, len(s)):
            prev, cur = s[i-1], s[i]
            if cur == "ř":
                if prev in VOICED_TRIG:
                    add_char(i, "ř", 50, "ř→ř / ZPS _ (36)")
                if prev in VOICELESS_TRIG:
                    add_char(i, "Ř", 50, "ř→Ř / NPS _ (37)")

        # ----- N E W : ř at start or end → Ř -----
        if s:
            if s[0] == "ř":
                add_char(0, "Ř", 90, "ř→Ř (word-initial)")
            if s[-1] == "ř":
                add_char(len(s) - 1, "Ř", 90, "ř→Ř (word-final)")

        # ----- P Ř E S   H R A N I C I   S L O V  (regressive across boundary) -----
        if idx + 1 < len(base) and base[idx + 1]:
            first_next = base[idx + 1][0]

            # Apply ONLY when last char is ř, per rules (34)/(35)
            if s and s[-1] == "ř":
                # (34) ř → ř / _ ZPS
                if first_next in VOICED_TRIG:
                    add_char(len(s) - 1, "ř", 80, "ř→ř / _ ZPS (34, cross-word)")
                # (35) ř → Ř / _ NPS
                if first_next in VOICELESS_TRIG:
                    add_char(len(s) - 1, "Ř", 80, "ř→Ř / _ NPS (35, cross-word)")

            # keep your normal cross-word assimilation for other consonants
            if s:
                last = s[-1]
                if last in VOICE_MAP and first_next in VOICED_TRIG:
                    add_char(len(s)-1, VOICE_MAP[last], 40, "voice#")
                if last in DEVOICE_MAP and first_next in VOICELESS_TRIG:
                    add_char(len(s)-1, DEVOICE_MAP[last], 45, "devoice#")

        # resolve conflicts at same index: pick highest priority
        by_pos = {}
        for pos, rep, pr, tag in edits:
            cur = by_pos.get(pos)
            if cur is None or pr > cur[1]:
                by_pos[pos] = (rep, pr, tag)

        chars = list(s)
        for pos, (rep, _, _) in by_pos.items():
            chars[pos] = rep
        word_after_pos = "".join(chars)

        # propagate cluster devoicing (Ř excluded as before)
        out.append(_devoice_tail_cluster(word_after_pos))

    return out


# ---------- main API ----------
def rewrite_text(text: str) -> str:
    # 1) lex ORIGINAL input
    text = nfc(text)
    stream = InputStream(text)
    lexer = CzechLexer(stream)
    tokens = CommonTokenStream(lexer)
    tokens.fill()

    # 2) gather words (original), then first parallel pass (word-internal)
    T_WORD = lexer.WORD
    idxs = [i for i,t in enumerate(tokens.tokens) if t.type == T_WORD]
    originals = [tokens.tokens[i].text for i in idxs]
    base_words = [rewrite_word_parallel(w) for w in originals]

    # 3) NEW: place/manner pass (parallel, uses snapshot of base_words)
    placed_words = apply_place_manner_parallel(base_words)

    # 4) second parallel pass: voicing/devoicing + ř across word boundaries
    voiced_words = apply_voicing_parallel(placed_words)

    # 5) commit all replacements at once
    rewriter = TokenStreamRewriter(tokens)
    for i, val in zip(idxs, voiced_words):
        rewriter.replaceRange(i, i, val)
    return rewriter.getText(rewriter.DEFAULT_PROGRAM_NAME, 0, len(tokens.tokens)-1)


# ---------- place/manner assimilation (parallel) ----------
def _within_word_place_manner(s: str) -> str:
    # Nasal place: n->N / _ k|g ; m->M / _ f|v
    s = re.sub(r"n(?=[kg])", "N", s)
    s = re.sub(r"m(?=[fv])", "M", s)

    # Cluster reductions (mutually exclusive, no cascade risk)
    # Order doesn't matter; outputs (c, č, C, Č) don't trigger any other rule here.
    s = s.replace("tš", "č").replace("dš", "č").replace("dž", "Č")
    s = s.replace("ts", "c").replace("ds", "c").replace("dz", "C")
    return s

def apply_place_manner_parallel(words: list[str]) -> list[str]:
    """
    Parallel over tokens:
      - First, apply within-word substitutions on a frozen snapshot.
      - Then, do cross-word assimilation using the snapshot of the original pair,
        editing BOTH sides in the output (e.g., ...t + s... -> ...c + ...).
    """
    base = words[:]                      # frozen view for decisions
    out  = [_within_word_place_manner(w) for w in base]  # edit-once per word

    # Cross-word cluster reductions and nasal place assimilation
    pair_reduce = {
        ("t", "s"): ("c", ""),  # ts -> c
        ("t", "š"): ("č", ""),  # tš -> č
        ("d", "s"): ("c", ""),  # ds -> c
        ("d", "š"): ("č", ""),  # dš -> č
        ("d", "z"): ("C", ""),  # dz -> C
        ("d", "ž"): ("Č", ""),  # dž -> Č
    }

    for i in range(len(base) - 1):
        wL, wR = base[i], base[i + 1]
        if not wL or not wR:
            continue

        lastL, firstR = wL[-1], wR[0]

        # Nasal place across boundary
        if lastL == "n" and firstR in ("k", "g"):
            out[i] = out[i][:-1] + "N"
        if lastL == "m" and firstR in ("f", "v"):
            out[i] = out[i][:-1] + "M"

        # Cluster reductions across boundary (e.g., '...t' + 's...' => '...c' + '...')
        key = (lastL, firstR)
        if key in pair_reduce:
            rep_last, drop_first = pair_reduce[key]
            # replace last char of left word
            out[i] = out[i][:-1] + rep_last
            # remove the leading s/š/z/ž from the right word
            if drop_first == "":
                out[i + 1] = out[i + 1][1:]

    return out


if __name__ == "__main__":
    samples = [
        # base
        "chata", "kůň", "wow xylophon", "quark byl dým", "xenon ypsilon ý",
        "marie biologie", "běh pěna věc město", "dik dívka ticho tíž nikdy nízko",

        # voicing/devoicing examples
        "hrad", "vůz", "Radka", "drozd",
        "kresba", "kdo", "leckde",

        # ř behavior
        "keř", "břicho", "tři přímo", "pařba",

        # place/manner assimilation (sanity checks)
        "banka",       # n -> N / _k  → baNka
        "gongy",       # n -> N / _g  → goNgi
        "tramvaj",     # m -> M / _v  → traMvaj
        "nymfa",       # m -> M / _f  → niMfa
        "pět set",      # ts -> c across boundary → pjecet
        "větší",       # tš -> č → vječí
        "beskydský",   # ds -> c → bescický (depending on context)
        "mlaďší",      # dš -> č → mlačí
        "podzemí",     # cross-word cluster test
        "leckde",      # leCgde (already tested in voicing)
        "Džorč",       # dž/č cluster tests
        "lodžie",     # dž cluster test
        "džungle"       # dz → C or dž → Č, N assimilation
    ]

    samples2 = [
        "Spolek byl založen devatenáctého listopadu roku devatenáct set třicet dva.",
        "Sejdeme se v naší restauraci ve čtvrt na sedm večer.",
        "Kdy dnes odjíždí poslední vlak nebo autobus z Liberce do Pardubic.",
        "Na konferenci senátor rovněž kritizoval současné právní prostředí.",
        "Výkon brankáře znamenal pro hokejové družstvo dobré umístění v tabulce.",
        "Dnes bude oblačno až polojasno, místy možno očekávat přeháňky."
    ]

    # if len(sys.argv) > 1:
    #     print(rewrite_text(" ".join(sys.argv[1:])))
    # elif not sys.stdin.isatty():
    #     print(rewrite_text(sys.stdin.read()))
    # else:
    #     for s in samples:
    #         print(f"{s} -> {rewrite_text(s)}")
    #     for s in samples2:
    #         print(f"{s} -> {rewrite_text(s)}")

    for s in samples:
         print(f"{s} -> {rewrite_text(s)}")
    for s in samples2:
         print(f"{s} -> {rewrite_text(s)}")

# problemy:
#  kriťizoval, univerzita, komunikovat, diskutovat -> viktoriia fenomen; nutno udelat seznam vyjimek
# sedm -> sedum; 8 taky
# chybi spelling "HTML" dodo
# devatenácc et; pjec et problem -> odstraneni mezer

# oboje ř a Ř by mely byt ve voiced
# z -> s; zalezi na kontextu, treba doopravit; predlozky k, nad, pod :( taky nutne odstranit mezery pak bude fungovat
# misto dnes by to melo byt dnez; dnez bude -> kvuli B, meli bychom nejprve prece odstranovat mezery proto to tak susi?
# čísla 1234, nepřevádět na jejich

# slova ciziho puvodu prepsat rucne
# do phonu pridat i symboly ticha kde je ticho,  zacatek a konec!
# vyvarovat se cizich slov obecne

# vygenerovat pravidla dle chat gpt udelat maly skypt pro analyzu cetnosti phonemu aby byly spravne reprezentovane

# to run:
# python fun.py "chata kůň wow quark"
# @  ~/Programming/Datascience/ING/PMR/antlr_fun
