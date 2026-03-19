from matplotlib import pyplot as plt
from ppmc_lexer import PPMCLexer
from ppmc_parser import PPMCParser
from pm_exceptions import ParserException
import sys

def make_plot(config: str):
    lexer = PPMCLexer()
    parser = PPMCParser()

    with open(config, "r") as cfg:
        try:
            parser.parse(lexer.tokenize(cfg.read()))
        except ParserException as pe:
            print(str(pe), file=sys.stderr)
            sys.exit(1)

    p = parser.plot_obj

    for g in p.graphs:
        if g.plot_type == 'plot':
            plt.plot(
                p.variables_values[g.x], 
                p.variables_values[g.y], 
                color=g.color,
                linewidth=g.linewidth
            )

    if p.xlabel:
        plt.xlabel(p.xlabel)

    if p.ylabel:
        plt.ylabel(p.ylabel)

    if p.title:
        plt.title(p.title)

    if p.show:
        plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No config file given", file=sys.stderr)
        sys.exit(1)

    make_plot(sys.argv[1])

