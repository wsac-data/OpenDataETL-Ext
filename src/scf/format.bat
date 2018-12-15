@echo off

set py=start C:\Programs\Anaconda3\python.exe
set fp="../../data/scf/scf2016_tables_{source}_{dollar}_historical.xlsx"

echo Start processing Table 1...
%py% format.py %fp% --beg_col "SCF Table" 1 --beg_col !Calculation {source}-{dollar} "^Table 1\s+\d+\-\d+$"       "../../data/scf/{source}_{dollar}/SCF 1. Before-tax family income, pct families that saved, distrib of families.csv"

echo Start processing Table 2...
%py% format.py %fp% --beg_col "SCF Table" 2 --beg_col !Calculation {source}-{dollar} "^Table 2$"                  "../../data/scf/{source}_{dollar}/SCF 2. Amount of before-tax family income by source and net worth percentile.csv"

echo Start processing Table 3...
%py% format.py %fp% --beg_col "SCF Table" 3 --beg_col !Calculation {source}-{dollar} "^Table 3$"                  "../../data/scf/{source}_{dollar}/SCF 3. Reasons most important for their families' saving.csv"

echo Start processing Table 4...
%py% format.py %fp% --beg_col "SCF Table" 4 --beg_col !Calculation {source}-{dollar} "^Table 4$"                  "../../data/scf/{source}_{dollar}/SCF 4. Family net worth, by selected characteristics of families.csv"

echo Start processing Table 13...
%py% format.py %fp% --beg_col "SCF Table" 13 --beg_col !Calculation {source}-{dollar} "^\s*Table 13 \d{2} Alt\s*$" "../../data/scf/{source}_{dollar}/SCF 13alt. Family holdings of debt by type and family characteristics.csv"

echo Start processing Table 15...
%py% format.py %fp% --beg_col "SCF Table" 15 --beg_col !Calculation {source}-{dollar} "^Table 15\s+\d+\-\d+$"      "../../data/scf/{source}_{dollar}/SCF 15. Installment debt by type and family characteristics.csv"

echo Start processing Table 16...
%py% format.py %fp% --beg_col "SCF Table" 16 --beg_col !Calculation {source}-{dollar} "^Table 16$"                 "../../data/scf/{source}_{dollar}/SCF 16. Amount of debt of all families by purpose.csv"

echo Start processing Table 17...
%py% format.py %fp% --beg_col "SCF Table" 17 --beg_col !Calculation {source}-{dollar} "^Table 17$"                 "../../data/scf/{source}_{dollar}/SCF 17. Ratio of debt payments to family income.csv"

pause
