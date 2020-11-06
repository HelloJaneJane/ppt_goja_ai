import cv2
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


#input imgae랑 alpha image를 받아옴
input_img = 'test1.jpg'
input_img_a = 'test1.png'
thr = [1, 3, 5, 10, 25, 50, 100, 200]

def opencv_BR(input_img, input_img_a, thr):
    img = cv2.imread('/home/jh/swm/human/gpuEngine/U2Net/test_data/my_test/'+input_img, cv2.IMREAD_UNCHANGED)
    img_a = cv2.imread('/home/jh/swm/human/gpuEngine/U2Net/test_data/u2netmy_results/'+input_img_a, cv2.IMREAD_UNCHANGED)

    #alpha 이미지를 2d로 바꿔줌
    gray = cv2.cvtColor(img_a, cv2.COLOR_BGR2GRAY)

    #잘 받아와졌나 각 행렬의 크기 확인 [?,?,3], [?,?,3], [?,?] 나와야함
    print(img.shape)
    print(img_a.shape)
    print(gray.shape)

    #img 파일을 3채널에 alpha이미지를 더해서 4채널로 바꿔줌
    rgba = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    rgba[:, :, 3] = gray

    #threshold 설정

    gray_thr = np.zeros((gray.shape[0], gray.shape[1], len(thr)))
    rgba_thr = np.zeros((rgba.shape[0], rgba.shape[1], rgba.shape[2], len(thr)))
    print(gray_thr.shape) #[?,?,thr개수]
    print(rgba_thr.shape) #[?,?,4,thr개수]

    #thr에 따른 결과 이미지 저장
    for i in range(len(thr)):
        rgba_thr[:, :, :, i] = rgba
        ret, gray_thr[:,:,i] = cv2.threshold(rgba[:,:,3], thr[i], 255, cv2.THRESH_BINARY)
        rgba_thr[:, :, 3, i] = gray_thr[:,:,i]
        cv2.imwrite('./thr_'+str(thr)+'_'+input_img_a, rgba_thr)