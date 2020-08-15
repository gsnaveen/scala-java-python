import io
import pandas as pd

#Saving dataframe to a memory variable
def getJsonDataFrame(inDF):
    # The Web API wrapper
    buffer = io.StringIO()
    inDF.to_json(buffer, orient='records')
    output = buffer.getvalue()
    buffer.close()
    output = json.loads(output)
    # print(output[0])
    # outString = jsonify(output)
    return output
