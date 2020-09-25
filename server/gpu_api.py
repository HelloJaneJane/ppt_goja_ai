
import requests

# gpuUrl = 'http://101.101.172.15:6789'
gpuUrl = 'http://3.35.93.177:6789'


def backRmvAPI(inputFileName):
    data = { 'fileName': inputFileName }
    res = requests.post(gpuUrl+'/backrmv', data=data, verify=False)
    # print(res.text)
    return res.text


def supResolAPI(inputFileName):
    data = { 'fileName': inputFileName }
    res = requests.post(gpuUrl+'/supresol', data=data, verify=False)
    # print(res.text)
    return res.text

def iconifyAPI(inputFileName):
    data = { 'fileName': inputFileName }
    res = requests.post(gpuUrl+'/iconify', data=data, verify=False)
    # print(res.text)
    return res.text