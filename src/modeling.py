import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score, mean_squared_error, r2_score
import joblib


def split_data(df, target: str, test_size: float = 0.2, stratify=None):
    """Split data into training and testing sets"""
    X = df.drop(columns=[target])
    y = df[target]
    
    if stratify is not None and stratify in df.columns:
        stratify_col = df[stratify]
    else:
        stratify_col = None
        
    return train_test_split(X, y, test_size=test_size, random_state=42, stratify=stratify_col)


def prepare_features(df):
    """Prepare features for modeling"""
    df_model = df.copy()
    
    # Handle missing values
    df_model['Gender'] = df_model['Gender'].fillna('Unknown')
    df_model['MaritalStatus'] = df_model['MaritalStatus'].fillna('Unknown')
    
    # Create new features
    df_model['VehicleAge'] = 2015 - df_model['RegistrationYear']  # Assuming data is from 2015
    df_model['IsNewVehicle'] = (df_model['VehicleAge'] <= 2).astype(int)
    df_model['HighValueVehicle'] = (df_model['SumInsured'] > df_model['SumInsured'].quantile(0.75)).astype(int)
    
    # Encode categorical variables
    categorical_cols = ['Province', 'Gender', 'MaritalStatus', 'VehicleType', 'make', 'Model']
    
    for col in categorical_cols:
        if col in df_model.columns:
            le = LabelEncoder()
            df_model[f'{col}_encoded'] = le.fit_transform(df_model[col].astype(str))
    
    return df_model


def train_claim_prediction_models(X_train, y_train, X_test, y_test):
    """Train multiple models for claim prediction"""
    models = {
        'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42)
    }
    
    results = {}
    
    for name, model in models.items():
        # Train the model
        model.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test)
        y_pred_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
        
        # Calculate metrics
        accuracy = model.score(X_test, y_test)
        auc = roc_auc_score(y_test, y_pred_proba) if y_pred_proba is not None else None
        
        results[name] = {
            'model': model,
            'accuracy': accuracy,
            'auc': auc,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
    
    return results


def calculate_risk_score(model, X_data):
    """Calculate risk scores using a trained model"""
    if hasattr(model, 'predict_proba'):
        return model.predict_proba(X_data)[:, 1]  # Probability of claim
    else:
        return model.predict(X_data)


def recommend_premium_adjustment(risk_score, base_premium=1000):
    """Recommend premium adjustments based on risk score"""
    if risk_score < 0.1:
        return base_premium * 0.8  # 20% discount for low risk
    elif risk_score < 0.3:
        return base_premium * 0.9  # 10% discount for medium-low risk
    elif risk_score < 0.7:
        return base_premium * 1.0  # Standard premium
    else:
        return base_premium * 1.3  # 30% increase for high risk


def evaluate(model, X_test, y_test, task_type='classification'):
    """Evaluate a trained model"""
    if task_type == 'classification':
        preds = model.predict(X_test)
        return classification_report(y_test, preds)
    elif task_type == 'regression':
        preds = model.predict(X_test)
        mse = mean_squared_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        return f"MSE: {mse:.2f}\nR²: {r2:.4f}\nRMSE: {np.sqrt(mse):.2f}"
    else:
        raise ValueError("task_type must be 'classification' or 'regression'")
