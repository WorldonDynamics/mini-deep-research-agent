import numpy as np
import utils


def test_embed_texts_cache(tmp_path, monkeypatch):
    class FakeModel:
        def encode(self, texts_in):
            # deterministic, small embedding for tests
            return np.array([[1.0, 0.0], [0.0, 1.0]])

    # Ensure utils.get_model returns our fake model
    monkeypatch.setattr(utils, "get_model", lambda: FakeModel())

    cache_file = tmp_path / "embeddings.pkl"

    # First call should create cache using fake model
    emb1 = utils.embed_texts(["a", "b"], str(cache_file))
    assert emb1.shape == (2, 2)

    # Replace get_model with a function that raises if called
    monkeypatch.setattr(utils, "get_model", lambda: (_ for _ in ()).throw(RuntimeError("Should not be called")))

    # Second call should load from cache and not call get_model
    emb2 = utils.embed_texts(["a", "b"], str(cache_file))
    np.testing.assert_array_equal(emb1, emb2)
