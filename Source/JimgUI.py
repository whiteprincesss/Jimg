from tkinter import *

# GUI 함수
def search_img():
    keyword = search_box.get()
    print(keyword=="")

downloder = Tk()
downloder.geometry('580x780+700+100')
downloder.title('JIMG')

# 메뉴

# 검색 UI
search_box = Entry(downloder, width=47)
search_box.place(x=90,y=20)
search_btn = Button(downloder, text='Search', command=search_img).place(x=430,y=20)

# 모델 선택

# 분류 기준 선택

# 파일 확장자 선택

downloder.mainloop()