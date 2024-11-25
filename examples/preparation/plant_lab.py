import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_plant_lab = pd.read_csv("../../lte_westerfeld.V1_0_PLANT_LAB.csv")
df_plant_sampling = pd.read_csv("../../lte_westerfeld.V1_0_PLANT_SAMPLING.csv")
df_beneficial = pd.read_csv("../../lte_westerfeld.V1_0_BENEFICIAL.csv")

# Add PLANT_SAMPLING information
df_plant_lab = pd.merge(
    df_plant_lab, df_plant_sampling, on=["Plant_Sampling_ID"], how="left"
)

# Add BENEFICIAL information
df_plant_lab = pd.merge(
    df_plant_lab,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on=["Beneficial_ID"],
    how="left",
)
df_plant_lab = df_plant_lab.rename(columns={"Name_EN": "Beneficial"})

# Drop merged identifier columns
df_plant_lab = df_plant_lab.drop(columns=["Beneficial_ID", "Plant_Sampling_ID"])

# Add experiment information
df_plant_lab = prepare_table_experiment(df_plant_lab)

# Export data to excel
df_plant_lab.to_excel('plant_lab.xlsx', index=False)
