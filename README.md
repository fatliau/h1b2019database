# h1b2019database
A python script that load 2019 h1b petition data into local sqlite database

## requirement:
1. python 3
2. python module sqlalchemy

## step
1. download the raw data in format of xlsx from Department of Labor:
https://www.foreignlaborcert.doleta.gov/performancedata.cfm
2. use any online xlsx -> csv converting website to convert the file 
suggest: https://www.zamzar.com/convert/xlsx-to-csv/
3. create a sqlite database
```
sqlite3 h1b_data.db
```
4. run the python script 
```
# python establish2019H1BDatabas.py <csv file name> <db name>
python establish2019H1BDatabas.py H-1B_Disclosure_Data_FY2019.csv h1b_data.db
```

 
