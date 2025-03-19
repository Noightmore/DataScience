function [detectedWord, wordStart, wordEnd, logEnergy, zcr] = xtractWord(filePath)
    % Define parameters bbb
    frameSize = 400; % 25 ms (400 samples)
    frameStep = 160; % 10 ms (160 samples)
    energyThresholdPercentage = 0.30; % 30% of the energy difference
    zcrThresholdPercentage = 0.20;    % 20% of the ZCR difference

    % Load audio file
    [x, ~] = audioread(filePath);
    x = double(x);
    
    % Add subtle noise to reduce numerical instability
    noise = 0.01 * (randi(3, length(x), 1) - 2);
    noisy_signal = x + noise;
    
    % Apply pre-emphasis filtering
    xf = filter([1 -0.97], 1, noisy_signal);
    
    % Frame segmentation
    numFrames = floor((length(xf) - frameSize) / frameStep) + 1;
    frames = zeros(frameSize, numFrames);
    for k = 1:numFrames
        startIdx = (k-1) * frameStep + 1;
        endIdx = startIdx + frameSize - 1;
        frames(:, k) = xf(startIdx:endIdx);
    end
    
    % Compute Log Energy and Zero-Crossing Rate (ZCR)
    logEnergy = log(sum(frames.^2));
    zcr = sum(abs(diff(sign(frames)))) / (2 * frameSize);
    
    % Sort energy and ZCR values for adaptive thresholding
    sortedEnergy = sort(logEnergy);
    sortedZCR = sort(zcr);
    
    % Adaptive threshold calculation
    lowEnergyMean = mean(sortedEnergy(1:round(0.1 * length(sortedEnergy))));
    highEnergyMean = mean(sortedEnergy(end-round(0.1 * length(sortedEnergy))+1:end));
    energyThreshold = lowEnergyMean + energyThresholdPercentage * (highEnergyMean - lowEnergyMean);

    lowZCRMean = mean(sortedZCR(1:round(0.1 * length(sortedZCR))));
    highZCRMean = mean(sortedZCR(end-round(0.1 * length(sortedZCR))+1:end));
    zcrThreshold = lowZCRMean + zcrThresholdPercentage * (highZCRMean - lowZCRMean);
    
    % Detect word boundaries
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
    
    % Extract detected word
    if wordStart > 0 && wordEnd > 0
        detectedWord = xf(wordStart:wordEnd);
    else
        detectedWord = [];
        wordEnd = 0;
        wordStart = 0;
        disp(['No word detected in file: ', filePath]);
    end
end
