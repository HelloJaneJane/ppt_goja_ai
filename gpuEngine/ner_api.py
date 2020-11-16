# -*- coding:utf-8 -*-
import urllib3
import json
from collections import Counter
import itertools
from collections.abc import Iterable
from gpuEngine.topic_data import *

def get_topic(text):

    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "1d00844e-0b14-498b-a3c8-017784783627"
    analysisCode = "ner"

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

    #print(json.loads(response.data.decode('utf-8')))
    #print("[responseCode] " + str(response.status))  # status == 200
    #print(str(response.data, "utf-8"))                         #호출결과 확인
    temp_json = json.loads(response.data.decode('utf-8'))  # data를 json형식으로 read

    topic_list = []
    for j in range(len(temp_json['return_object']['sentence'])):  # 문장별로 topic 추출
        for i in range(len(temp_json['return_object']['sentence'][j]['NE'])):
            nerTag = temp_json['return_object']['sentence'][j]['NE'][i]['type']
            # print(temp_json['return_object']['sentence'][j]['NE'][i]['text'],end='->')
            # print(nerTag,end='->')
            # print(topicTagDict[nerTag])
            topic_list.extend(topicTagDict[nerTag])

    if len(topic_list)==0:
        return None

    topicCounter = Counter(topic_list)
    topicKeys = topicCounter.keys()
    for t in topicKeys:
        # print(t,end='->')
        # print(topicCounter[t],end='*')
        # print(topicWeightDict[t])
        topicCounter[t] = topicCounter[t]*topicWeightDict[t]
    topic = topicCounter.most_common(n=1)[0][0]
    # print(topic)

    return topic


def get_NNG(text):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "1d00844e-0b14-498b-a3c8-017784783627"
    analysisCode = "morp"

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

    temp_json = json.loads(response.data.decode('utf-8'))  # data를 json형식으로 read

    NNG_list = []
    for j in temp_json['return_object']['sentence']:  # 문장별로 topic 추출
        for i in j['morp']:
            if i['type'] == 'NNG':
                # print(i['lemma'])
                NNG_list.append(i['lemma'])

    return NNG_list


def get_MAJ(text):
    openApiURL = "http://aiopen.etri.re.kr:8000/WiseNLU"
    accessKey = "1d00844e-0b14-498b-a3c8-017784783627"
    analysisCode = "morp"

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

    temp_json = json.loads(response.data.decode('utf-8'))  # data를 json형식으로 read

    MAJ_list = []
    for j in temp_json['return_object']['sentence']:  # 문장별로 topic 추출
        for i in j['morp']:
            if i['type'] == 'MAJ':
                MAJ_list.append(i['lemma'])

    return MAJ_list


def json2str(json_data):
    text_list = json_data['_mainTitle']
    text_list += ' ' + ''.join(json_data['_subTitle'])
    text_list += ' ' + ' '.join(json_data['_midTitles'])
    text_list += json_data['_slideContents'][0]['_defStr']
    text_list += str(flatten(json_data['_slideTitles']))
    text_list += ' ' + ''.join(json_data['_slideContents'][1]['_lines'])
    return text_list


def flatten(lst):
    result = []
    for item in lst:
        result.extend(item)
    return result


