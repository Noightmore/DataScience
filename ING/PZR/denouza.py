import re

listing = r"""
D:/HTK/DATA/0000_MVL/c0_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c1_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c2_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c3_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c4_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c5_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c6_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c7_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c8_p0000_s04.fbank
D:/HTK/DATA/0000_MVL/c9_p0000_s04.fbank
D:/HTK/DATA/0001_ZJD/c0_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c1_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c2_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c3_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c4_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c5_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c6_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c7_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c8_p0001_s04.fbank
D:/HTK/DATA/0001_ZJD/c9_p0001_s04.fbank
D:/HTK/DATA/0002_MJD/c0_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c1_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c2_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c3_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c4_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c5_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c6_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c7_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c8_p0002_s04.fbank
D:/HTK/DATA/0002_MJD/c9_p0002_s04.fbank
D:/HTK/DATA/0003_ZJL/c0_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c1_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c2_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c3_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c4_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c5_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c6_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c7_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c8_p0003_s04.fbank
D:/HTK/DATA/0003_ZJL/c9_p0003_s04.fbank
D:/HTK/DATA/0004_MVL/c0_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c1_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c2_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c3_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c4_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c5_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c6_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c7_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c8_p0004_s04.fbank
D:/HTK/DATA/0004_MVL/c9_p0004_s04.fbank
"""

for win in listing.strip().splitlines():
    # strip "D:/HTK" (or any drive letter + /HTK) at the front
    rel = re.sub(r'^[A-Za-z]:/HTK', '', win)
    # ensure it always starts with a slash before DATA
    rel = rel if rel.startswith('/') else '/' + rel
    # prepend the "../"
    print(f"..{rel}")
