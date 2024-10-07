import os
import pandas as pd
from common import validate

db_file_path = "Westerfeld_DB_V_1_18.xlsx"
rd_file_path = "Gene_Expression_2019-2020.xlsx"
miss_id_file_path = "Missing_identifiers_GenExp.xlsx"
diff_file_path = "Differences_GenExp.xlsx"

if os.path.exists(miss_id_file_path):
    os.remove(miss_id_file_path)

if os.path.exists(diff_file_path):
    os.remove(diff_file_path)

# Load transformed / normalized data into data frames
sheets = pd.read_excel(
    db_file_path,
    sheet_name=[
        "V1_0_GENE_EXPRESSION",
        "V1_0_GENE_EXPRESSION_CATEGORY",
        "V1_0_BENEFICIAL",
    ],
)
df_gene_exp = sheets["V1_0_GENE_EXPRESSION"]
df_gene_exp_cat = sheets["V1_0_GENE_EXPRESSION_CATEGORY"]
df_beneficial = sheets["V1_0_BENEFICIAL"]

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name="RawData")

# Rename columns
df_beneficial.rename(columns={"Name_EN": "Beneficial"}, inplace=True)
df_gene_exp_cat.rename(columns={"Name_EN": "Category"}, inplace=True)
df_gene_exp.rename(
    columns={"Plot_ID": "Parcel_ID", "Experimental_Year": "Year"}, inplace=True
)

# Merge the individual data frames
df_gene_exp = pd.merge(
    df_gene_exp,
    df_gene_exp_cat[["Gene_Expression_Category_ID", "Category"]],
    on="Gene_Expression_Category_ID",
    how="left",
)

df_gene_exp = pd.merge(
    df_gene_exp,
    df_beneficial[["Beneficial_ID", "Beneficial"]],
    on="Beneficial_ID",
    how="left",
)

# Remove columns
df_gene_exp.drop(
    columns=["Gene_Expression_ID", "Beneficial_ID", "Gene_Expression_Category_ID"],
    inplace=True,
)

df_raw.drop(columns=["Parcel_2", "Crop", "Habitat", "Sample_Name"], inplace=True)

# Fix timestamps
df_gene_exp["Date"] = pd.to_datetime(df_gene_exp["Date"], dayfirst=True, format="mixed")
df_raw["Date"] = pd.to_datetime(df_raw["Date"], dayfirst=True, format="mixed")

# Create new unique identifier
df_raw["Identifier"] = (
    df_raw["Year"].astype(str)
    + df_raw["Date"].astype(str)
    + df_raw["Parcel_ID"].astype(str)
    + df_raw["Beneficial"].astype(str)
)
df_gene_exp["Identifier"] = (
    df_gene_exp["Year"].astype(str)
    + df_gene_exp["Date"].astype(str)
    + df_gene_exp["Parcel_ID"].astype(str)
    + df_gene_exp["Beneficial"].astype(str)
)

# Sort by rows and columns
df_gene_exp = df_gene_exp.sort_values(by="Identifier", ascending=True).reset_index(
    drop=True
)
df_gene_exp = df_gene_exp[sorted(df_gene_exp.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(by="Identifier", ascending=True).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# Finally, check for equality
validate(df_gene_exp, df_raw, miss_id_file_path, diff_file_path)
