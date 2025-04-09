//
// Created by rob on 4/8/25.
//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sndfile.h>
#include "TulAudioLib.hpp"

int detect_word_boundaries(const char* audio_file) {
    if (!audio_file) {
        fprintf(stderr, "Error: No audio file provided!\n");
        return -1;
    }

    // 1. Load WAV using libsndfile
    SF_INFO sfinfo;
    SNDFILE* sndfile = sf_open(audio_file, SFM_READ, &sfinfo);
    if (!sndfile) {
        fprintf(stderr, "Error: Failed to open file '%s'\n", audio_file);
        return -1;
    }

    if (sfinfo.channels != 1 || sfinfo.samplerate != SAMPLE_RATE || sfinfo.format != (SF_FORMAT_WAV | SF_FORMAT_PCM_16)) {
        fprintf(stderr, "Unsupported file format. Expected mono, 16-bit WAV at 16kHz.\n");
        sf_close(sndfile);
        return -1;
    }

    int num_samples = sfinfo.frames;
    short* samples = (short*)alloca(sizeof(short) * num_samples);
    if (!samples) {
        fprintf(stderr, "Memory allocation failed (samples)\n");
        sf_close(sndfile);
        return -1;
    }

    sf_readf_short(sndfile, samples, num_samples);
    sf_close(sndfile);

    // 2. Pre-emphasis filter
    float* filtered = (float*)alloca(sizeof(float) * num_samples);
    if (!filtered) {
        fprintf(stderr, "Memory allocation failed (filtered)\n");
        return -1;
    }

    preemphasis(samples, filtered, num_samples, 0.97f);

    // 3. Run energy-based word boundary detection
    detect_boundaries(filtered, num_samples);

    return 0;
}
