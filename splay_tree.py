class Node:

    def __init__(self, key=None):
        self.key = key
        self.left = None
        self.right = None


class SplayTree:

    def __init__(self):
        self.root = None
        self.head = Node()

    def splay(self, key):
        left = self.head
        right = self.head
        tree = self.root
        self.head.left = None
        self.head.right = None
        while True:
            if key < tree.key:
                if tree.left is None:
                    break
                if key < tree.left.key:
                    y = tree.left
                    tree.left = y.right
                    y.right = tree
                    tree = y
                    if tree.left is None:
                        break
                right.left = tree
                right = tree
                tree = tree.left
            elif key > tree.key:
                if tree.right is None:
                    break
                if key > tree.right.key:
                    y = tree.right
                    tree.right = y.left
                    y.left = tree
                    tree = y
                    if tree.right is None:
                        break
                left.right = tree
                left = tree
                tree = tree.right
            else:
                break
        left.right = tree.left
        right.left = tree.right
        tree.left = self.head.right
        tree.right = self.head.left
        self.root = tree

    def insert(self, key):
        if self.root is None:
            self.root = Node(key)
            return

        self.splay(key)
        if self.root.key == key:
            # If the key is already there in the tree, don't do anything.
            return

        n = Node(key)
        if key < self.root.key:
            n.left = self.root.left
            n.right = self.root
            self.root.left = None
        else:
            n.right = self.root.right
            n.left = self.root
            self.root.right = None

        self.root = n

    def remove(self, key):
        self.splay(key)
        if key != self.root.key:
            raise 'key not found in tree'

        # Now delete the root.
        if self.root.left is None:
            self.root = self.root.right
        else:
            x = self.root.right
            self.root = self.root.left
            self.splay(key)
            self.root.right = x

    def find_min(self):
        if self.root is None:
            return
        x = self.root
        while x.left is not None:
            x = x.left
        self.splay(x.key)
        return x.key

    def find_max(self):
        if self.root is None:
            return None
        x = self.root
        while (x.right is not None):
            x = x.right
        self.splay(x.key)
        return x.key

    def find(self, key):
        if self.root is None:
            return None
        self.splay(key)
        if self.root.key != key:
            return None
        return self.root.key

    def is_empty(self):
        return self.root is None
