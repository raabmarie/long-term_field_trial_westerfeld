import pandas as pd
from prep_functions import prep_table_experiment

# Load data from CSV file
df_plant_lab = pd.read_csv("lte_westerfeld.V1_0_PLANT_LAB.csv")
df_plant_sampling = pd.read_csv("lte_westerfeld.V1_0_PLANT_SAMPLING.csv")
df_beneficial = pd.read_csv("lte_westerfeld.V1_0_BENEFICIAL.csv")

# Add PLANT_SAMPLING
df_plant_lab = pd.merge(
    df_plant_lab, df_plant_sampling, on=["Plant_Sampling_ID"], how="left"
)

# Add BENEFICIAL
df_plant_lab = pd.merge(
    df_plant_lab,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on=["Beneficial_ID"],
    how="left",
)

# Rename column 'Name_EN' and drop foreign keys that are no longer needed
df_plant_lab = df_plant_lab.rename(columns={"Name_EN": "Beneficial"})
df_plant_lab = df_plant_lab.drop(columns=["Beneficial_ID", "Plant_Sampling_ID"])


# Add the experiment information to the data frame (Crop, Tillage, Fertilization)
df_plant_lab = prep_table_experiment(df_plant_lab)

print(df_plant_lab.columns)
