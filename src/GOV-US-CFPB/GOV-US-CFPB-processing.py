import pandas as pd
import re
from pathlib import Path

data_path = Path(__file__).parents[2] / "data" / "GOV-US-CFPB"
in_data_path = data_path / "raw"
out_data_path = data_path
outfile_names = ["data_age.csv",
    "data_income.csv",
    "data_score.csv",
    "data_all.csv",
    "data_state.csv"]

def format_yoy_group(df, grouping, type_of_value):
    outdf = (
        df.rename({ "younger-than-30_yoy" : "Younger than 30",
            "30-44_yoy" : "Age 30-44",
            "45-64_yoy" : "Age 45-64",
            "65-and-older_yoy" : "Age 65 and older",
            "low_yoy" : "Low",
            "middle_yoy" : "Middle",
            "moderate_yoy" : "Moderate",
            "high_yoy" : "High",
            "deep-subprime_yoy" : "Deep subprime",
            "subprime_yoy" : "Subprime",
            "near-prime_yoy" : "Near-prime",
            "prime_yoy" : "Prime",
            "super-prime_yoy" : "Super-prime"}
            , axis="columns")
        .melt(id_vars = ["month", "date"], var_name = grouping,
            value_name = type_of_value))
    return(outdf)


def format_vol_group(df, grouping, type_of_value):
    outdf = (
        df.rename({ "vol" : type_of_value,
            "vol_unadj" : type_of_value + "_unadj",
            "age_group" : "Age_Group",
            "income_level_group" : "Income_Level",
            "credit_score_group" : "Score_Level"}, axis="columns"))
    return(outdf)


def format_no_group(df, type_of_value):
    outdf = (
        df.rename({ "vol" : type_of_value,
            "vol_unadj" : type_of_value + "_unadj",
            "num" : type_of_value,
            "num_unadj" : type_of_value + "_unadj",
            "value" : type_of_value,
            "yoy_num" : "number_" + type_of_value,
            "yoy_vol" : "volume_" + type_of_value},  axis="columns"))
    return(outdf)


def merge_dfs(grouping_df, df, on_columns):
    if grouping_df is not None:
        grouping_df = grouping_df.merge(df, how="outer",
            on=on_columns)
    else:
        grouping_df = df
    return(grouping_df)


# I'm failing to see a better organization than one table for each
# grouping, with the observation unit being month-groups.  This
# will net us 4 + 1 master dfs:
# the 4 are the loan data divided by age, income, score, and no division
# the 1 is the map data, which doesn't go with anything.

csv_file_paths = list(in_data_path.glob("*.csv"))
csv_names = [re.sub("^(.*)\\.csv$", "\\1", p.name) for p in csv_file_paths]
csv_name_elements = [c.split("_") for c in csv_names]

age_group_df = None
income_level_df = None
score_level_df = None
no_grouping_df = None
map_df = None

for i, c in enumerate(csv_name_elements):
    #dealing with inconsistent filename convention
    if len(c) < 5:
        grouping = None
        if c[0] == "vol":
            type_of_value = "volume_" + c[2]
        elif c[0] == "num":
            type_of_value = "number_" + c[2]
        elif c[0] == "yoy":
            type_of_value = "yoy_" + c[3]
        elif c[0] == "map":
            type_of_value = "yoy_" + c[2]
    else:
        grouping = c[2] + "_" + c[3]
        type_of_value = c[0] + "_" + c[4]

    #reading in csv files now that names are sorted
    df = pd.read_csv(csv_file_paths[i])

    #formatting: 3 different broad formatting options necessary
    if grouping != None:
        if c[0] == "yoy":
            df = format_yoy_group(df, grouping, type_of_value)
        elif c[0] == "volume":
            df = format_vol_group(df, grouping, type_of_value)
    elif grouping == None:
        df = format_no_group(df, type_of_value)
    print(df.columns)

    #combine the df into the appropriate master
    if grouping == "Age_Group":
        age_group_df = merge_dfs(age_group_df, df,
            ["month", "date", grouping])
    elif grouping == "Income_Level":
        income_level_df = merge_dfs(income_level_df,
            df, ["month", "date", grouping])
    elif grouping == "Score_Level":
        score_level_df = merge_dfs(score_level_df,
            df, ["month", "date", grouping])
    elif grouping == None:
        if c[0] == "map":
            map_df = merge_dfs(map_df, df, ["state_abbr", "fips_code"])
        else:
            no_grouping_df = merge_dfs(no_grouping_df,
                df, ["month", "date"])

#write files
df_list = [age_group_df, income_level_df, score_level_df,
    no_grouping_df, map_df]
for name, df in zip(outfile_names, df_list):
    with (out_data_path / name).open("w", newline="") as file:
        df.to_csv(file)
