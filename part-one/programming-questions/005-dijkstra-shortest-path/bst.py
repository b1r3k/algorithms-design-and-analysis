# -*- coding: utf-8 -*-


class BinarySearchTreeNode:
    def __init__(self, key=None, parent=None, left=None, right=None):
        self.key = key
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s" % (self.key)

    def __bool__(self):
        return True

    def __len__(self):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> len(t)
        5

        >>> n = t.insert(6)
        >>> len(t)
        6

        >>> t.delete(5)
        >>> len(t)
        5

        :return:
        """
        size = 1

        if self.left:
            size += len(self.left)

        if self.right:
            size += len(self.right)

        return size

    def copy(self):
        return BinarySearchTreeNode(self.key, self.parent, self.left, self.right)

    def walk_till(self, key):
        """
        it performs search but unlike search it returns last node before node that is being searched
        thus it can be reused by search and insert methods

        >>> r = BinarySearchTreeNode(3)
        >>> r.left = BinarySearchTreeNode(1)
        >>> r.right = BinarySearchTreeNode(5)
        >>> r.left.right = BinarySearchTreeNode(2)
        >>> r.right.left = BinarySearchTreeNode(4)
        >>> item = r.walk_till(2)
        >>> item.key
        1

        >>> item = r.walk_till(6)
        >>> item.key
        5

        :param key:
        :return:
        """
        # next node has key we want
        try:
            if self.left and self.left.key == key or self.right and self.right.key == key:
                return self

        # or it's just root node
        except AttributeError:
            return self.root.walk_till(key)

        try:
            if key > self.key and self.right:
                return self.right.walk_till(key)
            if key < self.key and self.left:
                return self.left.walk_till(key)

        except AttributeError:
            if self.root:
                return self.root.walk_till(key)

        # nothing more nodes left to check
        return self

    def search(self, key):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> t.search(2)
        2

        >>> t.search(6)

        >>> t.search(3)
        3

        :param key:
        :return:
        """
        last_node = self.walk_till(key)

        # corner case for root - it doesnt have parent
        if not last_node:
            return None

        if last_node.key == key:
            return last_node

        if key > last_node.key and last_node.right:
            return last_node.right

        if key < last_node.key and last_node.left:
            return last_node.left

        return None

    def insert(self, key):
        """
        >>> r = BinarySearchTreeNode(3)
        >>> n5 = r.insert(5)
        >>> n1 = r.insert(1)
        >>> n4 = r.insert(4)
        >>> n2 = r.insert(2)
        >>> n6 = r.insert(6)
        >>> r.right.right == n6
        True

        :param key:
        :return:
        """

        new_node = BinarySearchTreeNode(key)
        last_node = self.walk_till(key)

        new_node.parent = last_node

        if key > last_node.key:
            last_node.right = new_node

        if key < last_node.key:
            last_node.left = new_node

        return new_node

    def in_order_walk(self):
        """
        >>> r = BinarySearchTreeNode(3)
        >>> r.left = BinarySearchTreeNode(1)
        >>> r.right = BinarySearchTreeNode(5)
        >>> r.left.right = BinarySearchTreeNode(2)
        >>> r.right.left = BinarySearchTreeNode(4)
        >>> r.in_order_walk()
        [1, 2, 3, 4, 5]

        :return:
        """
        steps_list = []

        if hasattr(self, 'root') and self.root:
            steps_list += self.root.in_order_walk()
            return steps_list

        if self.left:
            steps_list += self.left.in_order_walk()

        if hasattr(self, 'key'):
            steps_list.append(self.key)

        if self.right:
            steps_list += self.right.in_order_walk()

        return steps_list

    def min(self):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> i = t.min()
        >>> i.key
        1

        :return:
        """
        last_node = self.walk_till(-float('inf'))

        if last_node.left:
            return last_node.left

        return last_node

    def max(self):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> i = t.max()
        >>> i.key
        5

        :return:
        """
        last_node = self.walk_till(float('inf'))

        if last_node.right:
            return last_node.right

        return last_node

    def predecessor(self, key):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])

        >>> t.predecessor(3)
        2

        >>> t.predecessor(5)
        4

        >>> t.predecessor(2)
        1

        >>> t.predecessor(4)
        3

        :param key:
        :return:
        """

        node = self.search(key)

        if node.left:
            return node.left.max()

        if node.parent.key < key:
            return node.parent
        else:
            return node.parent.parent

        return

    def succesor(self, key):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])

        >>> t.succesor(3)
        4

        >>> t.succesor(5)


        >>> t.succesor(2)
        3

        >>> t.succesor(4)
        5

        :param key:
        :return:
        """

        node = self.search(key)

        if node.right:
            return node.right.min()

        if node.parent.key > key:
            return node.parent
        elif isinstance(node.parent.parent, BinarySearchTree):
            return None
        else:
            return node.parent.parent
        return

    def replace_child(self, old_child_node, new_child_node):
        try:
            if self.left == old_child_node:
                self.left = new_child_node

            if self.right == old_child_node:
                self.right = new_child_node

        except AttributeError:
            if self.root == old_child_node:
                self.root = new_child_node

        if new_child_node:
            new_child_node.left = old_child_node.left
            new_child_node.right = old_child_node.right
            new_child_node.parent = old_child_node.parent
            if old_child_node.left:
                old_child_node.left.parent = new_child_node

            if old_child_node.right:
                old_child_node.right.parent = new_child_node

        return

    def remove(self):
        parent = self.parent

        # no kids
        if not self.left and not self.right:
            parent.replace_child(self, None)
            return

        # has one child
        if not (self.left and self.right):
            parent.replace_child(self, self.left if self.left else self.right)
            return

        # switch predecessor with deleted node
        if self.left and self.right:
            # choose predecessor parent and point it to node being deleted
            predecessor = self.predecessor(self.key)
            predecessor_copy = predecessor.copy()
            predecessor_parent = predecessor.parent
            parent.replace_child(self, predecessor)

            predecessor_parent.replace_child(predecessor_copy, self)
            predecessor.replace_child(predecessor, None)

            self.remove()

        return

    def delete(self, key):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> t.delete(2)
        >>> t.search(2)

        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> t.delete(5)
        >>> t.search(5)

        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> t.delete(3)
        >>> t.search(3)

        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> n = t.insert(6)
        >>> t.delete(5)
        >>> t.search(5)

        :param key:
        :return:
        """
        node = self.search(key)

        return node.remove()

    def select(self, ith):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> t.select(1)
        1

        >>> t.select(5)
        5

        :param ith:
        :return:
        """

        if hasattr(self, 'root'):
            node = self.root
        else:
            node = self

        try:
            if hasattr(node, 'left') and node.left:
                a = len(node.left)
            else:
                a = 0

            if a >= ith:
                return node.left.select(ith)

            if a < ith - 1:
                return node.right.select(ith - a - 1)

        except (AttributeError, TypeError) as e:
            return node.root.select(ith)

        # if a == ith - 1:
        return node


class BinarySearchTree(BinarySearchTreeNode):
    def __init__(self, nodes=[]):
        self.root = None

        if len(nodes):
            self.root = self.get_bst(nodes)

    def __repr__(self):
        return "root: %s" % (self.root)

    def __len__(self):
        if self.root:
            return len(self.root)
        else:
            return 0

    def get_bst(self, nodes_keys):
        """
        >>> t = BinarySearchTree([3, 1, 5, 2, 4])
        >>> t.in_order_walk()
        [1, 2, 3, 4, 5]

        :param nodes_keys:
        :return:
        """
        root_node = BinarySearchTreeNode(nodes_keys[0])
        root_node.parent = self

        for node_key in nodes_keys[1:]:
            root_node.insert(node_key)

        return root_node


if __name__ == '__main__':
    import doctest

    doctest.testmod()
