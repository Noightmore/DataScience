aby mel filtr linearni fazovy posun: FIR

info k cviku: solved examples on topics for Lecture 4

pokud v amplitudovym filtru nejsou jen cary -> malo vzorku

AA; BB = koeficienty u vystupu a vstupu diferencni rovnice

pridat bily sum k signaly v matlabu vygenerujeme iid randn
x = s + v
snr1 = 10*log10(sum(s.^2)/sum(v.^2));

pokud chceme upravit sum tak, aby desired snr = 10; udelame ekvivaletni upravy na snr1 vzorec

-> = 10*log10(Es/(sum of k v[n].^2)))

odvozeni vzorce pro k, konstanta kterou vynasobime sum, aby nam vysel desired snr.
pro urceni k musime uz znat existujici sum?
k = 10^-(snr/20) * sqrt(Es/Ev)

Es = sum(s.^2)
Ev = sum(v.^2)