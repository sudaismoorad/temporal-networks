__all__ = ['heappush', 'heappop', 'heapify', 'heapreplace', 'merge',
           'heappushpop', 'heappeek']


def heappush(heap, item):
    heap.heappush(item)


def heappop(heap):
    return heap.heappop()


def heapify(item):
    heap = FHeap()
    if item:
        heap.heapify(item)
    return heap


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
        # if the node does not have a child
        if not self.child:
            # make the child the node you entered
            self.child = node
            # set left and right pointers of node to node itself
            node.lsibling, node.rsibling = node, node
        else:
            # get the node that is to the right of the child
            right_to_child = self.child.rsibling
            # set the current node to be right of the child
            self.child.rsibling = node
            # update the current child to be the left sibling
            # of the current node
            node.lsibling = self.child
            # set the right sibling to be the node that was to
            # the right of the child
            node.rsibling = right_to_child
            # what is this doing?
            right_to_child.lsibling = node
        # make the current node the parent of the node to be added
        node.parent = self
        # increase the degree of the current node
        self.degree += 1
        # reset the mark to be False
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

    def add_root(self, node):
        pass

    def remove_child(self, node):
        pass

    def heappush(self, node):
        pass

    def heappeek(self):
        return self.min

    def heappop(self):
        pass

    def consolidate(self):
        pass

    def link(self, n1, n2):
        pass

    def union(self, other):
        pass

    def decrease_key(self, x, k):
        pass

    def cut(self, x, y):
        pass

    def cascading_cut(self, y):
        pass

    def delete(self, x):
        pass
