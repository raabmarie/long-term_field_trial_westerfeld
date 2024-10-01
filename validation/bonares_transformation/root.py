import os
import pandas as pd
from validation.bonares_transformation.common import validate

db_file_path = "Westerfeld_DB_V_1_18.xlsx"
rd_file_path = "Wurzeln_2019-2020.xlsx"
miss_id_file_path = "Missing_identifiers_root.xlsx"
diff_file_path = "Differences_root.xlsx"

if os.path.exists(miss_id_file_path):
    os.remove(miss_id_file_path)

if os.path.exists(diff_file_path):
    os.remove(diff_file_path)

# Load transformed / normalized data into data frames
sheets = pd.read_excel(
    db_file_path,
    sheet_name=[
        "V1_0_ROOT",
        "V1_0_BENEFICIAL",
    ],
)
df_root = sheets["V1_0_ROOT"]
df_beneficial = sheets["V1_0_BENEFICIAL"]

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name="RawData")

# Rename columns
df_beneficial.rename(columns={"Name_EN": "Beneficials"}, inplace=True)

# Merge the individual data frames
df_root = pd.merge(
    df_root,
    df_beneficial[["Beneficial_ID", "Beneficials"]],
    on="Beneficial_ID",
    how="left",
)

# Remove columns
df_root.drop(columns=["Root_ID", "Beneficial_ID"], inplace=True)

df_raw.drop(columns=["Plot", "Crop", "Habitat", "Sample_Name"], inplace=True)

# Fix timestamps
df_root["Date"] = pd.to_datetime(df_root["Date"], dayfirst=True, format="mixed")
df_raw["Date"] = pd.to_datetime(df_raw["Date"], dayfirst=True, format="mixed")

# Create new unique identifier
df_raw["Identifier"] = (
    df_raw["Experimental_Year"].astype(str)
    + df_raw["Date"].astype(str)
    + df_raw["Plot_ID"].astype(str)
    + df_raw["Beneficials"].astype(str)
)
df_root["Identifier"] = (
    df_root["Experimental_Year"].astype(str)
    + df_root["Date"].astype(str)
    + df_root["Plot_ID"].astype(str)
    + df_root["Beneficials"].astype(str)
)

# Sort by rows and columns
df_root = df_root.sort_values(by="Identifier", ascending=True).reset_index(drop=True)
df_root = df_root[sorted(df_root.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(by="Identifier", ascending=True).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# Finally, check for equality
validate(df_root, df_raw, miss_id_file_path, diff_file_path)
