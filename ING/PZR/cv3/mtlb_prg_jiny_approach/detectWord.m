% Function to detect word boundaries
function [wordStart, wordEnd] = detectWord(logEnergy, zcr, energyThresholdPercentage, zcrThresholdPercentage, frameStep, frameSize)
    wordStart = 0;
    wordEnd = 0;
    
    % Sort energy and ZCR values for thresholding
    sortedEnergy = sort(logEnergy);
    sortedZCR = sort(zcr);
    
    % Calculate dynamic thresholds
    lowEnergyMean = mean(sortedEnergy(1:round(0.1 * length(sortedEnergy))));
    highEnergyMean = mean(sortedEnergy(end-round(0.1 * length(sortedEnergy))+1:end));
    energyThreshold = lowEnergyMean + energyThresholdPercentage * (highEnergyMean - lowEnergyMean);
    
    lowZCRMean = mean(sortedZCR(1:round(0.1 * length(sortedZCR))));
    highZCRMean = mean(sortedZCR(end-round(0.1 * length(sortedZCR))+1:end));
    zcrThreshold = lowZCRMean + zcrThresholdPercentage * (highZCRMean - lowZCRMean);
    
    % Find word boundaries
    for k = 1:length(logEnergy)
        if logEnergy(k) > energyThreshold && zcr(k) > zcrThreshold
            if wordStart == 0
                wordStart = (k-1) * frameStep + 1;
            end
            wordEnd = (k-1) * frameStep + frameSize;
        end
    end
end