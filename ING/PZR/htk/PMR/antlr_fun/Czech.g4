// Czech.g4
grammar Czech;

// Parser
text  : (word | punct)* EOF ;
word  : WORD ;
punct : PUNCT ;

// Lexer
WORD  : ~[ \t\r\n.,!?;:]+ ;  // keep any non-separator run (Czech diacritics stay in WORD)
PUNCT : [.,!?;:] ;
WS    : [ \t\r\n]+ -> channel(HIDDEN) ;