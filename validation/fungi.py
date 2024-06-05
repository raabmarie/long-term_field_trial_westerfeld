import os
import pandas as pd

db_file_path = 'Westerfeld_DB_V_1_7_MR.xlsx'
rd_file_path = 'Fungi_2015-2021.xlsx'
diff_file_path = 'Differences_Fungi.xlsx'

if os.path.exists(diff_file_path):
    os.remove(diff_file_path)

# Load transformed / normalized data into data frames
sheets = pd.read_excel(db_file_path, sheet_name=[
    'V1_0_PILZE',
    'V1_0_BIOPROJECT',
    'V1_0_HABITAT',
    'V1_0_KINGDOM',
    'V1_0_PHYLUM',
    'V1_0_CLASS',
    'V1_0_FAMILY',
    'V1_0_ORDER',
    'V1_0_GENUS',
    'V1_0_SPECIES',
    'V1_0_BEMERKUNGEN'
])
df_fungi = sheets['V1_0_PILZE']
df_bioProject = sheets['V1_0_BIOPROJECT']
df_habitat = sheets['V1_0_HABITAT']
df_kingdom = sheets['V1_0_KINGDOM']
df_phylum = sheets['V1_0_PHYLUM']
df_class = sheets['V1_0_CLASS']
df_family = sheets['V1_0_FAMILY']
df_order = sheets['V1_0_ORDER']
df_genus = sheets['V1_0_GENUS']
df_species = sheets['V1_0_SPECIES']
df_bemerkungen = sheets['V1_0_BEMERKUNGEN']

# Load raw source data
df_raw = pd.read_excel(rd_file_path, sheet_name='RawData')

# Merge the individual data frames
df_fungi = pd.merge(df_fungi, df_bioProject[['BioProject_ID', 'BioProject_Name']], on='BioProject_ID', how='left')
df_fungi = pd.merge(df_fungi, df_habitat[['Habitat_ID', 'Habitat']], on='Habitat_ID', how='left')
df_fungi = pd.merge(df_fungi, df_kingdom[['Kingdom_ID', 'Kingdom_Name']], on='Kingdom_ID', how='left')
df_fungi = pd.merge(df_fungi, df_phylum[['Phylum_ID', 'Phylum_Name']], on='Phylum_ID', how='left')
df_fungi = pd.merge(df_fungi, df_class[['Class_ID', 'Class_Name']], on='Class_ID', how='left')
df_fungi = pd.merge(df_fungi, df_family[['Family_ID', 'Family_Name']], on='Family_ID', how='left')
df_fungi = pd.merge(df_fungi, df_order[['Order_ID', 'Order_Name']], on='Order_ID', how='left')
df_fungi = pd.merge(df_fungi, df_genus[['Genus_ID', 'Genus_Name']], on='Genus_ID', how='left')
df_fungi = pd.merge(df_fungi, df_species[['Species_ID', 'Species_Name']], on='Species_ID', how='left')
df_fungi = pd.merge(df_fungi, df_bemerkungen[['Bemerkungen_ID', 'Bemerkungen']], on='Bemerkungen_ID', how='left')

# Remove and rename columns
df_fungi.drop(columns=['Pilze_ID', 'BioProject_ID','Habitat_ID','Kingdom_ID', 'Phylum_ID', 'Class_ID', 'Family_ID', 'Order_ID', 'Genus_ID', 'Species_ID', 'Bemerkungen_ID'], inplace=True)
df_fungi.rename(columns={
    'Versuchsjahr': 'Year',
    'Termin': 'Date',
    'Parzelle_ID': 'Parcel_ID',
    'Bemerkungen': 'Remark',
    'BioProject_Name': 'BioProject_ID',
    'Kingdom_Name': 'Kingdom',
    'Phylum_Name': 'Phylum',
    'Class_Name': 'Class',
    'Family_Name': 'Family',
    'Order_Name': 'Order',
    'Genus_Name': 'Genus',
    'Species_Name':'Species'}, inplace=True)

df_raw.drop(columns=['Parcel', 'Crop', 'Sample_Name', 'Internal_ID'], inplace=True)
df_raw['Identifier'] = (
    df_raw['Year'].astype(str) +
    df_raw['Parcel_ID'].astype(str) +
    df_raw['Habitat'].astype(str) +
    df_raw['Beneficials'].astype(str) +
    df_raw['Seq_ID'].astype(str) +
    df_raw['SH_Code'].astype(str)
)

# Create new unique identifier
df_fungi['Identifier'] = (
    df_fungi['Year'].astype(str) +
    df_fungi['Parcel_ID'].astype(str) +
    df_fungi['Habitat'].astype(str) +
    df_fungi['Beneficials'].astype(str) +
    df_fungi['Seq_ID'].astype(str) +
    df_fungi['SH_Code'].astype(str)
)

# TODO: Remove the following line when the data from 2015 comes in
df_raw = df_raw[df_raw['Year'] != 2015]

# Fix timestamps
df_fungi['Date'] = pd.to_datetime(df_fungi['Date'], dayfirst=True, format='mixed')
df_raw['Date'] = pd.to_datetime(df_raw['Date'], dayfirst=True, format='mixed')

# Sort by rows and columns
df_fungi = df_fungi.sort_values(by=['Identifier', 'Date'], ascending=[True, False]).reset_index(drop=True)
df_fungi = df_fungi[sorted(df_fungi.columns)].reset_index(drop=True)
df_raw = df_raw.sort_values(by=['Identifier', 'Date'], ascending=[True, False]).reset_index(drop=True)
df_raw = df_raw[sorted(df_raw.columns)].reset_index(drop=True)

# FInally, check for equality
if list(df_fungi.columns) != list(df_raw.columns):
    print("1. The column names are not equal.")
else:
    print("1. The column names are equal.")

    rd_num_rows = df_raw.shape[0]
    db_num_rows = df_fungi.shape[0]
    if rd_num_rows != db_num_rows:
        print('2. The number of rows do not match.')
    else:
        print('2. The number of rows match.')
        are_equal = df_fungi.equals(df_raw)
        if are_equal == False:
            difference = df_fungi.compare(df_raw)
            difference.to_excel(diff_file_path)
            diff_num_rows = difference.shape[0]
            print(f'3. The values do not match: {diff_num_rows} differences found. See {diff_file_path}.')
        else:
            print('3. The values match.')
