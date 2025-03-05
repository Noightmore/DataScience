y[n] = 1/3 (x[n] + x[n-1] + x[n-2])

- je kauzalni v bode 0
- je stabilni
- FIR filter

impulsni odezva:
udelat h[n] = 1/3 (d[n] + d[n-1] + d[n-2]) 

frekvencni charakteristiku (dtft):
- dle pomocne tabulky v prezentaci

H(e^iw) = 1/3(1 + e^-jw + e^-j2)

|H(e^jw)| w = pi/2; = abs(1/3*(1 + e^-j*pi/2 + e^-j*2*pi/2)) = abs(1/3*(1 + j + 1)) 
= abs(1/3 * (1 - j - j)) = abs(-j/3)= 1/3

arg(-j/3) = -pi/2


-> zmensi amplitudu na 1/3, posune  o -pi/2

fazovy zpozdeni: Tau = -q(w)/w = 1 ; zpozduje prave o 1 vzorek

------------------------------------------------------------

IIR filter:

y[n] = x[n] + 1/2 y[n-1]

nejprve musime udelat dtf:

y(e^-jw) = X(e^jw) + 1/2 Y(e^jw) * Y(e^-jw1)
H(e^jw) = Y(e^jw)/X(e^jw)
Y(e^jw)*(1-1/2e^-jw) = X(e^jw)

 pak prevedeme do impulzni odezvy, nelze dat do impulsni odezvy primo
y(e^jw)/X(e^jw) = 1/(1-1/2e^-jw)

h[n] = 1/2^n u[n] ; dle tabulky v te prezentaci

3. bod destiminutovky -- prevody mezi popisy LTI systemu

-------------------------------------------------------

reseni diferencni rovnice: analyticky filtrovani

y[n] = 3/4 y[n-1] - 1/8y[n-2] + x[n] - x[n-1]

x[n] = d[n]

y[n] = [-2* (1/2)^n + 3* (1/4)^n]u[n]

matlab script:

N = 20
n = 0:N-1
y_n = -2* (1/2).^n + 3* (1/4).^n;

stem(n,y_n), 'LineWidth', 2)

b = [1 -2]
a = [1 -3/4 1/8]
imp = [1;zeros(N-1,1)];
y_n = filter(b,a,imp);

hold on
stem(n,y_n)

energie chybovosti signalu?
(y_a - y_n').^2 

kdyz vyjde cista nula, melo by to byt co nejbliž k nule

-------------------------------------------------------

jaka je odezva filtru na vstupni signal:

x[n] = 1/2^n u[n]
h[n] = 1/3^n u[n]
y[n] = x[n] * h[n]

dtft:

Y(e^jw) = X(e^jw) * H(e^jw)

Y(e^jw) = 1/(1-1/2e^-jw) * 1/(1-1/3e^-jw)

idtft:

parcialni zlomky...

Y(e^jw) = A/(1-1/2e^-jw) + B/(1-1/3e^-jw)

A * (1 - 1/3e^-jw) + B * (1 - 1/2e^-jw) = 1:

resime soustavu rovnic (vyjadrime to axiomy o polynomech):

- rovnaji se koeficienty u e^jw, nebo koeficienty u 
A + B = 1
-1/3*A - 1/2*B = 0

B = -2
A = 3

vysledek:
y[n] = (3 * 1/2^n - 2 * 1/3^n)u[n]

upravy dle tabulky...

tohle je 4. bod z prikladu do desetiminutovky

----------------------------

prednaska:

magnituda: abs of amplituda

proc ma filter zpozdeni N/2?

h[n] = 1/3(d[n] + d[n-1] + d[n-2])
H(e^jw) = 1/3(1 + e^-jw + e^-j2w)

vytknu clen uprostred

H(e^jw) e^-jw * 1/3 * (e^jw + 1 + e^-jw)
= e^-jw * 1/3 * (1+2cos(w))


SNR = vysoke -> dobry signal

snr = 10 log_base10(Es/Ev)

Es = (s^2 = v^2 + 2sv)
2sv = korelace sumu k signalu, pokud sum se signalem nesouvisi, muzeme ignorovat tuto cast

