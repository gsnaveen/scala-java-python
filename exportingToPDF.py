#https://wkhtmltopdf.org/downloads.html
# install and add binary/bin folder to the path
import pandas as pd
import pdfkit as pdf
from jinja2 import Template,FileSystemLoader,Environment
import re,sys,os,json

inputHTMLtemplate =  "inputHTMLFile"
context = {'pic1': './images/pic_trulli'}
jinja_env = Environment(loader=FileSystemLoader('./template/'),trim_blocks=True, lstrip_blocks=True)
template = jinja_env.get_template(inputHTMLtemplate+'.html.j2')
output = template.render(context)
with open(inputHTMLtemplate+".html","+w" ) as fp:
    fp.write(output)
# df = pd.DataFrame.from_records([[1,11,111],[2,22,222]],columns=["fist","second","third"])
# df.to_html('./data/mydf.html')
outPdffile='./data/mydfhtml2.pdf'
pdf.from_file('./data/my.html', outPdffile)
# pdf.from_file(inputHTMLtemplate+ '.html', outPdffile)
