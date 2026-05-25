"""
stata_to_pandas_tutorial.py
============================

A line-by-line translation of a Stata data-manipulation tutorial into Python
using pandas. Demonstrates the equivalent pandas operations for the most
common Stata commands: importing data, renaming and labelling variables,
formatting, encoding, row-wise operations, recoding, duplicates handling,
reshape (long/wide), appending, and merging.

The original Stata code was written by the author during their MSc training;
this file translates it into Python for portfolio purposes.

Author:   Diana Lagravinese
Python:   3.10+
Requires: pandas, numpy

Run with:
    python stata_to_pandas_tutorial.py
"""

import os
from pathlib import Path

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Set working directory
# Stata:  cd "/Users/dianalagravinese/STATA TUTORIAL"
# ---------------------------------------------------------------------------
# In Python it is more portable to use pathlib than to chdir. Setting BASE_DIR
# to the script's own folder means the code runs anywhere.
BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)


# ===========================================================================
# 1. IMPORTING DATA
# ===========================================================================

# Stata:  use Entrance, clear
# pandas equivalent: read a Stata .dta file
# df = pd.read_stata("Entrance.dta")

# Stata:  import delimited entrance.txt, clear
# pandas equivalent: read a text/CSV file. The `sep=None, engine="python"`
# trick lets pandas infer the delimiter automatically.
# df = pd.read_csv("entrance.txt", sep=None, engine="python")

# Stata:  import delimited flavor2.csv, clear
# df = pd.read_csv("flavor2.csv")

# For this tutorial we build the dataframe in memory so the script is
# self-contained and runnable without external files.
df = pd.DataFrame({
    "v1": ["Anna", "Marco", "Sara", "Luca", "Giulia"],
    "v2": [17, 22, 30, 18, 25],
    "v3": ["chocolate", "vanilla", "strawberry", "mint", "chocolate"],
    "v4": [2, 1, 2, 1, 2],   # 1 = male, 2 = female (as in the Stata code)
})


# ===========================================================================
# 2. RENAMING VARIABLES
# ===========================================================================

# Stata:
#   rename v1 Name
#   rename v2 Age
#   rename v3 Flavor
#   rename v4 Gender
df = df.rename(columns={
    "v1": "Name",
    "v2": "Age",
    "v3": "Flavor",
    "v4": "Gender",
})


# ===========================================================================
# 3. LABELLING
# ===========================================================================

# Stata stores variable labels and value labels as metadata. pandas does not
# have a direct equivalent, but two common approaches are:
#   (a) Use `pd.Categorical` with ordered categories - good for analysis.
#   (b) Keep a separate dictionary of labels - good for documentation.

# Stata:  label variable Flavor "Icecream flavor"
variable_labels = {
    "Flavor": "Icecream flavor",
}

# Stata:  label define sex 1 "male" 2 "female"
#         label values Gender sex
gender_map = {1: "male", 2: "female"}
df["Gender_label"] = df["Gender"].map(gender_map)


# ===========================================================================
# 4. FORMATTING (string <-> numeric conversion)
# ===========================================================================

# Stata:  tostring id, replace        --> convert numeric to string
# Stata:  destring year, replace      --> convert string to numeric

# Example: convert Age (numeric) to string
df["Age_str"] = df["Age"].astype(str)

# And back to numeric. `errors="coerce"` mirrors Stata's behaviour of
# producing missing values for unparseable entries rather than crashing.
df["Age_num"] = pd.to_numeric(df["Age_str"], errors="coerce")


# ===========================================================================
# 5. CREATION AND DELETION
# ===========================================================================

# Stata:  encode sex, gen(gender)
# This turns a string variable into a numeric one with value labels.
# pandas equivalent: convert to Categorical and use the integer codes.
df["Flavor_encoded"] = pd.Categorical(df["Flavor"]).codes

