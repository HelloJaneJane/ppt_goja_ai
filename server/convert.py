#-*- coding:utf-8 -*-
from pptx import Presentation
from json import JSONEncoder
import os
import time

from pptEngine.PyPPTModule import *
from gpuEngine.ner_api import *

from server.awsModule import *

from bs4 import BeautifulSoup


def convert(htmlStr):

    bs = BeautifulSoup(htmlStr, 'lxml')

    tagBlackList = ['html','body','a','span','br','ul','ol','hr']

    tagList = []
    textList = []
    for tag in bs.find_all():
        if tag.name not in tagBlackList:
            tagList.append(tag.name)
            if tag.name=='img':
                textList.append(tag['src'])
            else:
                textList.append(tag.get_text())

    # tagList = [tag.name for tag in bs.find_all() if tag.name not in ['html','body','a','span','br','ul']]
    # textList = [tag.get_text() for tag in bs.find_all() if tag.name not in ['html','body','a','span','br','ul']]

    
    # [0] 태그가 없으면 에러 메시지 리턴
    if tagList == []:
        errMsg = '내용을 입력한 후 변환하기 버튼을 눌러주세요.'
        return { 'status': 'error', 'message': errMsg }


    # [1] html을 파싱하여 slide별 딕셔너리로 변환
    slideDictList = []

    slideIdx = -1
    headIdx = -1

    for n in range(len(tagList)):
        tag = tagList[n]
        text = textList[n]
        # print(tag + "  : " + text)

        slideDict = slideDictList[slideIdx] if slideIdx>=0 else {}
        headDict = slideDict['Head'][headIdx] if headIdx>=0 and slideDict.get('Head',None)!=None else {}

        if tag=='h1':
            # 새 슬라이드 만들기
            slideDictList.append({'h1':text, 'h2':'', 'img':[]})
            slideIdx += 1

        elif tag=='h2':
            # h1이 없으면
            if slideDict.get('h1',None)==None:
                # 새 슬라이드 만들기
                slideDictList.append({'h1':'', 'h2':text, 'img':[]})
                slideIdx += 1
            # h1이 있으면
            else:
                # 기존 슬라이드에 추가하기
                slideDict['h2']=text

        elif tag=='h3':
            # 새 슬라이드 만들기
            slideDictList.append({'h3':text, 'img':[]})
            slideIdx += 1

        elif tag=='h4':
            # 새 슬라이드 만들기
            slideDictList.append({'h4':text, 'Contents':[], 'pCnt':0, 'liCnt':0, 'img':[], })
            slideIdx += 1
            headIdx = -1

        elif tag=='h5':
            # h4이 없으면
            if slideDict.get('h4',None)==None:
                # 새 슬라이드, 새 헤드 만들기
                slideDictList.append({'h4':'', 'Head':[{'h5':text, 'Contents':[], 'pCnt':0, 'liCnt':0}], 'img':[]})
                slideIdx += 1
                headIdx += 1
            # h4이 있으면
            else:
                # 기존 헤드가 있으면
                if slideDict.get('Head',None)!=None:
                    # 새 헤드 만들고, 기존 슬라이드에 추가하기
                    slideDict['Head'].append({'h5':text, 'Contents':[], 'pCnt':0, 'liCnt':0})
                    headIdx += 1
                # 기존 헤드가 없으면
                else:
                    # 기존 내용이 없으면
                    if slideDict['pCnt']==0 and slideDict['liCnt']==0:
                        # 기존 내용 태그 지우고, 새 헤드 만들고, 기존 슬라이드에 추가하기
                        slideDict.pop('Contents',None)
                        slideDict.pop('pCnt',None)
                        slideDict.pop('liCnt',None)
                        slideDict['Head']=[{'h5':text, 'Contents':[], 'pCnt':0, 'liCnt':0}]
                        headIdx += 1
                    # 기존 내용이 있으면
                    else:
                        # 새 슬라이드 (제목은 기존 꺼), 새 헤드 만들기
                        slideTitle = slideDict['h4']
                        slideDictList.append({'h4':slideTitle, 'Head':[{'h5':text, 'Contents':[], 'pCnt':0, 'liCnt':0}], 'img':[]})
                        slideIdx += 1
                        headIdx += 1
                
        elif tag=='p':
            # h4이 없으면
            if slideDict.get('h4',None)==None:
                # 새 슬라이드 만들기
                slideDictList.append({'h4':'', 'Contents':[('p',text)], 'pCnt':1, 'liCnt':0, 'img':[]})
                slideIdx += 1
                headIdx = -1
            # h4이 있으면
            else:
                # h5이 있으면
                if headDict!={}:
                    # 기존 헤드에 추가하기
                    if text :#changed
                        headDict['Contents'].append(('p',text))
                        headDict['pCnt'] += 1
                # h5이 없으면
                else:
                    # 기존 슬라이드에 추가하기
                    if text:#changed
                        slideDict['Contents'].append(('p',text))
                        slideDict['pCnt'] += 1

        elif tag=='li':
            # h4이 없으면
            if slideDict.get('h4',None)==None:
                # 새 슬라이드 만들기
                slideDictList.append({'h4':'', 'Contents':[('li',text)], 'pCnt':0, 'liCnt':1, 'img':[]})
                slideIdx += 1
                headIdx = -1
            # h4이 있으면
            else:
                # h5이 있으면
                if headDict!={}:
                    # 기존 헤드에 추가하기
                    if text :#changed
                        headDict['Contents'].append(('li',text))
                        headDict['liCnt'] += 1
                # h5이 없으면
                else:
                    if text :#changed
                    # 기존 슬라이드에 추가하기
                        slideDict['Contents'].append(('li',text))
                        slideDict['liCnt'] += 1

        elif tag=='img':
            # 맨 처음이면
            if slideDict=={}:
                # 새 슬라이드 만들기
                slideDictList.append({'h4':'', 'Contents':[], 'pCnt':0, 'liCnt':0, 'img':[text]})
            # 맨 처음이 아니면
            else:
                # 기존 슬라이드에 추가하기
                slideDict['img'].append(text)

        # 기타
        else:
            pass

    print(slideDictList)

    # [2] 슬라이드 별 딕셔너리로 슬라이드 타입 분류
    slideList = [getSlideType(slideDict) for slideDict in slideDictList]

    print(slideList)
    
    
    # [3] 피피티 생성

    userName = 'test'
    timeStamp = time.strftime('%y%m%d_%H%M')
    outputName = userName+'_'+timeStamp+'.pptx'

    # 목차
    toc = [midTitle.get_text() for midTitle in bs.find_all('h3')]
    # print("목차",end='')
    # print(toc)

    # [3.1] topic 추출
    slideDictValueList = list(getAllValues(slideDictList))
    # print(slideDictValueList)
    textDataStr = ''
    for s in slideDictValueList:
        if s!=None: textDataStr += s + ' '
    
    # print(textDataStr)
    pptTopic = get_topic(textDataStr)
    print("토픽",end='')
    print(pptTopic)


    # [3.2] 피피티 엔진 작업
    # myPPTData = PPTData(slideList, pptTopic, toc)
    # myPPTData.generate()
    # myPPTData.write(outputName)

    # [3.3] 유저 다운로드
    # 만든 피피티 파일을 s3로 업로드 (+서버 안에선 파일 지우기)
    # uploadFileToS3(outputName, 'outputPPT/'+outputName)
    # os.remove(outputName)

    # 파일 다운로드할 수 있는 s3 링크 받아오기
    # url = getUrlFromS3('outputPPT/'+outputName)
    # print(url)

    # 링크를 클라이언트로 전송 -> 피피티 다운로드 버튼에 연결
    # return { 'status': 'success', 'url': url }

    return { 'status': 'success', 'url': "/ppt" }


