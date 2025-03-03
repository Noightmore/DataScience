function LTWtest(referenceFile, fileListPath, method)
    % LTWtest - Tests speech recognition using LTW and appends results to an Excel file.
    %
    % Usage:
    %   LTWtest('LTW_reference_features_all.mat', 'TestFileList.txt', 1);
    %
    % Inputs:
    %   referenceFile - Path to the reference feature file (MAT file)
    %   fileListPath - Path to the test file list (TXT file)
    %   method - Integer (1-4) selecting the evaluation method:
    %       1 -> Just Energy
    %       2 -> Energy + ZCR
    %       3 -> K Spectral Features
    %       4 -> All Features (Energy + ZCR + Spectral)

    if ~ismember(method, 1:4)
        error('Invalid method selection! Choose between 1-4.');
    end

    % Load reference features
    if exist(referenceFile, 'file') ~= 2
        error('Reference file %s not found!', referenceFile);
    end
    load(referenceFile);

    % Read test file list
    if exist(fileListPath, 'file') ~= 2
        error('Test file list %s not found!', fileListPath);
    end
    [testFiles, numTestFiles] = FileListRead(fileListPath);

    % Initialize accuracy counters
    correctPredictions = 0;
    totalPredictions = 0;

    % Metric selection mapping
    metricNames = ["Just Energy", "Energy + ZCR", "K Spectral Features", "All Features"];
    metricUsed = metricNames(method);

    % Loop through all test files
    for i = 1:numTestFiles
        % Extract word
        extractedWord = extractWord(testFiles(i));

        % Skip if no word detected
        if isempty(extractedWord)
            continue;
        end

        % Frame segmentation
        frameSize = 400;
        frameStep = 160;
        numFrames = floor((length(extractedWord) - frameSize) / frameStep) + 1;
        frames = zeros(frameSize, numFrames);
        for k = 1:numFrames
            startIdx = (k-1) * frameStep + 1;
            endIdx = startIdx + frameSize - 1;
            frames(:, k) = extractedWord(startIdx:endIdx);
        end

        % Compute ZCR, Energy & Spectral Features (full sequences)
        energySeq = log(sum(frames.^2));
        zcrSeq = sum(abs(diff(sign(frames)))) / (2 * frameSize);
        spectralSeq = spectralFeatures(frames, 16);

        % Compute LTW distances based on selected method
        distances = zeros(1, length(referenceEnergy));
        for j = 1:length(referenceEnergy)
            switch method
                case 1 % Just Energy
                    distances(j) = LTWDistance(energySeq, referenceEnergy{j});
                case 2 % Energy + ZCR
                    distEnergy = LTWDistance(energySeq, referenceEnergy{j});
                    distZCR = LTWDistance(zcrSeq, referenceZCR{j});
                    distances(j) = distEnergy + distZCR;
                case 3 % K Spectral Features
                    distances(j) = LTWDistance(spectralSeq, referenceSpectral{j});
                case 4 % All Features
                    distEnergy = LTWDistance(energySeq, referenceEnergy{j});
                    distZCR = LTWDistance(zcrSeq, referenceZCR{j});
                    distSpectral = LTWDistance(spectralSeq, referenceSpectral{j});
                    distances(j) = distEnergy + distZCR + distSpectral;
            end
        end

        % Find closest match
        [~, detectedIndex] = min(distances);
        detectedDigit = wordLabels(detectedIndex);

        % Extract actual digit from filename
        tokens = regexp(testFiles(i), 'c(\d+)_p(\d+)_s(\d+)\.wav', 'tokens');
        if ~isempty(tokens)
            actualDigit = str2double(tokens{1}{1});
        else
            actualDigit = -1;
        end

        % Count correct predictions
        if detectedDigit == actualDigit
            correctPredictions = correctPredictions + 1;
        end
        totalPredictions = totalPredictions + 1;

        % Display result
        fprintf('File: %s -> Detected: %d, Actual: %d\n', testFiles(i), detectedDigit, actualDigit);
    end

    % Compute & print accuracy
    if totalPredictions > 0
        accuracy = (correctPredictions / totalPredictions) * 100;
        fprintf('\nTesting Accuracy: %.2f%% (%d/%d correct)\n', accuracy, correctPredictions, totalPredictions);
    else
        fprintf('\nNo words detected, accuracy cannot be computed.\n');
        return;
    end

    %% ✅ **Append Results to Excel File (`Results.xlsx`)**
    excelFile = 'Results.xlsx';

    % Define table headers and data
    columnNames = {'Timestamp', 'Dataset Used', 'Reference File', 'Metric Used', 'Method Selected', 'Accuracy (%)'};
    timestamp = datestr(now, 'yyyy-mm-dd HH:MM:SS');
    methodSelected = "LTW - " + metricUsed;
    rowData = {timestamp, fileListPath, referenceFile, metricUsed, methodSelected, accuracy};

    % Check if file exists
    if isfile(excelFile)
        % Append data
        try
            existingData = readcell(excelFile);  % Read existing data
            newData = [existingData; rowData];   % Append new row
            writecell(newData, excelFile);       % Save updated data
        catch
            warning('Could not read existing Excel file, writing a new one.');
            newData = [columnNames; rowData];
            writecell(newData, excelFile);
        end
    else
        % Create file with headers
        newData = [columnNames; rowData];
        writecell(newData, excelFile);
    end

    fprintf('\nResults saved to %s\n', excelFile);
end
