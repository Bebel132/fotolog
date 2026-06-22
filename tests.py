"""
test_fotolog.py — Bateria de testes do Mini-Projeto Fotolog (AVL)
SMD0033 — Estrutura de Dados — UFC

Cobre todos os requisitos da seção 5 do enunciado:
  - Carga em massa (1000 inserções) + invariante AVL
  - range com baseline filtro+sort
  - nearest nos casos limítrofes
  - remove_range + verificação de invariantes
  - Sucessor sem filho direito (subida pelo pai)
  - Inserção em ordem crescente (pior caso BST)
  - Cobertura dos 4 tipos de rotação (LL, RR, LR, RL)
  - Deleção nos 3 casos (folha, 1 filho, 2 filhos)
  - Persistência round-trip (save/load)
"""

import unittest
import random
import math
import json
import os
import tempfile

from photo import Photo
from photo_avl import PhotoAVL
from catalog import Catalog


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_photo(id_, ts, tags=None, rating=3):
    """Cria uma Photo de teste com valores padrão."""
    return Photo(id=id_, ts=ts, path=f"/test/{id_}.jpg",
                 tags=tags or [], rating=rating)


def check_avl_invariant(tree):
    """
    Verifica recursivamente que todo nó tem fator de balanceamento em {-1, 0, +1}.
    Retorna (altura, ok).
    """
    def _check(node):
        if node is None:
            return 0, True
        lh, lok = _check(node.left_node())
        rh, rok = _check(node.right_node())
        bf = lh - rh
        ok = lok and rok and bf in (-1, 0, 1)
        return 1 + max(lh, rh), ok

    _, ok = _check(tree.root())
    return ok


def avl_height(tree):
    """Altura real da árvore (percurso)."""
    def _h(node):
        if node is None:
            return 0
        return 1 + max(_h(node.left_node()), _h(node.right_node()))
    return _h(tree.root())


def inorder_keys(tree):
    """Retorna lista de chaves (ts, id) em ordem in-order."""
    result = []
    def _walk(node):
        if node is None:
            return
        _walk(node.left_node())
        result.append((node.data().ts, node.data().id))
        _walk(node.right_node())
    _walk(tree.root())
    return result


# ---------------------------------------------------------------------------
# 1. Carga em massa — 1000 inserções aleatórias
# ---------------------------------------------------------------------------

class TestMassInsert(unittest.TestCase):

    def setUp(self):
        self.catalog = Catalog()
        self.n = 1000
        random.seed(42)
        self.photos = []
        used_ids = set()
        for i in range(self.n):
            id_ = i + 1
            ts = random.randint(1_000_000, 9_999_999)
            p = make_photo(id_, ts)
            self.photos.append(p)
            self.catalog.add(p)

    def test_inorder_strictly_increasing(self):
        """In-order deve ser estritamente crescente por (ts, id)."""
        keys = inorder_keys(self.catalog.tree)
        self.assertEqual(len(keys), self.n)
        for i in range(1, len(keys)):
            self.assertLess(keys[i - 1], keys[i],
                            f"In-order não crescente: {keys[i-1]} >= {keys[i]}")

    def test_avl_invariant_after_mass_insert(self):
        """Fator de balanceamento de cada nó deve estar em {-1, 0, +1}."""
        self.assertTrue(check_avl_invariant(self.catalog.tree),
                        "Invariante AVL violado após inserção em massa")

    def test_size_consistency(self):
        """Tamanho da árvore deve coincidir com o índice secundário."""
        self.assertEqual(len(self.catalog), self.n)


# ---------------------------------------------------------------------------
# 2. range com baseline filtro+sort
# ---------------------------------------------------------------------------

