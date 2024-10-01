import pandas as pd
from common import prep_table_experiment

# Load data from CSV file
df_fertilizer = pd.read_csv("lte_westerfeld.V1_0_FERTILIZER.csv")
df_fertilization = pd.read_csv("lte_westerfeld.V1_0_FERTILIZATION.csv")

# Add FERTILIZER
df_fertilization = pd.merge(
    df_fertilization,
    df_fertilizer[["Fertilizer_ID", "Name_EN"]],
    on=["Fertilizer_ID"],
    how="left",
)

# Rename column 'Name_EN' and drop foreign keys that are no longer needed
df_fertilization = df_fertilization.rename(columns={"Name_EN": "Fertilizer"})
df_fertilization = df_fertilization.drop(columns=["Fertilizer_ID"])

df_fertilization = prep_table_experiment(df_fertilization)

print(df_fertilization.columns)
