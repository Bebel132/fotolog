from abc import ABC, abstractmethod

class TreeADT(ABC):

    @abstractmethod
    def insert(self, value):
        """Insere <value> na árvore"""
        pass

    @abstractmethod
    def empty(self):
        """Verifica se a árvore está vazia"""
        pass

    @abstractmethod
    def root(self):
        """Retorna o nó raiz da árvore"""
        pass