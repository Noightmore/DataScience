//
// Created by rob on 4/9/25.
//

#ifndef PLOTAUDIO_HPP
#define PLOTAUDIO_HPP

#pragma once


#include "../lib/TulAudioLib.hpp"

#include <vector>
#include <iostream>
#include <QPointF>
#include <sndfile.h>
#include <vector>
#include <QtCharts/QLineSeries>
#include <QtCharts/QChartView>
#include <QtCharts/QValueAxis>
#include <QtCharts/QChart>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QApplication>

namespace view::chart_plot {
    bool load_wav_for_plot(const char* path, std::vector<QPointF>& points);
    void plot_waveform(const std::vector<QPointF>& points, const char* title = "Audio Waveform");
}



#endif //PLOTAUDIO_HPP
