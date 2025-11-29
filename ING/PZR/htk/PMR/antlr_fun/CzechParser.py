# Generated from Czech.g4 by ANTLR 4.9.3
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO


def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\5")
        buf.write("\26\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\7\2\13\n\2\f\2\16")
        buf.write("\2\16\13\2\3\2\3\2\3\3\3\3\3\4\3\4\3\4\2\2\5\2\4\6\2\2")
        buf.write("\2\24\2\f\3\2\2\2\4\21\3\2\2\2\6\23\3\2\2\2\b\13\5\4\3")
        buf.write("\2\t\13\5\6\4\2\n\b\3\2\2\2\n\t\3\2\2\2\13\16\3\2\2\2")
        buf.write("\f\n\3\2\2\2\f\r\3\2\2\2\r\17\3\2\2\2\16\f\3\2\2\2\17")
        buf.write("\20\7\2\2\3\20\3\3\2\2\2\21\22\7\3\2\2\22\5\3\2\2\2\23")
        buf.write("\24\7\4\2\2\24\7\3\2\2\2\4\n\f")
        return buf.getvalue()


class CzechParser ( Parser ):

    grammarFileName = "Czech.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [  ]

    symbolicNames = [ "<INVALID>", "WORD", "PUNCT", "WS" ]

    RULE_text = 0
    RULE_word = 1
    RULE_punct = 2

    ruleNames =  [ "text", "word", "punct" ]

    EOF = Token.EOF
    WORD=1
    PUNCT=2
    WS=3

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.3")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class TextContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(CzechParser.EOF, 0)

        def word(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CzechParser.WordContext)
            else:
                return self.getTypedRuleContext(CzechParser.WordContext,i)


        def punct(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CzechParser.PunctContext)
            else:
                return self.getTypedRuleContext(CzechParser.PunctContext,i)


        def getRuleIndex(self):
            return CzechParser.RULE_text

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterText" ):
                listener.enterText(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitText" ):
                listener.exitText(self)




    def text(self):

        localctx = CzechParser.TextContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_text)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 10
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==CzechParser.WORD or _la==CzechParser.PUNCT:
                self.state = 8
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [CzechParser.WORD]:
                    self.state = 6
                    self.word()
                    pass
                elif token in [CzechParser.PUNCT]:
                    self.state = 7
                    self.punct()
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 12
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 13
            self.match(CzechParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class WordContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WORD(self):
            return self.getToken(CzechParser.WORD, 0)

        def getRuleIndex(self):
            return CzechParser.RULE_word

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWord" ):
                listener.enterWord(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWord" ):
                listener.exitWord(self)




    def word(self):

        localctx = CzechParser.WordContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_word)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 15
            self.match(CzechParser.WORD)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PunctContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PUNCT(self):
            return self.getToken(CzechParser.PUNCT, 0)

        def getRuleIndex(self):
            return CzechParser.RULE_punct

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPunct" ):
                listener.enterPunct(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPunct" ):
                listener.exitPunct(self)




    def punct(self):

        localctx = CzechParser.PunctContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_punct)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 17
            self.match(CzechParser.PUNCT)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





