@echo off

set py=C:\Programs\Anaconda3\python.exe

%py% format.py "../../data/scf/scf2016_tables_{source}_{dollar}_historical.xlsx"   "^Table 2$"                  "../../data/scf/{source}_{dollar}/2. Amount of before-tax family income, distributed by income sources, by percentile of net worth, 1989 to 2016 surveys.csv"
%py% format.py "../../data/scf/scf2016_tables_{source}_{dollar}_historical.xlsx"   "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/{source}_{dollar}/Alternate 13. Family holdings of debt, by selected characteristics of families and type of debt, 1989 to 2016 surveys.csv"

pause
