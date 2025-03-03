function d = LTWDistance(X, R)
    % LTWDistance - Computes Linear Time Warping (LTW) distance 
    % by resampling the reference sequence to match the test word length.
    %
    % Usage:
    %   d = LTWDistance(X, R)
    %
    % Input:
    %   X - Feature matrix of the test word (PxI), P = num. of features, I = num. frames
    %   R - Feature matrix of the reference word (PxJ), P = num. of features, J = num. frames
    %
    % Output:
    %   d - LTW distance (scalar)

    [P, I] = size(X);  % I = Frames in test word, P = Number of features
    [~, J] = size(R);  % J = Frames in reference word
    
    % Compute warping function (resampling indices)
    w = round(linspace(1, J, I));  % Map I frames to J
    
    % Resample the reference to match the test word
    R_warped = R(:, w);  % Interpolate or duplicate frames
    
    % Compute Euclidean distance between X and resampled R
    d = sum(vecnorm(X - R_warped, 2, 1));  % Sum over frames
end
