import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_root = pd.read_csv("../../lte_westerfeld.V1_0_ROOT.csv")
df_beneficial = pd.read_csv("../../lte_westerfeld.V1_0_BENEFICIAL.csv")

# Add BENEFICIAL information
df_root = pd.merge(
    df_root, df_beneficial[["Beneficial_ID", "Name_EN"]], on="Beneficial_ID", how="left"
)
df_root = df_root.rename(columns={"Name_EN": "Beneficial"})

# Drop merged identifier columns
df_root = df_root.drop(columns=["Beneficial_ID"])

# Add experiment information
df_root = prepare_table_experiment(df_root)

print(df_root.columns)
