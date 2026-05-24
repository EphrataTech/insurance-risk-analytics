from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def split_data(df, target: str, test_size: float = 0.2):
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(X, y, test_size=test_size, random_state=42)


def evaluate(model, X_test, y_test) -> str:
    preds = model.predict(X_test)
    return classification_report(y_test, preds)
