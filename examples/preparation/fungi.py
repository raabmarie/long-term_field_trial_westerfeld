import pandas as pd
from common import prepare_table_experiment
from common import prepare_table_taxonomy

# Load CSV files
df_beneficial = pd.read_csv("../../lte_westerfeld.V1_0_BENEFICIAL.csv")
df_bioproject = pd.read_csv("../../lte_westerfeld.V1_0_BIOPROJECT.csv")
df_habitat = pd.read_csv("../../lte_westerfeld.V1_0_HABITAT.csv")
dtypes = {"Seq_ID": "str", "ACC_Num": "str"}
df_fungi = pd.read_csv("../../lte_westerfeld.V1_0_FUNGI.csv", dtype=dtypes)

# Add BENEFICIAL information
df_fungi = pd.merge(
    df_fungi,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on="Beneficial_ID",
    how="left",
)
df_fungi = df_fungi.rename(columns={"Name_EN": "Beneficial"})

# Add HABITAT information
df_fungi = pd.merge(
    df_fungi, df_habitat[["Habitat_ID", "Name_EN"]], on="Habitat_ID", how="left"
)
df_fungi = df_fungi.rename(columns={"Name_EN": "Habitat"})

# Add BIOPROJECT information
df_fungi = pd.merge(
    df_fungi, df_bioproject[["BioProject_ID", "Name"]], on="BioProject_ID", how="left"
)
df_fungi = df_fungi.rename(columns={"Name": "BioProject"})

# Drop merged identifier columns
df_fungi = df_fungi.drop(columns=["Beneficial_ID", "Habitat_ID", "BioProject_ID"])

# Add experiment information
df_fungi = prepare_table_experiment(df_fungi)

# Add taxonomy information
df_fungi = prepare_table_taxonomy(df_fungi)

# Export data to excel
df_fungi.to_excel("fungi.xlsx", index=False)
