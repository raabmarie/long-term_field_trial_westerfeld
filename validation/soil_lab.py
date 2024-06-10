import os
import pandas as pd
from common import validate

db_file_path = "Westerfeld_DB_V_1_10.xlsx"
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
        "V1_0_BODENLABORWERTE",
        "V1_0_PROBENAHME_BODEN",
        "V1_0_BENEFICIALS",
    ],
)
df_soil_lab = sheets["V1_0_BODENLABORWERTE"]
df_soil_sample = sheets["V1_0_PROBENAHME_BODEN"]
df_beneficials = sheets["V1_0_BENEFICIALS"]

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name="RawData")

# Merge the individual data frames
df_soil_lab = pd.merge(
    df_soil_lab,
    df_soil_sample[
        [
            "Probenahme_Boden_ID",
            "Versuchsjahr",
            "Termin",
            "Parzelle_ID",
            "Beneficials_ID",
            "Obergrenze",
            "Untergrenze",
        ]
    ],
    on="Probenahme_Boden_ID",
    how="left",
)
df_soil_lab = pd.merge(
    df_soil_lab,
    df_beneficials[["Beneficials_ID", "Beneficials"]],
    on="Beneficials_ID",
    how="left",
)

# Remove and rename columns
df_soil_lab.drop(
    columns=["Bodenlaborwerte_ID", "Probenahme_Boden_ID", "Beneficials_ID"],
    inplace=True,
)
df_soil_lab.rename(
    columns={
        "Versuchsjahr": "Year",
        "Termin": "Date",
        "Parzelle_ID": "Parcel_ID",
        "Obergrenze": "Upper_Limit",
        "Untergrenze": "Lower_Limit",
        "NFK": "UFC",
    },
    inplace=True,
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
    + df_raw["Beneficials"].astype(str)
    + df_raw["Lower_Limit"].astype(str)
)
df_soil_lab["Identifier"] = (
    df_soil_lab["Year"].astype(str)
    + df_soil_lab["Date"].astype(str)
    + df_soil_lab["Parcel_ID"].astype(str)
    + df_soil_lab["Beneficials"].astype(str)
    + df_soil_lab["Lower_Limit"].astype(str)
)

# TODO: Remove the following two lines after further pre-processing
df_soil_lab = df_soil_lab.round(3)
df_raw = df_raw.round(3)

# Sort by rows and columns
df_soil_lab = df_soil_lab.sort_values(by="Identifier", ascending=True).reset_index(
    drop=True
)
df_soil_lab = df_soil_lab[sorted(df_soil_lab.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(by="Identifier", ascending=True).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# Finally, check for equality
validate(df_soil_lab, df_raw, miss_id_file_path, diff_file_path)
