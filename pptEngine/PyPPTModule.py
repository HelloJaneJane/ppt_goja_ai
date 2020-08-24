#-*- coding:utf-8 -*-
from pptx import Presentation
from pptx.util import Pt

class TextData:
    def __init__(self, mainTitle, subTitle, midTitles, slideTitles):
        self._mainTitle = mainTitle
        self._subTitle = subTitle
        self._midTitles = midTitles
        self._slideTitles = slideTitles

    def __print__(self):
        print("제목: " + self._mainTitle)
        print("부제목: " + self._subTitle)
        print("중제목들 : ", end='')
        print(self._midTitles)
        print("소제목들: ", end='')
        print(self._slideTitles)


class PPTData:

    def __init__(self, textData, slideTypes):
        self._textData = textData
        # initial value
        self._topic = None
        self._slideTypes = slideTypes
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
            self._basePrs = Presentation("ISW.pptx")
        else:
            self._basePrs = Presentation("ISW.pptx")

    def newSlide(self, slideType):
        slide = self._basePrs.slides.add_slide(self._basePrs.slide_layouts[slideType])  # ppt 객체, 슬라이드마스터 번호, 제목
        #slide.shapes.title.text = self._textData._mainTitle
        return slide

    # 제목 슬라이드를 만드는 함수
    def titleSlide(self):  # NewSlide, 제목, 부제목
        slide = self.newSlide(1)
        slide.shapes.placeholders[1].text = self._textData._mainTitle
        return slide

    # 슬라이드 객체의 특정 텍스트박스에 대한 설정
    def setTextBox(self, slide, cnt, fontAdr):  # 슬라이드 객체, 텍스트박스 번호, 폰트주소
        text_box = slide.shapes.placeholders[cnt].text_frame
        text_box.fit_text(font_file=fontAdr)
        return text_box

    # 텍스트박스 객체에 새로운 텍스트를 추가한다. (줄단위)
    def newLine(self, textbox, text, font, size):  # 텍스트박스 객체, 내용, 폰트, 크기
        line = textbox.add_paragraph()
        line.font.name = font
        line.font.size = Pt(size)
        line.text = text

    # ppt를 저장한다.
    def write(self, file_name):
        self._basePrs.save(file_name)

    def generate_slide(self, slideObj):
        if (isinstance(slideObj,SlideType_timeline)):  # timeline
            slide = self.newSlide(0)#timeline
            text_box = self.setTextBox(slide, 1, '.\DOSSaemmul.ttf')
            line_cnt=1
            for tuples in slideObj.timeTuples:
                text_box = self.setTextBox(slide, line_cnt,'.\DOSSaemmul.ttf')
                self.newLine(text_box, tuples[0], 'Arial', 10)
                line_cnt = line_cnt + 1
                text_box = self.setTextBox(slide,line_cnt,'.\DOSSaemmul.ttf')
                self.newLine(text_box, tuples[1], 'DOSSaemmul', 13)
                line_cnt = line_cnt + 1
            return slide

        elif (isinstance(slideObj,SlideType_h5)):
            slide = self.newSlide(1)#h5
            textbox_cnt=1
            for tuples in slideObj._h5Tuples:
                text_box = self.setTextBox(slide,textbox_cnt,'.\DOSSaemmul.ttf')
                self.newLine(text_box,tuples[0],'DOSSaemmul',15)
                for line in tuples[1]:
                    self.newLine(text_box,line,'Arial',12)
                textbox_cnt = textbox_cnt+1


        else:
            slide = self.newSlide(2)
            text_box = self.setTextBox(slide,1,'.\DOSSaemmul.ttf')
            for line in slideObj._lines:
                self.newLine(text_box,line,'DOSSaemmul',13)
            return slide

    def generate(self):
        self.basePrs()
        self.titleSlide()
        for slide_ in self._slideTypes:
            self.generate_slide(slide_)


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
