from zipfile import ZipFile

source_file=['C:/Users/shp67/zf_file/source_code.zip',
             'C:/Users/shp67/zf_file/java.zip']
dest_path='C:/Users/shp67/zf_file'

def unzip():	
    # for i in source_file:
    #     final_zip = zipfile.ZipFile(i)
    #     final_zip.extractall(dest_path)
    #     final_zip.close()
    # 위 코드는 압축해제했을 때 파일 이름이 깨져서 아래로 바꿈...
    
    for i in source_file:
        with ZipFile(i, 'r') as zf:
            zipinfo=zf.infolist()

            for member in zipinfo:
                member.filename=member.filename.encode("cp437").decode("euc-kr")
                zf.extract(member,dest_path)

    print('File is unzipped')


if __name__ == "__main__":
    unzip()