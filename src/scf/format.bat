@echo off

set py=C:\Programs\Anaconda3\python.exe

%py% format.py "../../data/scf/scf2016_tables_public_nominal_historical.xlsx"   "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/public_nominal/Alternate 13. Family holdings of debt, by selected characteristics of families and type of debt, 1989 to 2016 surveys.csv"
%py% format.py "../../data/scf/scf2016_tables_internal_nominal_historical.xlsx" "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/internal_nominal/Alternate 13. Family holdings of debt, by selected characteristics of families and type of debt, 1989 to 2016 surveys.csv"
%py% format.py "../../data/scf/scf2016_tables_public_real_historical.xlsx"      "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/public_real/Alternate 13. Family holdings of debt, by selected characteristics of families and type of debt, 1989 to 2016 surveys.csv"
%py% format.py "../../data/scf/scf2016_tables_internal_real_historical.xlsx"    "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/internal_real/Alternate 13. Family holdings of debt, by selected characteristics of families and type of debt, 1989 to 2016 surveys.csv"

pause
