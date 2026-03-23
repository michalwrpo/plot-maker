from typing import List, Dict

class Graph:
    def __init__(self, x, y):
        self.x: List[float] = x
        self.y: List[float] = y
        self.color = "blue"
        self.plot_type = "plot"
        self.linewidth : float = 1

class Plot:
    def __init__(self):
        self.graphs : List[Graph] = []
        self.variables: List[str] = []
        self.variables_values: Dict[str, List[float]] = {}
        self.xlabel: str = ""
        self.ylabel: str = ""
        self.xlog: bool = False
        self.ylog: bool = False
        self.show: bool = False
        self.save: bool = False
        self.out_filename: str = ""
        self.filename: str = ""
        self.suptitle: str = ""
        self.title: str = ""
