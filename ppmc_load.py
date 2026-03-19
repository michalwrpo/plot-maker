from pmplot import Plot
from ppmc_lexer import PPMCLexer
import re

def get_data(filename: str) -> Plot:
    lexer = PPMCLexer()
    plot = Plot()

    with open(filename, "r") as f:
        config = f.read()

        for tok in lexer.tokenize(config):
            print(tok)
            if tok.type == 'FILE':
                #do things
                print(tok.value)
            elif tok.type == 'KEY':
                if tok.value == 'title':
                    

    return plot

# COLORS = ["red", "green", "blue", "orange", "magenta", "yellow", "black", "white"]
# INFILE = ["data", "file", "infile", "in_file", "in-file", "input_file", "input-file"]

# def get_data(filename: str) -> Plot:
#     with open(filename, "r") as f:
#         config = f.read().strip().split("\n")

#         plot_params = {}

#         for line in config:
#             args = line.split()
#             args = [arg.strip() for arg in args]

#             if m := re.compile("title=\"[^\"]*\"").search(line):
#                 plot_params["title"] = line[m.start() + 7 : m.end() - 1]

#             for arg in args:
#                 if plot_params.get("in_filename") == None:
#                     plot_params["in_filename"] = arg
                    
#                     with open(arg, "r") as file:
#                         data = file.read().strip().split("\n")
#                         x = [int(line.split()[0]) for line in data]
#                         y = [int(line.split()[1]) for line in data]

#                         plot_params["x"] = x
#                         plot_params["y"] = y
#                     continue

#                 if arg in COLORS:
#                     plot_params["color"] = arg
#                 elif m := re.compile("xlabel=").match(arg):
#                     plot_params["xlabel"] = arg[m.end():]
#                 elif m := re.compile("ylabel=").match(arg):
#                     plot_params["ylabel"] = arg[m.end():]

#     return Plot()


