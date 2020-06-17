from collections import deque


class Tarjan:

    def __init__(self, network):
        self.length = network.length
        self.network = network
        self.ids = [-1 for _ in range(self.length)]
        self.low = [0 for _ in range(self.length)]
        self.onStack = [False for _ in range(self.length)]
        self.stack = deque()
        self.id = 0

    def tarjan(self):
        # used to compute strongly connected components
        # and hence the rigid component subgraphs
        # runs in O(V + E) time

        for i in range(self.length):
            if self.ids[i] == -1:
                self._dfs(i)

        return self.low

    def _dfs(self, idx):
        self.stack.append(idx)
        self.onStack[idx] = True
        self.ids[idx] = self.id
        self.low[idx] = idx
        self.id += 1

        # for target_idx in self.graph[idx]:
        for target_idx in self.network.successor_edges[idx]:
            if self.ids[target_idx] == -1:
                self._dfs(target_idx)
            if self.onStack[target_idx]:
                self.low[idx] = min(self.low[idx], self.low[target_idx])

        if self.ids[idx] == self.low[idx]:
            while self.stack:
                node = self.stack.pop()
                self.onStack[node] = False
                self.low[node] = self.ids[idx]
                if node == idx:
                    break
