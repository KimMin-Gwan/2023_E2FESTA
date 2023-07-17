# serv_utf-8.py
"""
* Program Purpose and Features :
* for record
* Author : Juwhan Kim
* First WriJuwhante Date : 2023.07.16
* ==========================================================================
* Program history
* ==========================================================================
* Author    	Date		 Version		History           code to fix
* Juwhan KIM	2023.07.16      v0.10	    make file
* 
"""

## mongodb 에 엑셀 한글도 같이 저장하기 위한 변환 utf-8.py
import pandas as pd

# 엑셀 파일 경로
excel_file = 'C:\\Users\\shp67\\OneDrive\\바탕 화면\\data.xlsx'

# 엑셀 파일을 DataFrame으로 읽어오기
df = pd.read_excel(excel_file)

utf8_file = 'C:\\Users\\shp67\\OneDrive\\바탕 화면\\data.csv'
df.to_csv(utf8_file, encoding='utf-8', index=False)