//
// Created by rob on 4/9/25.
//


#include "PlotAudio.hpp"


namespace view::chart_plot {

    // Load WAV using libsndfile for plotting
    bool load_wav_for_plot(const char* path, std::vector<QPointF>& points) {
        SF_INFO sfinfo;
        SNDFILE* sndfile = sf_open(path, SFM_READ, &sfinfo);
        if (!sndfile) {
            std::cerr << "Failed to open: " << path << "\n";
            return false;
        }
        if (sfinfo.channels != 1 || sfinfo.samplerate != SAMPLE_RATE || sfinfo.format != (SF_FORMAT_WAV | SF_FORMAT_PCM_16)) {
            std::cerr << "Unsupported format.\n";
            sf_close(sndfile);
            return false;
        }

        int N = sfinfo.frames;
        std::vector<short> samples(N);
        sf_readf_short(sndfile, samples.data(), N);
        sf_close(sndfile);

        // Convert to points for plotting
        points.reserve(N);
        for (int i = 0; i < N; ++i) {
            points.emplace_back(i, samples[i]);
        }

        return true;
    }

    void plot_waveform(const std::vector<QPointF>& points, const char* title) {
        auto* series = new QtCharts::QLineSeries();
        series->append(QList<QPointF>(points.begin(), points.end()));

        auto* chart = new QtCharts::QChart();
        chart->addSeries(series);
        chart->setTitle(title);

        auto* axisX = new QtCharts::QValueAxis();
        axisX->setTitleText("Sample Index");
        axisX->setRange(0, points.size());
        chart->addAxis(axisX, Qt::AlignBottom);
        series->attachAxis(axisX);

        auto* axisY = new QtCharts::QValueAxis();
        axisY->setTitleText("Amplitude");
        axisY->setRange(-32768, 32767);
        chart->addAxis(axisY, Qt::AlignLeft);
        series->attachAxis(axisY);

        auto* chartView = new QtCharts::QChartView(chart);
        chartView->setRenderHint(QPainter::Antialiasing);

        auto* window = new QMainWindow();
        window->setCentralWidget(chartView);
        window->resize(800, 600);
        window->show();
    }

} // view::chart_plot
