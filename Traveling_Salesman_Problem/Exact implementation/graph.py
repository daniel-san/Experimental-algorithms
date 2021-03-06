class Node():
    def __init__(self,x,y):
        self.group = -1
        self.X = x
        self.Y = y
    
    
class Edge():
    def __init__(self,n1,n2):
        self.n1 = n1
        self.n2 = n2
        self.peso = None
        
    def calcPeso(self):
	self.peso = math.sqrt((self.n2.X - self.n1.X)**2 + (self.n2.Y - self.n1.Y)**2)
	
    def __cmp__(self,other):
        if self.peso < other.peso:
	    return -1
	elif self.peso > other.peso:
	    return 1
	else:
	    return 0
	
class Graph():
    def __init__(self):
        self.nodes = []
        self.edges = []
        