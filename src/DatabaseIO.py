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
                   + "`RefAbsID` INTEGER NOT NULL," \
                   + "`Labels` TEXT," \
                   + "`AddedTime` TEXT NOT NULL," \
                   + "`Citekey` TEXT," \
                   + "`Flags` TEXT," \
                   + "`Attachments` TEXT," \
                   + "`Links` TEXT,"
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
    tablename = refItem1['MType']
    sql = "SELECT * FROM " + tablename + " WHERE title=? AND author=? AND year=?"
    cur = dbConnection.cursor()
    cur.execute(sql, (refItem1['title'], refItem1['author'], refItem1['year']))
    rows = cur.fetchall()
    refItem2 = {}
    tempDBFieldsList = DB_BaseFields + DatabaseStandardStructure[tablename] + DB_ExtendFields
    if len(rows) >= 1:
        if len(rows[0]) <= len(tempDBFieldsList):
            for i in range(len(rows[0])):
                refItem2[tempDBFieldsList[i]] = rows[0][i]

    return refItem2

# Checked
def writeRefToDB(dbConnection, refDict):
    # Check item existance first
    tempItem = readRefFromDBByDict(dbConnection, refDict)
    if len(tempItem):
        tempItem1 = {}
        tempItem1['title'] = tempItem['title']
        tempItem1['author'] = tempItem['author']
        tempItem1['year'] = tempItem['year']
        tempItem2 = {}
        tempItem2['title'] = refDict['title']
        tempItem2['author'] = refDict['author']
        tempItem2['year'] = refDict['year']
        if tempItem1 == tempItem2:
            pass
        else:
            # Not exact the same, wait to check by users
            tablename = refDict['MType']
            tempDBFieldsList = DB_BaseFields + DatabaseStandardStructure[tablename] + DB_ExtendFields
            sql = "INSERT INTO " + tablename + "(" + ",".join(tempDBFieldsList[1:]) + ") VALUES(" + ",".join(["?"]*len(tempDBFieldsList[1:])) + ")"
            task = ()
            for field in tempDBFieldsList[1:]:
                task = task + (refDict[field],)
            cur = dbConnection.cursor()
            cur.execute(sql, task)
            dbConnection.commit()
    else:
        # Not exist, add to database
        tablename = refDict['MType']
        tempDBFieldsList = DB_BaseFields + DatabaseStandardStructure[tablename] + DB_ExtendFields
        sql = "INSERT INTO " + tablename + "(" + ",".join(tempDBFieldsList[1:]) + ") VALUES(" + ",".join(["?"]*len(tempDBFieldsList[1:])) + ")"
        task = ()
        for field in tempDBFieldsList[1:]:
            task = task + (refDict[field],)
        cur = dbConnection.cursor()
        cur.execute(sql, task)
        dbConnection.commit()

# Checked
def writeRefsToDB(dbConnection, refDictList):
    if len(refDictList):
        for refDict in refDictList:
            writeRefToDB(dbConnection, refDict)
            updateRefAbsID(dbConnection, refDict)

def updateRefAbsID(dbConnection, refDict):
    tempItem = readRefFromDBByDict(dbConnection, refDict)
    tablename = refDict['MType']
    sql = "UPDATE " + tablename + " SET  RefAbsID= ? WHERE id = ?"
    refAbsID = int(str(DB_TypeCode[tablename])+str(tempItem['ID']).zfill(8))
    task = (refAbsID, tempItem['ID'])
    cur = dbConnection.cursor()
    cur.execute(sql, task)
    dbConnection.commit()

def readRefInDBTableByID(dbConnection, refType, refAbsID):
    tablename = refType
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM " + tablename +" WHERE RefAbsID=?", (refAbsID,))
    rows = cur.fetchall()
    refItem = {}
    tempDBFieldsList = DB_BaseFields + DatabaseStandardStructure[refType] + DB_ExtendFields
    row = rows[0]
    refItem = DB2Dict(rows, tablename)[0]
    return refItem

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

def readAllRecentInDB(dbConnection, timeStr):
    allRefItemList = []
    for type in BibTeXTypes:
        tablename = type.capitalize()
        tempList = readRecentInTable(dbConnection, tablename, timeStr)
        allRefItemList = allRefItemList + tempList
    return allRefItemList


def readRecentInTable(dbConnection, tablename, timeStr):
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM " + tablename + " WHERE AddedTime>?", (timeStr,))
    rows = cur.fetchall()
    refItemList = DB2Dict(rows, tablename)
    return refItemList

def DB2Dict(dbRows, tablename):
    refItemList = []
    tempDBFieldsList = DB_BaseFields + DatabaseStandardStructure[tablename] + DB_ExtendFields
    if len(dbRows):
        for row in dbRows:
            if len(row) <= len(tempDBFieldsList):
                refItem = {}
                refItem['MType'] = tablename
                refItem['PubIn'] = ""
                baseLength = len(DB_BaseFields)
                for i in range(baseLength):
                    refItem[DB_BaseFields[i]] = row[i]

                for i in range(baseLength, len(row)):
                    tempFieldName = tempDBFieldsList[i].capitalize()
                    if tempFieldName == 'Journal':
                        tempFieldName = 'PubIn'
                    elif tempFieldName == 'Booktitle':
                        tempFieldName = 'PubIn'
                    refItem[tempFieldName] = row[i]
                    if row[i] is None:
                        refItem[tempFieldName] = ""
                refItemList.append(refItem)
    return refItemList

