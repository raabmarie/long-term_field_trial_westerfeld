import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_sowing = pd.read_csv("../../lte_westerfeld.V1_0_SOWING.csv")
df_seed_stock = pd.read_csv("../../lte_westerfeld.V1_0_SEED_STOCK.csv")
df_plant_variety = pd.read_csv("../../lte_westerfeld.V1_0_PLANT_VARIETY.csv")

# Add SEED STOCK information
df_sowing = pd.merge(
    df_sowing,
    df_seed_stock[["Seed_Stock_ID", "Plant_Variety_ID"]],
    on=["Seed_Stock_ID"],
    how="left",
)

# Add PLANT VARIETY information
df_sowing = pd.merge(
    df_sowing,
    df_plant_variety[["Plant_Variety_ID", "Name"]],
    on=["Plant_Variety_ID"],
    how="left",
)
df_sowing = df_sowing.rename(columns={"Name": "Plant_Variety"})

# Drop merged identifier columns
df_sowing = df_sowing.drop(columns=["Plant_Variety_ID", "Seed_Stock_ID"])

# Add experiment information
df_sowing = prepare_table_experiment(df_sowing)

# Export data to excel
df_sowing.to_excel('sowing.xlsx', index=False)
