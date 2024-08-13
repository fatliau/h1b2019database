import heapq
import sys
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError


def getEmployersList(limit, dbName):
    employers = []
    querySQL = "SELECT COUNT(*), EMPLOYER_NAME FROM h1bdata_2019 " \
               "WHERE JOB_TITLE like '%Engineer%' AND PREVAILING_WAGE > 25000 " \
               "GROUP BY EMPLOYER_NAME HAVING COUNT(*) > 5 " \
               "ORDER BY COUNT(*) DESC LIMIT {};".format(limit)
    db_connect = create_engine('sqlite:///{}'.format(dbName))
    conn = db_connect.connect()
    try:
        query = conn.execute(text(querySQL))
        for row in query.fetchall():
            employers.append(row[1])
    except SQLAlchemyError as e:
        print("SQL error: {}".format(e))
    return employers

def getMedianSalary(employerName, dbName):
    querySQL = "SELECT PREVAILING_WAGE FROM h1bdata_2019 " \
               "WHERE JOB_TITLE LIKE '%Engineer%' " \
               "AND PREVAILING_WAGE > 25000 " \
               "AND EMPLOYER_NAME = '{}';".format(employerName)
    db_connect = create_engine('sqlite:///{}'.format(dbName))
    conn = db_connect.connect()
    H = []
    try:
        query = conn.execute(text(querySQL))
        for row in query.fetchall():
            heapq.heappush(H, row[0])
    except SQLAlchemyError as e:
        print("SQL error: {}".format(e))
    total = len(H)
    mid = len(H) // 2
    for i in range(mid):
        medium = heapq.heappop(H)
        if i == mid // 2:
            quartile = medium
    return total, medium, quartile

def createEmployerSalaryStatTable(dbName='h1b_data.db'):
    createSQL = "CREATE TABLE employer_salary_stats(" \
                "EMPLOYER_NAME  TEXT, " \
                "TOTAL_CASES    INT, " \
                "MEDIUM_PAY     REAL, " \
                "QUARTILE_PAY   REAL);"
    db_connect = create_engine('sqlite:///{}'.format(dbName))
    conn = db_connect.connect()
    try:
        query = conn.execute(text(createSQL))
        print("table employer_salary_stats created")
    except SQLAlchemyError as e:
        print("SQL error: {}".format(e))
    conn.commit()

def calculateEmployerSalaryStatAndInsertTable(employers, dbName):
    size_allEmployers = len(employers)
    for i, employer in enumerate(employers):
        totalHire, medium, quartile = getMedianSalary(employer, dbName)
        insertSQL = "INSERT INTO employer_salary_stats VALUES( '{}',{},{},{} );" \
            .format(employer, totalHire, medium, quartile)
        db_connect = create_engine('sqlite:///{}'.format(dbName))
        conn = db_connect.connect()
        try:
            query = conn.execute(text(insertSQL))
            print("insert data into employer_salary_stats {}/{}".format(i+1, size_allEmployers))
        except SQLAlchemyError as e:
            print("SQL error: {}".format(e))
        conn.commit()


if __name__ == '__main__':
    if len(sys.argv) >= 3:
        EmployerNumber = sys.argv[1]
        dbName = sys.argv[2]
    else:
        EmployerNumber = 500
        dbName = 'h1b_data.db'
    print("prepare to enter {} employers data into DB: {}".format(EmployerNumber, dbName))
    try:
        createEmployerSalaryStatTable(dbName)
        employers_to_add = getEmployersList(EmployerNumber, dbName)
        calculateEmployerSalaryStatAndInsertTable(employers_to_add, dbName)
    except SQLAlchemyError as e:
        print("Error: {}".format(e))
