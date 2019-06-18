d = {'a':5,
   'b':6,
   'c':{'f':9,
        'g' :{'m':17,
             'n':3}
       }
   }

def flaten(parent,d,mydict):
    for key,value in d.items():
        if isinstance(value,dict):
            if parent != '':
                parent += '.' +key
            else:
                parent = key
                
            flaten(parent,value,mydict)
        else:
            if  parent != '':
                parent += '.' +key 
                mydict[parent] = value
            else:
                mydict[key] = value
    return
    

mydict = {}
parent = ''
flaten(parent,d,mydict)    
print(mydict)
