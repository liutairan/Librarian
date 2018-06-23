import sqlite3
from sqlite3 import Error

from ReferenceStructure import *

def createDB(db_path):
    pass

# Checked
def createConnectionToDB(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
        return None

def countRefs(dbConnection):
    sql = "SELECT Count(*) FROM ReferencesData"
    cur = dbConnection.cursor()
    cur.execute(sql)
    refNum = cur.fetchone()
    return refNum[0]

# Checked
def createTempCitationTable(dbConnection):
    """
    Create a table in the database
    """
    sql = ''' CREATE TABLE TempCitation
              (ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, Self TEXT, Cited TEXT, CitedBy TEXT)'''
    cur = dbConnection.cursor()
    cur.execute(sql)
    dbConnection.commit()

# Checked
def deleteTempCitationTable(dbConnection):
    """
    Delete temp citation table from the database
    """
    sql = ''' DROP TABLE TempCitation'''
    cur = dbConnection.cursor()
    cur.execute(sql)
    dbConnection.commit()

def readRefFromDBByDict(dbConnection, refItem1):
    """
    Read one piece of reference from database with reference dictionary
    :param dbConnection: the Connection object
    :param refItem: reference dictionary
    :return:
    """
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM ReferencesData WHERE Title=? AND Authors=? AND Year=?",
                (refItem1['Title'], refItem1['Authors'], refItem1['Year']))
    rows = cur.fetchall()
    refItem2 = {}
    if len(rows) == 1:
        if len(rows[0]) <= len(DatabaseReferenceStructure):
            for i in range(len(rows[0])):
                refItem2[DatabaseReferenceStructure[i]] = rows[0][i]
    return refItem2

# Checked
def writeRefToDB(dbConnection, refDict):
    # Check item existance first
    tempItem = readRefFromDBByDict(dbConnection, refDict)
    if len(tempItem):
        tempItem1 = {}
        tempItem1['Title'] = tempItem['Title']
        tempItem1['Authors'] = tempItem['Authors']
        tempItem1['Year'] = tempItem['Year']
        tempItem2 = {}
        tempItem2['Title'] = refDict['Title']
        tempItem2['Authors'] = refDict['Authors']
        tempItem2['Year'] = refDict['Year']
        if tempItem1 == tempItem2:
            pass
        else:
            # Not exact the same, wait to check by users
            sql = ''' INSERT INTO ReferencesData(Title, Authors, Type, PubIn, Year, Labels, AddedTime)
              VALUES(?,?,?,?,?,?,?) '''
            task = (refDict['Title'], refDict['Authors'], refDict['Type'], refDict['PubIn'], refDict['Year'], refDict['Labels'], refDict['AddedTime'])
            cur = dbConnection.cursor()
            cur.execute(sql, task)
            dbConnection.commit()
    else:
        # Not exist, add to database
        sql = ''' INSERT INTO ReferencesData(Title, Authors, Type, PubIn, Year, Labels, AddedTime)
          VALUES(?,?,?,?,?,?,?) '''
        task = (refDict['Title'], refDict['Authors'], refDict['Type'], refDict['PubIn'], refDict['Year'], refDict['Labels'], refDict['AddedTime'])
        cur = dbConnection.cursor()
        cur.execute(sql, task)
        dbConnection.commit()

# Checked
def writeRefsToDB(dbConnection, refDictList):
    if len(refDictList):
        for refDict in refDictList:
            writeRefToDB(dbConnection, refDict)

# Checked
def readRefFromDBByID(dbConnection, refAbsID):
    """
    Read one piece of reference from database with reference id
    :param dbConnection: the Connection object
    :param refAbsID: reference absolution id
    :return:
    """
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM ReferencesData WHERE id=?", (refAbsID,))
    rows = cur.fetchall()
    refItem = {}
    if len(rows[0]) <= len(DatabaseReferenceStructure):
        for i in range(len(rows[0])):
            refItem[DatabaseReferenceStructure[i]] = rows[0][i]
    return refItem

# Checked
def readRefsFromDBByIDs(dbConnection, refAbsIDList):
    refDictList = []
    for refID in refAbsIDList:
        refItem = readRefFromDBByID(dbConnection, refID)
        refDictList.append(refItem)
    return refDictList

def readAllRefsFromDB(dbConnection):
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM ReferencesData")
    rows = cur.fetchall()
    refItemList = []
    if len(rows):
        for row in rows:
            if len(row) <= len(DatabaseReferenceStructure):
                refItem = {}
                for i in range(len(row)):
                    refItem[DatabaseReferenceStructure[i]] = row[i]
                refItemList.append(refItem)
    return refItemList

def updateRefToDBByID(dbConnection, refAbsID, value):
    sql = ''' UPDATE ReferencesData
              SET Labels = ?
              WHERE id = ?'''
    task = (value, refAbsID)
    cur = dbConnection.cursor()
    cur.execute(sql, task)
    dbConnection.commit()

# Checked
def updateRefFieldToDBByID(dbConnection, refAbsID, field, value):
    sql = ''' UPDATE ReferencesData
              SET ''' + field + ''' = ?
              WHERE id = ?'''
    task = (value, refAbsID)
    cur = dbConnection.cursor()
    cur.execute(sql, task)
    dbConnection.commit()

# Checked
def getLabelsFromDB(dbConnection):
    """
    Get labels from database
    This function will concentrate the labels to a list
    """
    labelRows = readLabelsFromDB(dbConnection)
    labels = list(map(lambda x: x[1], labelRows))
    return labels

# Checked
def readLabelsFromDB(dbConnection):
    """
    Read labels from Labels table of the database
    """
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM Labels")
    rows = cur.fetchall()
    return rows

# Checked
def getCitationsFromDB(dbConnection, refAbsID):
    citationRows = readCitationsFromDB(dbConnection, refAbsID)
    citationListStr = None
    if len(citationRows):
        citations = citationRows[0][2]
        if len(citations):
            try:
                citationListStr = citations.split(",")
            except:
                pass
    return citationListStr

# Checked
def readCitationsFromDB(dbConnection, refAbsID):
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM Citation WHERE Self=?", (refAbsID,))
    rows = cur.fetchall()
    return rows

# Checked
def copyCitationData(dbConnection, refAbsID):
    citationRows = readCitationsFromDB(dbConnection, refAbsID)
    if len(citationRows) > 0:
        cur = dbConnection.cursor()
        cur.execute("SELECT * FROM TempCitation WHERE Self=?", (refAbsID,))
        rows = cur.fetchall()
        if len(rows) == 0:
            sql = ''' INSERT INTO TempCitation(Self, Cited, CitedBy)
                      VALUES(?,?,?) '''
            task = (citationRows[0][1], citationRows[0][2], citationRows[0][3])
            cur = dbConnection.cursor()
            cur.execute(sql, task)
            dbConnection.commit()
        else:
            pass

# Checked
def getTempCitationsFromDB(dbConnection):
    citationRows = readTempCitationsFromDB(dbConnection)
    return citationRows

# Checked
def readTempCitationsFromDB(dbConnection):
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM TempCitation")
    rows = cur.fetchall()
    return rows


if __name__ == "__main__":
    pass
