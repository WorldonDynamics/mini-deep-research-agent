import os
import sys
import pickle
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd

# Ensure the mini-repo src is importable when running tests from repo root
ROOT = os.path.dirname(os.path.dirname(__file__))
SRC_PATH = os.path.join(ROOT, "mini-deep-research-agent", "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

import utils as utils_mod


class UtilsTest(unittest.TestCase):
    def setUp(self):
        # Simple dataframe matching expected schema
        self.df = pd.DataFrame([
            {"title": "A", "abstract": "alpha", "authors": "X"},
            {"title": "B", "abstract": "beta", "authors": "Y"},
            {"title": "C", "abstract": "gamma", "authors": "Z"},
        ])

    @patch.object(utils_mod, "embed_texts")
    @patch.object(utils_mod, "model")
    def test_semantic_search_with_mocked_embeddings(self, mock_model, mock_embed_texts):
        # Mock embed_texts to return deterministic embeddings
        # 3 documents -> 3 embeddings of dimension 2
        mock_embed_texts.return_value = np.array([
            [1.0, 0.0],
            [0.0, 1.0],
            [0.7, 0.7],
        ])

        # Mock model.encode for query to produce an embedding similar to doc 3
        mock_model.encode.return_value = np.array([[0.7, 0.7]])

        top = utils_mod.semantic_search(self.df, "test query", top_k=2)

        # Should return 2 rows
        self.assertEqual(len(top), 2)

    def test_embed_texts_cache_behaviour(self):
        # Create a temporary cache file
        cache_file = os.path.join(os.path.dirname(__file__), "tmp_embeddings.pkl")
        try:
            arr = np.arange(6).reshape(3, 2)
            with open(cache_file, "wb") as f:
                pickle.dump(arr, f)

            loaded = utils_mod.embed_texts(["a", "b", "c"], cache_file=cache_file)
            # should return the same array from cache
            np.testing.assert_array_equal(loaded, arr)
        finally:
            if os.path.exists(cache_file):
                os.remove(cache_file)


if __name__ == "__main__":
    unittest.main()
