#-*- coding:utf-8 -*-
from pptx import Presentation
from json import JSONEncoder
import os
import time

from pptEngine.PyPPTModule import *
from gpuEngine.ner_api import *

from server.awsModule import *

class MyEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


def convert(htmlStr):

    errMsgs = []
    
    # [1] 제목 (mainTitle)
    if '<h1' in htmlStr:
        mainTitle = (htmlStr.split('</h1>')[0]).split('</span>')[1]
        htmlStr = htmlStr.split('</h1>')[1]
    else:
        mainTitle = None
        errMsgs.append('제목(h1)을 입력하세요.')
    # print("제목: "+mainTitle)

    # [2] 부제목 (subTitle)
    if '<h2' in htmlStr:
        subTitle = (htmlStr.split('</h2>')[0]).split('</span>')[1]
        htmlStr = htmlStr.split('</h2>')[1]
    else:
        subTitle = None
        errMsgs.append('부제목(h2)을 입력하세요.')
    # print("부제목: "+subTitle)

    # [3] 중제목 (midTitle)
    midTitles = []
    h3Contents = []
    if '<h3' in htmlStr:
        h3List = htmlStr.split('<h3')
        for h3Index, h3Elem in enumerate(h3List):
            if h3Index==0:
                pass
            else:
                midTitles.append((h3Elem.split('</h3>')[0]).split('</span>')[1])
                h3Contents.append((h3Elem.split('</h3>')[1],h3Index-1))
    else:
        errMsgs.append('중제목(h3)을 입력하세요.')
    # print("중제목들: ",end='')
    # print(midTitles)

    # [4] 슬라이드별 소제목 (slideTitle)
    slideTitles = []
    h4Contents = []
    if len(h3Contents)==0:
        errMsgs.append('각 중제목(h3)마다 해당하는 슬라이드소제목(h4) 및 내용을 입력하세요.')
    for h3ConElem in h3Contents:
        if '<h4' in h3ConElem[0]:
            h4List = h3ConElem[0].split('<h4')
            h3Index = h3ConElem[1]
            for h4Index, h4Elem in enumerate(h4List):
                if h4Index==0:
                    pass
                else:
                    slideTitles.append(((h4Elem.split('</h4>')[0]).split('</span>')[1],h3Index))
                    h4Contents.append(h4Elem.split('</h4>')[1])
        else:
            errMsgs.append('각 중제목(h3)마다 슬라이드소제목(h4)을 하나 이상 입력하세요.')
    # print("소제목들: ",end='')
    # print(slideTitles)

    # [5] 슬라이드 컨텐츠 (slideContents)
    slideContents = []
    if len(h4Contents)==0:
        errMsgs.append('각 슬라이드소제목(h4)마다 해당하는 내용을 입력하세요.')
    for h4Index, h4ConElem in enumerate(h4Contents):
        h4ConElem.replace('\n','')
        h4Title = slideTitles[h4Index][0]

        slideType = getSlideType(h4Title, h4ConElem)
        slideContents.append(slideType)            
        
    # print("내용들: ",end='')
    # print(slideContents)


    # 에러메시지 있으면 에러 리턴
    if len(errMsgs)>0:
        # print(errMsgs)
        return { 'status': 'error', 'message': errMsgs }

    # 에러 없으면 피피티 만들어서 다운로드 링크 리턴
    else:
        myTextData = TextData(mainTitle, subTitle, midTitles, slideTitles, slideContents)
        # myTextData.__print__()
        myTextDataJSON = myTextData.toJSON()
        # print(myTextDataJSON)
        
        userName = 'test'
        timeStamp = time.strftime('%y%m%d_%H%M')
        outputName = userName+'_'+timeStamp+'.pptx'
        
        # topic 추출
        myTopic = get_topic(myTextDataJSON)
        
        # ppt 생성
        myPPTData = PPTData(myTextData, myTopic)
        myPPTData.generate()
        myPPTData.write(outputName)

        # 만든 피피티 파일을 s3로 업로드 (+서버 안에선 파일 지우기)
        uploadFileToS3(outputName, 'outputPPT/'+outputName)
        os.remove(outputName)

        # 파일 다운로드할 수 있는 s3 링크 받아오기
        url = getUrlFromS3('outputPPT/'+outputName)
        # print(url)

        # 링크를 클라이언트로 전송 -> 피피티 다운로드 버튼에 연결

        return { 'status': 'success', 'url': url }



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

def getSlideType(h4Title, h4ConElem):
    headerCnt =  h4ConElem.count('<h5')

    # h5가 있을 경우: (h5헤딩,h5내용) 튜플들의 리스트를 슬라이드 타입의 인자로
    h5Tuples = []
    if headerCnt>0:
        h5List = h4ConElem.split('<h5')
        for h5Index, h5Elem in enumerate(h5List):
            if h5Index==0:
                pass
            else:
                h5Heading = (h5Elem.split('</h5>')[0]).split('</span>')[1]
                h5Contents = parseStrToList(h5Elem.split('</h5>')[1])
                h5Tuples.append((h5Heading,h5Contents))

    # h5가 없을 경우: '불렛하나내용'이나 '엔터친거한줄내용' 스트링들의 리스트를 슬라이드 타입의 인자로
    lines = parseStrToList(h4ConElem)


    if headerCnt == 1 or headerCnt >= 5:
        return slideType_head_default(h5Tuples)
    else:
        titleNouns = getNouns(h4Title)
        isTimeLine = checkTimeLine(titleNouns)
        if 2<=headerCnt and headerCnt<=4:
            if isTimeLine:
                return slideType_head_timeLine(h5Tuples)
            else:
                return slideType_head_multiLine(h5Tuples)
        else:
            ## TODO: '입력이 짧다 == 글자수가 20이하다' 로 했는데 남지훈이 고쳐야 함
            if h4ConElem.count('<ul>') == 0 and len(h4ConElem)>20:            
                return slideType_default(lines)
            elif h4ConElem.count('<ul>')<=1:
                return slideType_singleLine(lines[0])
            else:
                if isTimeLine:
                    return slideType_timeLine(lines)
                else:
                    return slideType_multiLine(lines)

        

def getNouns(str):
    ## TODO: 이종호가 api 만들어주면
    # 문자열 api한테 전송
    # 명사구 담겨있는 리스트 리턴
    return []

def checkTimeLine(nounList):
    timeNounList = ['일정','스케쥴','단계','레시피','순서']
    for n in nounList:
        if n in timeNounList:
            return True
    return False