//
// Created by rob on 4/8/25.
//

#include <stdio.h>

#ifndef TUL_AUDIO_LIBRARY_H
#define TUL_AUDIO_LIBRARY_H

#define SAMPLE_RATE 16000
#define FRAME_SIZE 400     // 25 ms at 16 kHz
#define FRAME_SHIFT 160    // 10 ms step

#ifdef __cplusplus
extern "C" {
#endif


    int detect_word_boundaries(const char* audio_file);
    float preemphasis(short* x, float* y, int N, float alpha);
    float compute_log_energy(float* frame, int L);
    void detect_boundaries(float* signal, int num_samples);

#ifdef __cplusplus
}
#endif

#endif //TUL_AUDIO_LIBRARY_H
