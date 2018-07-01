import sqlite3
from sqlite3 import Error

from ReferenceStructure import *

# Checked
def createDB(db_path):
    conn = createConnectionToDB(db_path)
    if conn is not None:
        # create projects table
        initTables(conn)
    else:
        print("Error! cannot create the database connection.")

def initTables(dbConnection):
    # Create Article table
    # sql_create_article_table = """ CREATE TABLE IF NOT EXISTS "Article" (
    #                                     `ID` INTEGER NOT NULL PRIMARY KEY UNIQUE,
    #                                     `Title` TEXT NOT NULL,
    #                                     `Author` TEXT,
    #                                     `Type` TEXT NOT NULL,
    #                                     `Journal` TEXT,
    #                                     `Year` INTEGER NOT NULL,
    #                                     `Labels` TEXT,
    #                                     `AddedTime` TEXT NOT NULL
    #                                 ); """
    # print(sql_create_article_table)
    for type in BibTeXTypes:
        tablename = type.capitalize()
        sql_head = " CREATE TABLE IF NOT EXISTS " + "\"" + tablename + "\" ("
        DB_BaseStr = "`ID` INTEGER NOT NULL PRIMARY KEY UNIQUE," \
                   + "`Label` TEXT," \
                   + "`AddedTime` TEXT NOT NULL," \
                   + "`Citekey` TEXT,"
        DB_FieldsStrList = []
        DB_ExtendFieldsStrList = []
        for field in DatabaseStandardStructure[tablename]:
            tempStr = "`" + field + "` TEXT"
            DB_FieldsStrList.append(tempStr)
        for field in DB_ExtendFields:
            tempStr = "`" + field + "` TEXT"
            DB_ExtendFieldsStrList.append(tempStr)
        DB_FieldsStr = ",".join(DB_FieldsStrList + DB_ExtendFieldsStrList)
        sql_tail = "); "
        sql_create_table_expr =  sql_head + DB_BaseStr + DB_FieldsStr + sql_tail
        createTable(dbConnection, sql_create_table_expr)

    # Create Citation table
    sql_create_citation_table = """ CREATE TABLE IF NOT EXISTS "Citation" (
                                        `ID` INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                        `Self` TEXT,
                                        `Cited` TEXT,
                                        `CitedBy` TEXT
                                    ); """
    createTable(dbConnection, sql_create_citation_table)
    # Create Labels table
    sql_create_labels_table = """ CREATE TABLE IF NOT EXISTS "Labels" (
                                        `ID` INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                        `Name` TEXT NOT NULL UNIQUE
                                    ); """
    createTable(dbConnection, sql_create_labels_table)
    # Create PubIn table
    sql_create_pubin_table = """ CREATE TABLE IF NOT EXISTS "PubIn" (
                                        `ID` INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                        `Name` TEXT NOT NULL UNIQUE
                                    ); """
    createTable(dbConnection, sql_create_pubin_table)
    # Create Trash table
    sql_create_trash_table = """ CREATE TABLE IF NOT EXISTS "Trash" (
                                        `ID` INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                        `Title` TEXT NOT NULL UNIQUE
                                    ); """
    createTable(dbConnection, sql_create_trash_table)
    # Create Years table
    sql_create_years_table = """ CREATE TABLE IF NOT EXISTS "Years" (
                                        `ID` INTEGER NOT NULL PRIMARY KEY UNIQUE,
                                        `Year` TEXT NOT NULL UNIQUE
                                    ); """
    createTable(dbConnection, sql_create_years_table)

# Checked
def createTable(dbConnection, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = dbConnection.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


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


def countAllRefsInDB(dbConnection):
    allRefNum = 0
    for type in BibTeXTypes:
        tablename = type.capitalize()
        tempNum = countRefsInTable(dbConnection, tablename)
        allRefNum = allRefNum + tempNum
    return allRefNum

def countRefsInTable(dbConnection, tablename):
    sql = "SELECT Count(*) FROM " + tablename
    cur = dbConnection.cursor()
    cur.execute(sql)
    refNum = cur.fetchone()
    return refNum[0]

# Checked
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

def readAllRefsInDB(dbConnection):
    allRefItemList = []
    for type in BibTeXTypes:
        tablename = type.capitalize()
        tempList = readAllRefsInTable(dbConnection, tablename)
        allRefItemList = allRefItemList + tempList
    return allRefItemList

def readAllRefsInTable(dbConnection, tablename):
    sql = "SELECT * FROM " + tablename
    cur = dbConnection.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    refItemList = []
    tempDBFieldsList = DB_BaseFields + DatabaseStandardStructure[tablename] + DB_ExtendFields
    if len(rows):
        for row in rows:
            if len(row) <= len(tempDBFieldsList):
                refItem = {}
                for i in range(len(row)):
                    refItem[tempDBFieldsList[i]] = row[i]
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
    createDB("Test2.db")
