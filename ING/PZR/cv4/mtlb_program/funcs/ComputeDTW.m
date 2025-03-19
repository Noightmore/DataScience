% function [globalDistance, A, B] = ComputeDTW(refFeatures, testFeatures, weights)
% % ComputeDTW - Compute the DTW distance between two feature sequences with axes swapped,
% % and restrict the number of consecutive horizontal moves to at most 1.
% %
% % In this version, the reference word is along the Y axis (rows) and the test
% % word (the one to classify) is along the X axis (columns).
% %
% % Inputs:
% %   refFeatures  - A J x P matrix (J frames, P features) for the reference word.
% %   testFeatures - An I x P matrix (I frames, P features) for the test word.
% %   weights      - A 1 x P vector containing weights for each feature.
% %                  (If not provided, equal weights are used.)
% %
% % Outputs:
% %   globalDistance - The DTW distance computed as A(J, I+2).
% %   A              - The accumulated cost matrix (size J x (I+2)).
% %   B              - The backtracking pointer matrix (same size as A).
% %
% % Note: This implementation uses the weighted Euclidean distance as the local
% %       distance measure and allows transitions from (j-1, i-2), (j-1, i-1) and 
% %       (j-1, i) with an additional restriction that at most one consecutive 
% %       horizontal move (i.e. move with no change in test index) is allowed.
% 
% if nargin < 3 || isempty(weights)
%     weights = ones(1, size(testFeatures, 2));
% end
% 
% % Dimensions:
% % J = number of frames in reference (vertical axis)
% % I = number of frames in test (horizontal axis)
% J = size(refFeatures, 1);
% I = size(testFeatures, 1);
% 
% % Use an offset of 2 for the test dimension so that allowed transitions are:
% % from (j-1, i+2-2) = (j-1, i), (j-1, i+2-1) = (j-1, i+1), and (j-1, i+2) = (j-1, i+2).
% A = inf(J, I+2);
% B = zeros(J, I+2);  % pointers: 1 for move from col-2, 2 for col-1, 3 for col (horizontal)
% 
% % Auxiliary matrix H to count consecutive horizontal moves.
% H = zeros(J, I+2);  % H(j, col) gives number of consecutive horizontal moves on best path to that cell.
% 
% % Precompute the local distance matrix dMat (size J x I)
% dMat = zeros(J, I);
% for j = 1:J
%     for i = 1:I
%         diff = refFeatures(j,:) - testFeatures(i,:);
%         dMat(j, i) = sqrt(sum(weights .* (diff.^2)));
%     end
% end
% 
% % --- Initialization ---
% % For the first row (j = 1), set A(1,3) equal to dMat(1,1).
% A(1, 3) = dMat(1, 1);
% % H remains 0 in row 1 (no moves yet). The first two columns are boundary placeholders.
% 
% % --- Main dynamic programming loop ---
% for j = 2:J
%     for i = 1:I
%         col = i + 2;  % current cell index in test dimension
%         % Allowed previous positions from row j-1:
%         % candidate1: (j-1, col-2) --> diagonal move; resets horizontal count to 0.
%         cost1 = A(j-1, col-2);
%         h1 = 0;
% 
%         % candidate2: (j-1, col-1) --> diagonal move; resets horizontal count to 0.
%         cost2 = A(j-1, col-1);
%         h2 = 0;
% 
%         % candidate3: (j-1, col)   --> horizontal move.
%         % The new horizontal count would be H(j-1, col) + 1.
%         h3 = H(j-1, col) + 1;
%         if H(j-1, col) >= 1
%             % If already one horizontal move, disallow another.
%             cost3 = Inf;
%         else
%             cost3 = A(j-1, col);
%         end
% 
%         % Collect candidate costs
%         candidateCosts = [cost1, cost2, cost3];
%         [minPrev, minIdx] = min(candidateCosts);
% 
%         % Update A(j, col): local cost + minimal previous cost.
%         A(j, col) = dMat(j, i) + minPrev;
% 
%         % Update pointer matrix B.
%         B(j, col) = minIdx;
% 
%         % Update horizontal count H.
%         if minIdx == 3
%             H(j, col) = h3;  % candidate3's horizontal count.
%         else
%             H(j, col) = 0;   % diagonal moves reset horizontal count.
%         end
%     end
% end
% 
% % The global DTW distance is the accumulated cost at (J, I+2)
% globalDistance = A(J, I+2);
% 
% end









