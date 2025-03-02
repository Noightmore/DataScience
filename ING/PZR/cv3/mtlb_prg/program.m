%% Clear environment
clearvars; clc; close all;

%% User-defined parameters
fileLists = {'FileList2206.txt', 'FileList2207.txt', 'FileList2204.txt', 'FileListAll.txt'}; % List of datasets
testRatio = 0.2;  % Percentage of data used for testing (20%)
K = 16;           % Number of spectral bands

knnMethods = [1, 2, 3, 4];  % KNN methods to run
ltwMethods = [1, 2, 3, 4];  % LTW methods to run

%% Loop through each dataset
for i = 1:length(fileLists)
    fileList = fileLists{i}; 
    trainFileList = strrep(fileList, 'FileList', 'TrainFileList'); % Generate train file list name
    testFileList = strrep(fileList, 'FileList', 'TestFileList');   % Generate test file list name
    knnReferenceFile = strrep(fileList, 'FileList', 'KNN_reference_features');
    knnReferenceFile = strrep(knnReferenceFile, '.txt', '.mat'); 
    ltwReferenceFile = strrep(fileList, 'FileList', 'LTW_reference_features');
    ltwReferenceFile = strrep(ltwReferenceFile, '.txt', '.mat'); 


    % Display dataset name
    fprintf('\nProcessing Dataset: %s\n', fileList);

    %% Step 1: Split dataset into Train & Test
    fprintf('\nSplitting file list...\n');
    splitFileList(fileList, trainFileList, testFileList, testRatio);

    %% Step 2: Train KNN
    fprintf('\nTraining KNN...\n');
    trainKNN(trainFileList, knnReferenceFile, K);

    %% Step 3: Test KNN with selected methods
    fprintf('\nTesting KNN...\n');
    for method = knnMethods
        fprintf('Running KNN test with method %d...\n', method);
        testKNN(knnReferenceFile, testFileList, method);
    end

    %% Step 4: Train LTW
    fprintf('\nTraining LTW...\n');
    LTWtrain(trainFileList, ltwReferenceFile, K);

    %% Step 5: Test LTW with selected methods
    fprintf('\nTesting LTW...\n');
    for method = ltwMethods
        fprintf('Running LTW test with method %d...\n', method);
        LTWtest(ltwReferenceFile, testFileList, method);
    end
end

fprintf('\nAll experiments completed!\n');