# Stata:  tab sex gender, nolabel  /  tab sex gender
# pandas equivalent: cross-tabulation.
print("\nCross-tab of Flavor vs Flavor_encoded:")
print(pd.crosstab(df["Flavor"], df["Flavor_encoded"]))

# Stata:  gen ImAStudent = 1
df["ImAStudent"] = 1


# ===========================================================================
# 6. ROW-WISE OPERATIONS (egen equivalents)
# ===========================================================================

# Create a small dataframe with some missing values to demonstrate row-wise
# operations, since the original Stata `egen rowtotal` etc. operate on
# multiple columns.
egen_df = pd.DataFrame({
    "id": [1, 2, 3, 4],
    "a":  [10, 20, np.nan, 40],
    "b":  [1, np.nan, 3, 4],
    "c":  [100, 200, 300, np.nan],
})

# Stata:  egen rtotal = rowtotal(a b c)
# Sum across columns row-wise, treating NaN as 0 (Stata's default).
egen_df["rtotal"] = egen_df[["a", "b", "c"]].sum(axis=1)

# Stata:  egen rnomiss = rownonmiss(a b c)
# Count non-missing values in each row.
egen_df["rnomiss"] = egen_df[["a", "b", "c"]].notna().sum(axis=1)

# Stata:  egen rfirst = rowfirst(a b c)
# First non-missing value across the listed columns.
egen_df["rfirst"] = egen_df[["a", "b", "c"]].bfill(axis=1).iloc[:, 0]

# Stata:  egen columntotal = total(a)
# Sum of a single column, broadcast back to every row.
egen_df["columntotal"] = egen_df["a"].sum(skipna=True)


# ===========================================================================
# 7. RECODING
# ===========================================================================

# Stata:  recode v4 (2=1) (1=0), gen(gender)
# Map values 2 -> 1 and 1 -> 0 in a new column.
df["gender_recoded"] = df["Gender"].replace({2: 1, 1: 0})

# Stata:  recode v2 (17/19=1) (20/max=0), gen(teenager)
# Bin ages: 17-19 -> 1, 20+ -> 0.
df["teenager"] = np.where(df["Age"].between(17, 19), 1, 0)


# ===========================================================================
# 8. DUPLICATES
# ===========================================================================

# Build a small dataframe with deliberate duplicates.
dup_df = pd.DataFrame({
    "id":     [1, 1, 2, 2, 3],
    "female": [1, 1, 0, 0, 1],
    "ses":    [3, 3, 2, 2, 1],
    "math":   [80, 80, 75, 90, 65],
})

# Stata:  duplicates report
#   -> overall duplicate-row count
n_duplicate_rows = dup_df.duplicated().sum()
print(f"\nDuplicate rows (all columns): {n_duplicate_rows}")

# Stata:  duplicates report id female ses
#   -> duplicates considering only these columns
n_dup_subset = dup_df.duplicated(subset=["id", "female", "ses"]).sum()
print(f"Duplicates on (id, female, ses): {n_dup_subset}")

# Stata:  duplicates tag id female ses, gen(NumCopy)
#   -> flag rows that are part of a duplicate group
dup_df["NumCopy"] = dup_df.duplicated(
    subset=["id", "female", "ses"], keep=False,
).astype(int)
print("\nRows flagged as duplicates:")
print(dup_df[dup_df["NumCopy"] >= 1])

# Stata:  replace math = 84 if id == 1
dup_df.loc[dup_df["id"] == 1, "math"] = 84

# Stata:  duplicates drop
dup_df = dup_df.drop_duplicates(subset=["id", "female", "ses"]).reset_index(drop=True)


# ===========================================================================
# 9. RESHAPE (wide <-> long)
# ===========================================================================

# Wide-format example (mirroring webuse reshape1).
wide_df = pd.DataFrame({
    "id":    [1, 2, 3],
    "inc80": [5000, 2000, 3000],
    "inc81": [5500, 2200, 2000],
    "inc82": [6000, 3300, 1000],
    "ue80":  [0, 1, 0],
    "ue81":  [1, 0, 0],
    "ue82":  [0, 0, 1],
})

