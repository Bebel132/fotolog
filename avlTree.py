from binaryTree import BinaryNode, BinaryTree


class AVLNode(BinaryNode):

    def __init__(self, data=None, parent=None, left=None, right=None):
        super().__init__(data, parent, left, right)
        self._bf = 1  # Cada nó começa com altura 1
        # vai servir para calcular o balance factor

    def get_balance_factor(self):
        return self._bf

    def set_balance_factor(self, h):
        self._bf = h

    def __repr__(self):
        return super().__repr__() + f' {self._bf}'

    def __str__(self):
        return super().__str__() + f' {self._bf}'


class AVLTree(BinaryTree):

    def __init__(self, data=None, node: AVLNode = None):
        super().__init__(data)
        if data:
            self._root = AVLNode(data)

    def insert(self, val):
        node = AVLNode(val)
        if self.empty():
            self._root = node
            self._qtd_nodes += 1
        else:
            self._root = self._insert_avl(self._root, node)
            self._qtd_nodes += 1

    def _insert_avl(self, root, node):
        if not root:
            return node

        if node < root:
            root.set_left_node(self._insert_avl(root.left_node(), node))
            root.left_node().set_parent(root)

        else:
            root.set_right_node(self._insert_avl(root.right_node(), node))
            root.right_node().set_parent(root)


        # Atualizar altura do nó atual
        root.set_balance_factor(1 + max(self._get_height(root.left_node()), self._get_height(root.right_node())))

        # Balancear a árvore
        return self._balance_tree(root)

    def _get_height(self, node):
        if not node:
            return 0
        return node.get_balance_factor()

    def _get_balance(self, node):
        if not node:
            return 0
        return self._get_height(node.left_node()) - self._get_height(node.right_node())

    def _balance_tree(self, root):
        balance = self._get_balance(root)

        # Caso Esquerda-Esquerda
        if balance > 1 and self._get_balance(root.left_node()) >= 0:
            return self._rotate_right(root)

        # Caso Direita-Direita
        if balance < -1 and self._get_balance(root.right_node()) <= 0:
            return self._rotate_left(root)

        if balance > 1 and self._get_balance(root.left_node()) < 0:
            root.set_left_node(self._rotate_left(root.left_node()))
            return self._rotate_right(root)

        if balance < -1 and self._get_balance(root.right_node()) > 0:
            root.set_right_node(self._rotate_right(root.right_node()))
            return self._rotate_left(root)

        return root

    def _rotate_left(self, z):
        y = z.right_node()
        T2 = y.left_node()

        # Executa a rotação
        y.set_left_node(z)
        z.set_right_node(T2)

        if T2:
            T2.set_parent(z)

        y.set_parent(z.parent_node())
        z.set_parent(y)

        # Atualiza as alturas
        z.set_balance_factor(1 + max(self._get_height(z.left_node()), self._get_height(z.right_node())))
        y.set_balance_factor(1 + max(self._get_height(y.left_node()), self._get_height(y.right_node())))

        return y

    def _rotate_right(self, z):
        y = z.left_node()
        T3 = y.right_node()

        # Executa a rotação
        y.set_right_node(z)
        z.set_left_node(T3)

        if T3:
            T3.set_parent(z)

        y.set_parent(z.parent_node())
        z.set_parent(y)

        # Atualiza as alturas
        z.set_balance_factor(1 + max(self._get_height(z.left_node()), self._get_height(z.right_node())))
        y.set_balance_factor(1 + max(self._get_height(y.left_node()), self._get_height(y.right_node())))

        return y

    def delete(self, value):
        if not self.empty():
            self._root = self._delete_node(self._root, value)
            self._qtd_nodes -= 1

    def _delete_node(self, root, value):
        if not root:
            return root

        # Procura o valor a ser deletado
        if value < root.data():
            root.set_left_node(self._delete_node(root.left_node(), value))
        elif value > root.data():
            root.set_right_node(self._delete_node(root.right_node(), value))
        else:
            # Caso o nó tenha um ou nenhum filho
            if not root.left_node() or not root.right_node():
                temp = root.left_node() if root.left_node() else root.right_node()

                if not temp:  # Nenhum filho
                    root = None
                else:  # Um filho
                    root = temp

            else:
                temp = self.minimum(root.right_node())
                root.set_data(temp.data())
                root.set_right_node(self._delete_node(root.right_node(), temp.data()))

        if not root:
            return root

        # Atualiza a altura
        root.set_balance_factor(1 + max(self._get_height(root.left_node()), self._get_height(root.right_node())))

        # Balanceia a árvore
        return self._balance_tree(root)

    def _range_recursive(self, node, ts1, ts2, result):
        if node is None:
            return

        ts = node.data().timestamp

        if ts > ts1:
            self._range_recursive(node.left_node(), ts1, ts2, result)

        if ts1 <= ts <= ts2:
            result.append(node.data())

        if ts < ts2:
            self._range_recursive(node.right_node(), ts1, ts2, result)

    def print_tree(self):
        self.__print_tree(self._root, "", True)

    def __print_tree(self, node, prefix="", is_last=True):
        if node is None:
            return

        print(prefix + ("└── " if is_last else "├── ") + str(node.data()))

        children = []

        if node.left_node():
            children.append(node.left_node())

        if node.right_node():
            children.append(node.right_node())

        for i, child in enumerate(children):
            last_child = (i == len(children) - 1)

            self.__print_tree(child, prefix + ("    " if is_last else "│   "), last_child)