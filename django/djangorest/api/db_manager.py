"""
Responsible for saving truck cycle informaiton to a persistent store
"""

import pandas
import pyodbc # odbc connection lib 
from matplotlib import pylab
from pylab import *
import numpy as np
import pickle
import os

class SaveSQL(object):
    """
    Parent class to insert records into a database
    # INSERT INTO table (colums) Values (values list), (values list), (values), (values)
    """
    def __init__(self):
        self.connectString = ''
        self.connection = '' # set when used.  The connection is not held open
        self.counter = 0
        self.cursor = ''
        self.insertStmt = ''
        self.values = ''
        self.inf = 1000000  #if a value is inf, it will be replaced with this value
        # Example Insert Statement to be overridden
        #self.insertStmt = (
            #'INSERT INTO [SaveSQLDemo].[dbo].[Cycle]'
            #+',[No Comm duration]'
            #+')     VALUES   '     
            #)
            
    def setConnectString(self, connectString):
        self.connectString = connectString
        

    def setValueString(self,str):
        """Sets the value string that will be appended to the insert string
             (Alternatively, this can be the full insert statement)
        Example:
                str =  ( 
            '( '+str(0) +     #CalendarID, int,>
            ', '+str(0) +     #TimesequenceID, int,>
            ', '+str(0) +     #EquipmentID, int,>
            ', '+"'"+self.runData.serialNo+"'" +     #PHSerialNo, nchar(20),>
            ', '+str(cycle[dig]['duration']/1000.) +     #Dig duration, real,>
            ', '+str(cycle[dig]['entries'])   +  #Dig entries, real,>
            ', '+str(cycle[noComm]['duration']/1000.) + #,<No Comm duration, real,>
            ')')  
        
        """
        self.values = str
     
    def setInsertString(self,str):
        """Set the string that will be prepended to the values
        """
        self.insertStmt = str     
     
    def getValueString(self,cycle):
        """This creates the Values part of the insert statment.
        This is an example to be overridden
        
        """
      

    def insert(self):
        """
        Appends the insertStmt and the values. Then sends this to the database indicated in the insertStmt.
        Also replaces nan, None and inf with appropriate values
        """
        if self.runData.production == True:
            return        
        cursor = self.cursor
        connection = pyodbc.connect(self.connectString, autocommit=True)
          
        cursor = connection.cursor()
            
        self.values = self.values.replace('nan', 'null')
        self.values = self.values.replace(' None', 'null')
        self.values = self.values.replace('inf', str(self.inf))
        
        statement = self.insertStmt + self.values
        if self.runData.production == False:
            print(statement)
            pass
        cursor.execute(statement)
        self.counter +=1
        if self.runData.production == False:
            print('Insert Counter '+ str(self.counter))
            
        cursor.close()
        connection.close() 
        
        
    def readDataPandas(self,  statementLocal):
        connection = pyodbc.connect(self.connectString, autocommit=True)
        
        records = pandas.read_sql(statementLocal, connection)
    
        #cursor = connection.cursor()
    
        #cursor.execute(statementLocal)
        #records = cursor.fetchall()
        #cursor.close()
        connection.close()
    
        return records        
        
    def readData(self,  statementLocal):
      

        connection = pyodbc.connect(self.connectString, autocommit=True)

        cursor = connection.cursor()
 
        cursor.execute(statementLocal)
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        return records
        
    def closeConnection(self):
        self.cursor.commit()
        self.cursor.close()
        self.connection.close() 
        
        
#################################  Test Program ########################################################
if __name__ == '__main__':
    from RunInformation import *
    runData = runInfo('DummyRuleName', 'DummySchedule',
                'ES41217')        
    ImpalaConnect = 'DRIVER={Cloudera ODBC Driver for Impala};HOST=testalarmodbc;PORT=21050'
    
    db = SaveSQL(runData)
    db.setConnectString(ImpalaConnect)
    statement = "select dump_start_ang,dump_start_tooth_extension from dwh.es_cycles where shiftId =25 and cycle_type=1"
    records = db.readData(statement)
