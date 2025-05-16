import numpy as np
import soundfile as sf

def simulate_walk(input_path, output_path,
                  walk_duration=10.0,
                  area_size=1.0,
                  fs_frame=0.050):
    """
    input_path  : path to your mono WAV
    output_path : path for stereo WAV out
    walk_duration : total walk time in seconds
    area_size   : side length (m) of square around mic
    fs_frame    : frame length for updating position (s)
    """
    # 1) load
    x, sr = sf.read(input_path)           # x.shape = (N,), sr=sample-rate
    N = len(x)
    T = N / sr

    # we’ll tile your trajectory to the length of the file
    t = np.linspace(0, T, N)

    # 2) build a random‐walk in a square [–area/2, +area/2]²
    #    sampled every fs_frame seconds, then linearly interp
    M = int(np.ceil(T / fs_frame)) + 1
    # start at (0, 1 m): 1 m in front of the mic on the y‐axis
    pts = np.zeros((M,2))
    pts[0] = np.array([0.0, 1.0])
    rng = np.random.default_rng(42)
    for i in range(1, M):
        step = rng.uniform(-0.2, +0.2, size=2)  # max 20 cm per step
        pts[i] = pts[i-1] + step
        # clamp into the square (centered at 0,0 in xy-plane)
        pts[i] = np.clip(pts[i], -area_size/2, area_size/2)

    # time stamps for each pt
    tt = np.linspace(0, T, M)

    # 3) interpolate your x(t), y(t)
    xs = np.interp(t, tt, pts[:,0])
    ys = np.interp(t, tt, pts[:,1])
    # z is fixed at 1 m
    zs = np.ones_like(xs) * 1.0

    # compute distance ‖r(t)‖ and attenuation = 1/r
    r = np.sqrt(xs*xs + ys*ys + zs*zs)
    gain = 1.0 / r

    # optional: stereo panning via equal-power law
    # azimuth = angle in horizontal plane from mic “front” (y-axis)
    az = np.arctan2(xs, ys)  # radians, negative=left, positive=right
    # equal-power panning:
    left  = gain * np.cos(az/2 + np.pi/4)
    right = gain * np.sin(az/2 + np.pi/4)

    # 4) apply and save
    # stack into stereo
    y = np.vstack([left * x, right * x]).T  # shape (N,2)
    sf.write(output_path, y, sr)
    print(f"Wrote simulated walk to {output_path}")

if __name__=="__main__":
    simulate_walk("stationary_mono.wav", "walking_simulated.wav")
