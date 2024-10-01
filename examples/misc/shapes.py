import pandas as pd

# Hard code the mapping for retrieving the data category
mapping = {
    "CROP": "Experimental data",
    "CROP_ROTATION": "Experimental data",
    "EXPERIMENTAL_SETUP": "Experimental data",
    "FACTOR": "Experimental data",
    "FACTOR_1_LEVEL": "Experimental data",
    "FACTOR_2_LEVEL": "Experimental data",
    "PLANT_VARIETY": "Experimental data",
    "PLOT": "Experimental data",
    "REMARK": "Experimental data",
    "SEED_STOCK": "Experimental data",
    "TREATMENT": "Experimental data",
    "FERTILIZATION": "Field data",
    "FERTILIZER": "Field data",
    "HARVEST": "Field data",
    "PLANT_PROTECTION": "Field data",
    "PLANT_PROTECTION_PRODUCT": "Field data",
    "PLANT_PROTECTION_PRODUCT_TYPE": "Field data",
    "SOWING": "Field data",
    "TILLAGE": "Field data",
    "TILLAGE_MEASURE": "Field data",
    "YIELD": "Field data",
    "FUNGI": "Microbe communities",
    "BACTERIA": "Microbe communities",
    "BIOPROJECT": "Microbe communities",
    "HABITAT": "Microbe communities",
    "BENEFICIAL": "Microbe communities",
    "KINGDOM": "Microbe communities",
    "PHYLUM": "Microbe communities",
    "CLASS": "Microbe communities",
    "ORDER": "Microbe communities",
    "FAMILY": "Microbe communities",
    "GENUS": "Microbe communities",
    "SPECIES": "Microbe communities",
    "SOIL_LAB": "Soil data",
    "SOIL_SAMPLING": "Soil data",
    "GENE_EXPRESSION": "Plant data",
    "GENE_EXPRESSION_CATEGORY": "Plant data",
    "PLANT_LAB": "Plant data",
    "PLANT_SAMPLING": "Plant data",
    "ROOT": "Plant data",
}

data_table_names = list(mapping.keys())

# Collect data table information
# Finally, output LaTeX and markdown codes for typesetting a table containing this information
data = {}
categories = []
names = []
observations = []
features = []
for name in data_table_names:
    file_path = f"../../lte_westerfeld.V1_0_{name}.csv"
    df = pd.read_csv(file_path)
    category = mapping[name]
    categories.append(category)
    names.append(name)
    observations.append(df.shape[0])
    features.append(df.shape[1])
data["Data category"] = categories
data["Data table"] = names
data["#Observations"] = observations
data["#Features"] = features
df = pd.DataFrame(data)
print(df.to_latex(index=False).replace("#", "\#").replace("_", "\_"))
print(df.to_markdown(index=False))
