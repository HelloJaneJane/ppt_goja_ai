#-*- coding:utf-8 -*-
from pptx import Presentation
from pptx.util import Pt
import json
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

from server.awsModule import *

class TextData:
    def __init__(self, mainTitle, subTitle, midTitles, slideTitles, slideContents):
        self._mainTitle = mainTitle
        self._subTitle = subTitle
        self._midTitles = midTitles
        self._slideTitles = slideTitles
        self._slideContents = slideContents

    def __print__(self):
        print("---TextData Print---")
        print("제목: " + self._mainTitle)
        print("부제목: " + self._subTitle)
        print("중제목들 : ", end='')
        print(self._midTitles)
        print("슬라이드소제목들: ",end='')
        print(self._slideTitles)
        print("슬라이드내용들: ",end='')
        print(self._slideContents)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, ensure_ascii = False, sort_keys=True, indent=4)


class PPTData:

    def __init__(self, textData):
        self._textData = textData
        # initial value
        self._topic = None
        self._slideTypes = textData._slideContents
        self._basePrs = Presentation()

    # 전체 주제 getter
    @property
    def topic_(self):
        return self._topic

    # 전체 주제 setter
    #@topic.setter
    def topic(self):
        # GPU 서버로 textData를 보내서 NLP 결과를 받아온다
        result = None
        # 결과를 토대로 topic을 선정한다
        self._topic = result

    # # 베이스 테마 파일 getter
    # @property
    def basePrs_(self):
        return self._basePrs

    # # 베이스 테마 파일 setter
    # @basePrs.setter
    def basePrs(self):
        #     # topic에 어울리는 테마의 피피티를 고른다
        if self._topic == "ISW":
