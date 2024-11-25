import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_plant_protection_product_type = pd.read_csv(
    "../../lte_westerfeld.V1_0_PLANT_PROTECTION_PRODUCT_TYPE.csv"
)
df_plant_protection_product = pd.read_csv(
    "../../lte_westerfeld.V1_0_PLANT_PROTECTION_PRODUCT.csv"
)
df_plant_protection = pd.read_csv("../../lte_westerfeld.V1_0_PLANT_PROTECTION.csv")

# Rename column 'Name_EN' to 'Plant_Protection_Product'
df_plant_protection_product = df_plant_protection_product.rename(
    columns={"Name_EN": "Plant_Protection_Product"}
)

# Add PLANT_PROTECTION_PRODUCT_TYPE information
df_plant_protection_product = pd.merge(
    df_plant_protection_product,
    df_plant_protection_product_type[["Plant_Protection_Product_Type_ID", "Name_EN"]],
    on=["Plant_Protection_Product_Type_ID"],
    how="left",
)
df_plant_protection_product = df_plant_protection_product.rename(
    columns={"Name_EN": "Plant_Protection_Product_Type"}
)

# Add PLANT_PROTECTION_PRODUCT information
df_plant_protection = pd.merge(
    df_plant_protection,
    df_plant_protection_product[
        [
            "Plant_Protection_Product_ID",
            "Plant_Protection_Product",
            "Plant_Protection_Product_Type",
        ]
    ],
    on=["Plant_Protection_Product_ID"],
    how="left",
)

# Drop merged identifier columns
df_plant_protection = df_plant_protection.drop(columns=["Plant_Protection_Product_ID"])

# Add experiment information
df_plant_protection = prepare_table_experiment(df_plant_protection)

# Export data to excel
df_plant_protection.to_excel('plant_protection.xlsx', index=False)
