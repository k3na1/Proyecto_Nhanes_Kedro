import pandas as pd

def convert_to_parquet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Recibe un DataFrame crudo desde el catálogo (SAS .xpt)
    y lo retorna tal cual para que el catálogo lo guarde como Parquet.
    """
    return df
