import math
import random
from collections import deque

class User:
    def __init__(self, name):
        self.name = name

class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()
        # Returns True if user_id and friend_id have successfully been added as friends

    def populate_graph_linear(self, num_users, avg_friendships):
        # Keep randomly making friendships until we've made the right amount
        # randomly select two vertices to become friends
        # if it's a success, then increment number of friendships made
        # else try again

        #reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users into the graph
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create random friendships until we've hit target number of friendships
        target_friendships = num_users * avg_friendships
        total_friendships = 0  # keep track of total friendships made
        collisions = 0 # how many friendships we are trying to make that were already made

        while total_friendships < target_friendships: # our runtime is O(n) now where n is number of target_friendships
            # keep adding friendships
            # choose two vertices(user_id and friend_id)
            user_id = random.randint(1, self.last_id)
            friend_id = random.randint(1, self.last_id)
            if self.add_friendship_linear(user_id, friend_id):
                total_friendships += 2
            else:
                collisions += 1
        print(f"Collisions: {collisions}")

    # returns True if making friendships was a success
    def add_friendship_linear(self, user_id, friend_id):
        if user_id == friend_id:
            return False

        # Check if friend_id and user_id are not already friends with each other
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            return False

        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)
            return True

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        # a dictionary, not a set, mapping from node id --> [path from user_Id]
        visited = {}  # make sure we dont visit nodes we already processed plus it serves as the datastructure we return in the end
        queue = deque() # need this for BFT
        queue.append([user_id]) # appending the path to the queue
        while len(queue) > 0:
            currPath = queue.popleft()
            currNode = currPath[-1]
            visited[currNode] = currPath # bft guarantees us that this is the shortest path to currNode from user_id

            for friend in self.friendships[currNode]:   # adjancency list we are using
                if friend not in visited:
                    # make an new path; copy of currPath and add friend to it
                    newPath =currPath.copy()
                    newPath.append(friend)
                    queue.append(newPath)
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph_linear(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)

