from tableausdk import *
from tableausdk.Server import * 
from tableausdk.Extract import *
import tableausdk.Extract as tde

#Define a new tde file.
tdefile = tde.Extract('test1.tde')

#Defining a new data set/ table defination in tde
tableDef = tde.TableDefinition()
tableDef.addColumn("company", 15)   #INTEGER
tableDef.addColumn("projected", 10) #DOUBLE
tableDef.addColumn("realRev", 10) #DOUBLE
    
#Let's add dataset to the file

tabletran = tdefile.addTable("Extract",tableDef) 
  
#Create new Row 
newrow = tde.Row(tableDef)
# Adding data value
newrow.setCharString(0,'myCompany')
newrow.setDouble(1,1000)
newrow.setDouble(2,888)
# adding new row to the dataset
tabletran.insert(newrow)

#Create new Row
newrow = tde.Row(tableDef)
newrow.setCharString(0,'myCompany2')
newrow.setDouble(1,1000)
newrow.setDouble(2,777)
# adding new row to the dataset
tabletran.insert(newrow)

#Closing the file
tdefile.close()
