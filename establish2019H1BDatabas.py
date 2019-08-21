import csv
import sys
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


def createRawTable(fileName="H-1B_Disclosure_Data_FY2019.csv", dbName='h1b_data.db'):
    with open(fileName) as file:
        csvReader = csv.DictReader(file)
        headers = csvReader.fieldnames
        createTableSQL = "CREATE TABLE h1bdata_2019("
        for i, header in enumerate(headers):
            if header == "PREVAILING_WAGE":
                createTableSQL += header + " REAL"
            else:
                createTableSQL += header + " TEXT"
            if i != len(headers) - 1:
                createTableSQL += ", "
            else:
                createTableSQL += ");"
    db_connect = create_engine('sqlite:///{}'.format(dbName))
    conn = db_connect.connect()
    try:
        query = conn.execute(createTableSQL)
        print("created table: h1bdata_2019")
    except SQLAlchemyError as e:
        print("SQL error: {}".format(e))
        raise SQLAlchemyError

def insertDataIntoRawTabe(fileName="H-1B_Disclosure_Data_FY2019.csv", dbName='h1b_data.db'):
    db_connect = create_engine('sqlite:///{}'.format(dbName))
    conn = db_connect.connect()
    with open(fileName) as file:
        csvReader = csv.DictReader(file)
        headers = csvReader.fieldnames
        rowNo = 0
        for row in csvReader:
            if rowNo % 1000 == 0:
                print("insert {} rows".format(rowNo))
            rowNo += 1
            insertSQL = "INSERT INTO h1bdata_2019 "
            valueSQL = "("
            for i, key in enumerate(headers):

                if i != len(headers) - 1:
                    if key == "PREVAILING_WAGE":
                        valueSQL += moneyParser(row[key]) + ","
                    else:
                        valueSQL += "'" + escapeHelper(row[key]) + "'" + ","
                else:
                    valueSQL += "'" + escapeHelper(row[key]) + "'" + ");"
            insertSQL += "VALUES " + valueSQL
            try:
                query = conn.execute(insertSQL)
            except SQLAlchemyError as e:
                print("SQL error: {}".format(e))

def escapeHelper(string):
    return string.replace("'", "`")

def moneyParser(moneyString):
    moneyString = moneyString.replace('$', '')
    moneyString = moneyString.replace(',', '')
    return moneyString

def showHeader(dbName='h1b_data.db'):
    engine = create_engine('sqlite:///{}'.format(dbName))
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    jobs = sqlalchemy.Table('h1bdata_2019', metadata, autoload=True, autoload_with=engine)
    print(jobs.columns.keys())

def displayCSV(fileName="H-1B_Disclosure_Data_FY2019.csv"):
    with open(fileName)as file:
        csvReader = csv.DictReader(file)
        i = 0
        for row in csvReader:
            print(moneyParser(row["PREVAILING_WAGE"]))
            i += 1
            if i > 10:
                break


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        fileName = sys.argv[1]
        dbName = sys.argv[2]
    else:
        fileName = 'H-1B_Disclosure_Data_FY2019.csv'
        dbName = 'h1b_data.db'
    print(fileName, dbName)
    try:
        createRawTable(fileName, dbName)
        insertDataIntoRawTabe(fileName, dbName)
    except SQLAlchemyError as e:
        print("Error: {}".format(e))
