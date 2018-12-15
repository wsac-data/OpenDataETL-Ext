@echo off

set py=C:\Programs\Anaconda3\python.exe
set fp="../../data/scf/scf2016_tables_{source}_{dollar}_historical.xlsx"

echo Start processing Table 1...
start %py% format.py %fp% "^Table 1\s+\d+\-\d+$"       "../../data/scf/{source}_{dollar}/SCF 1. Before-tax family income, pct families that saved, distrib of families.csv"

echo Start processing Table 2...
start %py% format.py %fp% "^Table 2$"                  "../../data/scf/{source}_{dollar}/SCF 2. Amount of before-tax family income by source and net worth percentile.csv"

echo Start processing Table 3...
start %py% format.py %fp% "^Table 3$"                  "../../data/scf/{source}_{dollar}/SCF 3. Reasons most important for their families' saving.csv"

echo Start processing Table 4...
start %py% format.py %fp% "^Table 4$"                  "../../data/scf/{source}_{dollar}/SCF 4. Family net worth, by selected characteristics of families.csv"

echo Start processing Table 13...
start %py% format.py %fp% "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/{source}_{dollar}/SCF 13alt. Family holdings of debt by type and family characteristics.csv"

echo Start processing Table 15...
start %py% format.py %fp% "^Table 15\s+\d+\-\d+$"      "../../data/scf/{source}_{dollar}/SCF 15. Installment debt by type and family characteristics.csv"

echo Start processing Table 16...
start %py% format.py %fp% "^Table 16$"                 "../../data/scf/{source}_{dollar}/SCF 16. Amount of debt of all families by purpose.csv"

echo Start processing Table 17...
start %py% format.py %fp% "^Table 17$"                 "../../data/scf/{source}_{dollar}/SCF 17. Ratio of debt payments to family income.csv"

pause
