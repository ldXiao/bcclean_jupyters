import numpy as nu
import networkx as nx
from pybcclean import Node, Edge

class Loop():
    def __init__(self, nodes: list, edges: list, label:int):
        self.loop_list = []
        self.match_dict = {}
        if not nodes:
            self.loop_list.append("Edge", edg)
            self.match_dict[("Edge", edg)]=False
        else:
            for nd, edg in zip(nodes, edges):
                self.loop_list.append(("Node", nd))
                self.loop_list.append("Edge", edg)
                self.match_dict[("Node", nd)]=False
                self.match_dict[("Edge", edg)]=False
        self.label = label

class pyNode():
    def __init__(nd: Node):
        self.labels = nd.labels
        self.matched = False

class pyEdge():
    def __init__(edg:Edge):
        self.vertices_list = edg.vertices_list
        self.head = edg.head
        self.tail  = edg.tail
        self.matched = False
        self.label_pair = edg.label_pair

class LoopFrame():
    self.Loops = []
    self.Edges = []
    self.Nodes = []
    

    

