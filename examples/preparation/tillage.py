import pandas as pd
from common import prep_table_experiment

# Load data from CSV file
df_tillage = pd.read_csv("lte_westerfeld.V1_0_TILLAGE.csv")
df_tillage_measure = pd.read_csv("lte_westerfeld.V1_0_TILLAGE_MEASURE.csv")

# Add TILLAGE_MEASURE
df_tillage = pd.merge(
    df_tillage,
    df_tillage_measure[["Tillage_Measure_ID", "Name_EN"]],
    on="Tillage_Measure_ID",
    how="left",
)

# Rename column 'Name_EN' and drop foreign keys that are no longer needed
df_tillage = df_tillage.rename(columns={"Name_EN": "Tillage_Measure"})
df_tillage = df_tillage.drop(columns=["Tillage_Measure_ID"])

# Add the experiment information to the data frame (Crop, Tillage, Fertilization)
df_tillage = prep_table_experiment(df_tillage)

print(df_tillage.columns)