#            downloadFileFromS3("basePPT/ISW.pptx","pptEngine/ISW.pptx")
            self._basePrs = Presentation("ISW.pptx")
        else:
            self._basePrs = Presentation("ISW.pptx")

    def newSlide(self, slideType):
        slide = self._basePrs.slides.add_slide(self._basePrs.slide_layouts[slideType])  # ppt 객체, 슬라이드마스터 번호, 제목
        #slide.shapes.title.text = self._textData._mainTitle
        return slide

    # 제목 슬라이드를 만드는 함수
    def titleSlide(self):  # NewSlide, 제목, 부제목
        slide = self.newSlide(0)#2에 제목 넣자
        slide.shapes.placeholders[0].text = self._textData._mainTitle
        slide.shapes.placeholders[10].text = self._textData._subTitle
        return slide


    # 슬라이드 객체의 특정 텍스트박스에 대한 설정
    def setTextBox(self, slide, cnt, fontAdr):  # 슬라이드 객체, 텍스트박스 번호, 폰트주소
        text_box = slide.shapes.placeholders[cnt].text_frame
        p = slide.shapes.add_textbox(1,1,1,1)
        text_box.fit_text(font_file=fontAdr)
        return text_box

    # 텍스트박스 객체에 새로운 텍스트를 추가한다. (줄단위)

    def firstLine(self, textbox, text, font, size):
        #textbox.font.name = font
        #textbox.font.size = Pt(size)
        textbox.text = text
        textbox.alignment = PP_ALIGN.LEFT

    def newLine(self, textbox, text, font, size):  # 텍스트박스 객체, 내용, 폰트, 크기
        line = textbox.add_paragraph()
        line.font.name = font
        line.font.size = Pt(size)
        line.text = text
        line.alignment = PP_ALIGN.LEFT

    def newLine_beauty(self,textbox,text,font,size,bold,rgb,center):
        line = textbox.add_paragraph()
        line.font.name = font
        line.font.size = Pt(size)
        line.text = text
        line.font.color.rgb = RGBColor(rgb[0],rgb[1],rgb[2])
        line.font.bold = bold
        if(center):
            line.alignment = PP_ALIGN.CENTER

    def transitionSlide(self,idx):
        slide = self.newSlide(2)
        text_box = self.setTextBox(slide,0,'pptEngine/static/SangSangTitleM.ttf')
        self.newLine(text_box,self._textData._midTitles[idx],'SangSangTitleM',44)

    def index(self):
        slide = self.newSlide(1)
        text_box = self.setTextBox(slide,0,'pptEngine/static/SangSangTitleM.ttf')
        self.firstLine(text_box,'Contents','SangSangTitleM',32)
        text_box = self.setTextBox(slide, 11, 'pptEngine/static/a타이틀고딕3.ttf')
        pre_idx=0
        self.firstLine(text_box,self._textData._midTitles[0],'a타이틀고딕3',24)
        for sld_title in self._textData._slideTitles:
            if(sld_title[1]>pre_idx):
                pre_idx=sld_title[1]
                self.newLine(text_box,self._textData._midTitles[pre_idx],'a타이틀고딕3',24)
            self.newLine_beauty(text_box, '- '+sld_title[0],'a타이틀고딕3', 18,False,[0xD0,0xFF,0x80],False)

    # ppt를 저장한다.
    def write(self, file_name):
        self._basePrs.save(file_name)

    def input_title(self,slide, title):
        text_box = self.setTextBox(slide, 0, 'pptEngine/static/SangSangTitleM.ttf')
        self.newLine(text_box, title, 'SangSangTitleM', 32)


    def timeMultiLine(self,slide,title,headers,bodies):
        self.input_title(slide,title)
        line_cnt = 13
        for header in headers:
            text_box = self.setTextBox(slide, line_cnt,'pptEngine/static/DOSSaemmul.ttf')
            self.firstLine(text_box,header,'Arial',10)
            line_cnt = line_cnt+2
        line_cnt = 14
        for body in bodies:
            text_box = self.setTextBox(slide, line_cnt, 'pptEngine/static/DOSSaemmul.ttf')
            self.firstLine(text_box, body, 'Arial', 10)
            line_cnt = line_cnt + 2
        return slide

    def defaultLine(self,title,contents):
        slide = self.newSlide(3)
        self.input_title(slide, title)
        text_box = self.setTextBox(slide, 1, 'pptEngine/static/a타이틀고딕3.ttf')
        for line in contents:
            self. newLine(text_box,line,'a타이틀고딕3',20)
        return slide

    def singleLine(self,title,lines):
        slide = self.newSlide(4)
        self.input_title(slide, title)
        text_box = self.setTextBox(slide, 13, 'pptEngine/static/a타이틀고딕3.ttf')
        line = lines[0]
        self.firstLine(text_box, line, 'a타이틀고딕3', 24)
        return slide

    def generate_slide(self, title, slideObj):
        if (isinstance(slideObj,slideType_head_default)):
            contents=[]
            for tuple in slideObj._h5Tuples:
                contents.append(tuple[0])
                contents.append(tuple[1])
            return self.defaultLine(title,contents)
        elif (isinstance(slideObj, slideType_head_timeLine)):
            headers=[]
            bodies=[]
            for tuple in slideObj._h5Tuples:
                headers.append(tuple[0])
                bodies.append(tuple[1])
            slide = self.newSlide(2 + len(bodies) * 2)  # 6th~9th
            return self.timeMultiLine(slide,title,headers,bodies)
        elif (isinstance(slideObj, slideType_head_multiLine)):
            headers = []
            bodies = []
            for tuple in slideObj._h5Tuples:
                headers.append(tuple[0])
                bodies.append(tuple[1])
                print(len(bodies))
            slide = self.newSlide(2 + len(bodies) * 2)  # 6th~9th NOT!! will be changed
            return self.timeMultiLine(slide, title, headers, bodies)
        elif (isinstance(slideObj, slideType_head_timeLine)):
            headers = []
            bodies = []
            for tuple in slideObj._h5Tuples:
                headers.append(tuple[0])
                bodies.append(tuple[1])
            slide = self.newSlide(2 + len(bodies) * 2)  # 6th~9th
            return self.timeMultiLine(slide, title, headers, bodies)
        elif (isinstance(slideObj,slideType_default)):
            return self.defaultLine(title,slideObj._lines)
        elif (isinstance(slideObj,slideType_singleLine)):
            return self.singleLine(title,slideObj._lines)
        elif (isinstance(slideObj, slideType_multiLine)):
            headers = []
            bodies = []
            for line in slideObj._lines:
                bodies.append(line)
            slide = self.newSlide(2 + len(bodies) * 2)  # 6th~9th NOT!! will be changed
            return self.timeMultiLine(slide, title, headers, bodies)
        elif (isinstance(slideObj, slideType_timeLine)):
            headers = []
            bodies = []
            for line in slideObj._lines:
                bodies.append(line)
            slide = self.newSlide(2 + len(bodies) * 2)  # 6th~9th
            return self.timeMultiLine(slide, title, headers, bodies)

        #old functions
        elif (isinstance(slideObj,SlideType_timeline)):  # timeline
            slide = self.newSlide(5)#timeline 5th
            self.input_title(slide,title)

            line_cnt=13
            for tuples in slideObj._timeTuples:
                text_box = self.setTextBox(slide, line_cnt,'pptEngine/static/DOSSaemmul.ttf')
                self.firstLine(text_box, tuples[0], 'Arial', 10)
                text_box = self.setTextBox(slide,line_cnt+4,'pptEngine/static/DOSSaemmul.ttf')
                self.firstLine(text_box, tuples[1], 'DOSSaemmul', 13)
                line_cnt = line_cnt + 1
            return slide

        elif (isinstance(slideObj,SlideType_h5)):
            slide = self.newSlide(6)#h5
            self.input_title(slide, title)
            textbox_cnt= 1
            for tuples in slideObj._h5Tuples:
                text_box = self.setTextBox(slide,textbox_cnt,'pptEngine/static/a타이틀고딕3.ttf')
                self.newLine_beauty(text_box,tuples[0],'a타이틀고딕3',28,True,[0xCC,0xFF,0x33],True)
                for line in tuples[1]:
                    self.newLine(text_box,line,'a타이틀고딕3',20)
                textbox_cnt = textbox_cnt+1

        elif (isinstance(slideObj,slideType_definition)):
            slide = self.newSlide(3)
            self.input_title(slide, title)

            text_box = self.setTextBox(slide,1,'pptEngine/static/a타이틀고딕3.ttf')
            line =slideObj._defStr
            self.firstLine(text_box,line,'a타이틀고딕3',24)

        else:
            slide = self.newSlide(4)
            self.input_title(slide, title)
            text_box = self.setTextBox(slide,1,'pptEngine/static/a타이틀고딕3.ttf')
            line =slideObj._lines[0]
            self.firstLine(text_box,line,'a타이틀고딕3',24)
            return slide

    def generate(self):
        self.basePrs()
        self.titleSlide()
        self.index()
        slide_idx = -1
        mid_slide = -1
        for slide_ in self._slideTypes:
            slide_idx = slide_idx + 1
            if(self._textData._slideTitles[slide_idx][1]>mid_slide):
                mid_slide = mid_slide + 1
                self.transitionSlide(mid_slide)

            self.generate_slide(self._textData._slideTitles[slide_idx][0],slide_)

    def idx_check(self,idx):
        slide = self.newSlide(idx)
        for shape in slide.shapes:
            if shape.is_placeholder:
                phf = shape.placeholder_format
                print('%d,%s'%(phf.idx,phf.type))


