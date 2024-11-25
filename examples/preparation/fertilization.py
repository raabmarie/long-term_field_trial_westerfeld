import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_fertilizer = pd.read_csv("../../lte_westerfeld.V1_0_FERTILIZER.csv")
df_fertilization = pd.read_csv("../../lte_westerfeld.V1_0_FERTILIZATION.csv")

# Add FERTILIZER information
df_fertilization = pd.merge(
    df_fertilization,
    df_fertilizer[["Fertilizer_ID", "Name_EN"]],
    on=["Fertilizer_ID"],
    how="left",
)
df_fertilization = df_fertilization.rename(columns={"Name_EN": "Fertilizer"})

# Drop merged identifier columns
df_fertilization = df_fertilization.drop(columns=["Fertilizer_ID"])

# Add experiment information
df_fertilization = prepare_table_experiment(df_fertilization)

# Export data to excel
df_fertilization.to_excel('fertilization.xlsx', index=False)
