# tests/test_g2p_pdf_examples.py
# Run with: pytest -q
import re

from ING.PMR.g2p.core_g2p_cz import g2p  # <-- change if your module is named differently

# ---- small helpers ----------------------------------------------------------
def norm_spaces(s: str) -> str:
    """Match the PDF's underscore word separators:
       - collapse whitespace
       - compare using underscores between tokens
    """
    s = re.sub(r"\s+", " ", s.strip())
    return s.replace(" ", "_")

def assert_eq_pdf(actual: str, expected_pdf: str):
    """Compare after normalizing spaces to underscores, exactly like the PDF lines."""
    a = norm_spaces(actual)
    e = norm_spaces(expected_pdf)
    assert a == e, f"\nExpected: {e}\nActual:   {a}\n"

# -----------------------------------------------------------------------------
# Base grapheme rules: ch→X, ů→ú, w→v, q→kv, x→ks, y/ý→i/í
# Source: “Pravidla fonetického přepisu (2)”, bullet list of basic rules. :contentReference[oaicite:0]{index=0}
def test_base_grapheme_rules():
    pairs = {
        "ch": "X",
        "kůň": "kúň",          # ů → ú
        "wow": "vov",          # w → v
        "quark": "kvark",      # q → kv
        "xenon": "ksenon",     # x → ks
        "byl": "bil",          # y → i
        "dým": "dím",          # ý → í
    }
    for src, exp in pairs.items():
        assert g2p(src) == exp

# -----------------------------------------------------------------------------
# Syllabic j insertion: i→ij before a following vowel
# Source: “Pravidla fonetického přepisu (3): Slabikotvorné j … i → ij / _ <SA>” with examples. :contentReference[oaicite:1]{index=1}
def test_syllabic_j_insertion():
    ex = {
        "marie": "marije",
        "biologie": "bijologije",
    }
    for src, exp in ex.items():
        assert g2p(src) == exp

# -----------------------------------------------------------------------------
# ě rules and palatalization: ě→je after b/p/f/v; dě/ťe/ňe/mě; d/t/n→ď/ť/ň before i/í
# Source: “Pravidla … (4)” tables and lines. :contentReference[oaicite:2]{index=2}
def test_e_palatalization_rules():
    data = {
        "běh": "jeh".replace("j","bje").replace("jeh","bjeh"),  # explicit: bě → bje
        "pěna": "pjena",
        "fě": "fje",
        "vědět": "vjeďet",
        "dě": "ďe",
        "tě": "ťe",
        "ně": "ňe",
        "město": "mňesto",
        "di": "ďi",
        "tí": "ťí",
        "nikdy": "ňikdi",
    }
    for src, exp in data.items():
        assert g2p(src) == exp

# -----------------------------------------------------------------------------
# Voicing assimilation (spodoba znělosti) + behavior of ř
# Source: “Pravidla … (5)” including examples hrad→hrat, vůz→vús, Radka→ratka,
# drozd→drost, kresba→krezba, kdo→gdo, leckde→leCgde; ř depends on neighbors. :contentReference[oaicite:3]{index=3}
def test_voicing_assimilation_words():
    pairs = {
        "hrad": "hrat",
        "vůz": "vús",
        "Radka": "ratka",
        "drozd": "drost",
        "kresba": "krezba",
        "kdo": "gdo",
        "leckde": "leCgde",
        # ř examples (line notes show voiced/devoiced realizations by context)
        "keř": "keŘ",
        "břicho": "břiXo",
        "tři": "tŘi",
        "přímo": "pŘímo",
        "pařba": "pařba",
    }
    for src, exp in pairs.items():
        assert g2p(src) == exp

# -----------------------------------------------------------------------------
# Place/manner assimilation (spodoba artikulační)
# Source: “Pravidla … (6)” with examples baNka, goNgi, traMvaj, niMfa, pět set→pjecet, atd. :contentReference[oaicite:4]{index=4}
def test_place_manner_assimilation():
    pairs = {
        "banka": "baNka",
        "gongy": "goNgi",
        "tramvaj": "traMvaj",
        "nimfa": "niMfa",
        "pět set": "pjecet",     # ts → c across word boundary after normalization
        "větší": "vječí",        # tš → č
        "besdicky": "beskickí".replace("ck","ck").replace("besdicky","besdicky"),  # from slide “„beskickí””
        "džungle": "ČuNgle",     # dž → Č ; also N before g
        "pozemí": "poCemí",      # dz → C (as in examples)
        "leckde": "leCgde",      # again to ensure ts/dz mapping appears in complex clusters
    }
    for src, exp in pairs.items():
        assert g2p(src) == exp

# -----------------------------------------------------------------------------
# Full-sentence examples at the end of the PDF
# Source: “Příklady přepisu vět” block (compare with underscores). :contentReference[oaicite:5]{index=5}
def test_full_sentences_from_pdf():
    cases = [
        (
            "Spolek byl založen devatenáctého listopadu roku devatenáct set třicet dva.",
            "spoleg bil založen devatenáctého listopadu roku devatenácetŘicedva",
        ),
        (
            "Sejdeme se v naší restauraci ve čtvrt na sedm večer.",
            "sejdeme se v naší restauraci ve čtvrt na seduM večer",
        ),
        (
            "Kdy dnes odjíždí poslední vlak nebo autobus z Liberce do Pardubic.",
            "gdi dnes odjížďí posledňí vlak nebo autobuz z liberce do pardubic",
        ),
        (
            "Na konferenci senátor rovněž kritizoval současné právní prostředí.",
            "na konferenci senátor rovňeš kritizoval současné právňí prostŘeďí",
        ),
        (
            "Výkon brankáře znamenal pro hokejové družstvo dobré umístění v tabulce.",
            "víkon braNkáře znamenal pro hokejové drušstvo dobré umísťeňí f tabulce",
        ),
        (
            "Dnes bude oblačno až polojasno, místy možno očekávat přeháňky.",
            "dnez bude oblačno aš polojasno místi možno očekávat pŘeháňki",
        ),
        (
            "Najdeš to ve zdrojovém kódu HTML, stačí hledat řetězec mp3",
            "najdeš to ve zdrojovém kódu hEtEmElE stačí hledat řeťezec empétŘi",
        ),
    ]
    for src, expected_like_pdf in cases:
        # PDF uses underscores between tokens; we normalize both sides for fair comparison.
        assert_eq_pdf(g2p(src), expected_like_pdf)

# -----------------------------------------------------------------------------
# Idempotence: applying the rewrite twice should not change the result
# Rationale: each rule set is defined to be in “final” phoneme space, so a second pass
# shouldn’t introduce further changes (good regression check).
def test_idempotence_property():
    samples = [
        "vůz",
        "Radka",
        "pět set",
        "břicho",
        "Sejdeme se v naší restauraci ve čtvrt na sedm večer.",
    ]
    for s in samples:
        once = g2p(s)
        twice = g2p(once)
        assert once == twice, f"Rewrite not idempotent for: {s!r}"

