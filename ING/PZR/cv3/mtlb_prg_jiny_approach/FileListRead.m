function [fileNames, numFiles] = FileListRead(filePath)
    % FileListsRead - Reads a list of file paths from a text file.
    %
    % Usage:
    %   [fileNames, numFiles] = FileListsRead('FileList.txt');
    %
    % Input:
    %   filePath - Path to the text file containing file paths.
    %
    % Output:
    %   fileNames - String array containing file paths.
    %   numFiles  - Number of files in the list.

    % Open the file
    fileID = fopen(filePath, 'r');
    if fileID == -1
        error('Error: Could not open file %s', filePath);
    end

    % Read the file contents
    textdata = textscan(fileID, '%s');  

    % Close the file
    fclose(fileID);  

    % Convert to string array
    fileNames = string(textdata{:}); 
    numFiles = size(fileNames, 1);  
end
