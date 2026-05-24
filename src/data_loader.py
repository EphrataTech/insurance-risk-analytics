import pandas as pd


def load_data(filepath: str, chunksize: int = 100_000, usecols=None) -> pd.DataFrame:
    kwargs = {"sep": "|", "low_memory": False, "chunksize": chunksize}
    if usecols is not None:
        kwargs["usecols"] = usecols
    return pd.concat(pd.read_csv(filepath, **kwargs), ignore_index=True)
