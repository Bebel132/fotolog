from avlTree import AVLTree
from photo import Photo


class PhotoAVL(AVLTree):
    def __init__(self):
        super().__init__()

    def range(self, ts1, ts2):
        result = []
        self._range_recursive(self._root, ts1, ts2, result)
        return result

    def nearest(self, ts):
        ts = int(ts)
        current = self._root
        best = None

        while current:
            photo = current.data()

            if best is None or abs(photo.ts - ts) < abs(best.ts - ts):
                best = photo

            if ts < photo.ts:
                current = current.left_node()
            elif ts > photo.ts:
                current = current.right_node()
            else:
                return photo

        print(best)
        return best

    def successor(self, photo : Photo):
        found, node = super().search(photo)
        if not found:
            raise ValueError(f"Photo with id {photo.id} not found")
        return super().successor(node)
        
    def predecessor(self, photo : Photo):
        found, node = super().search(photo)
        if not found:
            raise ValueError(f"Photo with id {photo.id} not found")
        return super().predecessor(node)