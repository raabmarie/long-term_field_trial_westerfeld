import os
import pandas as pd
from common import validate

db_file_path = "Westerfeld_DB_V_1_18.xlsx"
rd_file_path = "Plant_Lab_Results_2019-2021.xlsx"
miss_id_file_path = "Missing_identifiers_PlantLab.xlsx"
diff_file_path = "Differences_PlantLab.xlsx"

if os.path.exists(diff_file_path):
    os.remove(diff_file_path)

if os.path.exists(miss_id_file_path):
    os.remove(miss_id_file_path)

# Load transformed / normalized data into data frames
sheets = pd.read_excel(
    db_file_path,
    sheet_name=[
        "V1_0_PLANT_LAB",
        "V1_0_PLANT_SAMPLING",
        "V1_0_BENEFICIAL",
    ],
)
df_plant_lab = sheets["V1_0_PLANT_LAB"]
df_plant_sample = sheets["V1_0_PLANT_SAMPLING"]
df_beneficial = sheets["V1_0_BENEFICIAL"]

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name="RawData")

# Rename columns
df_beneficial.rename(columns={"Name_EN": "Beneficials"}, inplace=True)
df_plant_sample.rename(
    columns={"Experimental_Year": "Year", "Plot_ID": "Parcel_ID"}, inplace=True
)

# Merge the individual data frames
df_plant_lab = pd.merge(
    df_plant_lab,
    df_plant_sample[
        ["Plant_Sampling_ID", "Year", "Date", "Parcel_ID", "Beneficial_ID"]
    ],
    on="Plant_Sampling_ID",
    how="left",
)
df_plant_lab = pd.merge(
    df_plant_lab,
    df_beneficial[["Beneficial_ID", "Beneficials"]],
    on="Beneficial_ID",
    how="left",
)

# Remove columns
df_plant_lab.drop(
    columns=["Plant_Lab_ID", "Plant_Sampling_ID", "Beneficial_ID"], inplace=True
)

df_raw.drop(
    columns=["Parcel", "Crop", "Sample_Name", "Habitat", "Remark"], inplace=True
)

# Fix timestamps
df_plant_lab["Date"] = pd.to_datetime(
    df_plant_lab["Date"], dayfirst=True, format="mixed"
)
df_raw["Date"] = pd.to_datetime(df_raw["Date"], dayfirst=True, format="mixed")

# Create new unique identifier
df_raw["Identifier"] = (
    df_raw["Year"].astype(str)
    + df_raw["Date"].astype(str)
    + df_raw["Parcel_ID"].astype(str)
    + df_raw["Beneficials"].astype(str)
)
df_plant_lab["Identifier"] = (
    df_plant_lab["Year"].astype(str)
    + df_plant_lab["Date"].astype(str)
    + df_plant_lab["Parcel_ID"].astype(str)
    + df_plant_lab["Beneficials"].astype(str)
)

# Round all digits
df_plant_lab = df_plant_lab.round(10)
df_raw = df_raw.round(10)

# Sort by rows and columns
df_plant_lab = df_plant_lab.sort_values(by="Identifier", ascending=True).reset_index(
    drop=True
)
df_plant_lab = df_plant_lab[sorted(df_plant_lab.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(by="Identifier", ascending=True).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# Finally, check for equality
validate(df_plant_lab, df_raw, miss_id_file_path, diff_file_path)
