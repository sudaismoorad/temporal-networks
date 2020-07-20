from collections import deque


class Tarjan:

    def __init__(self, network):
        self.num_tps = network.num_tps()
        self.network = network
        self.ids = [-1 for _ in range(self.num_tps)]
        self.low = [0 for _ in range(self.num_tps)]
        self.onStack = [False for _ in range(self.num_tps)]
        self.stack = deque()
        self.id = 0

    def tarjan(self):
        # used to compute strongly connected components
        # and hence the rigid component subgraphs
        # runs in O(V + E) time

        for i in range(self.num_tps):
            if self.ids[i] == -1:
                self._dfs(i)
        # self.low = [0, 0, 2, 3, 3]
        rc_map = {}
        counter = 0
        for i in self.low:
            if i not in rc_map:
                rc_map[i] = counter
                counter += 1

        rigid_components = [[] for i in range(len(set(self.low)))]
        for idx, rc in enumerate(self.low):
            i = rc_map[rc]
            rigid_components[i].append(idx)

        # rigid_components = [[0, 1], [2], [3, 4]]

        return rigid_components

    def _dfs(self, idx):
        self.stack.append(idx)
        self.onStack[idx] = True
        self.ids[idx] = self.id
        self.low[idx] = self.id
        self.id += 1

        for target_idx in self.network.successor_edges[idx]:
            if self.ids[target_idx] == -1:
                self._dfs(target_idx)
                self.low[idx] = min(self.low[idx], self.low[target_idx])
            elif self.onStack[target_idx]:
                self.low[idx] = min(self.low[idx], self.ids[target_idx])

        if self.ids[idx] == self.low[idx]:
            while self.stack:
                node = self.stack.pop()
                self.onStack[node] = False
                self.low[node] = self.ids[idx]
                if node == idx:
                    break