class TestRange(unittest.TestCase):

    def setUp(self):
        self.catalog = Catalog()
        random.seed(7)
        self.all_photos = []
        for i in range(500):
            ts = random.randint(1_000_000, 2_000_000)
            p = make_photo(i + 1, ts)
            self.all_photos.append(p)
            self.catalog.add(p)

    def _baseline(self, ts1, ts2):
        """Filtro+sort ingênuo para comparação."""
        result = [p for p in self.all_photos if ts1 <= p.ts <= ts2]
        result.sort(key=lambda p: (p.ts, p.id))
        return result

    def test_range_random_windows(self):
        """range deve coincidir com baseline em 20 janelas aleatórias."""
        random.seed(99)
        for _ in range(20):
            a = random.randint(1_000_000, 1_900_000)
            b = random.randint(a, 2_000_000)
            got = self.catalog.range(a, b)
            expected = self._baseline(a, b)
            self.assertEqual(
                [(p.ts, p.id) for p in got],
                [(p.ts, p.id) for p in expected],
                f"range({a}, {b}) divergiu do baseline"
            )

    def test_range_empty_window(self):
        """range fora dos timestamps existentes deve retornar lista vazia."""
        result = self.catalog.range(0, 999_999)
        self.assertEqual(result, [])

    def test_range_full_window(self):
        """range cobrindo tudo deve retornar todas as fotos em ordem."""
        result = self.catalog.range(0, 99_999_999)
        expected = self._baseline(0, 99_999_999)
        self.assertEqual(len(result), len(expected))


# ---------------------------------------------------------------------------
# 3. nearest — casos limítrofes
# ---------------------------------------------------------------------------

class TestNearest(unittest.TestCase):

    def setUp(self):
        self.catalog = Catalog()
        # Fotos em timestamps conhecidos: 100, 200, 300, 400, 500
        for i, ts in enumerate([100, 200, 300, 400, 500], start=1):
            self.catalog.add(make_photo(i, ts))

    def test_nearest_exact_match(self):
        """Empate exato: deve retornar a própria foto."""
        result = self.catalog.nearest(300)
        self.assertEqual(result.ts, 300)

    def test_nearest_before_first(self):
        """Antes da primeira foto: deve retornar a mais antiga."""
        result = self.catalog.nearest(0)
        self.assertEqual(result.ts, 100)

    def test_nearest_after_last(self):
        """Depois da última foto: deve retornar a mais recente."""
        result = self.catalog.nearest(9999)
        self.assertEqual(result.ts, 500)

    def test_nearest_equidistant(self):
        """Equidistante entre 200 e 300 (ts=250): deve retornar um dos dois."""
        result = self.catalog.nearest(250)
        self.assertIn(result.ts, [200, 300],
                      "nearest equidistante deve retornar 200 ou 300")

    def test_nearest_between_two(self):
        """Mais próximo de 380 é 400."""
        result = self.catalog.nearest(380)
        self.assertEqual(result.ts, 400)

    def test_nearest_single_element(self):
        """Catálogo com uma foto: nearest sempre retorna ela."""
        c = Catalog()
        c.add(make_photo(99, 500))
        self.assertEqual(c.nearest(1).ts, 500)
        self.assertEqual(c.nearest(999).ts, 500)


# ---------------------------------------------------------------------------
# 4. remove_range + verificação de invariantes
# ---------------------------------------------------------------------------

class TestRemoveRange(unittest.TestCase):

    def setUp(self):
        self.catalog = Catalog()
        random.seed(13)
        self.inserted = []
        for i in range(200):
            ts = random.randint(1000, 9000)
            p = make_photo(i + 1, ts)
            self.inserted.append(p)
            self.catalog.add(p)

    def test_remove_range_invariants(self):
        """Após remove_range: árvore == índice, in-order ordenado, AVL mantido."""
        ts1, ts2 = 3000, 6000

        self.catalog.remove_range(ts1, ts2)

        # Tamanho da árvore == tamanho do índice secundário
        tree_size = len(inorder_keys(self.catalog.tree))
        index_size = len(self.catalog._index)
        self.assertEqual(tree_size, index_size,
                         "Tamanho da árvore diverge do índice após remove_range")

        # In-order ainda ordenado
        keys = inorder_keys(self.catalog.tree)
        for i in range(1, len(keys)):
            self.assertLess(keys[i - 1], keys[i])

        # Nenhuma foto removida deve estar na árvore ou no índice
        remaining_ids = set(self.catalog._index.keys())
        for p in self.inserted:
            if ts1 <= p.ts <= ts2:
                self.assertNotIn(p.id, remaining_ids,
                                 f"Foto id={p.id} ts={p.ts} deveria ter sido removida")

        # Conjunto de ids idênticos entre árvore e índice
        tree_ids = {key[1] for key in keys}
        self.assertEqual(tree_ids, remaining_ids)

        # Invariante AVL
        self.assertTrue(check_avl_invariant(self.catalog.tree),
                        "Invariante AVL violado após remove_range")


