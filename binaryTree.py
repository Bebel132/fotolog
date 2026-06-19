from treeADT import TreeADT


class BinaryNode:

    def __init__(self, data=None, parent=None, left=None, right=None):
        self._data = data
        self._parent = parent
        self._left = left
        self._right = right

    def empty(self):
        return self._data is None

    def data(self):
        return self._data

    def left_node(self):
        return self._left

    def right_node(self):
        return self._right

    def parent_node(self):
        return self._parent

    def set_parent(self, p):
        self._parent = p

    def set_left_node(self, l):
        self._left = l

    def set_right_node(self, r):
        self._right = r

    def set_data(self, d):
        self._data = d

    def has_left_child(self):
        result = False
        if self.left_node():
            result = True
        return result

    def is_leaf(self):
        return not self.has_left_child() and not self.has_right_child()

    def has_right_child(self):
        result = False
        if self.right_node():
            result = True
        return result

    def __repr__(self):
        return self._data.__repr__()

    def __str__(self):
        return self._data.__str__()

    def __eq__(self, other):
        result = False
        if isinstance(other, BinaryNode):
            if self._data == other._data:
                result = True
        return result

    def __ne__(self, other):
        return not self.__eq__(other)

    def __le__(self, other):
        result = False
        if isinstance(other, BinaryNode):
            if self._data <= other._data:
                result = True
        return result

    def __lt__(self, other):
        result = False
        if isinstance(other, BinaryNode):
            if self._data < other._data:
                result = True
        return result
    
    def __gt__(self, other):
        result = False
        if isinstance(other, BinaryNode):
            if self._data > other._data:
                result = True
        return result


