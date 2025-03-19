function aggregatedFeatures = aggregateFeatures(aggregatedFeatures, audioFilePath, wordStart, wordEnd, logEnergy, zcr, spectralFeatures)
    % Extract filename from the full path
    [~, fileName, ~] = fileparts(audioFilePath);
    
    % Use regular expression to extract c, pID, and sID from filename
    tokens = regexp(fileName, 'c(\d+)_p(\d+)_s(\d+)', 'tokens');
    
    if isempty(tokens)
        disp('❌ Filename format not recognized. Skipping.');
        return;
    end
    
    % Extract values from tokens (assume tokens{1} = {c, pID, sID})
    tokens = tokens{1}; % Convert to cell array of strings
    c = str2double(tokens{1});    % e.g. "c0" becomes 0
    pID = ['p', tokens{2}];         % e.g. "p2501"
    sID = tokens{3};              % e.g. "s01"
    
    % Create a new feature entry structure for this file
    newEntry = struct();
    newEntry.audioFilePath = audioFilePath;
    newEntry.wordStart = wordStart;
    newEntry.wordEnd = wordEnd;
    newEntry.logEnergy = logEnergy;
    newEntry.zcr = zcr;
    newEntry.spectralFeatures = spectralFeatures;
    newEntry.c = c;
    newEntry.sID = sID;
    
    % Append this new entry to the aggregated features for the user pID
    if ~isfield(aggregatedFeatures, pID)
        % Create a new entry (as a structure array)
        aggregatedFeatures.(pID) = newEntry;
    else
        % Append to the existing structure array
        aggregatedFeatures.(pID)(end+1) = newEntry;
    end
end
