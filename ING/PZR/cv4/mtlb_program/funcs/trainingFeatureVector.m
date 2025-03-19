%% Helper function (as a nested function) to ensure 1-D features are column vectors
function vec = trainingFeatureVector(feature)
    vec = feature(:);
end