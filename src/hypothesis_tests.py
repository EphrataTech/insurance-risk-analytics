from scipy import stats


def chi_square_test(contingency_table):
    chi2, p, dof, expected = stats.chi2_contingency(contingency_table)
    return {"chi2": chi2, "p_value": p, "dof": dof}


def t_test(group_a, group_b):
    t_stat, p_value = stats.ttest_ind(group_a, group_b)
    return {"t_stat": t_stat, "p_value": p_value}