def getAllValues(d):
    if isinstance(d, dict):
        for v in d.values():
            yield from getAllValues(v)
    elif isinstance(d, list):
        for v in d:
            yield from getAllValues(v)
    elif isinstance(d, tuple):
        if isinstance(d[1], str):
            yield d[1]
        else:
            yield None
    else:
        inputImageBaseUrl = "https://ppt-maker-bucket.s3.ap-northeast-2.amazonaws.com/editorInputImage/"
        if isinstance(d, str) and not d.startswith(inputImageBaseUrl):
            yield d
        else:
            yield None



def getSlideType(slideDict):


    # 인풋 이미지 링크들의 리스트를 슬라이드 타입의 2nd 인자로
    imageLinks = slideDict['img']

    # (1) h1, h2, img
    if slideDict.get('h1',None)!=None and slideDict.get('h2',None)!=None:
        # mainTitle, subTitle
        titleTuple = (slideDict['h1'], slideDict['h2'])
        return SlideType_title(titleTuple, imageLinks)

    # (2) h3, img
    elif slideDict.get('h3',None)!=None:
        # midTitle
        midTitle = slideDict['h3']
        return SlideType_midTitle(midTitle, imageLinks)

    # (3) h4, (), img
    elif slideDict.get('h4',None)!=None:
        slideTitle = slideDict['h4']

        headCnt = len(slideDict['Head']) if slideDict.get('Head',None)!=None else 0

        titleNouns = getNouns(slideTitle)
        isTimeLine = checkTimeLine(titleNouns)

        # (3.1) h4, Contents(p/li), img - h5가 없는 경우
        if headCnt==0:

            # 불렛 0개, 패러그랲 1개 + 글자수 짧음
            ## TODO: '입력이 짧다 == 글자수가 20이하다' 로 했는데 남지훈이 고쳐야 함
            if slideDict['liCnt']==0 and slideDict['pCnt']==1:
                pText = slideDict['Contents'][0][1]
                if len(pText)<=20: return SlideType_singleLine(slideTitle, pText, imageLinks) # 패러그랲 하나 문장

            # 불렛 1개, 패러그랲 0개
            elif slideDict['liCnt']==1 and slideDict['pCnt']==0:
                liText = slideDict['Contents'][0][1]
                return SlideType_singleLine(slideTitle, liText, imageLinks) # 불렛 하나 문장

            # 불렛 여러 개, 패러그랲 0개
            elif slideDict['liCnt']>1 and slideDict['pCnt']==0 and slideDict['liCnt']<5:
                liTextList = [contentsTuple[1] for contentsTuple in slideDict['Contents']]
                if isTimeLine:
                    return SlideType_timeLine(slideTitle, liTextList, imageLinks) # 불렛 문장들 리스트
                else:
                    return SlideType_multiLine(slideTitle, liTextList, imageLinks) # 불렛 문장들 리스트

            return SlideType_default(slideTitle, slideDict['Contents'],imageLinks)

        # (3.2) h4, Head(h5, Contents(p/li)), img - h5가 있는 경우
        else:
            headTuples = []
            for head in slideDict['Head']:
                headTuples.append((head['h5'],head['Contents']))

            if 2<=headCnt and headCnt<=4:
                if isTimeLine:
                    return SlideType_head_timeLine(slideTitle, headTuples, imageLinks) # (h5(스트링),Contents(튜플리스트))들 리스트
                else:
                    return SlideType_head_multiLine(slideTitle, headTuples, imageLinks)
            else: # headCnt==1 or headCnt>=5
                return SlideType_head_default(slideTitle, headTuples, imageLinks)



def getNouns(str):
    try:
        list = get_NNG(str)
    except:
        list = []
    return list

def checkTimeLine(nounList):
    timeNounList = ['일정','스케쥴','단계','레시피','순서']
    for n in nounList:
        if n in timeNounList:
            return True
    return False
