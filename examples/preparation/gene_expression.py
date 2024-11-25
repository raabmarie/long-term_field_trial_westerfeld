import pandas as pd
from common import prepare_table_experiment

# Load CSV files
df_gene_expression = pd.read_csv("../../lte_westerfeld.V1_0_GENE_EXPRESSION.csv")
df_gene_expression_category = pd.read_csv(
    "../../lte_westerfeld.V1_0_GENE_EXPRESSION_CATEGORY.csv"
)
df_beneficial = pd.read_csv("../../lte_westerfeld.V1_0_BENEFICIAL.csv")

# Add BENEFICIAL information
df_gene_expression = pd.merge(
    df_gene_expression,
    df_beneficial[["Beneficial_ID", "Name_EN"]],
    on="Beneficial_ID",
    how="left",
)
df_gene_expression = df_gene_expression.rename(columns={"Name_EN": "Beneficial"})

# Add GENE_EXPRESSION_CATEGORY information
df_gene_expression = pd.merge(
    df_gene_expression,
    df_gene_expression_category[["Gene_Expression_Category_ID", "Name_EN"]],
    on="Gene_Expression_Category_ID",
    how="left",
)
df_gene_expression = df_gene_expression.rename(
    columns={"Name_EN": "Gene_Expression_Category"}
)

# Drop merged identifier columns
df_gene_expression = df_gene_expression.drop(
    columns=["Gene_Expression_Category_ID", "Beneficial_ID"]
)

# Add experiment information
df_gene_expression = prepare_table_experiment(df_gene_expression)

# Export data to excel
df_gene_expression.to_excel('gene_expression.xlsx', index=False)
