import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_tillage = pd.read_csv("../../lte_westerfeld.V1_0_TILLAGE.csv")
df_tillage_measure = pd.read_csv("../../lte_westerfeld.V1_0_TILLAGE_MEASURE.csv")

# Add TILLAGE_MEASURE information
df_tillage = pd.merge(
    df_tillage,
    df_tillage_measure[["Tillage_Measure_ID", "Name_EN"]],
    on="Tillage_Measure_ID",
    how="left",
)
df_tillage = df_tillage.rename(columns={"Name_EN": "Tillage_Measure"})

# Drop merged identifier information
df_tillage = df_tillage.drop(columns=["Tillage_Measure_ID"])

# Add experiment information
df_tillage = prepare_table_experiment(df_tillage)

print(list(df_tillage.columns))
