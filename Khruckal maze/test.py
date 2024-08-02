class DisjointSet:
    def __init__(self, elements):
        self.parents = {element: element for element in elements}
        self.ranks = {element: 0 for element in elements}

    def find(self, element):
        if self.parents[element] != element:
            self.parents[element] = self.find(self.parents[element])
        return self.parents[element]

    def union(self, element1, element2):
        root1 = self.find(element1)
        root2 = self.find(element2)
        if root1 != root2:
            if self.ranks[root1] < self.ranks[root2]:
                self.parents[root1] = root2
            elif self.ranks[root1] > self.ranks[root2]:
                self.parents[root2] = root1
            else:
                self.parents[root2] = root1
                self.ranks[root1] += 1
