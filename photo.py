class Photo:

    def __init__(self, id, timestamp, path, tags: list = None, rating: int = None):
        self._id = id
        self._timestamp = timestamp
        self._path = path
        self._tags = tags if tags is not None else []   
        self._rating = rating

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        self._timestamp = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        if not isinstance(value, list):
            raise TypeError("tags deve ser uma lista")
        self._tags = value

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("rating deve ser um inteiro")
        self._rating = value

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
        return f'timestamp: {self._timestamp}, path: {self._path}'