import pandas as pd
from common import prepare_table_experiment

# Load data from CSV file
df_root = pd.read_csv("lte_westerfeld.V1_0_ROOT.csv")
df_beneficial = pd.read_csv("lte_westerfeld.V1_0_BENEFICIAL.csv")

# Add BENEFICIAL
df_root = pd.merge(
    df_root, df_beneficial[["Beneficial_ID", "Name_EN"]], on="Beneficial_ID", how="left"
)

# Rename column 'Name_EN' and drop foreign keys that are no longer needed
df_root = df_root.rename(columns={"Name_EN": "Beneficial"})
df_root = df_root.drop(columns=["Beneficial_ID"])

# Add the experiment information to the data frame (Crop, Tillage, Fertilization)
df_root = prepare_table_experiment(df_root)

print(df_root.columns)
