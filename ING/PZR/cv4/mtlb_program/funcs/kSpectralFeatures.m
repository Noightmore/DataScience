function spectralFeatures = kSpectralFeatures(frames, K)
    % Compute spectral features for each frame
    numFrames = size(frames, 2);
    spectralFeatures = zeros(K, numFrames);
    window = hamming(512); % Hamming window

    for i = 1:numFrames
        % Zero-padding to 512
        paddedFrame = zeros(512, 1);
        paddedFrame(1:400) = frames(:, i);

        % Apply Hamming window
        windowedFrame = paddedFrame .* window;

        % Compute 512-point FFT and extract first 256 amplitudes
        spectrum = abs(fft(windowedFrame, 512));
        spectrum = spectrum(1:256); % Keep only first half

        % Divide into K=16 bands and compute mean per band
        bandSize = floor(256 / K);
        for k = 1:K
            startIdx = (k-1) * bandSize + 1;
            endIdx = k * bandSize;
            spectralFeatures(k, i) = mean(spectrum(startIdx:endIdx));
        end
    end

    % Return mean spectral features across frames
    spectralFeatures = mean(spectralFeatures, 2);
end
