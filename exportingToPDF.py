
import pdfkit as pdf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jinja2 import Template,FileSystemLoader,Environment
import os
basePathDestinationFolder = "C:/Users/Box/users/"
jinja_env = Environment(loader=FileSystemLoader('./template/'), trim_blocks=True, lstrip_blocks=True)
inputHTMLtemplate =  "inputHTMLFile"
template = jinja_env.get_template(inputHTMLtemplate + '.html.j2')

df = pd.read_csv("./data/inputData.csv",sep=",",header=0)
df["sav_id_s"] = df["sav_id_s"].astype(str)


for email in df["email"].unique():
    dfPlot = df[df["email"] == email].reset_index()
    fullName = dfPlot['full_name'].iloc[0]
    # print(fullName)
    dfPlot.index = np.arange(1, len(dfPlot) + 1)

    savs = list(dfPlot["sav_id_s"])
    thescore = list(dfPlot["theScore"])
    plt.plot(savs, thescore, color='g')
    # plt.xticks(savs, rotation='vertical')
    plt.xticks(rotation=75)
    # plt.tight_layout()
    plt.gcf().subplots_adjust(bottom=0.20)
    plt.xlabel('SavIDs')
    plt.ylabel('Surge Score')
    plt.title('Surge Score Chart for ' + fullName)
    # plt.show()
    plt.savefig("./images/"+ email+'.jpg')
    dfPlot[["id","Node_Level_3","Node_Level_4","theScore"]].to_html("./datadf/"+ email + ".html") #,index=False
    plt.close()

    # Working on the template and pdf
    context = {'pic1': '../images/' + email ,'dataframe' :'../datadf/' + email ,'SalesPersonName' : fullName}
    output = template.render(context)
    # print(output)
    outHtml = "./thtml/"+email + ".html"
    with open(outHtml, "+w") as fp:
        fp.write(output)
    outPdf = './pdf/' + email+ '.pdf'
    # pdf.from_file(outHtml, outPdf)
    dirtoCheck = basePathDestinationFolder + email + "/"
    if not os.path.exists(dirtoCheck):
        os.makedirs(dirtoCheck)

    pdf.from_file(outHtml, dirtoCheck + email+'.pdf')
