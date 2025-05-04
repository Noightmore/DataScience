# time stretching without affecting pitch

# matlab:
#
# clear *
#
# [x, fs] = audioread('pisen_jana_KRAJIKA.wav');
# x = x(:,1);
# N = length(x);
#
# Nwin = 1024;
# Sa = 128;
# alpha = 1.5
# Ss = Sa*alpha;
#
# x_new = zeros(round(N*alpha), 1);
# Nnew = length(x_new);
# fadewin = hanning(2*(Nwin-Ss));
# fadeinwin = fadewin(1:Nwin-Ss);
# fadeoutwin = fadewin(Nwin-Ss+1:2*(Nwin-Ss));
# i_x = 1;
# i_y = 1;
# while i_x < Nnew-Sa
#     segment = x(i_x:i_x+Sa-1);
#     x_new(i_y:i_y+Sa-1) = overlap*fadeoutwin + segment(i_y:i_y+Nwin-Ss)*fadeinwin;
#     x_new(i_y+Nwin-Ss:i_y+Nwin-1) = segment(i_y+Nwin-Ss:i_y+Nwin-1)*fadeoutwin;
#
#     i_x = i_x + Sa;
#     i_y = round(i_y + Ss);
# end

# in python:

import numpy as np
import matplotlib.pyplot as plt

import numpy as np
import soundfile as sf
import sounddevice as sd

def time_stretch(infile, outfile, alpha,
                 Nwin=1024, Sa=128):
    """
    Time‑stretch audio by factor alpha without changing pitch,
    using simple overlap‑add.

    infile  – path to input WAV
    outfile – path to write stretched WAV
    alpha   – stretch factor (>1 = slower, <1 = faster)
    Nwin    – analysis window length (samples)
    Sa      – analysis hop size (samples)
    """
    # read mono
    x, fs = sf.read(infile)
    if x.ndim > 1:
        x = x[:,0]
    N = len(x)

    # synthesis hop
    Ss = int(round(Sa * alpha))
    # total length of output
    Nnew = int(round(N * alpha)) + Nwin
    y = np.zeros(Nnew)

    # make fade‑in/out windows
    fade_len = Nwin - Ss
    fadewin = np.hanning(2 * fade_len)
    fade_in  = fadewin[:fade_len]
    fade_out = fadewin[fade_len:]

    in_pos  = 0
    out_pos = 0

    # process one frame at a time
    while in_pos + Nwin < N:
        frame = x[in_pos:in_pos + Nwin]

        # first Ss samples just add
        y[out_pos : out_pos + Ss] += frame[:Ss]

        # now cross‑fade the remaining fade_len samples
        # existing y segment (fade-out) blended with new frame (fade-in)
        y_start = out_pos + Ss
        y_end   = y_start + fade_len
        y_seg = y[y_start : y_end] * fade_out
        f_seg = frame[Ss : Ss + fade_len] * fade_in
        y[y_start : y_end] = y_seg + f_seg

        # advance pointers
        in_pos  += Sa
        out_pos += Ss

    # trim to exact length and write
    y = y[: int(round(N * alpha))]
    sf.write(outfile, y, fs)
    # play
    sd.play(y, fs)
    print(f"Stretched {infile} → {outfile}, factor {alpha:.2f}")

# example usage:
if __name__ == "__main__":
    time_stretch(
        infile  ="pisen_Jana_KRAJIKA.wav",
        outfile ="pisen_jana_KRAJIKA_stretch.wav",
        alpha   =1.5,
        Nwin    =1024,
        Sa      =128
    )


# optional: add cross correlation for smoother sounds