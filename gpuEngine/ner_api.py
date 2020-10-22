# -*- coding:utf-8 -*-
import urllib3
import json
from collections import Counter
import itertools
from collections.abc import Iterable

def get_topic(text):

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "1d00844e-0b14-498b-a3c8-017784783627"
    analysisCode = "ner"

    #with open('text_json') as json_file:
    #    json_data = json.load(json_file)
    # text = "사용자가 텍스트와 이미지를 입력하면 '인공지능'이 그 데이터를 기반으로 완성된 발표자료를 만들어 줍니다"
    # text = "소프트웨어 마에스트로와 BOB는 과학기술정보통신부에서 주관하는 대한민국의 대표적인 소프트웨어 인재 양성 프로젝트이다."
    # input: text

    # text = json2str(json.loads(json_data))
    requestJson = {  # API 호출
        "access_key": accessKey,
        "argument": {
            "text": text,
            "analysis_code": analysisCode
        }
    }
    http = urllib3.PoolManager()
    response = http.request(  # API 응답
        "POST",
        openApiURL,  # 나의 GPU서버 url - ex) 'http://000.000.000:8000/NLPinference"
        headers={"Content-Type": "application/json; charset=UTF-8"},
        body=json.dumps(requestJson)
    )

    # print(json.loads(response.data.decode('utf-8')))

    # print("[responseCode] " + str(response.status))  # status == 200
    # print(str(response.data, "utf-8"))                         #호출결과 확인

    temp_json = json.loads(response.data.decode('utf-8'))  # data를 json형식으로 read

    topic_list = []
    for j in range(len(temp_json['return_object']['sentence'])):  # 문장별로 topic 추출
        for i in range(len(temp_json['return_object']['sentence'][j]['NE'])):
            topic_list.append(temp_json['return_object']['sentence'][j]['NE'][i]['type'].replace('_', '')[2:])

    print(topic_list)                                                        #topic 최빈값 출력
    topic = Counter(topic_list).most_common(n=1)[0][0] if len(topic_list)>0 else None
    return topic


# def json2str(json_data):
#     text_list = json_data['_mainTitle']
#     text_list += ' ' + ''.join(json_data['_subTitle'])
#     text_list += ' ' + ' '.join(json_data['_midTitles'])
#     text_list += json_data['_slideContents'][0]['_defStr']
#     text_list += str(flatten(json_data['_slideTitles']))
#     text_list += ' ' + ''.join(json_data['_slideContents'][1]['_lines'])
#     return text_list

def flatten(lst):
    result = []
    for item in lst:
        result.extend(item)
    return result


