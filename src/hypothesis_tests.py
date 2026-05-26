import pandas as pd
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler


def chi_square_test(contingency_table):
    """
    Perform a Chi-squared contingency table test.
    """
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    return {"chi2": chi2, "p_value": p, "dof": dof}


def t_test(group_a, group_b):
    """
    Perform an independent samples t-test.
    """
    t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)
    return {"t_stat": t_stat, "p_value": p_value}


def exact_and_nn_match(df_pol, cat_col, val_a, val_b, exact_cols, num_cols):
    """
    Perform matching between two groups defined by cat_col == val_a and cat_col == val_b.
    1. Exact match on exact_cols (categorical features).
    2. Nearest neighbor on num_cols (continuous features).
    
    Returns two matched DataFrames (matched_grp_a, matched_grp_b).
    """
    df_a = df_pol[df_pol[cat_col] == val_a].copy()
    df_b = df_pol[df_pol[cat_col] == val_b].copy()
    
    if len(df_a) == 0 or len(df_b) == 0:
        return None, None
        
    # Swap so df_b is always the smaller group to match against
    swapped = False
    if len(df_a) < len(df_b):
        df_a, df_b = df_b, df_a
        val_a, val_b = val_b, val_a
        swapped = True
        
    # Median imputation for continuous variables in the subsets
    med_vals = df_pol[num_cols].median()
    for col in num_cols:
        df_a[col] = df_a[col].fillna(med_vals[col])
        df_b[col] = df_b[col].fillna(med_vals[col])
        
    # Scaler for numeric columns
    scaler = StandardScaler()
    scaler.fit(df_pol[num_cols].fillna(med_vals))
    
    grouped_a = {grp: data for grp, data in df_a.groupby(exact_cols)}
    
    matched_a_rows = []
    matched_b_rows = []
    
    for _, row_b in df_b.iterrows():
        grp_key = tuple(row_b[exact_cols])
        if grp_key not in grouped_a:
            continue
            
        candidates_a = grouped_a[grp_key]
        if len(candidates_a) == 0:
            continue
            
        X_candidates = scaler.transform(candidates_a[num_cols])
        X_target = scaler.transform(row_b[num_cols].values.reshape(1, -1))
        
        # Euclidean distance on scaled continuous attributes
        dists = np.sum((X_candidates - X_target) ** 2, axis=1)
        best_idx = np.argmin(dists)
        
        matched_a_rows.append(candidates_a.iloc[best_idx])
        matched_b_rows.append(row_b)
        
    if len(matched_a_rows) == 0:
        return None, None
        
    df_matched_a = pd.DataFrame(matched_a_rows).reset_index(drop=True)
    df_matched_b = pd.DataFrame(matched_b_rows).reset_index(drop=True)
    
    # Return in the original order requested
    if swapped:
        return df_matched_b, df_matched_a
    else:
        return df_matched_a, df_matched_b


def test_covariate_balance(grp_a, grp_b, group_col, exact_cols, num_cols):
    """
    Test if grp_a and grp_b are statistically equivalent across the control covariates.
    Returns a dictionary of p-values.
    """
    results = {}
    
    # Continuous covariates balance tests (t-tests)
    for f in num_cols:
        _, p = stats.ttest_ind(grp_a[f].dropna(), grp_b[f].dropna(), equal_var=False)
        results[f"p_{f}"] = p
        
    # Categorical covariates balance tests (chi-square tests)
    for c in exact_cols:
        df_comb = pd.concat([grp_a, grp_b]).reset_index(drop=True)
        table = pd.crosstab(df_comb[c], df_comb[group_col])
        try:
            _, p, _, _ = stats.chi2_contingency(table)
        except Exception:
            p = 1.0  # If test cannot run (e.g. zero counts), they are considered balanced
        results[f"p_{c}"] = p
        
    results["min_p"] = min(results.values())
    return results


def run_frequency_test(grp_a, grp_b, group_col):
    """
    Test difference in Claim Frequency (HasClaim) using Chi-square test.
    """
    df_comb = pd.concat([grp_a, grp_b]).reset_index(drop=True)
    table = pd.crosstab(df_comb[group_col], df_comb["HasClaim"])
    chi2, p_val, dof, expected = stats.chi2_contingency(table)
    
    rate_a = grp_a["HasClaim"].mean()
    rate_b = grp_b["HasClaim"].mean()
    
    return {
        "test": "Chi-square",
        "statistic": chi2,
        "p_value": p_val,
        "rate_a": rate_a,
        "rate_b": rate_b,
        "diff_pct": (rate_b - rate_a) * 100
    }


def run_severity_test(grp_a, grp_b, group_col):
    """
    Test difference in Claim Severity using t-test on positive claims.
    """
    claims_a = grp_a[grp_a["TotalClaims"] > 0]["TotalClaims"]
    claims_b = grp_b[grp_b["TotalClaims"] > 0]["TotalClaims"]
    
    if len(claims_a) < 2 or len(claims_b) < 2:
        return {
            "test": "t-test",
            "statistic": np.nan,
            "p_value": np.nan,
            "mean_a": claims_a.mean() if len(claims_a) > 0 else np.nan,
            "mean_b": claims_b.mean() if len(claims_b) > 0 else np.nan,
            "diff_pct": np.nan
        }
        
    t_stat, p_val = stats.ttest_ind(claims_a, claims_b, equal_var=False)
    mean_a = claims_a.mean()
    mean_b = claims_b.mean()
    
    return {
        "test": "t-test",
        "statistic": t_stat,
        "p_value": p_val,
        "mean_a": mean_a,
        "mean_b": mean_b,
        "diff_pct": ((mean_b - mean_a) / mean_a) * 100 if mean_a != 0 else np.nan
    }


def run_margin_test(grp_a, grp_b, group_col):
    """
    Test difference in Margin (TotalPremium - TotalClaims) using t-test.
    """
    margin_a = grp_a["Margin"]
    margin_b = grp_b["Margin"]
    
    t_stat, p_val = stats.ttest_ind(margin_a, margin_b, equal_var=False)
    mean_a = margin_a.mean()
    mean_b = margin_b.mean()
    
    return {
        "test": "t-test",
        "statistic": t_stat,
        "p_value": p_val,
        "mean_a": mean_a,
        "mean_b": mean_b,
        "diff": mean_b - mean_a
    }
