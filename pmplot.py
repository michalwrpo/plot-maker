from typing import List, Tuple, Dict

class Graph:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = "blue"
        self.plot_type = "plot"

class Plot:
    # def __init__(self, x, y, xlabel: str = "x", ylabel: str = "y", color: str = "blue", show: bool = True, filename: str | None = None):
    #     self.x = x
    #     self.y = y
    #     self.xlabel = xlabel
    #     self.ylabel = ylabel
    #     self.color = color
    #     self.show = show
    #     self.filename = filename

    # def __init__(self, params):
    #     self.x = params.get("x")
    #     self.y = params.get("y")
    #     self.xlabel = params.get("xlabel", "x")
    #     self.ylabel = params.get("ylabel", "y")
    #     self.color = params.get("color", "blue")
    #     self.show = params.get("show", True)
    #     self.filename = params.get("filename")
    #     self.title = params.get("title")

    def __init__(self):
        # [ (x, y) ]
        self.graphs : List[Graph] = []
        self.variables: List[str] = []
        self.variables_values: Dict[str, List[float]] = {}
        self.xlabel = ""
        self.ylabel = ""
        self.color = "blue"
        self.show = False
        self.filename = ""
        self.title = ""
