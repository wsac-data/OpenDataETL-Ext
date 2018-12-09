@echo off

set py=C:\Programs\Anaconda3\python.exe

%py% format.py "../../data/scf/Original Tables.xlsx" "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/Alternate 13. Family holdings of debt, by selected characteristics of families and type of debt, 1989 to 2016 surveys.csv"

pause
