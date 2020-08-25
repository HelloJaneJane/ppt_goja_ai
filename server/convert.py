#-*- coding:utf-8 -*-
from pptx import Presentation
from json import JSONEncoder
import os
import time

from pptEngine.PyPPTModule import *

from server.awsModule import *

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def convert(htmlStr):

    mainTitle = (htmlStr.split('</h1>')[0]).split('</span>')[1]
    htmlStr = htmlStr.split('</h1>')[1]

    subTitle = (htmlStr.split('</h2>')[0]).split('</span>')[1]
    htmlStr = htmlStr.split('</h2>')[1]

    # print("제목: "+mainTitle)
    # print("부제목: "+subTitle)

    h3List = htmlStr.split('<h3')

    midTitles = []
    h3Contents = []

    for h3Index, h3Elem in enumerate(h3List):
        if h3Index==0:
            pass
        else:
            midTitles.append((h3Elem.split('</h3>')[0]).split('</span>')[1])
            h3Contents.append((h3Elem.split('</h3>')[1],h3Index-1))

    # print("중제목들: ",end='')
    # print(midTitles)

    slideTitles = []
    h4Contents = []

    for h3ConElem in h3Contents:
        h4List = h3ConElem[0].split('<h4')
        h3Index = h3ConElem[1]

        for h4Index, h4Elem in enumerate(h4List):
            if h4Index==0:
                pass
            else:
                slideTitles.append(((h4Elem.split('</h4>')[0]).split('</span>')[1],h3Index))
                h4Contents.append(h4Elem.split('</h4>')[1])

    
    # print("소제목들: ",end='')
    # print(slideTitles)

    slideContents = []

    for h4Index, h4ConElem in enumerate(h4Contents):
        h4ConElem.replace('\n','')
        h4Title = slideTitles[h4Index][0]
        
        # if 컨텐츠h5가 있으면 -> h5타입
        if '<h5' in h4ConElem:
            h5List = h4ConElem.split('<h5')
            h5Tuples = []
            for h5Index, h5Elem in enumerate(h5List):
                if h5Index==0:
                    pass
                else:
                    h5Heading = (h5Elem.split('</h5>')[0]).split('</span>')[1]
                    h5Contents = parseStrToList(h5Elem.split('</h5>')[1])
                    h5Tuples.append((h5Heading,h5Contents))
            slideContents.append(SlideType_h5(h5Tuples))

        # elif 슬라이드타이틀에 일정/과정/단계 가 있으면 -> 타임라인 타입
        elif h4Title.find('과정')!=-1 or h4Title.find('일정')!=-1 or h4Title.find('단계')!=-1 :
            timeContents = parseStrToList(h4ConElem)
            timeTuples = []
            for timeContent in timeContents:
                timeTuples.append(parseTimeStrToTuple(timeContent))
            slideContents.append(SlideType_timeline(timeTuples))

        # elif 슬라이드타이틀이 ? 로끝나고 내용이 한줄이면 -> 데피니션 타입
        elif h4Title.find('?')==len(h4Title)-1 and len(parseStrToList(h4ConElem)) == 1:
            defStr = eraseTags(h4ConElem)
            slideContents.append(SlideType_definition(defStr))

        # else ->디폴트타입
        else :
            lines = parseStrToList(h4ConElem)
            slideContents.append(SlideType(lines))
            
    myTextData = TextData(mainTitle, subTitle, midTitles, slideTitles, slideContents)
    # myTextData.__print__()
    myTextDataJSON = myTextData.toJSON()
    # print(myTextDataJSON)
    
    userName = 'test'
    timeStamp = time.strftime('%y%m%d_%H%M')
    outputName = userName+'_'+timeStamp+'.pptx'


    ## TODO
    # 1. myTextDataJSON을 GPU 로 보낸다
    # 2. GPU 가 찾아낸 결과물을 받는다
    # 3. myTextData랑 결과물이랑 합쳐서 PPT Data를 만든다
    myPPTData = PPTData(myTextData)
    # 4. myPPTData를 엔진한테 보내서 PPT 만들기를 시작한다
    myPPTData.generate()
    # 5. 엔진에서 만들어진 PPT 파일을 받아온다
    myPPTData.write(outputName)

    # 만든 피피티 파일을 s3로 업로드 (+서버 안에선 파일 지우기)
    uploadFileToS3(outputName, 'outputPPT/'+outputName)
    os.remove(outputName)

    # 파일 다운로드할 수 있는 s3 링크 받아오기
    url = getUrlFromS3('outputPPT/'+outputName)
    # print(url)

    # 링크를 클라이언트로 전송 -> 피피티 다운로드 버튼에 연결

    return url



def eraseTags(rawStr):
    while rawStr.find('<p>')!=-1:
        rawStr=rawStr.replace('<p>','')
        rawStr=rawStr.replace('</p>','')
    while rawStr.find('\n')!=-1:
        rawStr=rawStr.replace('\n','')
        rawStr=rawStr.replace('</p>','')
    return rawStr

def parseStrToList(rawStr):
    # <p> 있는 그냥 텍스트
    if rawStr.find('<p>')!=-1:
        rawStr=eraseTags(rawStr)
        # 한줄
        if rawStr.find('<br>')!=-1:
            return [rawStr]
        # 여러줄
        else:
            return rawStr.split('<br>')
    # <li> 있는 텍스트
    else:
        # 불렛
        if rawStr.find('<ul>')!=-1:
            rawStr=rawStr.replace('<ul>\n<li>','')
            rawStr=rawStr.replace('</li></ul>\n','')
        # 넘버링
        elif rawStr.find('<ol>')!=-1:
            rawStr=rawStr.replace('<ol>\n<li>','')
            rawStr=rawStr.replace('</li></ol>\n','')

        rawStr=eraseTags(rawStr)
        return rawStr.split('</li><li>')

def parseTimeStrToTuple(rawStr):
    # 시간 : 한줄내용
    if rawStr.find(' : ')!=-1:
        time = rawStr.split(' : ')[0]
        line = rawStr.split(' : ')[1]
        return (time,line)
    # 내용만
    else:
        return (None, rawStr)