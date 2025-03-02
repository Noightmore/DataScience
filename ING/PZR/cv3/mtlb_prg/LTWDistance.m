function d = LTWDistance(seq1, seq2, windowSize)
    % LTWDistance - Computes Local Temporal Warping (LTW) distance
    % with a constrained DTW algorithm
    %
    % Usage:
    %   d = LTWDistance(seq1, seq2, windowSize)
    %
    % Input:
    %   seq1 - Feature vector of test word (Nx1)
    %   seq2 - Feature vector of reference word (Mx1)
    %   windowSize - Constraint (Sakoe-Chiba band width)
    %
    % Output:
    %   d - LTW distance (scalar)

    N = length(seq1);
    M = length(seq2);
    
    % Initialize cost matrix with infinity
    DTW = inf(N + 1, M + 1);
    DTW(1, 1) = 0; % Start from (0,0)
    
    % Compute DTW with window constraint
    for i = 2:N+1
        for j = max(2, i - windowSize) : min(M+1, i + windowSize)
            cost = abs(seq1(i-1) - seq2(j-1));
            DTW(i, j) = cost + min([DTW(i-1, j), DTW(i, j-1), DTW(i-1, j-1)]);
        end
    end

    % Return final LTW distance
    d = DTW(N+1, M+1);
end
