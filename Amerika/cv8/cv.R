# pr 9 z centralni limitni vety
x_tilde  <- 90
smer_od <- 10
soucet <- 64
# vaha nesmi prekrocit 6000
# N (ny = 64*90, smer_od^2 = (64*10)^2)
# N (ny = soucet*x_tilde, (soucet*smer_odchylka)^2)
# P = 1 - normcdf(6000, 64 * 90, sqrt(6400))

# normcdf spocita jaka je pravdepodobnost ze neprokroci? asi
# 1 - normcdf je obracena pravdepodobnost