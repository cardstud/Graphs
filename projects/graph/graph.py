"""
Simple graph implementation
"""

from collections import deque

class Graph:

    def __init__(self):
        # vertex_id --> set of neighbors
        self.vertices = {}      # start off with an empty dictionary (will contain keys/values)

    def __repr__(self):
        return str(self.vertices)

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = set()       # empty set to hold the vertexes

    # remove vertex from graph and any incoming edges to it
    def remove_vertex(self,vertex_id):
        # check if exists
        if vertex_id not in self.vertices:
            print("Attempting to remove non-existant vertex")
            return
        
        self.vertices.pop(vertex_id)
        
        # remove the edge
        for remaining_vertex in self.vertices:
            self.vertices[remaining_vertex].discard(vertex_id)

    def remove_edge(self, from_vertex_id, to_vertex_id):
        # check that edges of the vertex exist
        if from_vertex_id not in self.vertices or to_vertex_id not in self.vertices:
            print("Attempting to remove edges from non-existant vertex")
            return

        self.vertices[from_vertex_id].discard(to_vertex_id)

    # adds a directed edge from_vertex_id to to_vertex_id
    def add_edge(self, from_vertex_id, to_vertex_id):
        # check if vertex_id is in dictionary
        if from_vertex_id not in self.vertices or to_vertex_id not in self.vertices:
            print("Attempting to add edge to non-existing nodes")
            return 
        
        # this line makes it a directed edge
        self.vertices[from_vertex_id].add(to_vertex_id)     # add onto the set

        # # to make it undirected
        # self.vertices[from_vertex_id].add(to_vertex_id)
        # self.vertices[to_vertex_id].add(from_vertex_id)

    # will return all the outgoing edges from vertex_id - if no neighbors, returns none
    def get_neighbors(self, vertex_id):
        return self.vertices[vertex_id]     # just do a dictionary lookup to get those values

    # based on the pseudocode up above
    # df traversal - traverse entire list
    def dft(self, starting_vertex):
        visited = set()
        stack = deque()
        stack.append(starting_vertex)

        while len(stack) > 0:
            currNode = stack.pop()
            if currNode not in visited:
                visited.add(currNode)
                print(currNode)

                for neighbor in self.vertices[currNode]:
                    stack.append(neighbor)

    # df search (you stop when its found)
    # returns a path to the goal_vertex from starting_vertex
    def dfs(self, starting_vertex, goal_vertex):
        visited = set()
        stack = deque()

        # push the current path onto the stack, instead of just a single vertex
        stack.append([starting_vertex])

        while len(stack) > 0:
            currPath = stack.pop()
            currNode = currPath[-1]     # the current node you're on is the last node in the path

            if currNode == goal_vertex:
                return currPath
    
            if currNode not in visited:
                visited.add(currNode)

                for neighbor in self.vertices[currNode]:
                    newPath = list(currPath)    # make a copy of the current path
                    newPath.append(neighbor)
                    stack.append(newPath)

    # bf traversal given a starting vertex
    def bft(self, starting_vertex):
        visited = set()
        queue = deque()
        queue.append(starting_vertex)

        while len(queue) > 0:
            currNode = queue.popleft()  # since queue is FIFO
            if currNode not in visited:
                visited.add(currNode)
                print(currNode)
                for neighbor in self.vertices[currNode]:
                    queue.append(neighbor)

    def bfs(self, starting_vertex, goal_vertex):
        pass

    # Basecases: already visited that neighbor or have no new neighbors
    # will use a helper function with below
    def dft_recursive(self, starting_vertex):
        visited = set()
        self.dft_recursive_helper(starting_vertex, visited)

    # dft recursive helper function
    def dft_recursive_helper(self, curr_vertex, visited):
        visited.add(curr_vertex)
        print(curr_vertex)
        for neighbor in self.vertices[curr_vertex]:
            if neighbor not in visited:
                # recursive case
                self.dft_recursive_helper(neighbor, visited)

    def dfs_recursive(self, starting_vertex, goal_vertex):
        visited = set()
        return self.dfs_recursive_helper([starting_vertex], visited, goal_vertex)

    # return the path to goal_vertex if it exists, if it doesn't, return an empty array
    def dfs_recursive_helper(self, curr_path, visited, goal_vertex):
        curr_vertex = curr_path[-1]

        # one of our base cases - if curr vertex is goal vertex, return its path
        if curr_vertex == goal_vertex:
            return curr_path
        visited.add(curr_vertex)
        for neighbor in self.vertices[curr_vertex]:
            if neighbor not in visited:
                newPath = list(curr_path)
                newPath.append(neighbor)

                # recursive case - keep traversing the graph and visit the neighbor next
                res = self.dfs_recursive_helper(newPath, visited, goal_vertex)
                if len(res) > 0:
                    return res

        # base case - return empty array if goal vertex is not found
        return []

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
