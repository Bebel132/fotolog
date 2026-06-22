import json

from avlTree import AVLTree
from photo import Photo
from photo_avl import PhotoAVL


class Catalog():
    def __init__(self, commands: list = []):
        self.tree = PhotoAVL()
        self._index = dict()
        self.running = True
        self.commands = commands
        self.count = 0

    def add(self, photo: Photo):
        if photo._id in self._index:
            raise ValueError(f"Photo with id {photo._id} already exists")
        self.tree.insert(photo)
        self._index[photo._id] = photo

    def input_add(self, ts, path, rating):
        if ts is None or path is None or rating is None:
            print("Comando inválido. O formato correto é: :add <ts> <path> [rating]")
            return
        
        photo = Photo(self.gerenate_id(), ts=int(ts), path=path, rating=int(rating))

        self.add(photo)

    def remove(self, id):
        id = int(id)
        self.tree.delete(self.get_by_id(id))
        self._index.pop(id)

    def get_by_id(self, id, print_result=False):
        id = int(id)
        result = self._index.get(id)

        if not result:
            print("Nenhuma foto encontrada.")
            return None
        
        if print_result:
            print(result.format('long'))

        return result

    def range(self, ts1, ts2):
        result = self.tree.range(int(ts1), int(ts2))
        if not result:
            print("Nenhuma foto encontrada.")
            return []
        
        list = [node for node in result]
        # print(f"{len(list)} foto(s) encontrada(s):")
        # for photo in list:
        #     print(photo.format('long'))
        return list

    def next_of(self, id):
        photo = self._index.get(int(id))
        result = self.tree.successor(photo)

        if result:
            print(result.data().format('long'))
            return result.data()
        else:
            print("Nenhuma foto encontrada.")
            return None

    def prev_of(self, id):
        photo = self._index.get(int(id))
        result = self.tree.predecessor(photo)

        if result:
            print(result.data().format('long'))
            return result.data()
        else:
            print("Nenhuma foto encontrada.")
            return None

    def remove_range(self, ts1, ts2):
        result = self.tree.range(int(ts1), int(ts2))
        
        for photo in result:
            self.remove(photo.id)
        
    def tag(self, id, t):
        id = int(id)
        photo = self._index.get(id)
        if photo:
            photo.tags.append(t)

    def rate(self, id, r):
        id = int(id)
        r = int(r)
        if r < 1 or r > 5:
            raise ValueError("Rating deve ser um inteiro entre 1 e 5")
        photo = self._index.get(id)
        if photo:
            photo.rating = r

    def find_by_tag(self, tag):
        result = self.tree.in_order() 
        result = [node.data() for node in result if tag in node.data().tags]
        if not result:
            print("Nenhuma foto encontrada.")
            return []
        
        for photo in result:
            print(photo.format('long'))
        return result

    def stats(self):
        result = self.tree.in_order()
        data = {}
        data['total'] = len(result)
        data['oldest'] = result[0].data()
        data['newest'] = result[-1].data()

        # ordena por rating
        ratings = sorted(
            [node.data().rating for node in result 
                if node.data().rating is not None]
        )

        if ratings:
            n = len(ratings)
            data['avg_rating'] = sum(ratings) / n

            # calcula a mediana
            if n % 2 == 1:
                # se for impar, resgata o valor do meio
                median = ratings[n // 2]
            else:
                # se for par, resgata os dois valores do meio e calcula a média
                median = (ratings[n//2 - 1] + ratings[n//2]) / 2

            data['median_rating'] = median
        else:
            data['median_rating'] = None
            data['avg_rating'] = None

        print(f"Total de fotos: {data['total']}")
        print(f"Foto mais antiga: {data['oldest'].format('long')}")
        print(f"Foto mais recente: {data['newest'].format('long')}")
        print(f"Rating médio: {data['avg_rating'] if data['avg_rating'] is not None else 'N/A'}")
        print(f"Rating mediano: {data['median_rating'] if data['median_rating'] is not None else 'N/A'}")

        return data

    def save(self, path):
        path += '.json' if not path.endswith('.json') else ''

        json_data = []

        for photo in self._index.values():
            json_data.append({
                'id': photo._id,
                'ts': photo._ts,
                'path': photo._path,
                'tags': photo._tags,
                'rating': photo._rating
            })

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f)

    def load(self, path):
        path += '.json' if not path.endswith('.json') else ''

        with open(path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)

        self.tree.reset()
        
        for data in json_data:
            photo = Photo(
                id=self.gerenate_id(),
                ts=int(data['ts']),
                path=data['path'],
                tags=data.get('tags', []),
                rating=data.get('rating', None)
            )
            self.tree.insert(photo)
            self._index[photo._id] = photo

    def import_manifest(self, path):
        path += '.json' if not path.endswith('.json') else ''
        ignored, imported = 0, 0

        with open(path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        for data in json_data:
            if data.get('ts') is None or not isinstance(data['ts'], int) or data.get('path') is None or data.get('id') is None:
            #if data['ts'] is None or not isinstance(data['ts'], int) or data['path'] is None:
                ignored += 1
                continue
            else:
                photo = Photo(
                    id=self.gerenate_id(),
                    ts=int(data['ts']),
                    path=data['path'],
                    tags=data.get('tags', []),
                    rating=data.get('rating', 1)
                )
                self.tree.insert(photo)
                self._index[photo._id] = photo
                imported += 1

        return imported, ignored

    def nearest(self, ts):
        return self.tree.nearest(ts)
    
    def range(self, ts1, ts2):
        ts1, ts2 = int(ts1), int(ts2)
        result = self.tree.range(ts1, ts2)

        if not result:
            print("Nenhuma foto encontrada.")
            return []
        
        for photo in result:
            print(photo.format('long'))
        return result

    def list(self):
        result = self.tree.in_order() 
        for node in result:
            print(node.data().format('long'))

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
            {'command': ':add', 'option': '<ts> <path> [rating]', 'function': self.input_add},
            {'command': ':import', 'option': '<manifest.json>', 'function': self.import_manifest},
            {'command': ':range', 'option': '<ts1> <ts2>', 'function': self.range},
            {'command': ':nearest', 'option': '<ts>', 'function': self.nearest},
            {'command': ':next', 'option': ' <id>', 'function': self.next_of},
            {'command': ':prev', 'option': ' <id>', 'function': self.prev_of},
            {'command': ':get', 'option': '<id>', 'function': lambda id: self.get_by_id(id, print_result=True)},
            {'command': ':tag', 'option': '<id> <tag>', 'function': self.tag},
            {'command': ':rate', 'option': '<id> <1..5>', 'function': self.rate},
            {'command': ':find-tag', 'option': '<tag>', 'function': self.find_by_tag},
            {'command': ':remove', 'option': '<id>', 'function': self.remove},
            {'command': ':remove-range', 'option': '<ts1> <ts2>', 'function': self.remove_range},
            {'command': ':stats', 'option': None, 'function': self.stats},
            {'command': ':list', 'option': None, 'function': self.list},
            {'command': ':tree', 'option': None, 'function': self.tree.print_tree},
            {'command': ':save', 'option': '<f>', 'function': self.save},
            {'command': ':load', 'option': '<f>', 'function': self.load},
            {'command': ':help', 'option': None, 'function': self.help},
            {'command': ':quit', 'option': None, 'function': self.quit},
        ]

    def __len__(self):
        return len(self._index)