class BinaryTree(TreeADT):

    def __init__(self, data=None):
        if data:
            self._root = BinaryNode(data)
            self._qtd_nodes = 1
        else:
            self._root = None
            self._qtd_nodes = 0

    def empty(self):
        return self._root is None

    def root(self):
        return self._root

    def minimum(self, root):
        result = root
        while result.left_node():
            result = result.left_node()
        return result

    def maximum(self, root):
        result = root
        while result.right_node():
            result = result.right_node()
        return result

    def get_node_level(self, node):
        level = 0
        current = node
        while current.parent_node():
            current = current.parent_node()
            level += 1
        return level

    def insert(self, elem):
        node = BinaryNode(elem)
        if self.empty():
            self._root = node
            self._qtd_nodes = 1
            return self._root
        else:
            return self.__insert_children(self._root, node)

    def __insert_children(self, root: BinaryNode, node):
        if node <= root:
            if not root.has_left_child():  # não existe nó a esquerda (caso base)
                root.set_left_node(node)
                root.left_node().set_parent(root)
                self._qtd_nodes += 1
                return root.left_node()
            else:
                return self.__insert_children(root.left_node(), node)  # sub-árvore esquerda
        else:
            if not root.has_right_child():  # não existe nó a direta (caso base)
                root.set_right_node(node)
                root.right_node().set_parent(root)
                self._qtd_nodes += 1
                return root.right_node()
            else:
                return self.__insert_children(root.right_node(), node)  # sub-árvore direta

    def search(self, value):
        node = BinaryNode(value)
        if not self.empty():
            return self.__search_children(self._root, node)
        else:
            return False, node

    def __search_children(self, root, node):
        if not root:
            return False, node
        if root == node:
            return True, root
        elif node < root:
            return self.__search_children(root.left_node(), node)
        else:
            return self.__search_children(root.right_node(), node)

    def search_iterative(self, value: int):
        node = BinaryNode(value)
        root = self._root
        while root and root != node:
            if node < root:
                root = root.left_node()
            else:
                root = root.right_node()

        if root:
            return True, root
        else:
            return False, node

    def successor(self, node):
        belongs, n = self.search_iterative(node.data())

        if not belongs:
            return None

        if n.right_node():
            return self.minimum(n.right_node())

        parent = n.parent_node()

        while parent and n == parent.right_node():
            n = parent
            parent = parent.parent_node()

        return parent

    def predecessor(self, node):
        belongs, n = self.search_iterative(node.data())

        if not belongs:
            return None

        if n.left_node():
            return self.maximum(n.left_node())

        parent = n.parent_node()

        while parent and n == parent.left_node():
            n = parent
            parent = parent.parent_node()

        return parent
        
    def delete(self, value):
        belongs, z = self.search(value)
        if belongs:
            if not z.has_left_child() or not z.has_right_child():
                y = z
            else:
                y = self.successor(z)

            if y.left_node():
                x = y.left_node()
            else:
                x = y.right_node()

            if x:
                x.set_parent(y.parent_node())

            if not y.parent_node():
                self._root = x
            elif y == y.parent_node().left_node():
                y.parent_node().set_left_node(x)
            else:
                y.parent_node().set_right_node(x)

            if y != z:
                z.set_data(y.data())

            self._qtd_nodes -= 1
            return y
        else:
            return None

    def traversal(self, in_order=True, pre_order=False, post_order=False):
        result = list()
        if in_order:
            in_order_list = list()
            result.append(self.__in_order(self._root, in_order_list))
        else:
            result.append(None)

        if pre_order:
            pre_order_list = list()
            result.append(self.__pre_order(self._root, pre_order_list))
        else:
            result.append(None)

        if post_order:
            post_order_list = list()
            result.append(self.__post_order(self._root, post_order_list))
        else:
            result.append(None)

        return result

    def __in_order(self, root, lista):
        if not root:
            return
        self.__in_order(root._left, lista)
        lista.append(root._data)
        self.__in_order(root._right, lista)
        return lista

    def __pre_order(self, root, lista):
        if not root:
            return
        lista.append(root._data)
        self.__pre_order(root._left, lista)
        self.__pre_order(root._right, lista)
        return lista

    def __post_order(self, root, lista):
        if not root:
            return
        self.__post_order(root._left, lista)
        self.__post_order(root._right, lista)
        lista.append(root._data)
        return lista

    def print_binary_tree(self):
        if self._root:
            print(self.traversal(False, True, False)[1])

    def __len__(self):
        return len(self.__in_order(self._root, []) or [])

    def number_of_left_leaves(self):
        if self.empty():
            return 0
        return self.__number_of_left_leaves(self._root)

    def __number_of_left_leaves(self, node):
        if not node:
            return 0

        count = 0
        if node.has_left_child() and node.left_node().is_leaf():
            count += 1

        count += self.__number_of_left_leaves(node.left_node())
        count += self.__number_of_left_leaves(node.right_node())

        return count

    def brothers(self, v1, v2):
        v1_exists, node1 = self.search(v1)
        v2_exists, node2 = self.search(v2)
        result = False
        if v1_exists and v2_exists and node1.parent_node() == node2.parent_node():
            result = True
        return result

    def cousins(self, v1, v2):
        v1_exists, node1 = self.search(v1)
        v2_exists, node2 = self.search(v2)
        result = False
        if v1_exists and v2_exists:
            parent1, parent2 = node1.parent_node(), node2.parent_node()
            if parent1 and parent2:
                result = self.brothers(parent1.data(), parent2.data())
        return result

    def __in_order_with_depth(self, root, lista):
        if not root:
            return None
        self.__in_order_with_depth(root.left_node(), lista)
        lista.append((root, self.get_node_level(root)))
        self.__in_order_with_depth(root.right_node(), lista)
        return lista

    def longest_path_values(self):
        nodes_depth = self.__in_order_with_depth(self._root, [])
        max_level = -1
        node = None
        for n, depth in nodes_depth:
            if depth > max_level:
                max_level = depth
                node = n
        # max_level = max(depth for node, depth in nodes_depth)
        # deepest = next(node for node, depth in nodes_depth if depth == max_level)
        result = []
        while node:
            result.append(node.data())
            node = node.parent_node()
        result.reverse()  # caminho inverso!
        return result

    def in_order(self):
        stack = []
        result = []
        visited_nodes = self._qtd_nodes
        if self._root:
            node = self._root
            stack.append(node)
            while visited_nodes > 0:
                topo = stack[-1]
                while topo.has_left_child() and not topo.left_node() in result:
                    stack.append(stack[-1].left_node())
                    topo = stack[-1]
                result.append(stack.pop())
                visited_nodes -= 1
                if result[-1].has_right_child():
                    stack.append(result[-1].right_node())
        return result

