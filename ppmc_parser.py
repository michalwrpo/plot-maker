from sly import Parser
from ppmc_lexer import PPMCLexer, PPMCFormatLexer, PPMCValueLexer, PPMCGraphLexer, PPMCGraphAttributesLexer
from pmplot import Plot, Graph
from pm_exceptions import ParserException

class PPMCParser(Parser):
    def __init__(self):
        self.plot_obj = Plot()
        self.in_data = None
        self.line = 0
        self.col = 0

    tokens = PPMCLexer.tokens | PPMCFormatLexer.tokens | PPMCValueLexer.tokens | PPMCGraphLexer.tokens | PPMCGraphAttributesLexer.tokens

    @_('plot plots')
    def plots(self, p):
        return 0
    
    @_('')
    def empty(self, p):
        pass
    
    @_('empty')
    def plots(self, p):
        return 0
    
    @_('plot_kw graphs attributes data')
    def plot(self, p):
        return 0

    @_('PLOT')
    def plot_kw(self, p):
        # ignore for now
        return 0
    
    @_('graph graphs')
    def graphs(self, p):
        pass

    @_('empty')
    def graphs(self, p):
        pass

    @_('GRAPH graph_data graph_attributes GRAPH_END')
    def graph(self, p):
        pass

    @_('GRAPH_VAR SEPARATOR GRAPH_VAR')
    def graph_data(self, p):
        self.plot_obj.variables.append(p.GRAPH_VAR0)
        self.plot_obj.variables.append(p.GRAPH_VAR1)
        self.plot_obj.graphs.append(Graph(p.GRAPH_VAR0, p.GRAPH_VAR1))


    @_('SEPARATOR graph_attr graph_attributes')
    def graph_attributes(self, p):
        pass

    @_('empty')
    def graph_attributes(self, p):
        pass

    # start of graph attributes

    @_('GRAPH_COLOR GRAPH_ASSIGN COLOR_HEX')
    def graph_attr(self, p):
        self.plot_obj.graphs[-1].color = p.COLOR_HEX

    @_('GRAPH_COLOR GRAPH_ASSIGN STRING')
    def graph_attr(self, p):
        self.plot_obj.graphs[-1].color = p.STRING

    @_('GRAPH_LINEWIDTH GRAPH_ASSIGN number')
    def graph_attr(self, p):
        self.plot_obj.graphs[-1].linewidth = p.number
    

    # end of graph attributes

    @_('attr attributes')
    def attributes(self, p):
        pass

    @_('empty')
    def attributes(self, p):
        pass

    # start of attributes

    @_('SUPTITLE ASSIGN STRING')
    def attr(self, p):
        self.plot_obj.suptitle = p.STRING

    @_('TITLE ASSIGN STRING')
    def attr(self, p):
        self.plot_obj.title = p.STRING

    @_('XLABEL ASSIGN STRING')
    def attr(self, p):
        self.plot_obj.xlabel = p.STRING

    @_('YLABEL ASSIGN STRING')
    def attr(self, p):
        self.plot_obj.ylabel = p.STRING

    @_('XLOG')
    def attr(self, p):
        self.plot_obj.xlog = True

    @_('YLOG')
    def attr(self, p):
        self.plot_obj.ylog = True

    @_('SHOW')
    def attr(self, p):
        self.plot_obj.show = True

    @_('SAVE ASSIGN STRING')
    def attr(self, p):
        self.plot_obj.save = True
        self.plot_obj.out_filename = p.STRING

    @_('SAVE')
    def attr(self, p):
        self.plot_obj.save = True


    # end of attributes

    @_('INT')
    def number(self, p):
        return p.INT
    
    @_('FLOAT')
    def number(self, p):
        return p.FLOAT

    @_('set_file FORMAT formatting FORMAT_END data')
    def data(self, p):
        pass

    @_('empty')
    def data(self, p):
        pass

    @_('FILE')
    def set_file(self, p):
        self.line = 0
        self.col = 0
        self.in_data = open(p.FILE, "r").read().split('\n')

        if self.plot_obj.save and self.plot_obj.out_filename == "":
            # cut off file extension and replace it with '.png'
            last_dot = p.FILE.rfind('.')
            self.plot_obj.out_filename = p.FILE[:last_dot] if last_dot > -1 else p.FILE + ".png"

    @_('format formatting')
    def formatting(self, p):
        pass
    
    @_('FORMAT_LINE')
    def formatting(self, p):
        pass

    @_('empty')
    def formatting(self, p):
        pass

    @_('SKIP_LINES')
    def format(self, p):
        self.line += p.SKIP_LINES

        if (self.in_data == None):
            raise ParserException(f"Line {p.lineno}: No file has been given for the format.")
        if (self.line >= len(self.in_data)):
            raise ParserException(f"Line {p.lineno}: The format exceedes the length of the file.")



    @_('ROW_FORMAT')
    def format(self, p):
        if (self.in_data == None):
            raise ParserException(f"Line {p.lineno}: No file has been given for the format.")
        if (self.line >= len(self.in_data)):
            raise ParserException(f"Line {p.lineno}: The format exceedes the length of the file.")
        
        var = p.ROW_FORMAT

        if (var not in self.plot_obj.variables):
            raise ParserException(f"Line {p.lineno}: Unknown variable {var} used in format.")

        print(var)
        data = list(map(lambda x : float(x), self.in_data[self.line].split()))
        self.line += 1
        self.plot_obj.variables_values[var] = data
        

    @_('COL_FORMAT')
    def format(self, p):
        return p.COL_FORMAT
