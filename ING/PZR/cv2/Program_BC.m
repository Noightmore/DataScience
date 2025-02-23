clear;
clc;
close all;

% Define parameters
folderPath = './p2501';
frameSize = 400; % 25 ms (400 samples)
frameStep = 160; % 10 ms (160 samples)
energyThresholdPercentage = 0.30; % 30% of the energy difference
zcrThresholdPercentage = 0.20;    % 20% of the ZCR difference

% List all .wav files in the directory
audioFiles = dir(fullfile(folderPath, '*.wav'));

% Loop through each file
for i = 1:length(audioFiles)
    % Load audio file
    [x, Fs] = audioread(fullfile(folderPath, audioFiles(i).name));
    x = double(x);

    % Display and play original signal
    figure;
    subplot(3, 1, 1);
    plot(x);
    title(['Original Signal - ', audioFiles(i).name]);
    xlabel('Samples');
    ylabel('Amplitude');
    sound(x, Fs);
    pause(length(x) / Fs + 1);

    % Add subtle noise
    noise = 0.01 * (randi(3, length(x), 1) - 2);
    noisy_signal = x + noise;

    % Pre-emphasis filtering
    xf = filter([1 -0.97], 1, noisy_signal);

    % Display filtered signal
    subplot(3, 1, 2);
    plot(xf);
    title('Filtered Signal');
    xlabel('Samples');
    ylabel('Amplitude');

    % Frame segmentation
    numFrames = floor((length(xf) - frameSize) / frameStep) + 1;
    frames = zeros(frameSize, numFrames);
    for k = 1:numFrames
        startIdx = (k-1) * frameStep + 1;
        endIdx = startIdx + frameSize - 1;
        frames(:, k) = xf(startIdx:endIdx);
    end

    % Calculate Log Energy and ZCR for each frame
    logEnergy = log(sum(frames.^2));
    zcr = sum(abs(diff(sign(frames)))) / (2 * frameSize);

    % Dynamic Thresholding
    sortedEnergy = sort(logEnergy);
    sortedZCR = sort(zcr);

    % Calculate dynamic thresholds
    lowEnergyMean = mean(sortedEnergy(1:round(0.1 * length(sortedEnergy))));
    highEnergyMean = mean(sortedEnergy(end-round(0.1 * length(sortedEnergy))+1:end));
    energyThreshold = lowEnergyMean + energyThresholdPercentage * (highEnergyMean - lowEnergyMean);

    lowZCRMean = mean(sortedZCR(1:round(0.1 * length(sortedZCR))));
    highZCRMean = mean(sortedZCR(end-round(0.1 * length(sortedZCR))+1:end));
    zcrThreshold = lowZCRMean + zcrThresholdPercentage * (highZCRMean - lowZCRMean);

    % Word Boundary Detection
    wordStart = 0;
    wordEnd = 0;
    for k = 1:numFrames
        if logEnergy(k) > energyThreshold && zcr(k) > zcrThreshold
            if wordStart == 0
                wordStart = (k-1) * frameStep + 1;
            end
            wordEnd = (k-1) * frameStep + frameSize;
        end
    end

    % Play detected word
    if wordStart > 0 && wordEnd > 0
        detectedWord = xf(wordStart:wordEnd);
        sound(detectedWord, Fs);
        pause(length(detectedWord) / Fs + 1);
    else
        disp('No word detected');
    end

    % Plot Feature Analysis
    subplot(3, 1, 3);
    hold on;
    plot(logEnergy, 'g', 'DisplayName', 'Log Energy');
    plot(zcr, 'b', 'DisplayName', 'ZCR');
    yline(energyThreshold, 'r--', 'DisplayName', 'Energy Threshold');
    yline(zcrThreshold, 'k--', 'DisplayName', 'ZCR Threshold');
    xline(wordStart / frameStep, 'm', 'DisplayName', 'Word Start');
    xline(wordEnd / frameStep, 'c', 'DisplayName', 'Word End');
    title('Feature Analysis');
    xlabel('Frames');
    ylabel('Feature Values');
    legend('show');
    hold off;

    % Pause between files
    pause(2);
end
