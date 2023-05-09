# kapitola 7 - teorie odhadu
# Př. 6: V prodejně si udělali průzkum, kolik zákazníků přijde do obchodu během jednoho dne. Byly
# zjištěny následující data:
# x=[541,574,585,596,612,618,632,641,654,671,681,692,711,713,718,719,754,796,812,815,835,858];
# Ověřte, že data jsou z normálního rozdělení. Zjistěte 99% interval spolehlivosti odhadu střední
# hodnoty.

# spravne reseni: [637.6, 746.8]

x <- c(541,574,585,596,612,618,632,641,654,671,681,692,711,713,718,719,754,796,812,815,835,858)

guess1 <- t.test(x, alternative = "two.sided", conf.level = 0.99)
print(guess1)

# in matlab: guess1 = [ h, p, ci, stat ] = ttest(x, 'stredni hodnota','Alpha', 'both');
# dosazeni za alpha: 0.01 - hladina vyznamnosti ->  1 - 0.99
# vysvetleni matlab fce je v prednasce 7.4.4 - Intervalovy odhad stredni hodnoty delta je neznama.

# zaver: s pravdepodobnosti 99% lezi stredni hodnota v intervalu <637.6, 746.8>

# jinak se to dosazuje do sileneho vzorce, ktery je kousek nize v kapitole 7.4.4

# rozptyl dat x (sigma squared):
var_x <- var(x)
print(var_x)

# dalsi testovani, jestli mean bude 10 000
# this may be wrong method used
guess2 <- var.test(x, sigma.squared = 10000)
print(guess2) # that is sussy bussin

# p-value aways ends up being 2.2e-16 which is basically 0, it should not be tho

# pr 11
# Př. 11: Při kontrole data spotřeby určitého druhu masové konzervy ve skladech produktů masného
# průmyslu bylo náhodně vybráno 320 z 20 000 konzerv a zjištěno, že 59 z nich má prošlou záruční
# lhůtu. Stanovte se spolehlivostí 95% intervalový odhad podílu konze rv s prošlou záruční lhůtou. A
# dále 95 % intervalový odhad počtu konzerv s prošlou záruční lhůtou.

