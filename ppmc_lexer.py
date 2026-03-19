from sly import Lexer

class PPMCLexer(Lexer):
    tokens = {
        PLOT,
        ASSIGN, 
        FILE,
        FORMAT,
        GRAPH, 
        SHOW,
        TITLE,
        XLABEL,
        YLABEL,
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
        self.graph_attributes = 0
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
    
    @_('xlabel')
    def XLABEL(self, t):
        return t
    
    @_('ylabel')
    def YLABEL(self, t):
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
        INT,
        FLOAT,
        ID,
        COLOR_HEX
    }

    ignore = "\t "

    @_(r'"[^"\n]*"')
    def STRING(self, t):
        t.value = t.value[1:-1]
        self.pop_state()
        return t

    @_(r'(\d+)?\.\d+|\d+\.(\d+)?')
    def FLOAT(self, t):
        t.value = float(t.value)
        self.pop_state()
        return t
    
    @_(r'\d+')
    def INT(self, t):
        t.value = int(t.value)
        self.pop_state()
        return t

    @_(r'[a-zA-Z_\-][a-zA-Z0-9_\-]*')
    def ID(self, t):
        self.pop_state()
        return t
    
    @_(r'\#[a-fA-F0-9]+')
    def COLOR_HEX(self, t):
        self.pop_state()
        return t


class PPMCGraphLexer(Lexer):
    tokens = {
        GRAPH_VAR,
        SEPARATOR,
        GRAPH_END,
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
        self.graph_attributes += 1

        if (self.graph_attributes == 2):
            self.push_state(PPMCGraphAttributesLexer)
        return t

    @_(r'\)')
    def GRAPH_END(self, t):
        self.pop_state()
        return t
    
class PPMCGraphAttributesLexer(Lexer):
    tokens = {
        GRAPH_ASSIGN,
        SEPARATOR,
        GRAPH_END,
        GRAPH_COLOR,
        GRAPH_LINEWIDTH,
    }

    ignore = '\t '
    
    @_(r'\=')
    def GRAPH_ASSIGN(self, t):
        self.push_state(PPMCValueLexer)
        return t
    
    @_(r',')
    def SEPARATOR(self, t):
        self.graph_attributes += 1
        return t
    
    @_(r'\)')
    def GRAPH_END(self, t):
        self.pop_state()
        self.pop_state()
        return t
    
    @_(r'color')
    def GRAPH_COLOR(self, t):
        return t

    @_(r'linewidth')
    def GRAPH_LINEWIDTH(self, t):
        return t
    



if __name__ == "__main__":
    data = open("tests/row-format.ppmc", "r").read()
    lexer = PPMCLexer()

    for tok in lexer.tokenize(data):
        print(f"{tok}'")
