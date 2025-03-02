function trainKNN(fileListPath, referenceFile, K)
    % KNNtrain - Trains KNN reference features and saves them to a MAT file.
    %
    % Usage:
    %   KNNtrain('TrainFileList.txt', 'KNN_reference_features.mat', 16);
    %
    % Inputs:
    %   fileListPath - Path to the training file list (TXT file)
    %   referenceFile - Output MAT file to save extracted features
    %   K - Number of spectral bands (default = 16)

    if nargin < 3
        K = 16; % Default number of spectral bands
    end

    clc; close all;  % ✅ Removed 'clear' to preserve function variables

    % Read file list
    if exist(fileListPath, 'file') ~= 2
        error('Training file list %s not found!', fileListPath);
    end
    [fileNames, numFiles] = FileListRead(fileListPath);

    % Define parameters
    frameSize = 400; 
    frameStep = 160; 

    % Initialize feature storage
    referenceZCR = zeros(1, numFiles);
    referenceEnergy = zeros(1, numFiles);
    referenceSpectral = zeros(K, numFiles);
    wordLabels = zeros(1, numFiles);
    personIDs = zeros(1, numFiles);
    batchNumbers = zeros(1, numFiles);

    % Training loop
    for i = 1:numFiles
        % Extract word
        extractedWord = extractWord(fileNames(i));

        % Skip if no word detected
        if isempty(extractedWord)
            continue;
        end

        % Frame segmentation
        numFrames = floor((length(extractedWord) - frameSize) / frameStep) + 1;
        frames = zeros(frameSize, numFrames);
        for k = 1:numFrames
            startIdx = (k-1) * frameStep + 1;
            endIdx = startIdx + frameSize - 1;
            frames(:, k) = extractedWord(startIdx:endIdx);
        end

        % Compute ZCR & Energy
        logEnergy = log(sum(frames.^2));
        zcr = sum(abs(diff(sign(frames)))) / (2 * frameSize);

        % Compute spectral features
        spectralFeaturess = spectralFeatures(frames, K);

        % Store feature values
        referenceEnergy(i) = mean(logEnergy);
        referenceZCR(i) = mean(zcr);
        referenceSpectral(:, i) = spectralFeaturess;

        % Extract metadata from filename
        tokens = regexp(fileNames(i), 'c(\d+)_p(\d+)_s(\d+)\.wav', 'tokens');
        if ~isempty(tokens)
            wordLabels(i) = str2double(tokens{1}{1});
            personIDs(i) = str2double(tokens{1}{2});
            batchNumbers(i) = str2double(tokens{1}{3});
        else
            wordLabels(i) = -1;
            personIDs(i) = -1;
            batchNumbers(i) = -1;
        end
    end

    % Save reference data
    save(referenceFile, 'referenceZCR', 'referenceEnergy', 'referenceSpectral', 'wordLabels', 'personIDs', 'batchNumbers');
    fprintf('Training complete. Reference vectors saved to %s\n', referenceFile);
end
