matlab:

nfft = 800;
hamming(win_N); % hammingovo okno, prekryv signalu, ve vykreslovani signalu ve spec
nula = 0;
figure; [X, aw] = spectogram(x,win,nula,win_N,x_fs,'yaxis'); colormap jet;

% navratovy parametr prikazu spectrogram je matice komplexnich cisel, jen pulka protoze spec je symmetricky
% ta dalsi cast hodnot je casova slozka. Blba implementace to vsechno rvat do 1D vektoru

L = size(X,2);
for lpL = 1:L
    figure;findpeaks(abs(X(:,lpL)), ax_aw); % hledani vrcholu
    % abs tam je kvuli amplitude, komplexni cisla
end