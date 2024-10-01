def validate(df, df_raw, miss_id_file_path, diff_file_path):
    if list(df.columns) != list(df_raw.columns):
        print("1. The column names are not equal.")
    else:
        print("1. The column names are equal.")

        rd_num_rows = df_raw.shape[0]
        db_num_rows = df.shape[0]
        if rd_num_rows != db_num_rows:
            df_mis_ident = df_raw[~df_raw["Identifier"].isin(df["Identifier"])]
            df_mis_ident.to_excel(miss_id_file_path)
            diff_num_rows = df_mis_ident.shape[0]
            print(
                f"2. The number of rows do not match: {diff_num_rows} missing identifiers found. See {miss_id_file_path}."
            )
        else:
            print("2. The number of rows match.")
            are_equal = df.equals(df_raw)
            if not are_equal:
                difference = df.compare(df_raw)
                difference.to_excel(diff_file_path)
                diff_num_rows = difference.shape[0]
                print(
                    f"3. The values do not match: {diff_num_rows} differences found. See {diff_file_path}."
                )
            else:
                print("3. The values match.")
