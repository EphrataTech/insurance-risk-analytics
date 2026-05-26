# Task 4: Machine Learning Modeling - Summary

## Overview
Task 4 implements comprehensive machine learning models to help ACIS optimize their insurance pricing and risk assessment strategy. This task builds upon the insights from EDA (Task 1) and hypothesis testing (Task 2) to create predictive models.

## Models Implemented

### 1. Claim Prediction Model (Binary Classification)
- **Purpose**: Predict whether a policy will have claims
- **Models**: Logistic Regression, Random Forest, Gradient Boosting
- **Target Variable**: HasClaim (0/1)
- **Evaluation Metrics**: Accuracy, AUC-ROC, Precision, Recall

### 2. Claim Severity Model (Regression)
- **Purpose**: Predict the amount of claims for policies that do have claims
- **Models**: Linear Regression, Random Forest Regressor
- **Target Variable**: TotalClaims (for policies with claims > 0)
- **Evaluation Metrics**: MSE, R², RMSE

### 3. Risk Scoring System
- **Purpose**: Assign risk scores to policies for premium optimization
- **Output**: Risk probability (0-1) and risk categories (Low, Medium, High, Very High)
- **Business Application**: Dynamic premium adjustments based on risk

## Key Features Used
- Province (encoded)
- Gender (encoded) 
- Marital Status (encoded)
- Sum Insured
- Custom Value Estimate
- Vehicle Age (derived feature)
- Is New Vehicle (derived feature)
- High Value Vehicle (derived feature)
- Postal Code
- Vehicle specifications (Cylinders, Cubic Capacity, Kilowatts, Number of Doors)

## Business Impact

### Premium Recommendations
- **Low Risk (0-10% claim probability)**: 20% premium discount
- **Medium Risk (10-30% claim probability)**: 10% premium discount  
- **High Risk (30-70% claim probability)**: Standard premium
- **Very High Risk (70%+ claim probability)**: 30% premium increase

### Expected Outcomes
- More accurate risk assessment
- Improved profitability through risk-based pricing
- Better customer segmentation
- Reduced adverse selection

## Model Deployment
- Best performing model saved as `best_claim_prediction_model.pkl`
- Feature importance analysis for interpretability
- Risk scoring function for real-time application
- Premium recommendation engine

## Implementation Recommendations
1. Deploy model for real-time risk scoring during quote generation
2. Implement risk-based premium adjustments gradually
3. Monitor model performance monthly
4. Retrain models quarterly with new data
5. A/B test premium adjustments to validate business impact

## Files Created
- `notebooks/03_modeling.ipynb`: Complete modeling workflow
- `src/modeling.py`: Enhanced modeling functions
- `models/`: Directory for storing trained models
- `reports/`: Model performance visualizations

This comprehensive modeling approach enables ACIS to move from traditional flat-rate pricing to sophisticated risk-based pricing, potentially improving both profitability and competitiveness in the market.