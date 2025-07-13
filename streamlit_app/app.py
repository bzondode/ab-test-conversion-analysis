
import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

st.title("A/B Test Analysis: Product Page Conversion")

# User Inputs
n_control = st.slider("Number of users in Control group", 500, 5000, 1000, step=100)
n_variant = st.slider("Number of users in Variant group", 500, 5000, 1000, step=100)
p_control = st.slider("Conversion rate for Control group (%)", 1, 50, 12) / 100
p_variant = st.slider("Conversion rate for Variant group (%)", 1, 50, 14) / 100

# Simulate data
control_data = np.random.binomial(1, p_control, n_control)
variant_data = np.random.binomial(1, p_variant, n_variant)

data = pd.DataFrame({
    'Group': ['Control'] * n_control + ['Variant'] * n_variant,
    'Converted': np.concatenate([control_data, variant_data])
})

# Calculate summary stats
summary = data.groupby('Group')['Converted'].agg(['mean', 'count', 'std']).reset_index()
summary['sem'] = summary['std'] / np.sqrt(summary['count'])

# Perform t-test
t_stat, p_val = ttest_ind(control_data, variant_data)

# Display results
st.subheader("Conversion Summary")
st.dataframe(summary[['Group', 'mean', 'count', 'sem']].rename(columns={
    'mean': 'Conversion Rate',
    'count': 'Sample Size',
    'sem': 'Standard Error'
}))

# Plotting
fig, ax = plt.subplots()
ax.bar(summary['Group'], summary['mean'], yerr=summary['sem'], capsize=10, color=['gray', 'blue'])
ax.set_ylabel("Conversion Rate")
ax.set_title("Conversion Rate with 95% CI")
st.pyplot(fig)

# Show p-value
st.subheader("Statistical Test Result")
st.write(f"T-statistic: {t_stat:.4f}")
st.write(f"P-value: {p_val:.4f}")

if p_val < 0.05:
    st.success("The result is statistically significant. The variant may be better!")
else:
    st.warning("The result is NOT statistically significant. We cannot conclude a real difference.")
