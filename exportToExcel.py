import pdfkit as pdf
import pandas as pd
import numpy as np
import os

import xlwt
from xlwt.Workbook import *
from pandas import ExcelWriter


basePathDestinationFolder = "C:/Users/Box/users/"
jinja_env = Environment(loader=FileSystemLoader('./template/'), trim_blocks=True, lstrip_blocks=True)

df = pd.read_csv("./data/weekly_avg_interest_score.csv",sep=",",header=0)
dfdetail = pd.read_csv("./data/topic_IntensityScore.csv",sep=",",header=0)

for customer_id in df["customer_id"].unique():
    dfPlot = df[df["customer_id"] == customer_id].reset_index()
    sav_name = dfPlot['customer_name'].iloc[0]
    salesp_email = dfPlot['email'].iloc[0]
    salesp_name = dfPlot['full_name'].iloc[0]

    writer = pd.ExcelWriter('./excel/'+sav_name + '.xlsx', engine='xlsxwriter')

    dfavg = pd.DataFrame(data=[list(dfPlot["avg_interest_score"])], columns=list(dfPlot["create_date"]))
    dfavg.to_excel(writer, sheet_name="mainSheet", startrow=0, startcol=0, index=False)

    dfdetailPlot =  dfdetail[dfdetail["customer_id"] == customer_id]
    rowsindfdetailPlot = len(dfdetailPlot)
    dfdetailPlot.index = np.arange(1, rowsindfdetailPlot + 1)
    dfdetailPlot.columns = ["col1","col2","col3","latest","SevenDaysOut","forteenDaysOut","twentyOnedaysOut"] 
    dfdetailPlot[["col1","col2","col3","latest","SevenDaysOut","forteenDaysOut","twentyOnedaysOut"]].to_excel(writer, sheet_name="mainSheet", startrow=5, startcol=0, index=False)
    writer.save()
