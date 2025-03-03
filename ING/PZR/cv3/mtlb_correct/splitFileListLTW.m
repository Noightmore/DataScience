function splitFileListLTW(fileListPath, trainFilePath, testFilePath)
    % splitFileListLTW - Reads a file list, splits it into training (batch s1)
    % and testing (remaining batches), ensuring a balanced distribution
    % of each digit (c0-c9) across both sets.
    %
    % Usage:
    %   splitFileListLTW('FileList.txt', 'TrainFileList.txt', 'TestFileList.txt');
    %
    % Inputs:
    %   fileListPath - Path to the input file containing file paths.
    %   trainFilePath - Output file path for training set.
    %   testFilePath - Output file path for testing set.

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

    % Group files into training (s01) and testing (s02-s05)
    trainFiles = [];
    testFiles = [];

    for i = 1:numFiles
        % Extract digit and batch number (e.g., 'c3_p2207_s01.wav' from 'p2207/c3_p2207_s01.wav')
        tokens = regexp(fileNames(i), '.*/c(\d+)_p\d+_s(\d+)\.wav$', 'tokens');  
        
        if ~isempty(tokens)
            digit = tokens{1}{1};  % Extract digit (e.g., '3')
            batch = tokens{1}{2};  % Extract batch number (e.g., '01')

            if strcmp(batch, '01')  % Training set: only s01 samples
                trainFiles = [trainFiles; fileNames(i)];
            else  % Testing set: all other batches (s02-s05)
                testFiles = [testFiles; fileNames(i)];
            end
        end
    end

    % Write TrainFileList_LTW.txt
    fileID = fopen(trainFilePath, 'w');
    if fileID == -1
        error('Error: Could not write to file %s', trainFilePath);
    end
    fprintf(fileID, '%s\n', trainFiles);
    fclose(fileID);

    % Write TestFileList_LTW.txt
    fileID = fopen(testFilePath, 'w');
    if fileID == -1
        error('Error: Could not write to file %s', testFilePath);
    end
    fprintf(fileID, '%s\n', testFiles);
    fclose(fileID);

    fprintf('File list split completed:\n');
    fprintf('Training set (s01 only): %d files\n', length(trainFiles));
    fprintf('Testing set (s02-s05): %d files\n', length(testFiles));
end
