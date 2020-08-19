#-*- coding:utf-8 -*-
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Pt
from PyPPTModule import *
def layout():
    #입력값으로 시작
    prs,f=Start('input.txt')

    #제목 슬라이드
    slide = TitleSlide(prs,0,f.readline(),f.readline())

    for line in f:
        #개행문자 입력시 슬라이드 추가
        if(line == '\n'):
            slide = NewSlide(prs, 1,f.readline())
            tf = SetTextBox(slide, 1, ".\DOSSaemmul.ttf")
            continue
        #아니면 텍스트 추가
        NewLine(tf,line,"DOSSaemmul",18)
        NewLine(tf,"개잘되지롱","Arial",10)

    #저장
    write(prs,'output.pptx')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    layout()