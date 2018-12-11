@echo off

set py=C:\Programs\Anaconda3\python.exe
set fp="../../data/scf/scf2016_tables_{source}_{dollar}_historical.xlsx"

%py% format.py %fp% "^Table 1\s+\d+\-\d+$"       "../../data/scf/{source}_{dollar}/1. Before-tax family income, percentage of families that saved, and distribution of families, by selected characteristics of families, 1989 to 2016 surveys.csv"
%py% format.py %fp% "^Table 15\s+\d+\-\d+$"      "../../data/scf/{source}_{dollar}/15. Value of installment debt distributed by type of installment debt by selected characteristics of families with installment debt, 1989 to 2016 surveys.csv"
REM %py% format.py %fp% "^Table 17$"                 "../../data/scf/{source}_{dollar}/17. Ratio of debt payments to family income (aggregate and median), 1989 to 2016 surveys.csv"
REM %py% format.py %fp% "^Table 16$"                 "../../data/scf/{source}_{dollar}/16. Amount of debt of all families, distributed by purpose of debt, 1989 to 2013 surveys.csv"
REM %py% format.py %fp% "^Table 4$"                  "../../data/scf/{source}_{dollar}/4. Family net worth, by selected characteristics of families, 1989 to 2016 surveys.csv"
REM %py% format.py %fp% "^Table 3$"                  "../../data/scf/{source}_{dollar}/3. Reasons respondents gave as most important for their families' saving, distributed by type of reason, 1989 to 2016 surveys.csv"
REM %py% format.py %fp% "^Table 2$"                  "../../data/scf/{source}_{dollar}/2. Amount of before-tax family income, distributed by income sources, by percentile of net worth, 1989 to 2016 surveys.csv"
REM %py% format.py %fp% "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/{source}_{dollar}/Alternate 13. Family holdings of debt, by selected characteristics of families and type of debt, 1989 to 2016 surveys.csv"

pause