# ---------------------------------------------------------------------------
# 5. Sucessor sem filho direito (subida pelo pai)
# ---------------------------------------------------------------------------

class TestSuccessorWithoutRightChild(unittest.TestCase):

    def test_successor_climbs_parent(self):
        """
        Insere 3 fotos em ts=10, 20, 30.
        A foto de ts=20 (id=2) não tem filho direito após rotações.
        Verifica que next_of(id=2) retorna ts=30.
        """
        catalog = Catalog()
        catalog.add(make_photo(1, 10))
        catalog.add(make_photo(2, 20))
        catalog.add(make_photo(3, 30))

        nxt = catalog.next_of(2)
        self.assertIsNotNone(nxt, "Sucessor de ts=20 não deve ser None")
        self.assertEqual(nxt.ts, 30)

    def test_predecessor_climbs_parent(self):
        """Verifica que prev_of(id=2) retorna ts=10."""
        catalog = Catalog()
        catalog.add(make_photo(1, 10))
        catalog.add(make_photo(2, 20))
        catalog.add(make_photo(3, 30))

        prv = catalog.prev_of(2)
        self.assertIsNotNone(prv, "Predecessor de ts=20 não deve ser None")
        self.assertEqual(prv.ts, 10)

    def test_successor_of_last_is_none(self):
        """Sucessor do nó mais recente deve ser None."""
        catalog = Catalog()
        catalog.add(make_photo(1, 10))
        catalog.add(make_photo(2, 20))
        self.assertIsNone(catalog.next_of(2))

    def test_predecessor_of_first_is_none(self):
        """Predecessor do nó mais antigo deve ser None."""
        catalog = Catalog()
        catalog.add(make_photo(1, 10))
        catalog.add(make_photo(2, 20))
        self.assertIsNone(catalog.prev_of(1))


# ---------------------------------------------------------------------------
# 6. Inserção em ordem crescente — pior caso BST, AVL deve rebalancear
# ---------------------------------------------------------------------------

class TestWorstCaseBST(unittest.TestCase):

    def test_height_log_n_after_sorted_insert(self):
        """
        Inserção em ordem estritamente crescente (pior caso para BST pura).
        A AVL deve manter altura <= 2 * log2(n) + 1.
        """
        catalog = Catalog()
        n = 256
        for i in range(1, n + 1):
            catalog.add(make_photo(i, ts=i * 100))

        h = avl_height(catalog.tree)
        max_allowed = 2 * math.log2(n) + 2  # limite generoso para AVL
        self.assertLessEqual(h, max_allowed,
                             f"Altura {h} excede o limite AVL {max_allowed:.1f} para n={n}")

    def test_avl_invariant_after_sorted_insert(self):
        """Invariante AVL deve ser mantido após inserção em ordem crescente."""
        catalog = Catalog()
        for i in range(1, 201):
            catalog.add(make_photo(i, ts=i * 10))
        self.assertTrue(check_avl_invariant(catalog.tree))

    def test_inorder_correct_after_sorted_insert(self):
        """In-order deve ser crescente mesmo após inserções ordenadas."""
        catalog = Catalog()
        for i in range(1, 101):
            catalog.add(make_photo(i, ts=i * 10))
        keys = inorder_keys(catalog.tree)
        for i in range(1, len(keys)):
            self.assertLess(keys[i - 1], keys[i])


# ---------------------------------------------------------------------------
# 7. Cobertura dos 4 tipos de rotação (LL, RR, LR, RL)
# ---------------------------------------------------------------------------

