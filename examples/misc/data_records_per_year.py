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
df_bacteria = pd.read_csv("../../lte_westerfeld.V1_0_BACTERIA.csv", dtype=dtypes_bacteria)

# Count data records per year
year_column = "Experimental_Year"
counts_df_crop_rotation = (
    df_crop_rotation.groupby(year_column).size().reset_index(name="counts")
)
counts_df_crop_rotation['Category'] = "Experimental_data"

counts_df_experimental_setup = (
    df_experimental_setup.groupby(year_column).size().reset_index(name="counts")
)
counts_df_experimental_setup['Category'] = "Experimental_data"

counts_df_plant_protection = (
    df_plant_protection.groupby(year_column).size().reset_index(name="counts")
)
counts_df_plant_protection['Category'] = "Field_data" 

counts_df_sowing = df_sowing.groupby(year_column).size().reset_index(name="counts")
counts_df_sowing['Category'] = "Field_data" 

counts_df_tillage = df_tillage.groupby(year_column).size().reset_index(name="counts")
counts_df_tillage['Category'] = "Field_data" 

counts_df_fertilization = (
    df_fertilization.groupby(year_column).size().reset_index(name="counts")
)
counts_df_fertilization['Category'] = "Field_data" 

counts_df_harvest = df_harvest.groupby(year_column).size().reset_index(name="counts")
counts_df_harvest['Category'] = "Field_data" 

counts_df_soil_sampling = (
    df_soil_sampling.groupby(year_column).size().reset_index(name="counts")
)
counts_df_soil_sampling['Category'] = "Soil_data" 

counts_df_plant_sampling = (
    df_plant_sampling.groupby(year_column).size().reset_index(name="counts")
)
counts_df_plant_sampling['Category'] = "Plant_data" 

counts_df_root = df_root.groupby(year_column).size().reset_index(name="counts")
counts_df_root['Category'] = "Plant_data" 

counts_df_gene_expression = (
    df_gene_expression.groupby(year_column).size().reset_index(name="counts")
)
counts_df_gene_expression['Category'] = "Plant_data" 

counts_df_fungi = df_fungi.groupby(year_column).size().reset_index(name="counts")
counts_df_fungi['Category'] = "Microbe_communities" 

counts_df_bacteria = df_bacteria.groupby(year_column).size().reset_index(name="counts")
counts_df_bacteria['Category'] = "Microbe_communities" 

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

# Sum all data records year
df = df.groupby(["Category", "Experimental_Year"])["counts"].sum().reset_index()

# pivot data records 
df_pivot = df.pivot_table(index="Experimental_Year", columns="Category", values="counts", fill_value=0)

# colours from Figure 1 
category_colors = {"Experimental_data": "#FFFF99", 
                   "Field_data": "#D8BFD8",
                   "Soil_data": "#FF9999",
                   "Plant_data": "#ADD8E6",
                   "Microbe_communities": "#C8E6C9"}

category_order = ["Microbe_communities", "Plant_data", "Soil_data", "Field_data", "Experimental_data"]
#category_order = ["Experimental_data", "Field_data", "Soil_data", "Plant_data", "Microbe_communities"]

# Create plot
plt.rcParams.update({"text.usetex": True})
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_axisbelow(True)
plt.grid(which="both", linestyle="dotted")
plt.yscale("log", base=10)
plt.xticks(df["Experimental_Year"])
plt.xlabel("Experimental year")
plt.ylabel(r"\#Data records ($\log_{10}$)")

# stacked barchart
bars = []
for category in category_order:
    bars.append(
        ax.bar(df_pivot.index, 
               df_pivot[category], 
               label=category, 
               color=category_colors[category],
               bottom=df_pivot[category_order[:category_order.index(category)]].sum(axis=1))
    )

for year in df_pivot.index:
    total = df_pivot.loc[year].sum()
    plt.text(
        year,
        total,
        format(int(total), ","),
        va="bottom",
        ha="center",
        fontsize=10,
        color="black",
        )

plt.tight_layout()
plt.savefig("stacked_data_records_per_year.jpg")
plt.show()
print('done')
