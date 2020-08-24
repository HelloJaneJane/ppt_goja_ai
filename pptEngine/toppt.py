#-*- coding:utf-8 -*-
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Pt
from PyPPTModule2 import *
from PyPPTModule import *
import wikipediaapi
import wikipedia
import wptools
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

def test2():
    sample_text = TextData('메인 타이투를','서부 타이투를',['미드타이틀1','미드타이틀2'],['슬라이드타이틀1','슬라이드타이틀2','슬라이드타이틀3','슬라이드타이틀4'])
    slides = [SlideType(['default']), SlideType_h5([('SWM', ['1', '2', '3']), ('BOB', ['1', '2', '3'])])]

    sample = PPTData(sample_text,slides)
    #sample.basePrs()

    #sample.titleSlide()
    sample.generate()
    sample.write('first_sample.pptx')

def slide_test():
    slides = [SlideType(['default']),SlideType_h5([('SWM',['1','2','3']),('SWM',['1','2','3'])])]

    for Sample_sld in slides:
        Sample_sld.generate()
def wiki_test():
    #wiki = wikipediaapi.Wikipedia('ko')
    #page_py = wiki.page
    #page_py = wiki.page('파이썬')
    #wikipage = wikipedia.page('kakao')
    #print(wikipage.images[0])
    #print(page_py.images[0])
    #print("Page - Exists: %s" % page_py.exists())
    #print("Page - Summary: %s" % page_py.summary[0:100])
    kr = wptools.page(lang='ko', action='kakao').get_query()
    kakao = wptools.page('kakao').get_query()
    kakao_img = kakao.pageimage
    print(kakao_img)
if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    test2()
    #wiki_test()