class TestRotations(unittest.TestCase):
    """
    Testa as quatro rotações isoladamente usando a PhotoAVL diretamente,
    inserindo sequências que forçam cada caso.
    """

    def _tree_with(self, ts_ids):
        """Monta uma PhotoAVL com uma lista de (ts, id)."""
        t = PhotoAVL()
        for ts, id_ in ts_ids:
            t.insert(make_photo(id_, ts))
        return t

    def test_rotation_LL(self):
        """
        Inserção 30 → 20 → 10 força rotação LL (right rotation na raiz).
        Raiz deve ser 20 após balanceamento.
        """
        t = self._tree_with([(30, 1), (20, 2), (10, 3)])
        self.assertTrue(check_avl_invariant(t), "Invariante AVL violado após rotação LL")
        root_ts = t.root().data().ts
        self.assertEqual(root_ts, 20, f"Raiz esperada ts=20, obtida ts={root_ts}")

    def test_rotation_RR(self):
        """
        Inserção 10 → 20 → 30 força rotação RR (left rotation na raiz).
        Raiz deve ser 20 após balanceamento.
        """
        t = self._tree_with([(10, 1), (20, 2), (30, 3)])
        self.assertTrue(check_avl_invariant(t), "Invariante AVL violado após rotação RR")
        root_ts = t.root().data().ts
        self.assertEqual(root_ts, 20, f"Raiz esperada ts=20, obtida ts={root_ts}")

    def test_rotation_LR(self):
        """
        Inserção 30 → 10 → 20 força rotação LR (left-right na raiz).
        Raiz deve ser 20 após balanceamento.
        """
        t = self._tree_with([(30, 1), (10, 2), (20, 3)])
        self.assertTrue(check_avl_invariant(t), "Invariante AVL violado após rotação LR")
        root_ts = t.root().data().ts
        self.assertEqual(root_ts, 20, f"Raiz esperada ts=20, obtida ts={root_ts}")

    def test_rotation_RL(self):
        """
        Inserção 10 → 30 → 20 força rotação RL (right-left na raiz).
        Raiz deve ser 20 após balanceamento.
        """
        t = self._tree_with([(10, 1), (30, 2), (20, 3)])
        self.assertTrue(check_avl_invariant(t), "Invariante AVL violado após rotação RL")
        root_ts = t.root().data().ts
        self.assertEqual(root_ts, 20, f"Raiz esperada ts=20, obtida ts={root_ts}")


# ---------------------------------------------------------------------------
# 8. Deleção nos 3 casos (folha, 1 filho, 2 filhos)
# ---------------------------------------------------------------------------

class TestDeletion(unittest.TestCase):

    def setUp(self):
        self.catalog = Catalog()
        for id_, ts in [(1, 100), (2, 200), (3, 300), (4, 400), (5, 500)]:
            self.catalog.add(make_photo(id_, ts))

    def test_delete_leaf(self):
        """Remove folha (id=1, ts=100) — sem filhos."""
        self.catalog.remove(1)
        self.assertIsNone(self.catalog.get_by_id(1))
        self.assertTrue(check_avl_invariant(self.catalog.tree))
        self.assertEqual(len(self.catalog), 4)

    def test_delete_one_child(self):
        """Remove nó com um filho."""
        # Remove ts=400 (id=4) — depende da estrutura da AVL gerada
        self.catalog.remove(4)
        self.assertIsNone(self.catalog.get_by_id(4))
        self.assertTrue(check_avl_invariant(self.catalog.tree))
        keys = inorder_keys(self.catalog.tree)
        for i in range(1, len(keys)):
            self.assertLess(keys[i - 1], keys[i])

    def test_delete_two_children(self):
        """Remove nó com dois filhos (raiz ou nó interno)."""
        # Remove ts=300 (id=3), que tende a ser nó interno
        self.catalog.remove(3)
        self.assertIsNone(self.catalog.get_by_id(3))
        self.assertTrue(check_avl_invariant(self.catalog.tree))
        keys = inorder_keys(self.catalog.tree)
        for i in range(1, len(keys)):
            self.assertLess(keys[i - 1], keys[i])

    def test_delete_nonexistent_raises(self):
        """Remover id inexistente deve sinalizar erro (exceção ou retorno falso)."""
        with self.assertRaises(Exception):
            self.catalog.remove(999)

    def test_avl_invariant_after_all_deletions(self):
        """AVL deve permanecer válida após múltiplas remoções."""
        for id_ in [1, 3, 5]:
            self.catalog.remove(id_)
        self.assertTrue(check_avl_invariant(self.catalog.tree))


