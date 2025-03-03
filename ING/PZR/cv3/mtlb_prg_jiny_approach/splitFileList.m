function splitFileList(fileListPath, trainFilePath, testFilePath, testRatio)
    % splitFileList - Reads a file list, shuffles the lines, and splits it
    % into training and testing sets while ensuring a balanced distribution
    % of each digit (c0-c9) across both sets.
    %
    % Usage:
    %   splitFileList('FileList.txt', 'TrainFileList.txt', 'TestFileList.txt', 0.2);
    %
    % Inputs:
    %   fileListPath - Path to the input file containing file paths.
    %   trainFilePath - Output file path for training set.
    %   testFilePath - Output file path for testing set.
    %   testRatio - Proportion of data used for testing (e.g., 0.2 for 20% test).
    
    % Read the file list
    fileID = fopen(fileListPath, 'r');
    if fileID == -1
        error('Error: Could not open file %s', fileListPath);
    end
    textdata = textscan(fileID, '%s', 'Delimiter', '\n'); 
    fclose(fileID);

    % Convert to string array
    fileNames = string(textdata{:});
    numFiles = length(fileNames);
    
    if numFiles == 0
        error('Error: File %s is empty or not readable.', fileListPath);
    end
    
    % Group files by digit (c0-c9)
    digitGroups = containers.Map;
    for i = 1:numFiles
        % Extract the digit from the filename (e.g., c3 from c3_p2206_s01.wav)
        tokens = regexp(fileNames(i), 'c(\d+)_p\d+_s\d+\.wav', 'tokens');
        if ~isempty(tokens)
            digit = tokens{1}{1}; % Extract digit as string (e.g., '3')
            if ~isKey(digitGroups, digit)
                digitGroups(digit) = [];
            end
            digitGroups(digit) = [digitGroups(digit); fileNames(i)];
        end
    end

    % Initialize training and testing sets
    trainFiles = [];
    testFiles = [];

    % Process each digit group separately
    digitKeys = keys(digitGroups);
    for k = 1:length(digitKeys)
        digit = digitKeys{k};
        files = digitGroups(digit);

        % Shuffle the files for randomness
        rng('shuffle');
        files = files(randperm(length(files)));

        % Determine the split indices
        numTest = round(length(files) * testRatio);
        numTrain = length(files) - numTest;

        % Assign files to training and testing sets
        trainFiles = [trainFiles; files(1:numTrain)];
        testFiles = [testFiles; files(numTrain+1:end)];
    end

    % Write TrainFileList.txt
    fileID = fopen(trainFilePath, 'w');
    if fileID == -1
        error('Error: Could not write to file %s', trainFilePath);
    end
    fprintf(fileID, '%s\n', trainFiles);
    fclose(fileID);

    % Write TestFileList.txt
    fileID = fopen(testFilePath, 'w');
    if fileID == -1
        error('Error: Could not write to file %s', testFilePath);
    end
    fprintf(fileID, '%s\n', testFiles);
    fclose(fileID);

    fprintf('File list split completed:\n');
    fprintf('Training set: %d files\n', length(trainFiles));
    fprintf('Testing set: %d files\n', length(testFiles));
end
