# h1b2019database
A python script that load 2019 h1b petition data into local sqlite database

## requirements
1. python 3
2. python module sqlalchemy

## steps
1. download the [raw data](https://www.foreignlaborcert.doleta.gov/pdf/PerformanceData/2019/H-1B_Disclosure_Data_FY2019.xlsx) in format of xlsx from [Department of Labor](https://www.foreignlaborcert.doleta.gov/performancedata.cfm)
2. use any online xlsx -> csv converting website(suggest: [zamar](https://www.zamzar.com/convert/xlsx-to-csv/)) to convert the file
3. create a sqlite database
```
sqlite3 h1b_data.db
```
4. run the python script 
```
# python establish2019H1BDatabas.py <csv file name> <db name>
python establish2019H1BDatabas.py H-1B_Disclosure_Data_FY2019.csv h1b_data.db
```
5. run the salary analytics script
```
# python calculateEmployerSalaryStatisitcs.py <number of employers to be calculated> <db name>
python calculateEmployerSalaryStatisitcs.py 2000 h1b_data.db
```

## check the data
### high salary h1b employers
```
   SELECT count(*), EMPLOYER_NAME FROM h1bdata_2019 
    WHERE PREVAILING_WAGE > 123000 
      AND JOB_TITLE LIKE "%Engineer%" 
 GROUP BY EMPLOYER_NAME ORDER BY COUNT(*) DESC LIMIT 100;
```
![H1B_TopHighSalaryEmployers.png](/pics/H1B_TopHighSalaryEmployers.png)

### certain employer/city/state/job_title
```
 SELECT PREVAILING_WAGE, EMPLOYER_NAME, JOB_TITLE, WORKSITE_CITY, WORKSITE_STATE
   FROM h1bdata_2019
  WHERE EMPLOYER_NAME LIKE "%Google%" 
    AND WORKSITE_CITY = 'Cambridge' LIMIT 100;
```
![H1B_Google_Cambridge.png](/pics/H1B_Google_Cambridge.png)
### top quartile salary emploer list
```
SELECT * FROM employer_salary_stats ORDER BY QUARTILE_PAY DESC LIMIT 100;
![H1B_TopQuartileSalaryEmployer.png](/pics/H1B_TopQuartileSalaryEmployer.png)
