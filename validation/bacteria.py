import os
import pandas as pd
from common import validate

db_file_path = "Westerfeld_DB_V_1_10.xlsx"
rd_file_path = "Bacteria_2015-2021.xlsx"
miss_id_file_path = "Missing_identifiers_Bacteria.xlsx"
diff_file_path = "Differences_Bacteria.xlsx"

if os.path.exists(diff_file_path):
    os.remove(diff_file_path)

if os.path.exists(miss_id_file_path):
    os.remove(miss_id_file_path)

# Load transformed / normalized data into data frames
sheets = pd.read_excel(
    db_file_path,
    sheet_name=[
        "V1_0_BAKTERIEN",
        "V1_0_BIOPROJECT",
        "V1_0_HABITAT",
        "V1_0_BENEFICIALS",
        "V1_0_KINGDOM",
        "V1_0_PHYLUM",
        "V1_0_CLASS",
        "V1_0_FAMILY",
        "V1_0_ORDER",
        "V1_0_GENUS",
        "V1_0_SPECIES",
    ],
)
df_bacteria = sheets["V1_0_BAKTERIEN"]
df_bio_project = sheets["V1_0_BIOPROJECT"]
df_habitat = sheets["V1_0_HABITAT"]
df_beneficials = sheets["V1_0_BENEFICIALS"]
df_kingdom = sheets["V1_0_KINGDOM"]
df_phylum = sheets["V1_0_PHYLUM"]
df_class = sheets["V1_0_CLASS"]
df_family = sheets["V1_0_FAMILY"]
df_order = sheets["V1_0_ORDER"]
df_genus = sheets["V1_0_GENUS"]
df_species = sheets["V1_0_SPECIES"]

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name="RawData")

# Merge the individual data frames
df_bacteria = pd.merge(
    df_bacteria,
    df_bio_project[["BioProject_ID", "BioProject_Name"]],
    on="BioProject_ID",
    how="left",
)
df_bacteria = pd.merge(
    df_bacteria, df_habitat[["Habitat_ID", "Habitat"]], on="Habitat_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria,
    df_beneficials[["Beneficials_ID", "Beneficials"]],
    on="Beneficials_ID",
    how="left",
)
df_bacteria = pd.merge(
    df_bacteria, df_kingdom[["Kingdom_ID", "Kingdom_Name"]], on="Kingdom_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_phylum[["Phylum_ID", "Phylum_Name"]], on="Phylum_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_class[["Class_ID", "Class_Name"]], on="Class_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_family[["Family_ID", "Family_Name"]], on="Family_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_order[["Order_ID", "Order_Name"]], on="Order_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_genus[["Genus_ID", "Genus_Name"]], on="Genus_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_species[["Species_ID", "Species_Name"]], on="Species_ID", how="left"
)

# Remove and rename columns
df_bacteria.drop(
    columns=[
        "Bakterien_ID",
        "BioProject_ID",
        "Habitat_ID",
        "Beneficials_ID",
        "Kingdom_ID",
        "Phylum_ID",
        "Class_ID",
        "Family_ID",
        "Order_ID",
        "Genus_ID",
        "Species_ID",
    ],
    inplace=True,
)
df_bacteria.rename(
    columns={
        "Versuchsjahr": "Year",
        "Termin": "Date",
        "Parzelle_ID": "Parcel_ID",
        "BioProject_Name": "BioProject_ID",
        "Kingdom_Name": "Kingdom",
        "Phylum_Name": "Phylum",
        "Class_Name": "Class",
        "Family_Name": "Family",
        "Order_Name": "Order",
        "Genus_Name": "Genus",
        "Species_Name": "Species",
    },
    inplace=True,
)

df_raw.drop(columns=["Parcel", "Crop", "Sample_Name", "Internal_ID"], inplace=True)

# Create new unique identifier
df_raw["Identifier"] = (
    df_raw["Year"].astype(str)
    + df_raw["Parcel_ID"].astype(str)
    + df_raw["Habitat"].astype(str)
    + df_raw["Beneficials"].astype(str)
    + df_raw["BioProject_ID"].astype(str)
    + df_raw["Seq_ID"].astype(str)
)
df_bacteria["Identifier"] = (
    df_bacteria["Year"].astype(str)
    + df_bacteria["Parcel_ID"].astype(str)
    + df_bacteria["Habitat"].astype(str)
    + df_bacteria["Beneficials"].astype(str)
    + df_bacteria["BioProject_ID"].astype(str)
    + df_bacteria["Seq_ID"].astype(str)
)

# Fix timestamps
df_bacteria["Date"] = pd.to_datetime(df_bacteria["Date"], dayfirst=True, format="mixed")
df_raw["Date"] = pd.to_datetime(df_raw["Date"], dayfirst=True, format="mixed")

# Sort by rows and columns
df_bacteria = df_bacteria.sort_values(
    by=["Identifier", "Date"], ascending=[True, False]
).reset_index(drop=True)
df_bacteria = df_bacteria[sorted(df_bacteria.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(
    by=["Identifier", "Date"], ascending=[True, False]
).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# Finally, check for equality
validate(df_bacteria, df_raw, miss_id_file_path, diff_file_path)
