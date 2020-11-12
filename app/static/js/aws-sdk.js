var bucketName = 'ppt-maker-bucket';
var bucketRegion = 'ap-northeast-2';
var IdentityPoolId = 'ap-northeast-2:16956c04-2bc2-4733-8859-5805b9206ac8';

AWS.config.update({
    region: bucketRegion,
    credentials: new AWS.CognitoIdentityCredentials({
        IdentityPoolId: IdentityPoolId
    })
});

var s3 = new AWS.S3({
    apiVersion: '2006-03-01',
    params: {Bucket: bucketName}
});