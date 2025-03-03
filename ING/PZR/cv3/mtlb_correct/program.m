%% Clear environment
clearvars; clc; close all;

%% User-defined parameters
fileLists = {'FileList2206.txt', 'FileList2203.txt', 'FileList2207.txt', 'FileList2204.txt', 'FileListAll.txt'}; % List of datasets
testRatio = 0.2;  % Percentage of data used for testing (20%)
K = 16;           % Number of spectral bands

knnMethods = [1, 2, 3, 4];  % KNN methods to run
ltwMethods = [1, 2, 3, 4];  % LTW methods to run

%% Loop through each dataset
for i = 1:length(fileLists)
    fileList = fileLists{i};

    %% Generate filenames for KNN
    trainFileListKNN = strrep(fileList, 'FileList', 'TrainFileList_KNN'); % KNN train file
    testFileListKNN = strrep(fileList, 'FileList', 'TestFileList_KNN');   % KNN test file
    knnReferenceFile = strrep(fileList, 'FileList', 'KNN_reference_features');
    knnReferenceFile = strrep(knnReferenceFile, '.txt', '.mat'); 

    %% Generate filenames for LTW
    trainFileListLTW = strrep(fileList, 'FileList', 'TrainFileList_LTW'); % LTW train file
    testFileListLTW = strrep(fileList, 'FileList', 'TestFileList_LTW');   % LTW test file
    ltwReferenceFile = strrep(fileList, 'FileList', 'LTW_reference_features');
    ltwReferenceFile = strrep(ltwReferenceFile, '.txt', '.mat'); 

    % Display dataset name
    fprintf('\nProcessing Dataset: %s\n', fileList);

    %% Step 1: Split dataset into Train & Test for KNN
    fprintf('\nSplitting file list for KNN...\n');
    splitFileList(fileList, trainFileListKNN, testFileListKNN, testRatio);

    %% Step 2: Split dataset into Train & Test for LTW
    fprintf('\nSplitting file list for LTW...\n');
    splitFileListLTW(fileList, trainFileListLTW, testFileListLTW);

    %% Step 3: Train KNN
    fprintf('\nTraining KNN...\n');
    trainKNN(trainFileListKNN, knnReferenceFile, K);

    %% Step 4: Test KNN with selected methods
    fprintf('\nTesting KNN...\n');
    for method = knnMethods
        fprintf('Running KNN test with method %d...\n', method);
        testKNN(knnReferenceFile, testFileListKNN, method);
    end

    %% Step 5: Train LTW
    fprintf('\nTraining LTW...\n');
    LTWtrain(trainFileListLTW, ltwReferenceFile, K);

    %% Step 6: Test LTW with selected methods
    fprintf('\nTesting LTW...\n');
    for method = ltwMethods
        fprintf('Running LTW test with method %d...\n', method);
        LTWtest(ltwReferenceFile, testFileListLTW, method);
    end
end

fprintf('\nAll experiments completed!\n');
