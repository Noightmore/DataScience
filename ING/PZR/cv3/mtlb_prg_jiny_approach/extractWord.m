function detectedWord = extractWord(filePath)
    % Define parameters
    frameSize = 400; % 25 ms (400 samples)
    frameStep = 160; % 10 ms (160 samples)
    energyThresholdPercentage = 0.30; % 30% of the energy difference
    zcrThresholdPercentage = 0.20;    % 20% of the ZCR difference

    % Load audio file
    [x, fs] = audioread(filePath);
    x = double(x);
    
    % Add subtle noise
    noise = 0.01 * (randi(3, length(x), 1) - 2);
    noisy_signal = x + noise;
    
    % Pre-emphasis filtering
    xf = filter([1 -0.97], 1, noisy_signal);
    
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
    
    % Call detectWord function to extract detected speech segment
    [wordStart, wordEnd] = detectWord(logEnergy, zcr, energyThresholdPercentage, zcrThresholdPercentage, frameStep, frameSize);
    
    % Return extracted word or empty array if no word found
    if wordStart > 0 && wordEnd > 0
        detectedWord = xf(wordStart:wordEnd);
    else
        detectedWord = [];
        disp(['No word detected in file: ', filePath]);
    end
end
