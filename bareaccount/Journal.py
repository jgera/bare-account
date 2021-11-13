import sqlite3
import pandas as pd
import os

class journal:
    
    def __init__(self, db):
        self.conn = sqlite3.connect(db + '.db')

    def show(self,journal):
        try:
            df = pd.read_sql_query("SELECT * FROM {}".format(journal), self.conn)
            return df
        except:
            print("no such journal")
        
    def getbalance(self,journal):
        try:
            cursor = self.conn.execute("SELECT balance FROM {0} WHERE ID = (SELECT MAX(ID)  FROM {0});".format(journal))
            return cursor.fetchall()[0][0]
        except:
            return 0
    
    def listJournals(self):
        c = self.conn.cursor()
        c.execute('SELECT name FROM sqlite_master WHERE type="table"')
        journals = []
        for a in c.fetchall():
            #print(a[0])
            journals.append(a[0])
            
        journals.remove('sqlite_sequence')
        return journals
    
    def deleteJournal(self,name):
        self.conn.execute('DROP TABLE IF EXISTS {};'.format(name))
        print("Journal '{}' deleted.".format(name))
        
    
    def createJournal(self,name,drop=False):
        if name == "":
            print("Journal name can't be empty")
            return None
        
        tables = self.conn.execute("SELECT name FROM sqlite_master WHERE name='{}';".format(name))

       
        if len(tables.fetchall()) != 0: 
            if drop == True:
                print("Journal '{}' already exists, dropping.".format(name))     
                self.conn.execute('DROP TABLE IF EXISTS {};'.format(name))
            else:
                print("Journal '{}' already exists.".format(name))     
                return name       
        
        self.conn.execute('''CREATE TABLE {} (ID INTEGER PRIMARY KEY AUTOINCREMENT, 
                                        credit real not null DEFAULT 0.0,
                                        debit real not null DEFAULT 0.0,
                                        balance real not null ) '''.format(name))
        self.conn.commit()
        print("Journal '{}' Created.".format(name))           

        
        return name

    def clear(self,journal,reset=True):
        self.conn.execute('DELETE FROM {};'.format(journal))
        self.conn.commit()
        print("Journal '{}' cleared.".format(journal))
        #sql reset id to 0
        if reset == True:
            self.conn.execute('delete from sqlite_sequence where name="{}";'.format(journal)) 
        self.conn.commit()
        
    def history(self,journal):
        df = pd.read_sql_query("SELECT * FROM {}".format(journal), self.conn)
        return df


    def transaction(self,journal,credit,debit):
        balance = self.getbalance(journal)
        #print("balance: " + str(balance))
        balance= balance+credit-debit
        #print("after balance: " + str(balance))
        tx = (credit,debit,balance)
        q = "INSERT INTO {} (credit,debit,balance) VALUES (?, ?, ? );".format(journal)
        self.conn.execute(q,tx)
        self.conn.commit()
        
        cursor = self.conn.execute("SELECT balance FROM {0} WHERE ID = (SELECT MAX(ID)  FROM {0});".format(journal))
        
    def close(self):
        self.conn.close()