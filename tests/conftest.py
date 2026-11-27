import numpy as np
import pandas as pd
import pytest

@pytest.fixture
def sample_df():
  rng = np.random.default_rng(0) # fixed seed, thus the fixture produces the same values each time
  return pd.DataFrame({
    "price":rng.uniform(5,50,50), # 50 random prices spread evenly between €5 and €50
    "sold":rng.integers(0,2,50) # 50 random whole numbers from 0 up to 2 (exclusive) – i.e each is 0 (not sold) or 1 (sold)
  })