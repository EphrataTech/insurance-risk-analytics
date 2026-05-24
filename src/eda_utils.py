import pandas as pd
import matplotlib.pyplot as plt


def summarize(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include="all")


def plot_distribution(df: pd.DataFrame, column: str) -> None:
    df[column].hist()
    plt.title(column)
    plt.show()
