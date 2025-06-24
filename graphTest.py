import unittest
from constructor import constructGraph
from Node import Node

class testNodeClass(unittest.TestCase):

    def test_linear(self):
        graph, dic = constructGraph("tests/sample1")
        self.assertEqual(len(dic), 19+3)    # check length. game + winning node

        while graph.getChilds() != {}:  # every node got a unique child
            self.assertEqual(len(graph.getChilds()), 1)
            key = list(graph.getChilds().keys())[0]
            graph = graph.getChilds()[key]

    def test_lastChildWin(self):
        """
        Check if the last child is a winning node.
        """
        graph, dic = constructGraph("tests/sample1")
        while graph.getChilds() != {}:
            key = list(graph.getChilds().keys())[0]
            graph = graph.getChilds()[key] 
        
        self.assertTrue(graph.board in ["WWIN", "BWIN", "DRAW"])

    def test_loop(self):
        """
        check if the graph loop
        """
        graph, dic = constructGraph("tests/sample2")
        loop = False
        visited = []
        while graph.getChilds() != {}:
            if graph in visited:
                loop = True
                break
            visited.append(graph)
            key = list(graph.getChilds().keys())[0]
            graph = graph.getChilds()[key] 
        
        self.assertTrue(visited)

    def test_loopStart(self):
        """
        Check if the graph loop on the starting game.
        Game is 8 move long
        """
        origin, dic = constructGraph("tests/sample3")
        graph = origin
        for i in range(4):
            key = list(graph.getChilds().keys())[0]
            graph = graph.getChilds()[key] 

        self.assertEqual(graph, origin)
        self.assertEqual(len(origin.getChilds()), 2)    # 2 childs, Win status and the game.


    
if __name__ == "__main__":
    unittest.main()