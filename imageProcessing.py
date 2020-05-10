import cv2
import pytesseract
import os
import pandas as pd

# brew install tesseract
# pip install pytesseract
# pip install opencv-python
# https://github.com/tesseract-ocr/tesseract/wiki

# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Grayscale, Gaussian blur, Otsu's threshold

wbDashSheet = []
for path, subdirs, files in os.walk('../../data/images/in/'):

    for currentDir in subdirs:
        # print(currentDir)
        for file in os.listdir(os.path.join(path,currentDir)):
            dashboard = file.split(".")[0]
            image = cv2.imread(os.path.join(path,currentDir,file))
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3,3), 0)
            thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # Morph open to remove noise and invert image
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
            opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
            invert = 255 - opening

            # Perform text extraction
            data = pytesseract.image_to_string(invert, lang='eng', config='--psm 6')
            # print(data)

            for txt in data.split('\n'):
                if txt and txt != '':
                    wbDashSheet.append([currentDir,dashboard, txt])
                    # print(currentDir,dashboard, txt)
            # cv2.imshow('thresh', thresh)
            # cv2.imshow('opening', opening)
            # cv2.imshow('invert', invert)

        df = pd.DataFrame.from_records(wbDashSheet,columns = ['workbook','dashboard','sheet'])
        df.to_csv(os.path.join(path,currentDir + "_dashboard_sheet.tsv"),header=True,index=False,sep='\t')
