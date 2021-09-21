import base64
import cv2
import numpy as np
import utlis

def stringToRGB(base64_string):
    img_str = base64.b64decode(str(base64_string))
    image = np.frombuffer(img_str, np.uint8)
    img_np = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return img_np


def ScanningImg(x):
    
    h = x.decode("utf-8")
    kernel = np.ones((5, 5))
    img = stringToRGB(h)
    heightImg , widthImg, deepImg = img.shape
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgGaus = cv2.GaussianBlur(imgGray, (5, 5), 1)
    thres=utlis.valTrackbars()
    imgCanny = cv2.Canny(imgGaus,thres[0],thres[1])
    imgContours = img.copy()
    imgBigContour = img.copy()
    contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    aaa = cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10)
    biggest, maxArea = utlis.biggestContour(contours)
    if biggest.size != 0:
        biggest=utlis.reorder(biggest)
        img = cv2.drawContours(imgBigContour, biggest, -1, (0, 255, 0), 20)
        imgBigContour = utlis.drawRectangle(imgBigContour,biggest,2)
        pts1 = np.float32(biggest)
        pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) 
        imgWarpColored=imgWarpColored[20:imgWarpColored.shape[0] - 20, 20:imgWarpColored.shape[1] - 20] 
        imgTTT = cv2.detailEnhance(imgWarpColored, sigma_s=10, sigma_r=0.35)
        imgTT = cv2.fastNlMeansDenoisingColored(imgTTT,None,6,10,7,21)
        cv2.imwrite("Documents\scanned_img.jpg",imgTT)
        return True
    else:
        return False

