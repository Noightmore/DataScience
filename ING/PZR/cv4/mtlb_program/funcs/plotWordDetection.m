function plotWordDetection(filePath, wordStart, wordEnd, logEnergy, zcr, spectralFeatures)
    % Load original audio for visualization
    [x, fs] = audioread(filePath);
    x = double(x);
    
    % Time axis for the original waveform
    time = (0:length(x)-1) / fs;
    
    % Frame axis for logEnergy and ZCR
    numFrames = length(logEnergy);
    frameTime = linspace(0, max(time), numFrames);
    
    % Create figure
    figure;

    % 1️⃣ **Plot Original Waveform**
    subplot(3,1,1);
    plot(time, x, 'b', 'LineWidth', 1);
    hold on;
    
    % Highlight detected word boundaries
    if wordStart > 0 && wordEnd > 0
        wordTimeStart = wordStart / fs;
        wordTimeEnd = wordEnd / fs;
        xline(wordTimeStart, 'g--', 'LineWidth', 2); % Start boundary
        xline(wordTimeEnd, 'r--', 'LineWidth', 2); % End boundary
    end
    
    title(['Original Waveform - ', filePath], 'Interpreter', 'none');
    xlabel('Time (s)');
    ylabel('Amplitude');
    legend({'Waveform', 'Start', 'End'});
    grid on;
    
    % 2️⃣ **Plot Log Energy and ZCR Together**
    subplot(3,1,2);
    yyaxis left;
    plot(frameTime, logEnergy, 'r', 'LineWidth', 1.5);
    ylabel('Log Energy');
    
    yyaxis right;
    plot(frameTime, zcr, 'k--', 'LineWidth', 1.2);
    ylabel('Zero-Crossing Rate');
    
    title('Log Energy & ZCR Over Time');
    xlabel('Time (s)');
    legend({'Log Energy', 'ZCR'}, 'Location', 'northwest');
    grid on;
    
    % 3️⃣ **Plot Spectral Features**
    subplot(3,1,3);
    bar(spectralFeatures, 'FaceColor', [0 0.7 0.7]); % Bar graph for spectral features
    title('Spectral Features (Mean over Frames)');
    xlabel('Frequency Bands');
    ylabel('Mean Amplitude');
    grid on;

    % Display the figure
    sgtitle('Word Detection & Feature Analysis');
end
