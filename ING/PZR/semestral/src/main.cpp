#include <QApplication>

#include "chart_plot/PlotAudio.hpp"

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    std::vector<QPointF> points;
    if (view::chart_plot::load_wav_for_plot("../p2501/c0_p2501_s01.wav", points)) {
        view::chart_plot::plot_waveform(points, "Waveform of ./p2501/c0_p2501_s01.wav");
    }

    return app.exec();
}