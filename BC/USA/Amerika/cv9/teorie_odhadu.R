# teorie odhadu
#
# Př. 5: Naměřili jsme 10 údajů o životnosti žárovky: 380, 402, 408, 412, 454, 459, 472, 481, 491, 502
# hodin. Odhadněte, zda data jsou z normálního rozdělení (například pravděpodobnostním papírem) a
# dale určete 95% intervalový odhad střední hodnoty životnosti žárovky. Určete i 95% jednostranný
# intervalový odhady pro minimální a maximální odhad střední hodnoty. Interpretujte výsledky.

# matlab funkce: ttest()
vec <- c(380, 402, 408, 412, 454, 459, 472, 481, 491, 502)
guess1 <- t.test(vec, alternative = "two.sided", conf.level = 0.95)
print(guess1)
print("#########################################################")

# in  matlab: [h, p, ci, stat] = ttest(vec, 450, 0.05, 'both')

# one sided test
guess2 <- t.test(vec, alternative = "less", conf.level = 0.95)
print(guess2) # tenhle susuje
print("#########################################################")

# in  matlab: [h, p, ci, stat] = ttest(vec, 450, 0.05, 'left')

# one sided test
guess3 <- t.test(vec, alternative = "greater", conf.level = 0.95)
print(guess3)
print("#########################################################")

# in  matlab: [h, p, ci, stat] = ttest(vec, 450, 0.05, 'right')

# pokud bychom nemeli surova namerena data, ale pouze odhad stredni hodnoty a odchylky
# pocita se to pomoci silenych f-uj vzorcu

# funckce normplot atd.. matlab