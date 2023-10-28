my_bytes = b'Hello, World!'
search_bytes = b'o'  # 찾을 문자
if search_bytes in my_bytes:
    print("찾았습니다.")
else:
    print("찾지 못했습니다.")