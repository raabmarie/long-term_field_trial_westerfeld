import os
import pandas as pd
from common import validate

db_file_path = "Westerfeld_DB_V_1_18.xlsx"
rd_file_path = "Fungi_2015-2021.xlsx"
miss_id_file_path = "Missing_identifiers_Fungi.xlsx"
diff_file_path = "Differences_Fungi.xlsx"

if os.path.exists(diff_file_path):
    os.remove(diff_file_path)

if os.path.exists(miss_id_file_path):
    os.remove(miss_id_file_path)

# Load transformed / normalized data into data frames
sheets = pd.read_excel(
    db_file_path,
    sheet_name=[
        "V1_0_FUNGI",
        "V1_0_BIOPROJECT",
        "V1_0_HABITAT",
        "V1_0_BENEFICIAL",
        "V1_0_KINGDOM",
        "V1_0_PHYLUM",
        "V1_0_CLASS",
        "V1_0_FAMILY",
        "V1_0_ORDER",
        "V1_0_GENUS",
        "V1_0_SPECIES",
        "V1_0_REMARK",
    ],
)
df_fungi = sheets["V1_0_FUNGI"]
df_bio_project = sheets["V1_0_BIOPROJECT"]
df_habitat = sheets["V1_0_HABITAT"]
df_beneficial = sheets["V1_0_BENEFICIAL"]
df_kingdom = sheets["V1_0_KINGDOM"]
df_phylum = sheets["V1_0_PHYLUM"]
df_class = sheets["V1_0_CLASS"]
df_family = sheets["V1_0_FAMILY"]
df_order = sheets["V1_0_ORDER"]
df_genus = sheets["V1_0_GENUS"]
df_species = sheets["V1_0_SPECIES"]

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name="RawData")

# Rename columns
df_beneficial.rename(columns={"Name_EN": "Beneficial"}, inplace=True)
df_habitat.rename(columns={"Name_EN": "Habitat"}, inplace=True)
df_bio_project.rename(columns={"Name": "BioProject"}, inplace=True)
df_kingdom.rename(columns={"Name": "Kingdom"}, inplace=True)
df_phylum.rename(columns={"Name": "Phylum"}, inplace=True)
df_class.rename(columns={"Name": "Class"}, inplace=True)
df_family.rename(columns={"Name": "Family"}, inplace=True)
df_order.rename(columns={"Name": "Order"}, inplace=True)
df_genus.rename(columns={"Name": "Genus"}, inplace=True)
df_species.rename(columns={"Name": "Species"}, inplace=True)
df_fungi.rename(
    columns={"Experimental_Year": "Year", "Plot_ID": "Parcel_ID"}, inplace=True
)
df_raw.rename(columns={"BioProject_ID": "BioProject"}, inplace=True)

# Merge the individual data frames
df_fungi = pd.merge(
    df_fungi,
    df_bio_project[["BioProject_ID", "BioProject"]],
    on="BioProject_ID",
    how="left",
)
df_fungi = pd.merge(
    df_fungi, df_habitat[["Habitat_ID", "Habitat"]], on="Habitat_ID", how="left"
)
df_fungi = pd.merge(
    df_fungi,
    df_beneficial[["Beneficial_ID", "Beneficial"]],
    on="Beneficial_ID",
    how="left",
)
df_fungi = pd.merge(
    df_fungi, df_kingdom[["Kingdom_ID", "Kingdom"]], on="Kingdom_ID", how="left"
)
df_fungi = pd.merge(
    df_fungi, df_phylum[["Phylum_ID", "Phylum"]], on="Phylum_ID", how="left"
)
df_fungi = pd.merge(
    df_fungi, df_class[["Class_ID", "Class"]], on="Class_ID", how="left"
)
df_fungi = pd.merge(
    df_fungi, df_family[["Family_ID", "Family"]], on="Family_ID", how="left"
)
df_fungi = pd.merge(
    df_fungi, df_order[["Order_ID", "Order"]], on="Order_ID", how="left"
)
df_fungi = pd.merge(
    df_fungi, df_genus[["Genus_ID", "Genus"]], on="Genus_ID", how="left"
)
df_fungi = pd.merge(
    df_fungi, df_species[["Species_ID", "Species"]], on="Species_ID", how="left"
)


# Remove columns
df_fungi.drop(
    columns=[
        "Fungi_ID",
        "BioProject_ID",
        "Habitat_ID",
        "Beneficial_ID",
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

df_raw.drop(columns=["Parcel", "Crop", "Sample_Name", "Internal_ID"], inplace=True)

# Create new unique identifier
df_raw["Identifier"] = (
    df_raw["Year"].astype(str)
    + df_raw["Parcel_ID"].astype(str)
    + df_raw["Habitat"].astype(str)
    + df_raw["Beneficial"].astype(str)
    + df_raw["Seq_ID"].astype(str)
    + df_raw["SH_Code"].astype(str)
)
df_fungi["Identifier"] = (
    df_fungi["Year"].astype(str)
    + df_fungi["Parcel_ID"].astype(str)
    + df_fungi["Habitat"].astype(str)
    + df_fungi["Beneficial"].astype(str)
    + df_fungi["Seq_ID"].astype(str)
    + df_fungi["SH_Code"].astype(str)
)

# Fix timestamps
df_fungi["Date"] = pd.to_datetime(df_fungi["Date"], dayfirst=True, format="mixed")
df_raw["Date"] = pd.to_datetime(df_raw["Date"], dayfirst=True, format="mixed")

# Sort by rows and columns
df_fungi = df_fungi.sort_values(
    by=["Identifier", "Date"], ascending=[True, False]
).reset_index(drop=True)
df_fungi = df_fungi[sorted(df_fungi.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(
    by=["Identifier", "Date"], ascending=[True, False]
).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# Finally, check for equality
validate(df_fungi, df_raw, miss_id_file_path, diff_file_path)
