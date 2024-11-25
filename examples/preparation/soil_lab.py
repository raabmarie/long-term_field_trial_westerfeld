import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_soil_lab = pd.read_csv("../../lte_westerfeld.V1_0_SOIL_LAB.csv")
df_soil_sampling = pd.read_csv("../../lte_westerfeld.V1_0_SOIL_SAMPLING.csv")
df_beneficial = pd.read_csv("../../lte_westerfeld.V1_0_BENEFICIAL.csv")

# Add SOIL_SAMPLING information
df_soil_lab = pd.merge(
    df_soil_lab, df_soil_sampling, on=["Soil_Sampling_ID"], how="left"
)

# Add BENEFICIAL information
df_soil_lab = pd.merge(
    df_soil_lab,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on=["Beneficial_ID"],
    how="left",
)
df_soil_lab = df_soil_lab.rename(columns={"Name_EN": "Beneficial"})

# Drop merged identifier columns
df_soil_lab = df_soil_lab.drop(columns=["Beneficial_ID", "Soil_Sampling_ID"])

# Add experiment information
df_soil_lab = prepare_table_experiment(df_soil_lab)

# Export data to excel
df_soil_lab.to_excel('soil_lab.xlsx', index=False)
