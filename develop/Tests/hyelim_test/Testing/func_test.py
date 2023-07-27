class 저녁메뉴():
    def __init__(self):
        self.테마 = ['한식', '중식', '일식', '양식', '아시안']
        
    def printmember(self):
        print(self.테마)
        
    def ChangeTheme(self, 바꿀테마):
        self.테마[4] = 바꿀테마

def main():    
    저녁밥 = 저녁메뉴()
    저녁밥.printmember()
    
    저녁밥.ChangeTheme('패스트푸드')
    저녁밥.printmember()


if __name__ == "__main__":
    main()

# 다른 파일
"""
from func_test import 저녁메뉴 as 뫄뫄  # 하면 받아와짐 ~!

hi = 뫄뫄()
hi.printmember()
"""

exit()

def 덧셈뺄셈(num1, num2):
    sum1 = num1 + num2
    sum2 = num1 - num2
    
    return sum1, sum2

def main():
    num1 = 2
    num2 = 3
    
    result1, result2 = 덧셈뺄셈(num1, num2)
    
    print("덧셈: ", result1)
    print("뺄셈: ", result2)
    
if __name__ == "__main__":
    main()