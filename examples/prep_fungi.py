import pandas as pd
from prep_functions import prep_table_experiment
from prep_functions import prep_table_taxonomy

# Load data from CSV file
df_beneficial = pd.read_csv("lte_westerfeld.V1_0_BENEFICIAL.csv")
df_bioproject = pd.read_csv("lte_westerfeld.V1_0_BIOPROJECT.csv")
df_habitat = pd.read_csv("lte_westerfeld.V1_0_HABITAT.csv")

# Data types are requested for both columns to import table FUNGI
dtype_dict = {"Seq_ID": "str", "ACC_Num": "str"}

df_fungi = pd.read_csv("lte_westerfeld.V1_0_FUNGI.csv", dtype=dtype_dict)

# Add BENEFICIAL
df_fungi = pd.merge(
    df_fungi,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on="Beneficial_ID",
    how="left",
)

# Rename column 'Name_EN' in 'Beneficial'
df_fungi = df_fungi.rename(columns={"Name_EN": "Beneficial"})

# Add HABITAT
df_fungi = pd.merge(
    df_fungi, df_habitat[["Habitat_ID", "Name_EN"]], on="Habitat_ID", how="left"
)

# Rename column 'Name_EN' in 'Habitat'
df_fungi = df_fungi.rename(columns={"Name_EN": "Habitat"})

# Add BIOPROJECT
df_fungi = pd.merge(
    df_fungi, df_bioproject[["BioProject_ID", "Name"]], on="BioProject_ID", how="left"
)

# Rename column 'Name_EN' in 'BioProject'
df_fungi = df_fungi.rename(columns={"Name": "BioProject"})

# Drop merged columns
df_fungi = df_fungi.drop(columns=["Beneficial_ID", "Habitat_ID", "BioProject_ID"])

# Add the experiment information to the data frame (Crop, Tillage, Fertilization)
df_fungi = prep_table_experiment(df_fungi)

# Add taxonomy to the data frame
df_fungi = prep_table_taxonomy(df_fungi)

print(df_fungi.columns)
