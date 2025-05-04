import re

text = r"""#!MLF!#
"D:/HTK/DATA/0000_MVL/c0_p0000_s04.lab"
NULA
.
"D:/HTK/DATA/0000_MVL/c1_p0000_s04.lab"
JEDNA
.
"D:/HTK/DATA/0000_MVL/c2_p0000_s04.lab"
DVA
.
"D:/HTK/DATA/0000_MVL/c3_p0000_s04.lab"
TRI
.
"D:/HTK/DATA/0000_MVL/c4_p0000_s04.lab"
CTYRI
.
"D:/HTK/DATA/0000_MVL/c5_p0000_s04.lab"
PET
.
"D:/HTK/DATA/0000_MVL/c6_p0000_s04.lab"
SEST
.
"D:/HTK/DATA/0000_MVL/c7_p0000_s04.lab"
SEDM
.
"D:/HTK/DATA/0000_MVL/c8_p0000_s04.lab"
OSM
.
"D:/HTK/DATA/0000_MVL/c9_p0000_s04.lab"
DEVET
.
"D:/HTK/DATA/0001_ZJD/c0_p0001_s04.lab"
NULA
.
"D:/HTK/DATA/0001_ZJD/c1_p0001_s04.lab"
JEDNA
.
"D:/HTK/DATA/0001_ZJD/c2_p0001_s04.lab"
DVA
.
"D:/HTK/DATA/0001_ZJD/c3_p0001_s04.lab"
TRI
.
"D:/HTK/DATA/0001_ZJD/c4_p0001_s04.lab"
CTYRI
.
"D:/HTK/DATA/0001_ZJD/c5_p0001_s04.lab"
PET
.
"D:/HTK/DATA/0001_ZJD/c6_p0001_s04.lab"
SEST
.
"D:/HTK/DATA/0001_ZJD/c7_p0001_s04.lab"
SEDM
.
"D:/HTK/DATA/0001_ZJD/c8_p0001_s04.lab"
OSM
.
"D:/HTK/DATA/0001_ZJD/c9_p0001_s04.lab"
DEVET
.
"D:/HTK/DATA/0002_MJD/c0_p0002_s04.lab"
NULA
.
"D:/HTK/DATA/0002_MJD/c1_p0002_s04.lab"
JEDNA
.
"D:/HTK/DATA/0002_MJD/c2_p0002_s04.lab"
DVA
.
"D:/HTK/DATA/0002_MJD/c3_p0002_s04.lab"
TRI
.
"D:/HTK/DATA/0002_MJD/c4_p0002_s04.lab"
CTYRI
.
"D:/HTK/DATA/0002_MJD/c5_p0002_s04.lab"
PET
.
"D:/HTK/DATA/0002_MJD/c6_p0002_s04.lab"
SEST
.
"D:/HTK/DATA/0002_MJD/c7_p0002_s04.lab"
SEDM
.
"D:/HTK/DATA/0002_MJD/c8_p0002_s04.lab"
OSM
.
"D:/HTK/DATA/0002_MJD/c9_p0002_s04.lab"
DEVET
.
"D:/HTK/DATA/0003_ZJL/c0_p0003_s04.lab"
NULA
.
"D:/HTK/DATA/0003_ZJL/c1_p0003_s04.lab"
JEDNA
.
"D:/HTK/DATA/0003_ZJL/c2_p0003_s04.lab"
DVA
.
"D:/HTK/DATA/0003_ZJL/c3_p0003_s04.lab"
TRI
.
"D:/HTK/DATA/0003_ZJL/c4_p0003_s04.lab"
CTYRI
.
"D:/HTK/DATA/0003_ZJL/c5_p0003_s04.lab"
PET
.
"D:/HTK/DATA/0003_ZJL/c6_p0003_s04.lab"
SEST
.
"D:/HTK/DATA/0003_ZJL/c7_p0003_s04.lab"
SEDM
.
"D:/HTK/DATA/0003_ZJL/c8_p0003_s04.lab"
OSM
.
"D:/HTK/DATA/0003_ZJL/c9_p0003_s04.lab"
DEVET
.
"D:/HTK/DATA/0004_MVL/c0_p0004_s04.lab"
NULA
.
"D:/HTK/DATA/0004_MVL/c1_p0004_s04.lab"
JEDNA
.
"D:/HTK/DATA/0004_MVL/c2_p0004_s04.lab"
DVA
.
"D:/HTK/DATA/0004_MVL/c3_p0004_s04.lab"
TRI
.
"D:/HTK/DATA/0004_MVL/c4_p0004_s04.lab"
CTYRI
.
"D:/HTK/DATA/0004_MVL/c5_p0004_s04.lab"
PET
.
"D:/HTK/DATA/0004_MVL/c6_p0004_s04.lab"
SEST
.
"D:/HTK/DATA/0004_MVL/c7_p0004_s04.lab"
SEDM
.
"D:/HTK/DATA/0004_MVL/c8_p0004_s04.lab"
OSM
.
"D:/HTK/DATA/0004_MVL/c9_p0004_s04.lab"
DEVET
.

"""

def rewrite_mlf_content(mlf_text: str) -> str:
    """
    Rewrite every line of the form "D:/HTK/DATA/.../... .lab" to "../DATA/... .lab"
    and return the full modified MLF as a single string.
    """
    # matches drive letter + HTK prefix (case‑insensitive), e.g. D:/HTK/ or C:\HTK\
    prefix_re = re.compile(r'^[A-Za-z]:[/\\]+HTK[/\\]+', flags=re.IGNORECASE)
    out = []
    for line in mlf_text.splitlines():
        # detect a quoted filename line
        m = re.match(r'\s*"([^"]+)"\s*$', line)
        if m:
            orig_path = m.group(1)
            # strip drive+HTK, normalize slashes, prepend "../"
            stripped = prefix_re.sub('', orig_path)
            stripped = stripped.replace('\\', '/')
            out.append(f'"../{stripped}"')
        else:
            # leave labels and periods intact
            out.append(line)
    return "\n".join(out)

if __name__ == "__main__":
    fixed = rewrite_mlf_content(text)
    print(fixed)
