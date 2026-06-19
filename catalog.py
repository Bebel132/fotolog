
# TODO é necessário implementar um gerador de id's para cada foto
# a restrição é que o id tem que ser único
from avlTree import AVLTree
from photo import Photo


class Catalog:

    def __init__(self, photo: Photo):
        self._index = AVLTree(photo)
        self.sec_index = dict()
        self.sec_index[photo._id] = photo

    def add(self, photo: Photo):
        self._index.insert(photo)
        self.sec_index[photo._id] = photo

    def remove(self, id: int):
        p = self.sec_index.get(id)
        self._index.delete(p)
        self.sec_index.pop(id)

    def get_by_id(self, id):
        result = self.sec_index.get(id)
        if not result:
            raise ValueError(f"Photo with id {id} not found")
        return result

    def __get_by_id_in_tree(self, id):
        """
        Procura por uma foto pelo seu identificador único e recupera a representação
        dentro da árvore de indexação

        Args:
            id: Identificador único

        Returns:
            Nó que representa a foto na árvode de indexação
        """
        p: Photo = self.get_by_id(id)  # aqui eu tenho uma foto
        return self._index.search(p)[1]  # aqui eu tenho a foto na árvore

    def next_of(self, id):
        return self._index.successor(self.__get_by_id_in_tree(id))

    def prev_of(self, id):
        return self._index.predecessor(self.__get_by_id_in_tree(id))

    def nearest(self, ts):
        ...

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self._index.in_order().__str__()

