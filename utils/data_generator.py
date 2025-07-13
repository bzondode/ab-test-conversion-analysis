
import numpy as np
import pandas as pd

def generate_ab_data(n_control=1000, n_variant=1000, p_control=0.12, p_variant=0.145, seed=42):
    np.random.seed(seed)
    control = np.random.binomial(1, p_control, n_control)
    variant = np.random.binomial(1, p_variant, n_variant)

    df = pd.DataFrame({
        'group': ['control'] * n_control + ['variant'] * n_variant,
        'converted': np.concatenate([control, variant])
    })
    return df

if __name__ == "__main__":
    df = generate_ab_data()
    df.to_csv("../data/synthetic_ab_data.csv", index=False)
    print("Synthetic A/B test data saved to ../data/synthetic_ab_data.csv")
