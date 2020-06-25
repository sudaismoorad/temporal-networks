__all__ = ['heappush', 'heappop', 'heapify', 'heapreplace', 'merge',
           'heappushpop', 'heappeek']


def heappush(heap, item):
    heap.heappush(item)


def heappop(heap):
    return heap.heappop()


def heapify(item):
    pass


def heapreplace():
    pass


def heappeek(heap):
    return heap.heappeek()


def merge():
    pass


def heappushpop():
    pass


class Node:

    def __init__(self, key, parent=None, lsibling=None, rsibling=None,
                 child=None, mark=False):
        self.key = key
        self.parent = parent
        self.lsibling = lsibling
        self.lsibling = lsibling
        self.child = child
        self.mark = mark
        self.degree = 0

    def add_child(self, node):
        if not self.child:
            self.child = node
            node.lsibling, node.rsibling = node, node
        else:
            right_of_child = self.child.rsibling
            self.child.rsibling = node
            node.lsibling = self.child
            node.rsibling = right_of_child
            right_of_child.lsibling = node
        node.parent = self
        self.degree += 1
        self.mark = False

    def remove_child(self, node):
        if not self.child:
            raise Exception("Child does not exist in the node.")

        if self.degree == 1:
            self.child = None
        else:
            if self.child is node:
                self.child = node.rsibling
            left_to_node, right_to_node = node.lsibling, node.rsibling
            left_to_node.rsibling = right_to_node
            right_to_node.lsibling = left_to_node

        self.degree -= 1


class FHeap:

    def __init__(self, minimum=None):
        self.min = minimum
        self.num_nodes = 0
        self.num_trees = 0
        self.num_marks = 0

    def __str__(self):
        stringy = ""
        return stringy

    def heapify(self, item):
        pass

    def remove_root(self, node):
        right_of_node, left_of_node = node.lsibling, node.rsibling
        right_of_node.lsibling = left_of_node
        left_of_node.rsibling = right_of_node

        self.num_trees -= 1

    def add_root(self, node):
        if self.min is None:
            node.lsibling, node.rsibling = node, node
        else:
            right_of_min = self.min.rsibling
            self.min.rsibling = node
            node.lsibling = self.min
            node.rsibling = right_of_min
            right_of_min.lsibling = node

        self.num_trees -= 1

    def remove_child(self, node):
        pass

    def heappush(self, node):
        self.add_root(node)

        if self.min is None or node.key < self.min.key:
            self.min = node

        self.num_nodes += 1

    def heappeek(self):
        return self.min

    def heappop(self):
        rtn = self.min
        if rtn is not None:
            node = rtn.child
            for _ in range(rtn.degree):
                succ_node = node.rsibling
                self.add_root(node)
                node.parent = None
                node = succ_node

            if rtn.mark:
                self.num_marks -= 1
            self.remove_root(rtn)

            if rtn == rtn.rsibling:
                self.min = None
            else:
                self.min = rtn.rsibling
                self.consolidate()

        return rtn

    def consolidate(self):
        pass

    def link(self, n1, n2):
        self.remove_root(n1)
        if n1.mark:
            self.num_marks -= 1
        n2.add_child(n1)

    def union(self, other):
        if self.min is None:
            self.min = other.min
        elif other.min:
            self_first_root, other_last_root = self.min.lsibling, other.min.rsibling
            self_first_root.lsibling = other_last_root
            self.min.rsibling = other.min
            other.min.lsibling = self.min
            other_last_root.rsibling = self_first_root

        if self.min is None or (other.min is not None and other.min.key < self.min.key):
            self.min = other.min

        self.num_nodes += other.num_nodes
        self.num_trees += other.num_trees
        self.num_marks += other.num_marks

    def decrease_key(self, node, key):
        if key > node.key:
            raise ValueError("New key is greater than second key")
        node.key = key
        parent = node.parent

        if parent and node.key < parent.key:
            self.cut(node, parent)
            self.cascading_cut(parent)

        if node.key < self.min.key:
            self.min = node

    def cut(self, node, node_parent):
        if node.mark:
            self.num_marks -= 1
            node.mark = False
        node_parent.remove_child(node)
        self.add_root(node)
        node.parent = None

    def cascading_cut(self, node):
        node_parent = node.parent
        if node_parent:
            if not node.mark:
                node.mark = True
                self.num_marks += 1
            else:
                self.cut(node, node_parent)
                self.cascading_cut(node_parent)

    def delete(self, x):
        pass
