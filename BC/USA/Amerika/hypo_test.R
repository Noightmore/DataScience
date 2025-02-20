#define vector of turtle weights
turtle_weights <- c(300, 315, 320, 311, 314, 309, 300, 308, 305, 303, 305, 301, 303)

#perform one sample t-test
t.test(x = turtle_weights, mu = 310)