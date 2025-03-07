# kriteria pro vyber filtru
- jednoduchost (nizky rad filtru)
- parametrizace, rychle ovladani freq characteristiky
- minimalni zpozdeni, pod 1ms
- numericka stabilita

## typy filtru
- notch -- k potlaceni harmonicke slozky signalu
- comb -- zesileni/odstraneni harmonicke slozky a jejiho nasobku
- navrh pomoci nul a polu

navrh ve filter designer in matlab

- todo: jak navhnout filter co filtruje specifickou frekvenci

phi = 2*pi*f/fs
fvtool([1 -2*cos(phi) 1], 1, 'fs', 8000)

eps = 1-0.1;
fvtool([1 -2*cos(phi) 1], [1 -2*eps*cos(phi) eps^2], 'fs', 8000)
t = 0:1/8000::2-1/8000;
s = sin(2*pi*1000*t)
plot(t, s)
sounds(s, 8000)

y = filter([1 -2*cos(phi) 1], [1 -2*eps*cos(phi) eps^2], s)
soundsc(y, 8000)
plot(y)

kazdy filter ma nabeh