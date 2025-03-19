function saveFeatures(audioFilePath, data_path, wordStart, wordEnd, logEnergy, zcr, spectralFeatures)
    % Ensure the output directory exists
    if ~exist(data_path, 'dir')
        mkdir(data_path);
    end

    % Extract filename from the full path
    [~, fileName, ~] = fileparts(audioFilePath);
    
    % Use regular expression to extract `c`, `pXXXX`, and `sXX`
    tokens = regexp(fileName, 'c(\d+)_p(\d+)_s(\d+)', 'tokens');
    
    if isempty(tokens)
        disp('❌ Filename format not recognized. Skipping.');
        return;
    end
    
    % Extract values
    tokens = tokens{1}; % Convert to cell array
    c = str2double(tokens{1});    % Convert "c0" → 0, "c1" → 1, etc.
    pID = tokens{2};              % Extract "p2501"
    sID = tokens{3};              % Extract "s01"
    
    % Define output file path using the full filename
    outputFile = fullfile(data_path, [fileName, '_features.mat']);

    % Save all extracted features to the `.mat` file
    save(outputFile, 'audioFilePath', 'wordStart', 'wordEnd', 'logEnergy', 'zcr', 'spectralFeatures', 'c');

    disp(['✅ Features saved to: ', outputFile]);
end
