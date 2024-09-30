import pandas as pd
from prep_functions import prep_table_experiment

# Load data from CSV file
df_soil_lab = pd.read_csv("lte_westerfeld.V1_0_SOIL_LAB.csv")
df_soil_sampling = pd.read_csv("lte_westerfeld.V1_0_SOIL_SAMPLING.csv")
df_beneficial = pd.read_csv("lte_westerfeld.V1_0_BENEFICIAL.csv")

# Add SOIL_SAMPLING
df_soil_lab = pd.merge(
    df_soil_lab, df_soil_sampling, on=["Soil_Sampling_ID"], how="left"
)

# Add BENEFICIAL
df_soil_lab = pd.merge(
    df_soil_lab,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on=["Beneficial_ID"],
    how="left",
)

# Rename column 'Name_EN' and drop foreign keys that are not longer needed
df_soil_lab = df_soil_lab.rename(columns={"Name_EN": "Beneficial"})
df_soil_lab = df_soil_lab.drop(columns=["Beneficial_ID", "Soil_Sampling_ID"])

# Add the experiment information to the data frame (Crop, Tillage, Fertilization)
df_soil_lab = prep_table_experiment(df_soil_lab)

print(df_soil_lab.columns)
