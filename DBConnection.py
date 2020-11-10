import pymysql

class DBConnection:

    hostName = "localhost"
    userName = "root"
    userPassword="root"
    dbName="moon"
    db = None


    #   def __init__(self):
    #       self.hostName = hostName
    #       self.userName = userName
    #       self.userPassword = userPassword
    #       self.dbName = dbName

    def openDB(self):
        self.db = pymysql.connect(self.hostName,self.userName, self.userPassword, self.dbName)
        return self.db.cursor()
    def openDB2(self):
        self.db = pymysql.connect(self.hostName,self.userName, self.userPassword, self.dbName,cursorclass = pymysql.cursors.DictCursor)
        return self.db.cursor()

    def closeDB(self):
        self.db.close()

    def commitSQL(self):
        self.db.commit()
