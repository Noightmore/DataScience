# kapitola 8.6 prehled testu
# pr. 5
# [h, p, ci, stats] = ttest(x, 8.8,  0.05, 'both')

# v pisemce bude potreba intepretace vysledku, nejen vzorec

# pr. 1
# stroj ma sackovani smazenych bramburku  vyrabi  100 gramove sacky. Stroj ma  povolenou maximalni smerodatnou
# odchylku 1.5g na jeden sacek (rozptyl 2.25 g^2) data jsou ulozena v souboru P0801.mat

#  vypoctete z dat rozptyl. Uvedte hypotezu H0 a H1. Otestujte na hladine vyznamnosti 5 %,
#  zda je tato smerodatna odchylka splnena

library(R.matlab)

file <- readMat("Amerika/cv10/P0801.mat") # .mat file

# convert x to vector
x <- as.vector(file)
# get rid off nonnumeric values
x <- x[!is.na(x)]

# convert each item of vector x to be numeric
x <- as.numeric(unlist(x))

# in matlab: vartest(x, 2.25, 0.05, 'both')

# idk, not what is expected
# hypoteza H0, ze rozptyl je mensi nebo roven 2.25 g^2 prijimame, pvalue = 0.3798

# incorrect
#H0 <- t.test(x, mu = 2.25, alternative = "two.sided", conf.level = 0.95)
#H <- var.test(x, y = 2.25, alternative = "two.sided", conf.level = 0.95)

print(H0)
#H0 <- var.test(x, x, mu=0, alternative = "two.sided", conf.level = 0.95, ratio = 2.25)

print(H0)



