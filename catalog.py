
# TODO é necessário implementar um gerador de id's para cada foto
# a restrição é que o id tem que ser único
from avlTree import AVLTree
from photo import Photo


class Catalog:

    def __init__(self, photo: Photo, commands: list = []):
        self._index = AVLTree(photo)
        self.sec_index = dict()
        self.sec_index[photo._id] = photo
        self.running = True
        self.commands = commands

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
    
    def help(self):
        for command in self.commands:
            if command['option']:
                print(f"{command['command']} {command['option']}")
            else:
                print(command['command'])

    def quit(self):
        self.running = False
    
    def registerCommands(self):
        self.commands = [
            {'command': ':add', 'option': '<id> <ts> <path> [rating]', 'function': None, 'input_type': str},
            {'command': ':import', 'option': '<manifest.json>', 'function': None, 'input_type': str},
            {'command': ':range', 'option': '<ts1> <ts2>', 'function': None, 'input_type': str},
            {'command': ':nearest', 'option': '<ts>', 'function': None, 'input_type': str},
            {'command': ':next', 'option': ' <id>', 'function': None, 'input_type': int},
            {'command': ':prev', 'option': ' <id>', 'function': None, 'input_type': int},
            {'command': ':get', 'option': '<id>', 'function': None, 'input_type': int},
            {'command': ':tag', 'option': '<id> <tag>', 'function': None, 'input_type': str},
            {'command': ':rate', 'option': '<id> <0..5>', 'function': None, 'input_type': str},
            {'command': ':find-tag', 'option': '<tag>', 'function': None, 'input_type': str},
            {'command': ':remove', 'option': '<id>', 'function': None, 'input_type': int},
            {'command': ':remove-range', 'option': '<ts1> <ts2>', 'function': None, 'input_type': str},
            {'command': ':stats', 'option': None, 'function': None, 'input_type': None},
            {'command': ':list', 'option': None, 'function': None, 'input_type': None},
            {'command': ':tree', 'option': None, 'function': None, 'input_type': None},
            {'command': ':save', 'option': '<f>', 'function': None, 'input_type': str},
            {'command': ':load', 'option': '<f>', 'function': None, 'input_type': str},
            {'command': ':help', 'option': None, 'function': self.help, 'input_type': None},
            {'command': ':quit', 'option': None, 'function': self.quit, 'input_type': None},
        ]

