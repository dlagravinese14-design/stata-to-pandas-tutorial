# Stata-to-pandas tutorial

A line-by-line translation of a Stata data-manipulation tutorial into Python
using **pandas**. Originally written by me during my MSc in Economics and
Finance for Stata, then translated into Python for portfolio purposes.

## What it covers

The script `stata_to_pandas_tutorial.py` demonstrates the pandas equivalents
of the most common Stata data-management commands:

| Section                              | Stata commands shown                                |
|--------------------------------------|-----------------------------------------------------|
| Importing data                       | `use`, `import delimited`                           |
| Renaming and labelling               | `rename`, `label variable`, `label define/values`   |
| String/numeric conversion            | `tostring`, `destring`                              |
| Creation, deletion, encoding         | `encode`, `tab`, `gen`                              |
| Row-wise operations                  | `egen rowtotal/rownonmiss/rowfirst/total`           |
| Recoding                             | `recode`                                            |
| Duplicates                           | `duplicates report/tag/drop`                        |
| Reshape long/wide                    | `reshape long`, `reshape wide`                      |
| Append (vertical stacking)           | `append using`                                      |
| Merge (horizontal joins)             | `merge 1:1`                                         |

Each section in the Python file mirrors the corresponding Stata block, with
comments showing the Stata original above each pandas equivalent.

## Why this project

The tutorial demonstrates how the standard Stata data-management workflow
maps onto Python's pandas. It is intended as:

1. A reference for analysts moving from Stata to Python.
2. A self-contained, runnable example covering common data tasks.
3. A small portfolio piece showing fluency in both tools.

## How to run

Requires Python 3.10+ and the libraries listed in `requirements.txt`.

```bash
pip install -r requirements.txt
python stata_to_pandas_tutorial.py
```

The script is self-contained: all example dataframes are built in memory, so
no external files are needed.

## Author

Diana Lagravinese — junior economist, Luiss Guido Carli (MSc Economics and
Finance, 2024).
