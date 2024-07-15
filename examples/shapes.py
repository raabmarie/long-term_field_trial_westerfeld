import os
import pandas as pd
import pickle

db_file_path = "../Westerfeld.xlsx"
pickle_file_path = "../Westerfeld.pickle"

df_dict = {}

# Speed up the data access after the first load by using a Pickle file
if os.path.exists(pickle_file_path):
    with open(pickle_file_path, "rb") as file:
        df_dict = pickle.load(file)
else:
    df_dict = pd.read_excel(db_file_path, sheet_name=None)
    with open(pickle_file_path, "wb") as file:
        pickle.dump(df_dict, file, protocol=pickle.HIGHEST_PROTOCOL)

sheet_names = df_dict.keys()
print(sheet_names)

# Hard code the mapping for retrieving the data record type
mapping = {
    "REMARK": "Experimental data",
    "CROP": "Experimental data",
    "CROP_ROTATION": "Experimental data",
    "PLANT_VARIETY": "Experimental data",
    "SEED_STOCK": "Experimental data",
    "FACTOR": "Experimental data",
    "FACTOR_1_LEVEL": "Experimental data",
    "FACTOR_2_LEVEL": "Experimental data",
    "TREATMENT": "Experimental data",
    "PLOT": "Experimental data",
    "EXPERIMENTAL_SETUP": "Experimental data",
    "PLANT_PROTECTION_PRODUCT_T": "Field data",
    "PLANT_PROTECTION_PRODUCT": "Field data",
    "PLANT_PROTECTION": "Field data",
    "SOWING": "Field data",
    "TILLAGE_MEASURE": "Field data",
    "TILLAGE": "Field data",
    "FERTILIZER": "Field data",
    "FERTILIZATION": "Field data",
    "HARVEST": "Field data",
    "YIELD": "Field data",
    "SOIL_SAMPLING": "Soil data",
    "SOIL_LAB": "Soil data",
    "PLANT_SAMPLING": "Plant data",
    "PLANT_LAB": "Plant data",
    "ROOT": "Plant data",
    "FUNGI": "Microbe communities",
    "BACTERIA": "Microbe communities",
    "BIOPROJECT": "Microbe communities",
    "HABITAT": "Microbe communities",
    "BENEFICIAL": "Microbe communities",
    "GENE_EXPRESSION_CATEGORY": "Plant data",
    "GENE_EXPRESSION": "Plant data",
    "KINGDOM": "Microbe communities",
    "PHYLUM": "Microbe communities",
    "CLASS": "Microbe communities",
    "ORDER": "Microbe communities",
    "FAMILY": "Microbe communities",
    "GENUS": "Microbe communities",
    "SPECIES": "Microbe communities",
}

# Output LaTeX and markdown codes for typesetting a table
data = {}
categories = []
names = []
observations = []
features = []
for name in sheet_names:
    df = df_dict[name]
    name = name[5:]
    category = mapping[name]
    categories.append(category)
    names.append(name)
    observations.append(df.shape[0])
    features.append(df.shape[1])
data["Data record type"] = categories
data["File"] = names
data["#Observations"] = observations
data["#Features"] = features
df = pd.DataFrame(data)
print(df.to_latex(index=False))
print(df.to_markdown(index=False))
