import boto3
import botocore

bucketName = 'ppt-maker-bucket'


# 파일이 현재 위치한 로컬 경로 -> 업로드하려는 위치의 s3 경로
def uploadFileToS3(myPath, s3Path):
    s3 = boto3.client('s3')
    s3.upload_file(myPath, bucketName, s3Path)

# 파일이 현재 위치한 s3 경로 -> 다운로드하려는 위치의 로컬 경로
def downloadFileFromS3(s3Path, myPath):
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucketName).download_file(s3Path, myPath)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise


# 데이터 -> 업로드하려는 위치의 s3 경로
def uploadJsonToS3(jsonData, s3Path):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucketName, s3Path)
    obj.put(Body=jsonData)

# 다운로드하려는 위치의 s3 경로에서 데이터 리턴
def downloadJsonFromS3(s3Path):
    s3 = boto3.resource('s3')
    obj = s3.Object(bucketName, s3Path)
    return obj.get()['Body'].read().decode('utf-8') 

# s3 경로에서 다운로드 링크 리턴
def getUrlFromS3(s3Path):
    s3 = boto3.client('s3')
    location = s3.get_bucket_location(Bucket=bucketName)['LocationConstraint']
    url = "https://s3-%s.amazonaws.com/%s/%s" % (location, bucketName, s3Path)
    return url