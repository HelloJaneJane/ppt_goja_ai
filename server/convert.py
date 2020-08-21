#-*- coding:utf-8 -*-
from pptx import Presentation

from pptEngine.PyPPTModule import *

def convert(htmlStr):
    prs = Presentation()

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

    myTextData = TextData(mainTitle, subTitle, midTitles, slideTitles)
    myTextData.__print__()

    print("안에내용들: ",end='')
    print(h4Contents)

    # myPPTData = PPTData(myTextData)
    # myPrs = myPPTData.basePrs()








