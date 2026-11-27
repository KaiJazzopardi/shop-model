import pandas as pd
import pytest

from shop_model.features import add_vat
from shop_model.model import train_model

def test_add_vat_value(): # value test
  df = pd.DataFrame({"price":[100.0]})
  result = add_vat(df,0.18)
  assert result["price"].iloc[0] == pytest.approx(118.0)

def test_add_vat_value_zero(): # value test
  df = pd.DataFrame({"price":[100.0]})
  result = add_vat(df,0)
  assert result["price"].iloc[0] == pytest.approx(100.0)

def test_add_vat_does_not_modify_input(sample_df): # side effect test
  original = sample_df.copy()
  add_vat(sample_df,0.18)
  pd.testing.assert_frame_equal(sample_df, original)

def test_training_smoke_and_determinism(sample_df):

  # smoke test – does the training run? "smoke" as in does it catch fire? does it train?
  a = train_model(sample_df, seed=42).predict_proba(sample_df[["price"]])[:,1] 
  b = train_model(sample_df, seed=42).predict_proba(sample_df[["price"]])[:,1]
  assert len(a) == len(sample_df) # Checks that we obtained one prediction for every observation.
  assert ((a>=0)&(a<=1)).all() # is every output a valid probability (Checks that all predicted probabilities are between 0 and 1)
  assert a == pytest.approx(b) # determinism: training twice with the same seed gives the same predictions