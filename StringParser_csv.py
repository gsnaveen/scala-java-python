def parse(line):
    output = []
    mystring = ""
    ActiveQuote = False
    output.append("START")
    for char in line:
        if ActiveQuote == False and char == "'":
            ActiveQuote = True
        elif ActiveQuote == True and char == "'":
            ActiveQuote = False
        elif char == ',' and ActiveQuote != True :
            output.append(mystring)
            mystring = ""
        else:
             mystring += char
    else:
        output.append(mystring)
        output.append("END")
        
    return output

myString = "Hello,World"
myString = "'this',is,'good,bad'"

parse(myString)
