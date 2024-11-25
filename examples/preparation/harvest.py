import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_harvest = pd.read_csv("../../lte_westerfeld.V1_0_HARVEST.csv")
df_yield = pd.read_csv("../../lte_westerfeld.V1_0_YIELD.csv")

# Add YIELD information
df_harvest = pd.merge(
    df_yield,
    df_harvest[["Harvest_ID", "Experimental_Year", "Date", "Plot_ID"]],
    on=["Harvest_ID"],
    how="left",
)
  
# Drop merged identifier columns
df_harvest = df_harvest.drop(columns=["YIELD_ID"])

# Add experiment information
df_harvest = prepare_table_experiment(df_harvest)

# Export data to excel
df_harvest.to_excel('harvest.xlsx', index=False)
