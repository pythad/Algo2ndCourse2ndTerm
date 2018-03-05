class Node:

    def __init__(self, value=0):
        self.parent = None
        self.value = value
        self.childs = []
        self.index = 0


class Binomial:

    def __init__(self):
        self.head = {}
        self.min = None

    def insert(self, x, idx=0):
        index = idx
        new_node = x
        while index in self.head:
            if new_node.value < self.head[index].value:
                self.head[index].parent = new_node
                new_node.childs.append(self.head[index])
            else:
                new_node.parent = self.head[index]
                self.head[index].childs.append(new_node)
                new_node = self.head[index]
            new_node.index += 1
            del self.head[index]
            index += 1
        self.head[index] = new_node
        self.update_min()

    def update_min(self):
        minimum = float("inf")
        minimum_node = None
        for i in self.head.values():
            if min(minimum, i.value) == i.value:
                minimum_node = i
                minimum = i.value
        self.min = minimum_node

    def merge(self, tree):
        tree2_keys = tree.head.keys()
        for i in tree2_keys:
            self.insert(tree.head[i], ind=i)
        self.update_min()

    def delete_min(self):
        if self.head:
            minimum = self.min
            new_tree = dict(minimum.childs)
            for node in new_tree:
                node.parent = None
            del self.head[minimum.index]
            del minimum
            for node in new_tree:
                self.insert(node, node.index)
        self.update_min()

    def decrease_key(self, node, new_value):
        node.value = new_value
        while node.parent:
            if node.parent.value > node.value:
                temp = node.parent.value
                node.parent.value = node.value
                node.value = temp
                node = node.parent
            else:
                break
        self.update_min()

    def delete(self, node):
        self.decrease_key(node, -1 * float('inf'))
        self.delete_min()
        self.update_min()
