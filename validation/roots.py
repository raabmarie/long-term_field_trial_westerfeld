import os
import pandas as pd
from common import validate

db_file_path = "Westerfeld_DB_V_1_10.xlsx"
rd_file_path = "250324_Wurzeln_2019-2020.xlsx"
miss_id_file_path = "Missing_identifiers_roots.xlsx"
diff_file_path = "Differences_roots.xlsx"

if os.path.exists(diff_file_path):
    os.remove(diff_file_path)

if os.path.exists(miss_id_file_path):
    os.remove(miss_id_file_path)

# Load transformed / normalized data into data frames
sheets = pd.read_excel(
    db_file_path,
    sheet_name=[
        "V1_0_WURZELN",
        "V1_0_BENEFICIALS",
    ],
)
df_roots = sheets["V1_0_WURZELN"]
df_beneficials = sheets["V1_0_BENEFICIALS"]

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name="RawData")

# Merge the individual data frames
df_roots = pd.merge(
    df_roots,
    df_beneficials[["Beneficials_ID", "Beneficials"]],
    on="Beneficials_ID",
    how="left",
)

# Remove and rename columns
df_roots.drop(columns=["Wurzeln_ID", "Beneficials_ID"], inplace=True)
df_roots.rename(
    columns={
        "Versuchsjahr": "Year",
        "Termin": "Date",
        "Parzelle_ID": "Parcel_ID",
        "Wurzellaenge": "total_root_length",
        "Trockengewicht": "root_dry_weight",
        "Indol_3_Essigsaeure": "Indol-3-essigsaeure",
        "Proline": "Prolin",
        "Polyphenole": "Phenol",
        "Glycin_Betain": "Glycin-Betain",
    },
    inplace=True,
)

df_raw.drop(
    columns=["Parcel", "Crop", "Habitat", "Sample_Name", "Bemerkung "], inplace=True
)

# Fix timestamps
df_roots["Date"] = pd.to_datetime(df_roots["Date"], dayfirst=True, format="mixed")
df_raw["Date"] = pd.to_datetime(df_raw["Date"], dayfirst=True, format="mixed")

# Create new unique identifier
df_raw["Identifier"] = (
    df_raw["Year"].astype(str)
    + df_raw["Date"].astype(str)
    + df_raw["Parcel_ID"].astype(str)
    + df_raw["Beneficials"].astype(str)
)
df_roots["Identifier"] = (
    df_roots["Year"].astype(str)
    + df_roots["Date"].astype(str)
    + df_roots["Parcel_ID"].astype(str)
    + df_roots["Beneficials"].astype(str)
)

# Sort by rows and columns
df_roots = df_roots.sort_values(by="Identifier", ascending=True).reset_index(drop=True)
df_roots = df_roots[sorted(df_roots.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(by="Identifier", ascending=True).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# Finally, check for equality
validate(df_roots, df_raw, miss_id_file_path, diff_file_path)
