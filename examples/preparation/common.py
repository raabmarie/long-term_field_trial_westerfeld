import pandas as pd


def prepare_table_experiment(df):
    # Load CSV files
    df_plot = pd.read_csv("../../lte_westerfeld.V1_0_PLOT.csv")
    df_experimental_setup = pd.read_csv(
        "../../lte_westerfeld.V1_0_EXPERIMENTAL_SETUP.csv"
    )
    df_crop = pd.read_csv("../../lte_westerfeld.V1_0_CROP.csv")
    df_treatment = pd.read_csv("../../lte_westerfeld.V1_0_TREATMENT.csv")
    df_factor_1_level = pd.read_csv("../../lte_westerfeld.V1_0_FACTOR_1_LEVEL.csv")
    df_factor_2_level = pd.read_csv("../../lte_westerfeld.V1_0_FACTOR_2_LEVEL.csv")

    # Check if Crop_ID is already available
    if "Crop_ID" in df.columns:
        # If yes, join table PLOT by Treatment_ID
        df = pd.merge(
            df, df_plot[["Plot_ID", "Treatment_ID"]], on="Plot_ID", how="left"
        )
    else:
        # If no, join table EXPERIMENTAL_SETUP by Crop_ID and Treatment_ID
        df = pd.merge(
            df,
            df_experimental_setup[
                ["Plot_ID", "Experimental_Year", "Crop_ID", "Treatment_ID"]
            ],
            on=["Experimental_Year", "Plot_ID"],
            how="left",
        )

    # Add CROP information
    df = pd.merge(df, df_crop[["Crop_ID", "Name_EN"]], on="Crop_ID", how="left")
    df = df.rename(columns={"Name_EN": "Crop"})

    # Add TREATEMENT information for 'Factor_1_Level_ID' and 'Factor_2_Level_ID'
    df = pd.merge(
        df,
        df_treatment[["Treatment_ID", "Factor_1_Level_ID", "Factor_2_Level_ID"]],
        on="Treatment_ID",
        how="left",
    )

    # Add FACTOR_1_LEVEL information for Tillage
    df = pd.merge(
        df,
        df_factor_1_level[["Factor_1_Level_ID", "Name_EN"]],
        on="Factor_1_Level_ID",
        how="left",
    )
    df = df.rename(columns={"Name_EN": "Tillage"})

    # Add FACTOR_2_LEVEL information for Fertilization
    df = pd.merge(
        df,
        df_factor_2_level[["Factor_2_Level_ID", "Name_EN"]],
        on="Factor_2_Level_ID",
        how="left",
    )
    df = df.rename(columns={"Name_EN": "Fertilization"})

    # Drop merged identifier columns
    df = df.drop(
        columns=["Factor_2_Level_ID", "Factor_1_Level_ID", "Treatment_ID", "Crop_ID"]
    )

    return df


def prepare_table_taxonomy(df):
    # Load CSV files
    df_kingdom = pd.read_csv("../../lte_westerfeld.V1_0_KINGDOM.csv")
    df_phylum = pd.read_csv("../../lte_westerfeld.V1_0_PHYLUM.csv")
    df_class = pd.read_csv("../../lte_westerfeld.V1_0_CLASS.csv")
    df_family = pd.read_csv("../../lte_westerfeld.V1_0_FAMILY.csv")
    df_order = pd.read_csv("../../lte_westerfeld.V1_0_ORDER.csv")
    df_genus = pd.read_csv("../../lte_westerfeld.V1_0_GENUS.csv")
    df_species = pd.read_csv("../../lte_westerfeld.V1_0_SPECIES.csv")

    # Add KINGDOM information
    df = pd.merge(df, df_kingdom[["Kingdom_ID", "Name"]], on="Kingdom_ID", how="left")
    df = df.rename(columns={"Name": "Kingdom"})

    # Add PHYLUM information
    df = pd.merge(df, df_phylum[["Phylum_ID", "Name"]], on="Phylum_ID", how="left")
    df = df.rename(columns={"Name": "Phylum"})

    # Add CLASS information
    df = pd.merge(df, df_class[["Class_ID", "Name"]], on="Class_ID", how="left")
    df = df.rename(columns={"Name": "Class"})

    # Add ORDER information
    df = pd.merge(df, df_order[["Order_ID", "Name"]], on="Order_ID", how="left")
    df = df.rename(columns={"Name": "Order"})

    # Add FAMILY information
    df = pd.merge(df, df_family[["Family_ID", "Name"]], on="Family_ID", how="left")
    df = df.rename(columns={"Name": "Family"})

    # Add GENUS information
    df = pd.merge(df, df_genus[["Genus_ID", "Name"]], on="Genus_ID", how="left")
    df = df.rename(columns={"Name": "Genus"})

    # Add SPECIES information
    df = pd.merge(df, df_species[["Species_ID", "Name"]], on="Species_ID", how="left")
    df = df.rename(columns={"Name": "Species"})

    # Drop merged identifier columns
    df = df.drop(
        columns=[
            "Species_ID",
            "Genus_ID",
            "Family_ID",
            "Order_ID",
            "Class_ID",
            "Phylum_ID",
            "Kingdom_ID",
        ]
    )

    return df
