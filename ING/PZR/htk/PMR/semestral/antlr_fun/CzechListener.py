# Generated from Czech.g4 by ANTLR 4.9.3
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CzechParser import CzechParser
else:
    from CzechParser import CzechParser

# This class defines a complete listener for a parse tree produced by CzechParser.
class CzechListener(ParseTreeListener):

    # Enter a parse tree produced by CzechParser#text.
    def enterText(self, ctx:CzechParser.TextContext):
        pass

    # Exit a parse tree produced by CzechParser#text.
    def exitText(self, ctx:CzechParser.TextContext):
        pass


    # Enter a parse tree produced by CzechParser#word.
    def enterWord(self, ctx:CzechParser.WordContext):
        pass

    # Exit a parse tree produced by CzechParser#word.
    def exitWord(self, ctx:CzechParser.WordContext):
        pass


    # Enter a parse tree produced by CzechParser#punct.
    def enterPunct(self, ctx:CzechParser.PunctContext):
        pass

    # Exit a parse tree produced by CzechParser#punct.
    def exitPunct(self, ctx:CzechParser.PunctContext):
        pass



del CzechParser