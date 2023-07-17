## mongodb 에 엑셀 한글도 같이 저장하기 위한 변환 utf-8.py
import pandas as pd

# 엑셀 파일 경로
excel_file = 'C:\\Users\\maths\\Desktop\\엑셀 data\\DATA_TEMP.xlsx'

# 엑셀 파일을 DataFrame으로 읽어오기
df = pd.read_excel(excel_file)

utf8_file = 'C:\\Users\\maths\\Desktop\\엑셀 data\\data_temp.csv'
df.to_csv(utf8_file, encoding='utf-8', index=False)