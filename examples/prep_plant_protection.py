import pandas as pd
from prep_functions import prep_table_experiment

# Load data from CSV file
df_plant_protection_product_type = pd.read_csv(
    "lte_westerfeld.V1_0_PLANT_PROTECTION_PRODUCT_TYPE.csv"
)
df_plant_protection_product = pd.read_csv(
    "lte_westerfeld.V1_0_PLANT_PROTECTION_PRODUCT.csv"
)
df_plant_protection = pd.read_csv("lte_westerfeld.V1_0_PLANT_PROTECTION.csv")

# Rename column 'Name_EN' in 'Plant_Protection_Product'
df_plant_protection_product = df_plant_protection_product.rename(
    columns={"Name_EN": "Plant_Protection_Product"}
)

# Add PLANT_PROTECTION_PRODUCT_TYPE
df_plant_protection_product = pd.merge(
    df_plant_protection_product,
    df_plant_protection_product_type[["Plant_Protection_Product_Type_ID", "Name_EN"]],
    on=["Plant_Protection_Product_Type_ID"],
    how="left",
)

# Rename column 'Name_EN' in 'Plant_Protection_Product_Type'
df_plant_protection_product = df_plant_protection_product.rename(
    columns={"Name_EN": "Plant_Protection_Product_Type"}
)

# Add PLANT_PROTECTION_PRODUCT
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

# Drop foreign keys that are no longer needed
df_plant_protection = df_plant_protection.drop(columns=["Plant_Protection_Product_ID"])

# Add the experiment information to the data frame (Crop, Tillage, Fertilization)
df_plant_protection = prep_table_experiment(df_plant_protection)

print(df_plant_protection.columns)