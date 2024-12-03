import matplotlib.pyplot as plt
import pandas as pd

# Load CSV Files
df_crop_rotation = pd.read_csv("../../lte_westerfeld.V1_0_CROP_ROTATION.csv")
df_experimental_setup = pd.read_csv("../../lte_westerfeld.V1_0_EXPERIMENTAL_SETUP.csv")
df_plant_protection = pd.read_csv("../../lte_westerfeld.V1_0_PLANT_PROTECTION.csv")
df_sowing = pd.read_csv("../../lte_westerfeld.V1_0_SOWING.csv")
df_tillage = pd.read_csv("../../lte_westerfeld.V1_0_TILLAGE.csv")
df_fertilization = pd.read_csv("../../lte_westerfeld.V1_0_FERTILIZATION.csv")
df_harvest = pd.read_csv("../../lte_westerfeld.V1_0_HARVEST.csv")
df_soil_sampling = pd.read_csv("../../lte_westerfeld.V1_0_SOIL_SAMPLING.csv")
df_plant_sampling = pd.read_csv("../../lte_westerfeld.V1_0_PLANT_SAMPLING.csv")
df_root = pd.read_csv("../../lte_westerfeld.V1_0_ROOT.csv")
df_gene_expression = pd.read_csv("../../lte_westerfeld.V1_0_GENE_EXPRESSION.csv")
dtypes_fungi = {"Seq_ID": "str", "ACC_Num": "str"}
df_fungi = pd.read_csv("../../lte_westerfeld.V1_0_FUNGI.csv", dtype=dtypes_fungi)
dtypes_bacteria = {"Seq_ID": "str", "ACC_Num": "str", "OTU_ID": "str"}
df_bacteria = pd.read_csv(
    "../../lte_westerfeld.V1_0_BACTERIA.csv", dtype=dtypes_bacteria
)

# Count data records per year
year_column = "Experimental_Year"
counts_df_crop_rotation = (
    df_crop_rotation.groupby(year_column).size().reset_index(name="counts")
)
counts_df_experimental_setup = (
    df_experimental_setup.groupby(year_column).size().reset_index(name="counts")
)
counts_df_plant_protection = (
    df_plant_protection.groupby(year_column).size().reset_index(name="counts")
)
counts_df_sowing = df_sowing.groupby(year_column).size().reset_index(name="counts")
counts_df_tillage = df_tillage.groupby(year_column).size().reset_index(name="counts")
counts_df_fertilization = (
    df_fertilization.groupby(year_column).size().reset_index(name="counts")
)
counts_df_harvest = df_harvest.groupby(year_column).size().reset_index(name="counts")
counts_df_soil_sampling = (
    df_soil_sampling.groupby(year_column).size().reset_index(name="counts")
)
counts_df_plant_sampling = (
    df_plant_sampling.groupby(year_column).size().reset_index(name="counts")
)
counts_df_root = df_root.groupby(year_column).size().reset_index(name="counts")
counts_df_gene_expression = (
    df_gene_expression.groupby(year_column).size().reset_index(name="counts")
)
counts_df_fungi = df_fungi.groupby(year_column).size().reset_index(name="counts")
counts_df_bacteria = df_bacteria.groupby(year_column).size().reset_index(name="counts")

# Combine all data frames
dfs = [
    counts_df_crop_rotation,
    counts_df_experimental_setup,
    counts_df_plant_protection,
    counts_df_sowing,
    counts_df_tillage,
    counts_df_fertilization,
    counts_df_harvest,
    counts_df_soil_sampling,
    counts_df_plant_sampling,
    counts_df_root,
    counts_df_gene_expression,
    counts_df_fungi,
    counts_df_bacteria,
]
df = pd.concat(dfs)
print(df.columns)
print(df.head())

# Sum all data records year
df = df.groupby("Experimental_Year")["counts"].sum().reset_index()

# Create plot
plt.rcParams.update({"text.usetex": True})
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_axisbelow(True)
plt.grid(which="both", linestyle="dotted")
plt.yscale("log", base=10)
plt.xticks(df["Experimental_Year"])
plt.xlabel("Experimental year")
plt.ylabel(r"\#Data records ($\log_{10}$)")
bars = plt.bar(df["Experimental_Year"], df["counts"], color="#008080")
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        yval,
        format(int(yval), ","),
        va="bottom",
        ha="center",
        fontsize=10,
        color="black",
    )
plt.tight_layout()
plt.savefig("data_records_per_year.jpg")
plt.show()