def readAllRefsInDBByField(dbConnection, fieldList, keywordList):
    allRefItemList = []
    for type in BibTeXTypes:
        tablename = type.capitalize()
        tempList = readAllRefsInTableByField(dbConnection, tablename, fieldList, keywordList)
        allRefItemList = allRefItemList + tempList
    return allRefItemList

def readAllRefsInTableByField(dbConnection, tablename, fieldList, keywordList):
    checkFlag = False
    tempFieldList = list(fieldList)
    if 'PubIn' not in fieldList:
        checkFlag = True
    else:
        tempInd = tempFieldList.index('PubIn')
        if tablename == 'Article':
            tempFieldList[tempInd] = 'journal'
            checkFlag = True
        elif tablename == 'Conference':
            tempFieldList[tempInd] = 'booktitle'
            checkFlag = True

    refItemList = []
    if checkFlag:
        sql = "SELECT * FROM " + tablename + " WHERE "
        if len(fieldList) == 1:
            sql = sql + tempFieldList[0] + "=?"
            cur = dbConnection.cursor()
            cur.execute(sql, (keywordList[0],))
        elif len(fieldList) == 2:
            sql = sql + tempFieldList[0] + "=? AND " + tempFieldList[1] + "=?"
            cur = dbConnection.cursor()
            cur.execute(sql, (keywordList[0],keywordList[1]))

        rows = cur.fetchall()
        refItemList = DB2Dict(rows, tablename)
    return refItemList

def readAllRefsInDBByLabelPartialMatch(dbConnection, keyword):
    allRefItemList = []
    for type in BibTeXTypes:
        tablename = type.capitalize()
        tempList = readAllRefsInTableByLabelPartialMatch(dbConnection, tablename, keyword)
        allRefItemList = allRefItemList + tempList
    return allRefItemList

def readAllRefsInTableByLabelPartialMatch(dbConnection, tablename, keyword):
    refItemList = []
    sql = '''SELECT * FROM ''' + tablename + ''' WHERE Labels LIKE "%''' + keyword + '''%"'''
    cur = dbConnection.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    if len(rows) > 0:
        refItemList = DB2Dict(rows, tablename)
    return refItemList


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
    # tempDBFieldsList = DB_BaseFields + DatabaseStandardStructure[tablename] + DB_ExtendFields
    if len(rows):
        refItemList = DB2Dict(rows, tablename)
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

# New
def updateRefLabelByID(dbConnection, tablename, refAbsID, value):
    sql = ''' UPDATE ''' + tablename + '''
              SET Labels = ?
              WHERE RefAbsID = ?'''
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

def addLabelToLabelsTable(dbConnection, labelText):
    tempLabelList = getLabelsFromDB(dbConnection)
    if labelText not in tempLabelList:
        sql = ''' INSERT INTO Labels(Name)
                  VALUES(?) '''
        task = (labelText,)
        cur = dbConnection.cursor()
        cur.execute(sql, task)
        dbConnection.commit()

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

def UpdateDatabase(dbConnection):
    indexYearsInDB(dbConnection)
    indexPubInDB(dbConnection)


def indexYearsInDB(dbConnection):
    allYearList = []
    for type in BibTeXTypes:
        tablename = type.capitalize()
        tempYearList = indexYearsInTable(dbConnection, tablename)
        allYearList = allYearList + tempYearList
    allYearList = list(set(allYearList))
    allYearList.sort()
    updateYearsTable(dbConnection, allYearList)

def updateYearsTable(dbConnection, yearList):
    cur = dbConnection.cursor()
    cur.execute("DELETE FROM Years")
    for year in yearList:
        sql = "INSERT INTO Years (Year) VALUES(?)"
        cur = dbConnection.cursor()
        cur.execute(sql, (year,))
        dbConnection.commit()

def indexYearsInTable(dbConnection, tablename):
    cur = dbConnection.cursor()
    cur.execute("SELECT GROUP_CONCAT(Year, ',') FROM " + tablename)
    tempValue = cur.fetchone()
    yearList = []
    if len(tempValue):
        if tempValue[0] is None:
            pass
        else:
            yearList = tempValue[0].split(',')
    return yearList

def indexPubInDB(dbConnection):
    allPubInList = []
    for type in BibTeXTypes:
        tablename = type.capitalize()
        tempPubInList = indexPubInTable(dbConnection, tablename)
        allPubInList = allPubInList + tempPubInList
    allPubInList = list(set(allPubInList))
    allPubInList.sort()
    updatePubInTable(dbConnection, allPubInList)

def updatePubInTable(dbConnection, pubInList):
    cur = dbConnection.cursor()
    cur.execute("DELETE FROM PubIn")
    for pubin in pubInList:
        sql = "INSERT INTO PubIn (Name) VALUES(?)"
        cur = dbConnection.cursor()
        cur.execute(sql, (pubin,))
        dbConnection.commit()

def indexPubInTable(dbConnection, tablename):
    fieldname = ""
    if tablename == 'Article':
        fieldname = 'journal'
    elif tablename == 'Conference':
        fieldname = 'booktitle'
    elif tablename == 'Inproceedings':
        fieldname = 'booktitle'
    pubInList = []
    if len(fieldname)>0:
        sql = "SELECT GROUP_CONCAT(" + fieldname + ", ';') FROM " + tablename
        cur = dbConnection.cursor()
        cur.execute(sql)
        tempValue = cur.fetchone()
        if len(tempValue):
            if tempValue[0] is None:
                pass
            else:
                pubInList = tempValue[0].split(';')
    return pubInList

if __name__ == "__main__":
    createDB("Test.db")
