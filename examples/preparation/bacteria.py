import pandas as pd
from common import prepare_table_experiment
from common import prepare_table_taxonomy

# Load CSV files
df_beneficial = pd.read_csv(f"../../lte_westerfeld.V1_0_BENEFICIAL.csv")
df_bioproject = pd.read_csv(f"../../lte_westerfeld.V1_0_BIOPROJECT.csv")
df_habitat = pd.read_csv(f"../../lte_westerfeld.V1_0_HABITAT.csv")
dtype_dict = {"Seq_ID": "str", "ACC_Num": "str", "OTU_ID": "str"}
df_bacteria = pd.read_csv(f"../../lte_westerfeld.V1_0_BACTERIA.csv", dtype=dtype_dict)

# Add BENEFICIAL information
df_bacteria = pd.merge(
    df_bacteria,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on="Beneficial_ID",
    how="left",
)
df_bacteria = df_bacteria.rename(columns={"Name_EN": "Beneficial"})

# Add HABITAT information
df_bacteria = pd.merge(
    df_bacteria, df_habitat[["Habitat_ID", "Name_EN"]], on="Habitat_ID", how="left"
)
df_bacteria = df_bacteria.rename(columns={"Name_EN": "Habitat"})

# Add BIOPROJECT information
df_bacteria = pd.merge(
    df_bacteria,
    df_bioproject[["BioProject_ID", "Name"]],
    on="BioProject_ID",
    how="left",
)
df_bacteria = df_bacteria.rename(columns={"Name": "BioProject"})

# Drop merged identifier columns
df_bacteria = df_bacteria.drop(columns=["Beneficial_ID", "Habitat_ID", "BioProject_ID"])

# Add experiment information
df_bacteria = prepare_table_experiment(df_bacteria)

# Add taxonomy information
df_bacteria = prepare_table_taxonomy(df_bacteria)

print(list(df_bacteria.columns))
