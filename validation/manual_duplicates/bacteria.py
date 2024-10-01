import pandas as pd


db_file_path = "Westerfeld_DB_V_1_21.xlsx"

# Load transformed / normalized data
sheets = pd.read_excel(
    db_file_path,
    sheet_name=[
        "V1_0_BACTERIA",
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
        "V1_0_EXPERIMENTAL_SETUP",
        "V1_0_CROP",
        "V1_0_TREATMENT",
        "V1_0_FACTOR_1_LEVEL",
        "V1_0_FACTOR_2_LEVEL",
    ],
)
df_bacteria = sheets["V1_0_BACTERIA"]
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
df_experimental_setup = sheets["V1_0_EXPERIMENTAL_SETUP"]
df_crop = sheets["V1_0_CROP"]
df_treatment = sheets["V1_0_TREATMENT"]
df_factor1 = sheets["V1_0_FACTOR_1_LEVEL"]
df_factor2 = sheets["V1_0_FACTOR_2_LEVEL"]

# Rename columns
df_beneficial.rename(columns={"Name_EN": "Beneficials"}, inplace=True)
df_habitat.rename(columns={"Name_EN": "Habitat"}, inplace=True)
df_bio_project.rename(columns={"Name": "BioProject"}, inplace=True)
df_kingdom.rename(columns={"Name": "Kingdom"}, inplace=True)
df_phylum.rename(columns={"Name": "Phylum"}, inplace=True)
df_class.rename(columns={"Name": "Class"}, inplace=True)
df_family.rename(columns={"Name": "Family"}, inplace=True)
df_order.rename(columns={"Name": "Order"}, inplace=True)
df_genus.rename(columns={"Name": "Genus"}, inplace=True)
df_species.rename(columns={"Name": "Species"}, inplace=True)
df_crop = df_crop.rename(columns={"Name_EN": "Crop"})
df_factor1 = df_factor1.rename(columns={"Name_EN": "Factor1"})
df_factor2 = df_factor2.rename(columns={"Name_EN": "Factor2"})

# Prepare the experimental setup
df_experimental_setup = pd.merge(
    df_experimental_setup,
    df_crop[["Crop_ID", "Crop"]],
    on="Crop_ID",
    how="left",
)
df_experimental_setup = pd.merge(
    df_experimental_setup,
    df_treatment[["Treatment_ID", "Factor_1_Level_ID", "Factor_2_Level_ID"]],
    on="Treatment_ID",
    how="left",
)
df_experimental_setup = pd.merge(
    df_experimental_setup,
    df_factor1[["Factor_1_Level_ID", "Factor1"]],
    on="Factor_1_Level_ID",
    how="left",
)
df_experimental_setup = pd.merge(
    df_experimental_setup,
    df_factor2[["Factor_2_Level_ID", "Factor2"]],
    on="Factor_2_Level_ID",
    how="left",
)
df_experimental_setup.drop(
    columns=[
        "Experimental_Setup_ID",
        "Crop_ID",
        "Plant_Variety_ID",
        "Remark_ID",
        "Treatment_ID",
        "Factor_1_Level_ID",
        "Factor_2_Level_ID",
    ],
    inplace=True,
)

# Merge the individual data frames
df_bacteria = pd.merge(
    df_bacteria,
    df_bio_project[["BioProject_ID", "BioProject"]],
    on="BioProject_ID",
    how="left",
)
df_bacteria = pd.merge(
    df_bacteria, df_habitat[["Habitat_ID", "Habitat"]], on="Habitat_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria,
    df_beneficial[["Beneficial_ID", "Beneficials"]],
    on="Beneficial_ID",
    how="left",
)
df_bacteria = pd.merge(
    df_bacteria, df_kingdom[["Kingdom_ID", "Kingdom"]], on="Kingdom_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_phylum[["Phylum_ID", "Phylum"]], on="Phylum_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_class[["Class_ID", "Class"]], on="Class_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_family[["Family_ID", "Family"]], on="Family_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_order[["Order_ID", "Order"]], on="Order_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_genus[["Genus_ID", "Genus"]], on="Genus_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria, df_species[["Species_ID", "Species"]], on="Species_ID", how="left"
)
df_bacteria = pd.merge(
    df_bacteria,
    df_experimental_setup[
        ["Experimental_Year", "Plot_ID", "Crop", "Factor1", "Factor2"]
    ],
    on=["Experimental_Year", "Plot_ID"],
    how="left",
)

# Remove identifier columns
df_bacteria.drop(
    columns=[
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

# Change order of the columns
new_column_order = [
    "Experimental_Year",
    "Date",
    "Plot_ID",
    "Crop",
    "Factor1",
    "Factor2",
    "Habitat",
    "Beneficials",
    "BioProject",
    "OTU_ID",
    "Seq_ID",
    "ACC_Num",
    "Value",
    "Kingdom",
    "Phylum",
    "Class",
    "Order",
    "Family",
    "Genus",
    "Species",
]
df_bacteria = df_bacteria[new_column_order]

# Check for duplicates
df_bacteria_duplicates = df_bacteria[df_bacteria.duplicated()]

if df_bacteria_duplicates.empty:
    print("No duplicates found.")
else:
    print("Duplicates found. See: Duplicates_Bacteria.csv")
    df_bacteria_duplicates.to_csv(
        "Duplicates_Bacteria.csv", sep=";", decimal=",", index=False
    )

# Export data as CSV
df_bacteria.to_csv("Bacteria.csv", sep=";", decimal=",", index=False)
