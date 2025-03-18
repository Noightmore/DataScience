matlab:

des_fs = 8000
des2_fs = 16000

[x,x_fs] = audioread()

x_8K = resample(x,des_fs,x_fs); % podvzorkujeme, zahodime  vyssi frekvence
soundsc(audio, des_fs)

% x_16K = resample(x,des2_fs,x_fs);

% nadvzorkovani
x_16k = zeros(size(x_8k)*2, 1);

x_16k(1:2:end) = x_8k;