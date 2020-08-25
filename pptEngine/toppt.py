#-*- coding:utf-8 -*-
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_THEME_COLOR
from pptx.util import Pt
from PyPPTModule2 import *
#from PyPPTModule import *
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
    slides = [SlideType_definition('창의도전형 SW인재 육성으로 SW산업의 미래를 선도하는 정부 지원 사업!')
        , SlideType(['5951명 지원 856명의 연수생 배출 현재 11기 150명의 연수생이 소프트웨어 산업의 리더를 꿈꾸며 역량을 키우고 있습니다.'])
        , SlideType_timeline([('4월','합격자발표'),('5월','교육준비 및 발대식'),('6-11월','본과정'),('12월','최종평가 및 인증자 선발')])
        , SlideType_h5([('BoB', ['국가 지원 사업', '소프트웨어 맴버십 활동', '개인활동 위주의 활동', '보안리더를 양성']), ('SWMaestro', ['국가 지원 사업', '소프트웨어 맴버십 활동', '팀 단위의 프로젝트 활동', '한국의 스티브잡스를 양성'])])]
    sample_text = TextData('SW Maestro 오리엔테이션','세상을 움직이는 최고급 SW 인재양성의 메카', ['소프트웨어 마에스트로 란', '소프트웨어 대외활동 비교'], [('SW Maestro?', 0), ('경쟁률 추이', 0), ('프로그램 일정', 0), ('BoB VS SWMaestro', 1)],slides)

    sample = PPTData(sample_text)
    #sample.basePrs()
    #slide_master = sample._basePrs.slide_masters(
    #slide_master[2].shape.add_text
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


def tmp():
    slides = [SlideType_definition('창의도전형 SW인재 육성으로 SW산업의 미래를 선도하는 정부 지원 사업!')
        , SlideType(['5951명 지원 856명의 연수생 배출 현재 11기 150명의 연수생이 소프트웨어 산업의 리더를 꿈꾸며 역량을 키우고 있습니다.'])
        , SlideType_timeline([('4월','합격자발표'),('5월','교육준비 및 발대식'),('6-11월','본과정'),('12월','최종평가 및 인증자 선발')])
        , SlideType_h5([('BoB', ['국가 지원 사업', '소프트웨어 맴버십 활동', '개인활동 위주의 활동', '보안리더를 양성']), ('SWMaestro', ['국가 지원 사업', '소프트웨어 맴버십 활동', '팀 단위의 프로젝트 활동', '한국의 스티브잡스를 양성'])])]
    sample_text = TextData('SW Maestro 오리엔테이션','세상을 움직이는 최고급 SW 인재양성의 메카', ['소프트웨어 마에스트로 란', '소프트웨어 대외활동 비교'], [('SW Maestro?', 0), ('경쟁률 추이', 0), ('프로그램 일정', 0), ('BoB VS SWMaestro', 1)],slides)

    sample = PPTData(sample_text)
    sample._basePrs = Presentation('ISW.pptx')
    for i in range(0,10):
        sample.idx_check(i)
        print('-----')


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    test2()
    #tmp()
    #wiki_test()
