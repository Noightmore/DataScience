function [detectedWords, wordStarts, wordEnds] = xtractWords(filePath, L)
    if nargin < 2
        L = 1000;  % Default moving average filter length
    end

    % Load the audio file
    [x, Fs] = audioread(filePath);
    x = double(x);
    
    % If stereo (2 columns), convert to mono by averaging the channels
    if size(x, 2) == 2  
        x = mean(x, 2); 
    end

    % Remove DC offset
    x = x - mean(x);

    % Compute instantaneous power
    powerSignal = x.^2;

    % Apply Moving Average (MA) filter
    h = ones(1, L) / L;
    smoothedPower = filter(h, 1, powerSignal);

    % Shift correction due to MA filtering (delay of L/2)
    smoothedPower = [smoothedPower(L/2+1:end); zeros(L/2, 1)];

    % Adaptive threshold for energy-based detection
    threshold = 0.2 * mean(smoothedPower) + 0.1 * std(smoothedPower); % adjust sensitivity

    % Define silence constraints
    minSilenceDuration = round(0.3 * Fs);  % Silence must be at least 0.3s to separate words

    % Detect high-energy speech regions
    speechRegions = smoothedPower > threshold;
    
    wordStarts = [];
    wordEnds = [];
    inWord = false;
    lastEnd = 0;

    for i = 1:length(speechRegions)
        if speechRegions(i) && ~inWord
            % Start a word when entering a speech region
            if i - lastEnd > minSilenceDuration
                wordStarts = [wordStarts; i];
                inWord = true;
            end
        elseif ~speechRegions(i) && inWord
            % End word detection when silence is detected
            wordEnds = [wordEnds; i];
            lastEnd = i;
            inWord = false;
        end
    end

    % Ensure word ends are set correctly
    if inWord
        wordEnds = [wordEnds; length(speechRegions)];
    end

    % Convert sample indices to time (in seconds)
    wordStartTimes = wordStarts / Fs;
    wordEndTimes = wordEnds / Fs;

    % Extract detected words
    detectedWords = cell(length(wordStarts), 1);
    for i = 1:length(wordStarts)
        if wordEnds(i) <= length(x)
            detectedWords{i} = x(wordStarts(i):wordEnds(i));
        else
            detectedWords{i} = x(wordStarts(i):end);
        end
    end

    % Improved Visualization
    t = (1:length(x)) / Fs;  % Time axis in seconds

    figure;
    
    % **Plot Only the Speech Signal (New Plot)**
    subplot(3,1,1);
    plot(t, x, 'b');  
    title('Raw Speech Signal');
    xlabel('Time (seconds)');
    ylabel('Amplitude');
    grid on;

    % **Plot Speech Signal with Detected Word Boundaries**
    subplot(3,1,2);
    plot(t, x, 'b');  % Use actual time for x-axis
    hold on;
    for i = 1:length(wordStarts)
        xline(wordStartTimes(i), 'r', 'LineWidth', 1.5);
        xline(wordEndTimes(i), 'g', 'LineWidth', 1.5);
    end
    title('Speech Signal with Detected Word Boundaries');
    xlabel('Time (seconds)');  
    ylabel('Amplitude');
    legend('Speech Signal', 'Word Start', 'Word End', 'Location', 'eastoutside');
    grid on;

    % **Plot Smoothed Power**
    subplot(3,1,3);
    plot((1:length(smoothedPower)) / Fs, smoothedPower, 'k');  
    hold on;
    yline(threshold, 'r--', 'Threshold', 'LineWidth', 1.5);
    title('Smoothed Power with Detection Threshold');
    xlabel('Time (seconds)');
    ylabel('Power');
    grid on;

    fprintf('\nDetected words: %d\n', length(wordStarts));
    for i = 1:length(wordStarts)
        fprintf('Word %d: Start = %.2f sec, End = %.2f sec\n', i, wordStartTimes(i), wordEndTimes(i));
    end

    if isempty(wordStarts)
        disp('No words detected.');
    end
end
