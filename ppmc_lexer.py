from sly import Lexer

class PPMCLexer(Lexer):
    tokens = {
        PLOT,
        ASSIGN, 
        FILE,
        FORMAT,
        TITLE,
        GRAPH, 
        SHOW
    }

    ignore = '\t '
    ignore_comments = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_('PLOT')
    def PLOT(self, t):
        return t

    @_(r'\(')
    def GRAPH(self, t):
        self.push_state(PPMCGraphLexer)
        return t

    @_(r'=')
    def ASSIGN(self, t):
        self.push_state(PPMCValueLexer)
        return t

    @_(r'\[[^\]]*\]')
    def FILE(self, t):
        t.value = t.value[1:-1]
        return t

    @_('format')
    def FORMAT(self, t):
        self.push_state(PPMCFormatLexer)
        return t

    @_('title')
    def TITLE(self, t):
        return t
    
    @_('show')
    def SHOW(self, t):
        return t



class PPMCFormatLexer(Lexer):
    tokens = {
        ROW_FORMAT,
        COL_FORMAT,
        FORMAT_LINE,
        FORMAT_END
    }

    ignore = '\t '

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    @_(r'\{\-.*?\-\}')
    def ROW_FORMAT(self, t):
        t.value = t.value[2:-2]
        return t
    
    @_(r'\{\|.*?\|\}')
    def COL_FORMAT(self, t):
        t.value = t.value[2:-2]
        return t

    @_(r'end format')
    def FORMAT_END(self, t):
        self.pop_state()
        return t

    @_(r'\n+')
    def FORMAT_LINE(self, t):
        self.lineno += t.value.count('\n')
        return t
    
class PPMCValueLexer(Lexer):
    tokens = {
        STRING,
        NUMBER,
        ID
    }

    ignore = "\t "

    @_(r'"[^"\n]*"')
    def STRING(self, t):
        self.pop_state()
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        self.pop_state()
        return t
    
    @_(r'[a-zA-Z_\-][a-zA-Z0-9_\-]*')
    def ID(self, t):
        self.pop_state()
        return t


class PPMCGraphLexer(Lexer):
    tokens = {
        GRAPH_VAR,
        SEPARATOR,
        GRAPH_END
    }

    ignore = '\t '
    ignore_comments = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')


    @_(r'[a-zA-Z_][a-zA-Z0-9_]*')
    def GRAPH_VAR(self, t):
        return t

    @_(r',')
    def SEPARATOR(self, t):
        return t

    @_(r'\)')
    def GRAPH_END(self, t):
        self.pop_state()
        return t

if __name__ == "__main__":
    data = open("tests/row-format.ppmc", "r").read()
    lexer = PPMCLexer()

    for tok in lexer.tokenize(data):
        print(f"{tok}'")
