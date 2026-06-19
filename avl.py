from avlTree import AVLTree
from binaryTree import BinaryTree
from photo import Photo
from catalog import Catalog

if __name__ == '__main__':
    values = [10, 20, 30, 40, 50, 25]
    binary = BinaryTree()
    avl = AVLTree()
    for value in values:
        binary.insert(value)
        avl.insert(value)

    print(binary.traversal(True, True, True))
    print(avl.traversal(True, True, True))

    p1 = Photo(1, 1, "/home/user/Pictures/1.jpg", ["natureza", "natureza2"], 5)
    p2 = Photo(2, 2, "/home/user/Pictures/2.jpg", ["natureza", "natureza2"], 4)
    p3 = Photo(3, 3, "/home/user/Pictures/3.jpg", ["natureza", "natureza2"], 3)
    p4 = Photo(4, 4, "/home/user/Pictures/4.jpg", ["natureza", "natureza2"], 2)

    c = Catalog(p3)
    c.add(p4)
    c.add(p1)
    c.add(p2)
    print(c)
    c.remove(2)
    print(c)
