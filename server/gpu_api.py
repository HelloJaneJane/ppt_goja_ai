
import requests

# gpuUrl = 'http://101.101.172.15:6789'
gpuUrl = 'http://3.35.68.108:5000'


def backRmvAPI(inputFileName):
    data = { 'fileName': inputFileName }
    res = requests.post(gpuUrl+'/backrmv', data=data)
    return res


