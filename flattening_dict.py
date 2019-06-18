d = {'a':5,
   'b':6,
   'c':{'f':9,
        'g' :{'m':17,
             'n':3}
       },
    'e':77
   }

def flaten(parent,d,mydict):
    
    for key,value in d.items():
        if isinstance(value,dict):
            if parent:
                callParent = parent +'.' +key
            else:
                callParent = key
                
            flaten(callParent,value,mydict)
        else:
            if parent:
                callParent = parent + '.' +key 
                mydict[callParent] = value
            else:
                mydict[key] = value
    return
    

mydict = {}
parent = None
flaten(parent,d,mydict)    
print(mydict)

{'a': 5, 'b': 6, 'c.f': 9, 'c.g.m': 17, 'c.g.n': 3, 'e': 77}
