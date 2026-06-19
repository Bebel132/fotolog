class Photo:

    def __init__(self, id, timestamp, path, tags: list = None, rating: int = None):
        self._id = id
        self._timestamp = timestamp
        self._path = path
        self._tags = tags
        self._rating = rating

    def __le__(self, other):
        result = False
        if isinstance(other, Photo):
            result = self._timestamp <= other._timestamp
        return result

    def __gt__(self, other):
        result = False
        if isinstance(other, Photo):
            result = self._timestamp > other._timestamp
        return result

    def __eq__(self, other):
        result = False
        if isinstance(other, Photo):
            result = self._timestamp == other._timestamp and self._id == other._id
        return result

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self._timestamp} {self._path}'

