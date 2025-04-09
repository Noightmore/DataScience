#!/bin/bash

# This script installs the required dependencies for the project.

sudo emerge -av dev-qt/qtcharts
sudo emerge -av dev-qt/qtwidgets
sudo emerge -av dev-qt/qtbase
sudo emerge -av media-libs/libsndfile

