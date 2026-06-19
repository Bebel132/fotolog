
# TODO é necessário implementar um gerador de id's para cada foto
# a restrição é que o id tem que ser único
from avlTree import AVLTree
from photo import Photo
from photo_avl import PhotoAVL


class Catalog(PhotoAVL):
    # 🆗 add(foto) — insere na AVL + no dict
    # 🆗 remove(id) — remove da AVL + do dict
    # 🆗 get_by_id(id) — acesso O(1) pelo dict
    # 🆗 range(ts1, ts2) — delega para AVL
    # 🆗 nearest(ts) — delega para AVL
    # 🆗 next_of(id) / prev_of(id) — delega successor/predecessor da AVL
    # remove_range(ts1, ts2) — remove lote da AVL + dict
    # 🆗 tag(id, t) / rate(id, r) — edita via dict
    # find_by_tag(tag) — in-order filtrando por tag
    # stats() — total, mais antiga, mais recente, rating médio e mediano
    # save(path) / load(path) — persistência JSON
    def __init__(self, commands: list = []):
        super().__init__()
        self.sec_index = dict()
        self.running = True
        self.commands = commands
        self.count = 0

    def add(self, user_input: list[str]):
        if len(user_input) != 3:
            print("Comando inválido. O formato correto é: :add <ts> <path> [rating]")
            return
        
        photo = Photo(self.gerenate_id(), timestamp=int(user_input[0]), path=user_input[1], rating=int(user_input[2]))

        self.insert(photo)
        self.sec_index[photo._id] = photo

    def remove(self, id):
        id = int(id)
        self.delete(self.get_by_id(id))
        self.sec_index.pop(id)

    def get_by_id(self, id):
        print(self.sec_index)
        result = self.sec_index.get(id)
        if not result:
            raise ValueError(f"Photo with id {id} not found")
        return result

    def range(self, ts1, ts2):
        result = super().range(int(ts1), int(ts2))
        if not result:
            raise ValueError("Nenhuma foto encontrada.")
        
        for photo in result:
            print(photo)

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
        return self.search(p)[1]  # aqui eu tenho a foto na árvore

    def next_of(self, id):
        photo = self.sec_index.get(int(id))
        result = self.successor(photo)

        if result:
            print(result.data())

    def prev_of(self, id):
        photo = self.sec_index.get(int(id))
        result = self.predecessor(photo)

        if result:
            print(result.data())

    def remove_range(self, ts1, ts2):
        ...
        
    def tag(self, id, t):
        id = int(id)
        photo = self.sec_index.get(id)
        if photo:
            photo.tags.append(t)

    def rate(self, id, r):
        id = int(id)
        r = int(r)
        if r < 0 or r > 5:
            raise ValueError("Rating deve ser um inteiro entre 0 e 5")
        photo = self.sec_index.get(id)
        if photo:
            photo.rating = r

    def find_by_tag(self, tag):
        ...

    def stats(self):
        ...

    def save(self, path):
        ...

    def load(self, path):
        ...

    def __repr__(self):
        return self.__str__()

    # def __str__(self):
    #     return self._index.in_order().__str__()
    
    def help(self):
        for command in self.commands:
            if command['option']:
                print(f"{command['command']} {command['option']}")
            else:
                print(command['command'])

    def quit(self):
        self.running = False

    def gerenate_id(self):
        self.count += 1
        return self.count
    
    def registerCommands(self):
        self.commands = [
            {'command': ':add', 'option': '<ts> <path> [rating]', 'function': self.add},
            {'command': ':import', 'option': '<manifest.json>', 'function': None},
            {'command': ':range', 'option': '<ts1> <ts2>', 'function': self.range},
            {'command': ':nearest', 'option': '<ts>', 'function': super().nearest},
            {'command': ':next', 'option': ' <id>', 'function': self.next_of},
            {'command': ':prev', 'option': ' <id>', 'function': self.prev_of},
            {'command': ':get', 'option': '<id>', 'function': None},
            {'command': ':tag', 'option': '<id> <tag>', 'function': None},
            {'command': ':rate', 'option': '<id> <0..5>', 'function': None},
            {'command': ':find-tag', 'option': '<tag>', 'function': None},
            {'command': ':remove', 'option': '<id>', 'function': self.remove},
            {'command': ':remove-range', 'option': '<ts1> <ts2>', 'function': None},
            {'command': ':stats', 'option': None, 'function': None},
            {'command': ':list', 'option': None, 'function': None},
            {'command': ':tree', 'option': None, 'function': None},
            {'command': ':save', 'option': '<f>', 'function': None},
            {'command': ':load', 'option': '<f>', 'function': None},
            {'command': ':help', 'option': None, 'function': self.help},
            {'command': ':quit', 'option': None, 'function': self.quit},
        ]