# Stata:  reshape long inc ue, i(id) j(year)
# pandas equivalent: pd.wide_to_long
long_df = pd.wide_to_long(
    wide_df, stubnames=["inc", "ue"], i="id", j="year",
).reset_index()
print("\nLong-format dataframe:")
print(long_df.head(10))

# Stata:  reshape wide inc ue, i(id) j(year)
# pandas equivalent: pivot back.
wide_again = long_df.pivot(index="id", columns="year", values=["inc", "ue"])
# Flatten the multi-level column names back to inc80, inc81, ... style.
wide_again.columns = [f"{var}{yr}" for var, yr in wide_again.columns]
wide_again = wide_again.reset_index()
print("\nReshaped back to wide:")
print(wide_again)


# ===========================================================================
# 10. APPEND (stacking dataframes vertically)
# ===========================================================================

ca_pop = pd.DataFrame({"city": ["Los Angeles", "San Diego"], "pop": [3900000, 1400000]})
il_pop = pd.DataFrame({"city": ["Chicago", "Aurora"],       "pop": [2700000, 200000]})
tx_pop = pd.DataFrame({"city": ["Houston", "Dallas"],       "pop": [2300000, 1300000]})

# Stata:  append using ilpop txpop, gen(state)
appended = pd.concat(
    [ca_pop.assign(state=0), il_pop.assign(state=1), tx_pop.assign(state=2)],
    ignore_index=True,
)

# Stata:  label define statelab 0 "CA" 1 "IL" 2 "TX"
#         label values state statelab
state_label = {0: "CA", 1: "IL", 2: "TX"}
appended["state_label"] = appended["state"].map(state_label)
print("\nAppended dataframe:")
print(appended)

# Stata:  preserve / keep if state == X / save / restore
# pandas does not need preserve/restore because filtering returns a new
# dataframe and leaves the original untouched.
ca_only = appended[appended["state"] == 0].copy()
il_only = appended[appended["state"] == 1].copy()
tx_only = appended[appended["state"] == 2].copy()


# ===========================================================================
# 11. MERGE (joining dataframes horizontally)
# ===========================================================================

autosize = pd.DataFrame({
    "make":   ["BMW", "Audi", "Fiat", "Toyota"],
    "weight": [1500, 1450, 1100, 1350],
    "length": [4.5, 4.6, 3.8, 4.4],
})

autoexpense = pd.DataFrame({
    "make":  ["BMW", "Audi", "Fiat", "Honda"],
    "price": [45000, 42000, 18000, 25000],
    "mpg":   [30, 32, 45, 38],
})

# Stata:  merge 1:1 make using autoexpense
# pandas equivalent: pd.merge with `how="outer"` mirrors Stata's default
# behaviour of keeping master, using and matched rows. The `indicator=True`
# argument creates a `_merge` column equivalent to Stata's.
merged = autosize.merge(
    autoexpense, on="make", how="outer", indicator="_merge",
)
print("\nMerged dataframe with merge indicator:")
print(merged)

# Stata:  drop _merge
merged = merged.drop(columns="_merge")

# Stata:  keep make weight length  /  save SIZE
size_subset = merged[["make", "weight", "length"]].copy()

# Stata:  keep make price mpg  /  save EXPENSE
expense_subset = merged[["make", "price", "mpg"]].copy()


# ===========================================================================
# 12. (BONUS) SAVING THE RESULTS
# ===========================================================================

# Stata:  save filename, replace
# pandas equivalents - uncomment any you want to actually run:
# df.to_csv("output_main.csv", index=False)
# df.to_parquet("output_main.parquet", index=False)
# df.to_stata("output_main.dta", write_index=False)   # writes a Stata file

print("\nScript complete. Final main dataframe:")
print(df)
