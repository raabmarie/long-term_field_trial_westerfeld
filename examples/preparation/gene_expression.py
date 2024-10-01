import pandas as pd
from prep_functions import prep_table_experiment

# Load data from CSV file
df_gene_expression = pd.read_csv("lte_westerfeld.V1_0_GENE_EXPRESSION.csv")
df_gene_expression_category = pd.read_csv(
    "lte_westerfeld.V1_0_GENE_EXPRESSION_CATEGORY.csv"
)
df_beneficial = pd.read_csv("lte_westerfeld.V1_0_BENEFICIAL.csv")

# Add BENEFICIAL
df_gene_expression = pd.merge(
    df_gene_expression,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on="Beneficial_ID",
    how="left",
)

# Rename column 'Name_EN' in 'Beneficial'
df_gene_expression = df_gene_expression.rename(columns={"Name_EN": "Beneficial"})


# Add GENE_EXPRESSION_CATEGORY
df_gene_expression = pd.merge(
    df_gene_expression,
    df_gene_expression_category[["Gene_Expression_Category_ID", "Name_EN"]],
    on="Gene_Expression_Category_ID",
    how="left",
)

# Rename column 'Name_EN' and drop foreign keys that are no longer needed
df_gene_expression = df_gene_expression.rename(
    columns={"Name_EN": "Gene_Expression_Category"}
)
df_gene_expression = df_gene_expression.drop(
    columns=["Gene_Expression_Category_ID", "Beneficial_ID"]
)

# Add the experiment information to the data frame (Crop, Tillage, Fertilization)
df_gene_expression = prep_table_experiment(df_gene_expression)

print(df_gene_expression.columns)
