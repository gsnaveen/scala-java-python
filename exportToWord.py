from mailmerge import MailMerge
from datetime import date

template = "./template/word1_temp.docx"
template_rec = "./template/word1_rec_temp.docx"
# document = MailMerge(template)
document_Multi = MailMerge(template)
# print(document.get_merge_fields())

myDict = {22222:"222244444",
          33333:"333366666"}
myList = []
for key in myDict:
    document = MailMerge(template)
    document.merge(
        cust_id=str(key),
        cust_name=myDict[key])
    myList.append( {"cust_id" :str(key),  "cust_name" : myDict[key]})
    document.write('./word/'+myDict[key]+'.docx')
# for key in myDict:
document_Multi.merge_pages(myList)
document_Multi.write('./word/combined.docx')

document_rec = MailMerge(template_rec)
document_rec.merge_rows('cust_id', myList)
document_rec.write('./word/combined_rec.docx')

document_test = MailMerge('./template/word1_test.docx')
print(document_test.get_merge_fields())
