import sqlite3
from sqlite3 import Error

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

def writeRefToDB(dbConnection, refDict):
    sql = ''' INSERT INTO ReferencesData(Title, Authors, Type, PubIn, Year, Labels)
              VALUES(?,?,?,?,?,?) '''
    task = (refDict['Title'], refDict['Authors'], refDict['Type'], refDict['PubIn'], refDict['Year'], refDict['Labels'])
    #print(refDict)
    #print(task)
    cur = dbConnection.cursor()
    cur.execute(sql, task)
    dbConnection.commit()

def writeRefsToDB(dbConnection, refDictList):
    pass

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
    return rows

def readRefsFromDBByIDs(dbConnection, refAbsIDList):
    pass

def readAllRefsFromDB(dbConnection):
    cur = dbConnection.cursor()
    cur.execute("SELECT * FROM ReferencesData")
    rows = cur.fetchall()
    return rows

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

if __name__ == "__main__":
    pass