import pandas as pd
from common import prep_table_experiment
from common import prep_table_taxonomy

# Load data from CSV file
df_beneficial = pd.read_csv("lte_westerfeld.V1_0_BENEFICIAL.csv")
df_bioproject = pd.read_csv("lte_westerfeld.V1_0_BIOPROJECT.csv")
df_habitat = pd.read_csv("lte_westerfeld.V1_0_HABITAT.csv")

# Data types are requested for these columns to import table BACTERIA
dtype_dict = {"Seq_ID": "str", "ACC_Num": "str", "OTU_ID": "str"}

df_bacteria = pd.read_csv("lte_westerfeld.V1_0_BACTERIA.csv", dtype=dtype_dict)

# Add BENEFICIAL
df_bacteria = pd.merge(
    df_bacteria,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on="Beneficial_ID",
    how="left",
)

# Rename column "Name_EN" in "Beneficial"
df_bacteria = df_bacteria.rename(columns={"Name_EN": "Beneficial"})

# Add HABITAT
df_bacteria = pd.merge(
    df_bacteria, df_habitat[["Habitat_ID", "Name_EN"]], on="Habitat_ID", how="left"
)

# Rename column "Name_EN" in "Habitat"
df_bacteria = df_bacteria.rename(columns={"Name_EN": "Habitat"})

# Add BIOPROJECT
df_bacteria = pd.merge(
    df_bacteria,
    df_bioproject[["BioProject_ID", "Name"]],
    on="BioProject_ID",
    how="left",
)

# Rename column "Name_EN" in "Habitat"
df_bacteria = df_bacteria.rename(columns={"Name": "BioProject"})

# Drop merged columns
df_bacteria = df_bacteria.drop(columns=["Beneficial_ID", "Habitat_ID", "BioProject_ID"])

# Add the experiment information to the data frame (Crop, Tillage, Fertilization)
df_bacteria = prep_table_experiment(df_bacteria)

# Add taxonomy to the data frame
df_bacteria = prep_table_taxonomy(df_bacteria)

print(df_bacteria.columns)
