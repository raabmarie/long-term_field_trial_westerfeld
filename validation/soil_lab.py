import os
import pandas as pd
from common import validate

db_file_path = "Westerfeld_DB_V_1_18.xlsx"
rd_file_path = "Soil_Lab_Results_2009-2021.xlsx"
miss_id_file_path = "Missing_identifiers_SoilLab.xlsx"
diff_file_path = "Differences_SoilLab.xlsx"

if os.path.exists(diff_file_path):
    os.remove(diff_file_path)

if os.path.exists(miss_id_file_path):
    os.remove(miss_id_file_path)

# Load transformed / normalized data into data frames
sheets = pd.read_excel(
    db_file_path,
    sheet_name=[
        "V1_0_SOIL_LAB",
        "V1_0_SOIL_SAMPLING",
        "V1_0_BENEFICIAL",
    ],
)
df_soil_lab = sheets["V1_0_SOIL_LAB"]
df_soil_sample = sheets["V1_0_SOIL_SAMPLING"]
df_beneficial = sheets["V1_0_BENEFICIAL"]

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name="RawData")

# Rename columns
df_beneficial.rename(columns={"Name_EN": "Beneficial"}, inplace=True)
df_soil_sample.rename(
    columns={
        "Experimental_Year": "Year",
        "Plot_ID": "Parcel_ID",
        "Depth_max": "Lower_Limit",
        "Depth_min": "Upper_Limit",
    },
    inplace=True,
)
df_soil_lab.rename(columns={"WHC": "UFC"}, inplace=True)

# Merge the individual data frames
df_soil_lab = pd.merge(
    df_soil_lab,
    df_soil_sample[
        [
            "Soil_Sampling_ID",
            "Year",
            "Date",
            "Parcel_ID",
            "Beneficial_ID",
            "Lower_Limit",
            "Upper_Limit",
        ]
    ],
    on="Soil_Sampling_ID",
    how="left",
)

df_soil_lab = pd.merge(
    df_soil_lab,
    df_beneficial[["Beneficial_ID", "Beneficial"]],
    on="Beneficial_ID",
    how="left",
)

# Remove columns
df_soil_lab.drop(
    columns=["Soil_Lab_ID", "Soil_Sampling_ID", "Beneficial_ID"], inplace=True
)

df_raw.drop(
    columns=["Parcel", "Crop", "Sample_Name", "Habitat", "Remark"], inplace=True
)

# Fix timestamps
df_soil_lab["Date"] = pd.to_datetime(df_soil_lab["Date"], dayfirst=True, format="mixed")
df_raw["Date"] = pd.to_datetime(df_raw["Date"], dayfirst=True, format="mixed")

# Create new unique identifier
df_raw["Identifier"] = (
    df_raw["Year"].astype(str)
    + df_raw["Date"].astype(str)
    + df_raw["Parcel_ID"].astype(str)
    + df_raw["Beneficial"].astype(str)
    + df_raw["Lower_Limit"].astype(str)
)
df_soil_lab["Identifier"] = (
    df_soil_lab["Year"].astype(str)
    + df_soil_lab["Date"].astype(str)
    + df_soil_lab["Parcel_ID"].astype(str)
    + df_soil_lab["Beneficial"].astype(str)
    + df_soil_lab["Lower_Limit"].astype(str)
)

# Round all digits
df_soil_lab = df_soil_lab.round(10)
df_raw = df_raw.round(10)

# Sort by rows and columns
df_soil_lab = df_soil_lab.sort_values(by="Identifier", ascending=True).reset_index(
    drop=True
)
df_soil_lab = df_soil_lab[sorted(df_soil_lab.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(by="Identifier", ascending=True).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# Finally, check for equality
validate(df_soil_lab, df_raw, miss_id_file_path, diff_file_path)
