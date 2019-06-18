d = {'a':5,
   'b':6,
   'c':{'f':9,
        'g' :{'m':17,
             'n':3}
       },
    'e':77
   }

def flatten(parent,d,mydict):
    
    for key,value in d.items():
        
        if parent:
            callParent = parent +'.' +key
        else:
            callParent = key
            
        if isinstance(value,dict):
            flatten(callParent,value,mydict)
        else:
              mydict[callParent] = value

    return
    

mydict = {}
parent = None
flatten(parent,d,mydict)    
print(mydict)
{'a': 5, 'b': 6, 'c.f': 9, 'c.g.m': 17, 'c.g.n': 3, 'e': 77}
