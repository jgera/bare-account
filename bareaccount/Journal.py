import sqlite3
import pandas as pd
import os

class journal:
    
    def __init__(self, db):
        self.conn = sqlite3.connect(db + '.db')

    def show(self,account):
        try:
            df = pd.read_sql_query("SELECT * FROM {}".format(account), self.conn)
            return df
        except:
            print("no such table")
        
    def getbalance(self,account):
        try:
            cursor = self.conn.execute("SELECT balance FROM {0} WHERE ID = (SELECT MAX(ID)  FROM {0});".format(account))
            return cursor.fetchall()[0][0]
        except:
            return 0
    
    def listAccounts(self):
        c = self.conn.cursor()
        c.execute('SELECT name FROM sqlite_master WHERE type="table"')
        accounts = []
        for a in c.fetchall():
            #print(a[0])
            accounts.append(a[0])
            
        accounts.remove('sqlite_sequence')
        return accounts
    
    def deleteAccount(self,name):
        self.conn.execute('DROP TABLE IF EXISTS {};'.format(name))
        print("Account '{}' deleted.".format(name))
        
    
    def createAccount(self,name,drop=False):
        if name == "":
            print("Account name can't be empty")
            return None
        
        tables = self.conn.execute("SELECT name FROM sqlite_master WHERE name='{}';".format(name))

       
        if len(tables.fetchall()) != 0: 
            if drop == True:
                print("Account '{}' already exists, dropping.".format(name))     
                self.conn.execute('DROP TABLE IF EXISTS {};'.format(name))
            else:
                print("Account '{}' already exists.".format(name))     
                return name       
        
        self.conn.execute('''CREATE TABLE {} (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        credit real not null DEFAULT 0.0,
                                        debit real not null DEFAULT 0.0,
                                        balance real not null ) '''.format(name))
        self.conn.commit()
        print("Account '{}' Created.".format(name))           

        
        return name
           
    def transaction(self,account,credit,debit):
        balance = self.getbalance(account)
        #print("balance: " + str(balance))
        balance= balance+credit-debit
        #print("after balance: " + str(balance))
        tx = (credit,debit,balance)
        q = "INSERT INTO {} (credit,debit,balance) VALUES (?, ?, ? );".format(account)
        self.conn.execute(q,tx)
        self.conn.commit()
        
        cursor = self.conn.execute("SELECT balance FROM {0} WHERE ID = (SELECT MAX(ID)  FROM {0});".format(account))
        
    def close(self):
        self.conn.close()