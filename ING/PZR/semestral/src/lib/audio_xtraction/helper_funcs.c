//
// Created by rob on 4/9/25.
//

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "TulAudioLib.hpp"

float preemphasis(short* x, float* y, int N, float alpha) {
    y[0] = x[0];
    for (int i = 1; i < N; ++i) {
        y[i] = (float)x[i] - alpha * (float)x[i - 1];
    }
    return 0;
}

float compute_log_energy(float* frame, int L) {
    float energy = 0.0f;
    for (int i = 0; i < L; ++i) {
        energy += frame[i] * frame[i];
    }
    return logf(energy + 1e-6f); // avoid log(0)
}

void detect_boundaries(float* signal, int num_samples) {
    int num_frames = (num_samples - FRAME_SIZE) / FRAME_SHIFT + 1;
    float* energies = (float*)alloca(sizeof(float) * num_frames);

    // compute energy per frame
    for (int i = 0; i < num_frames; ++i) {
        float* frame = signal + i * FRAME_SHIFT;
        energies[i] = compute_log_energy(frame, FRAME_SIZE);
    }

    // compute threshold (simple: average of top 5 and bottom 5)
    float max_energy = -INFINITY, min_energy = INFINITY;
    for (int i = 0; i < num_frames; ++i) {
        if (energies[i] > max_energy) max_energy = energies[i];
        if (energies[i] < min_energy) min_energy = energies[i];
    }
    float threshold = min_energy + 0.3f * (max_energy - min_energy);

    // find start
    int start = 0;
    for (; start < num_frames; ++start) {
        if (energies[start] > threshold) break;
    }

    // find end
    int end = num_frames - 1;
    for (; end > start; --end) {
        if (energies[end] > threshold) break;
    }

    printf("Detected word from frame %d to %d\n", start, end);
    printf("Approx. sample range: %d to %d\n", start * FRAME_SHIFT, (end + 1) * FRAME_SHIFT);

}
