import pandas as pd

# 엑셀 파일 경로
excel_file = 'C:\\Users\\maths\\Desktop\\엑셀 data\\data.xlsx'

# 엑셀 파일을 DataFrame으로 읽어오기
df = pd.read_excel(excel_file)

utf8_file = 'C:\\Users\\maths\\Desktop\\엑셀 data\\file.csv'
df.to_csv(utf8_file, encoding='utf-8', index=False)