def wrap_image(keywords):
    API_KEY = '9550200-7709f1b4e4c3d4b4c800b8188'
    #gmail_KEY
    image = Image(API_KEY)
    ims = image.search(q=keywords,
                       lang='es',
                       image_type='photo',
                       orientation='horizontal',
                       category='animals',
                       safesearch='true',
                       order='latest',
                       page=2,
                       per_page=3)
    print(ims)

# 디폴트 타입
# [String] - 한줄내용
class SlideType:
    def __init__(self, lines):
        self._lines = lines
    def generate(self):

        print('generated')

# 타임라인 타입 (일정, 과정, 단계)
# [(String, String)] - (시간, 한줄내용)
class SlideType_timeline(SlideType):
    def __init__(self, timeTuples):
        self._timeTuples = timeTuples


# h5 타입 (비교대조 등)
# [(String,[String])] - (헤딩,[내용들])
class SlideType_h5(SlideType):
    def __init__(self, h5Tuples):
        self._h5Tuples = h5Tuples
        self._lines = h5Tuples[0][0]


# 정의 타입 (? -> "")
# String
class SlideType_definition(SlideType):
    def __init__(self, defStr):
        self._defStr = defStr

# def slide_test():
#     slides = [SlideType('default'),SlideType_h5([('SWM',['1','2','3']),('SWM',['1','2','3'])])]
#
#     for Sample_sld in slides:
#         Sample_sld.generate()


class slideType_head_default(SlideType):
    def __init__(self, h5Tuples):
        self._h5Tuples = h5Tuples
        self._lines = h5Tuples[0][0]
class slideType_head_timeLine(SlideType):
    def __init__(self, h5Tuples):
        self._h5Tuples = h5Tuples
        self._lines = h5Tuples[0][0]
class slideType_head_multiLine(SlideType):
    def __init__(self, h5Tuples):
        self._h5Tuples = h5Tuples
        self._lines = h5Tuples[0][0]
class slideType_default(SlideType):
    def __init__(self, lines):
        self._lines = lines
class slideType_singleLine(SlideType):#definition
    def __init__(self, lines):
        self._lines = lines
class slideType_timeLine(SlideType):
    def __init__(self, lines):
        self._lines = lines
class slideType_multiLine(SlideType):
    def __init__(self, lines):
        self._lines = lines