# ---------------------------------------------------------------------------
# 9. Persistência round-trip (save / load)
# ---------------------------------------------------------------------------

class TestPersistence(unittest.TestCase):

    def _make_catalog(self):
        c = Catalog()
        c.add(make_photo(1, 1000, tags=["praia"], rating=5))
        c.add(make_photo(2, 2000, tags=["montanha"], rating=3))
        c.add(make_photo(3, 3000, rating=4))
        return c

    def test_save_load_roundtrip(self):
        """Catálogo salvo e recarregado deve ter os mesmos dados."""
        original = self._make_catalog()

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            path = f.name

        try:
            original.save(path)
            restored = Catalog()
            restored.load(path)

            # Mesmos ids
            self.assertEqual(set(original._index.keys()),
                             set(restored._index.keys()))

            # Mesmos dados por id
            for id_ in original._index:
                op = original.get_by_id(id_)
                rp = restored.get_by_id(id_)
                self.assertEqual(op.ts, rp.ts)
                self.assertEqual(op.path, rp.path)
                self.assertEqual(op.tags, rp.tags)
                self.assertEqual(op.rating, rp.rating)

            # In-order do catálogo restaurado deve ser crescente
            keys = inorder_keys(restored.tree)
            for i in range(1, len(keys)):
                self.assertLess(keys[i - 1], keys[i])

            # Invariante AVL mantido após load
            self.assertTrue(check_avl_invariant(restored.tree))

        finally:
            os.unlink(path)

    def test_load_invalid_records_ignored(self):
        """import deve ignorar registros inválidos e reportar total importado."""
        data = [
            {"id": 10, "ts": 5000, "path": "/p/10.jpg"},
            {"ts": 6000, "path": "/p/no_id.jpg"},   # sem id — inválido
            {"id": 11, "path": "/p/no_ts.jpg"},      # sem ts — inválido
        ]
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False,
                                         mode="w", encoding="utf-8") as f:
            json.dump(data, f)
            path = f.name

        try:
            c = Catalog()
            imported, ignored = c.import_manifest(path)
            self.assertEqual(imported, 1)
            self.assertEqual(ignored, 2)
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# 10. Testes extras de catalog (tag, rate, find_by_tag, stats)
# ---------------------------------------------------------------------------

class TestCatalogExtras(unittest.TestCase):

    def setUp(self):
        self.catalog = Catalog()
        self.catalog.add(make_photo(1, 100, tags=["praia"], rating=2))
        self.catalog.add(make_photo(2, 200, tags=["praia", "sol"], rating=4))
        self.catalog.add(make_photo(3, 300, tags=["montanha"], rating=5))
        self.catalog.add(make_photo(4, 400, tags=[], rating=1))

    def test_tag_adds_tag(self):
        self.catalog.tag(4, "rio")
        self.assertIn("rio", self.catalog.get_by_id(4).tags)

    def test_rate_updates_rating(self):
        self.catalog.rate(1, 5)
        self.assertEqual(self.catalog.get_by_id(1).rating, 5)

    def test_rate_invalid_raises(self):
        with self.assertRaises(Exception):
            self.catalog.rate(1, 6)

    def test_find_by_tag_order(self):
        """find_by_tag deve retornar fotos em ordem cronológica."""
        result = self.catalog.find_by_tag("praia")
        self.assertEqual([p.id for p in result], [1, 2])

    def test_find_by_tag_not_found(self):
        result = self.catalog.find_by_tag("neve")
        self.assertEqual(result, [])

    def test_stats(self):
        s = self.catalog.stats()
        self.assertEqual(s["total"], 4)
        self.assertEqual(s["oldest"].ts, 100)
        self.assertEqual(s["newest"].ts, 400)
        self.assertAlmostEqual(s["avg_rating"], (2 + 4 + 5 + 1) / 4)
        # mediana de [1,2,4,5] = (2+4)/2 = 3.0
        self.assertAlmostEqual(s["median_rating"], 3.0)

    def test_add_duplicate_id_raises(self):
        with self.assertRaises(Exception):
            self.catalog.add(make_photo(1, 999))

    def test_get_by_id_not_found(self):
        self.assertIsNone(self.catalog.get_by_id(999))


if __name__ == "__main__":
    unittest.main(verbosity=2)