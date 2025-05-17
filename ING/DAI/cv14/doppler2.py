import numpy as np
import soundfile as sf
from scipy.signal import fftconvolve

# the impulse response should change with the moving speaker
# need to use rir generator:
# pyromaacoustic python package

def simulate_walk(input_path,  rir_path, output_path,
                  walk_duration=10.0,
                  area_size=1.0,
                  fs_frame=0.050):

    # 1) load dry signal
    x, sr = sf.read(input_path)           # shape (N,), sr=sample-rate
    N = len(x)

    # 2) load RIR
    h_ir, sr_ir = sf.read(rir_path)
    if sr_ir != sr:
        raise ValueError(f"Sample rates differ: signal {sr} vs RIR {sr_ir}")

    # If your RIR is stereo, split it
    if h_ir.ndim == 2 and h_ir.shape[1] == 2:
        h_l, h_r = h_ir[:,0], h_ir[:,1]
    else:
        # mono → use same IR on both channels
        h_l = h_r = h_ir

    # 3) build the walk trajectory
    T = N / sr
    t = np.linspace(0, T, N)
    M = int(np.ceil(T / fs_frame)) + 1
    pts = np.zeros((M,2))
    pts[0] = [0.0, 1.0]
    rng = np.random.default_rng(42)
    for i in range(1, M):
        step = rng.uniform(-0.2, +0.2, size=2)
        pts[i] = np.clip(pts[i-1] + step, -area_size/2, area_size/2)
    tt = np.linspace(0, T, M)
    xs = np.interp(t, tt, pts[:,0])
    ys = np.interp(t, tt, pts[:,1])
    zs = np.ones_like(xs) * 1.0

    # 4) compute gain & panning
    r = np.sqrt(xs*xs + ys*ys + zs*zs)
    gain = 1.0 / r
    az = np.arctan2(xs, ys)
    left  = gain * np.cos(az/2 + np.pi/4)
    right = gain * np.sin(az/2 + np.pi/4)

    # 5) apply to dry signal → dry stereo
    y_dry = np.vstack([left * x, right * x]).T   # (N,2)

    # 6) convolve each channel with its RIR
    # ’full’ mode gives length N + len(h_ir) – 1; we trim back to N
    y_l = fftconvolve(y_dry[:,0], h_l, mode='full')[:N]
    y_r = fftconvolve(y_dry[:,1], h_r, mode='full')[:N]
    y_wet = np.vstack([y_l, y_r]).T

    # add hluk to the signal at 0.8 magnitude
    hluk = "CHiME3/BGD_150204_030_CAF.CH1.wav"

    # y_wet is your final stereo array of shape (N,2)
    N = y_wet.shape[0]
    sr = sr  # your sample-rate

    # 1) load the background noise
    noise, sr_n = sf.read(hluk)
    if sr_n != sr:
        raise ValueError(f"Sample-rate mismatch: signal {sr} vs noise {sr_n}")

    # 2) trim or tile the noise to length N
    if noise.ndim > 1:
        # if it’s stereo, just take one channel (or mix)
        noise = noise[:,0]
    if len(noise) < N:
        # repeat it until it's at least N
        reps = int(np.ceil(N/len(noise)))
        noise = np.tile(noise, reps)
    noise = noise[:N]

    # 3) normalize & scale to 0.8
    noise = noise / np.max(np.abs(noise)) * 0.4

    # 4) make it stereo
    noise_stereo = np.column_stack([noise, noise])  # shape (N,2)

    # 5) add
    y_noisy = y_wet + noise_stereo

    # 6) optional: avoid clipping
    peak = np.max(np.abs(y_noisy))
    if peak > 1.0:
        y_noisy = y_noisy / peak

    # 7) write out
    sf.write(output_path, y_noisy, sr)
    print(f"Wrote walking+RIR+noise to {output_path}")



if __name__=="__main__":
    simulate_walk(
        "WSJ/024c0202_0.077249_022a010v_-0.077249.wav",
        "air_type1_air_binaural_stairway_1_1_90.wav",
        "walking_reverb.wav"
    )