function [globalDistance, A, B] = ComputeDTW(testFeatures, refFeatures, weights)
% ComputeDTW - Compute the DTW distance between two feature sequences with axes swapped,
% applying the offset only to the reference data (columns).
%
% In this version, the test word is along the vertical axis (rows) and the 
% reference word (the one to classify) is along the horizontal axis (columns).
%
% Inputs:
%   testFeatures  - An I x P matrix (I frames, P features) for the test word.
%   refFeatures   - A J x P matrix (J frames, P features) for the reference word.
%   weights       - A 1 x P vector containing weights for each feature.
%                   (If not provided, equal weights are used.)
%
% Outputs:
%   globalDistance - The DTW distance computed as A(I, J+2).
%   A              - The accumulated cost matrix (size I x (J+2)).
%   B              - The backtracking pointer matrix (same size as A).
%
% Note: This implementation uses the weighted Euclidean distance as the local
%       distance measure and allows transitions from (i-1, j-2), (i-1, j-1) and 
%       (i-1, j) with an additional restriction that at most one consecutive 
%       horizontal move (i.e. move with no change in reference index) is allowed.

if nargin < 3 || isempty(weights)
    weights = ones(1, size(testFeatures, 2));
end

% Dimensions:
% I = number of frames in test (vertical axis)
% J = number of frames in reference (horizontal axis)
I = size(testFeatures, 1);
J = size(refFeatures, 1);

% Use an offset of 2 for the reference (horizontal) axis.
A = inf(I, J+2);
B = zeros(I, J+2)';  % pointers: 1 for move from col-2, 2 for col-1, 3 for col (horizontal)

% Auxiliary matrix H to count consecutive horizontal moves.
H = zeros(I, J+2);  % H(i, col) gives the number of consecutive horizontal moves on the best path to that cell.

% Precompute the local distance matrix dMat (size I x J)
dMat = zeros(I, J);
for i = 1:I
    for j = 1:J
        diff = testFeatures(i,:) - refFeatures(j,:);
        dMat(i, j) = sqrt(sum(weights .* (diff.^2)));
    end
end

% --- Initialization ---
% For the first row (i = 1), set A(1,3) equal to dMat(1,1).
A(1, 3) = dMat(1, 1);
% The first two columns serve as boundary placeholders; H remains 0.

% --- Main dynamic programming loop ---
for i = 2:I
    for j = 1:J
        col = j + 2;  % current cell index in the reference (horizontal) dimension
        % Allowed previous positions from row i-1:
        % candidate1: (i-1, col-2) --> diagonal left move; resets horizontal count.
        cost1 = A(i-1, col-2);
        
        % candidate2: (i-1, col-1) --> diagonal right move; resets horizontal count.
        cost2 = A(i-1, col-1);
        
        % candidate3: (i-1, col)   --> horizontal move.
        % Increase horizontal count.
        h3 = H(i-1, col) + 1;
        if H(i-1, col) >= 1
            cost3 = Inf; % disallow if already one horizontal move
        else
            cost3 = A(i-1, col);
        end
        
        candidateCosts = [cost1, cost2, cost3];
        [minPrev, minIdx] = min(candidateCosts);
        
        % Update A(i, col) with local cost plus minimum previous cost.
        A(i, col) = dMat(i, j) + minPrev;
        
        % Set pointer B accordingly.
        B(i, col) = minIdx;
        
        % Update horizontal move counter.
        if minIdx == 3
            H(i, col) = h3;
        else
            H(i, col) = 0;
        end
    end
end

% The global DTW distance is taken at the last row and last column.
globalDistance = A(I, J+2);

end
