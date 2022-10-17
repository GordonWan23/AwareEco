import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

camera = PiCamera()
camera.resolution = (640, 480)
camera.iso = 800
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
flag1 = 0


global throttlePos

def empty(a):
    pass
# threshold1 = 110
# threshold2 = 55
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 1048, 720)
cv2.createTrackbar("pt1x", "Parameters", 37, 640, empty)
cv2.createTrackbar("pt1y", "Parameters", 46, 480, empty)
cv2.createTrackbar("pt2x", "Parameters", 504, 640, empty)
cv2.createTrackbar("pt2y", "Parameters", 32, 480, empty)
cv2.createTrackbar("pt3x", "Parameters", 0, 640, empty)
cv2.createTrackbar("pt3y", "Parameters", 425, 480, empty)
cv2.createTrackbar("pt4x", "Parameters", 586, 640, empty)
cv2.createTrackbar("pt4y", "Parameters", 422, 480, empty)
# cv2.createTrackbar("Threshold1", "Parameters", 110, 255, empty)
# cv2.createTrackbar("Threshold2", "Parameters", 110, 255, empty)


def rotateImage( img, angle):  #From asg1, test purpose
    #h,w,c=img.shape
    #center=(h//2,w//2)
    h,w=img.shape[:2]
    (cX,cY)=(w//2,h//2)
    rotation_matrix=cv2.getRotationMatrix2D((cX,cY),angle,1.0)
    cos=np.abs(rotation_matrix[0,0])
    sin=np.abs(rotation_matrix[0,1])
#in order to avoid image from being cropped or with blank space, we need to recalculate rotated height and width
    nW=int((h*sin)+(w*cos))
    nH=int((h*cos)+(w*sin))

    rotation_matrix[0,2] +=(nW/2)-cX
    rotation_matrix[1,2] +=(nH/2)-cY
    final_rotated=cv2.warpAffine(img,rotation_matrix,(nW,nH))

    return final_rotated

def skinDetection(src):
    hsv_src = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)

    src_hist = cv2.calcHist([hsv_src], [0], None, [180], [0, 180])  # draw histogram of hue channel only

    hist = [val[0] for val in src_hist]  # convert histogram to a list
    indices = list(range(0, 256))
    s = [(x, y) for y, x in sorted(zip(hist, indices), reverse=True)]  # sort the list
    for sn in s:
        print(sn)
    max = s[0][0]  # default maximum at the begining
    i = 0
    while max > 43:  # check if the maximum hue peak is in the desired value range
        i = i + 1
        max = s[i][0]  # switch to the next peak if not in range
    # set the lower and upper threshold for skin detection
    if max <= 30:
        lower = np.array([0, 0, 0], dtype="uint8")
    else:
        lower = np.array([max - 30, 0, 0], dtype="uint8")
    upper = np.array([max + 50, 255, 255], dtype="uint8")
    # lower = np.array([0, 48, 80], dtype="uint8")
    # upper = np.array([20, 255, 255], dtype="uint8")

    skinMask = cv2.inRange(hsv_src, lower, upper)  # check pixels in range
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
    # skinMask = cv2.erode(skinMask, kernel, iterations=2)
    # skinMask = cv2.dilate(skinMask, kernel, iterations=2)

    # skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skinFinal = cv2.bitwise_and(src, src, mask=skinMask)  # now, capture only the skin part
    return skinMask

def skinDetection2(img):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    h = hsv[:,:,0]
    s = hsv[:,:,1]
    v = hsv[:,:,2]
    hsv_split = np.concatenate((h,s,v),axis=1)
    ret,min_sat = cv2.threshold(s,40,255,cv2.THRESH_BINARY)
    ret,max_hue = cv2.threshold(h,15,255,cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
    final = cv2.bitwise_and(min_sat,max_hue)
    final = cv2.bitwise_not(final)
    skinMask = cv2.erode(final, kernel, iterations=2)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)
    skinFinal = cv2.bitwise_and(img, img, mask=skinMask)
    return final

def getContours(img, imgContour, imgO):
    global throttlePos

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    global x1, y1, h1, w1
    x1, y1, h1, w1 = 2, 2, 3, 3
    img_pl = np.zeros((img.shape[0], img.shape[1]))
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>4500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0 , 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x , y ,w , h =cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x , y ), (x + w, y + h),(0, 255, 0), 5)

            # cv2.putText(imgContour, "Points: " + str(len(approx)), (x +w +20, y +20), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            x1, y1, h1, w1 = x, y, h, w
            mask1 = img[y1:y1 + h1, x1:x1 + w1]
            cropped1 = imgO[y1:y1 + h1, x1:x1 + w1]
            fin_crop = cv2.bitwise_and(cropped1, cropped1, mask=mask1)
            cv2.imwrite("cropped.jpg",fin_crop)
            # cv2.+drawContours(img_pl, [cnt], -1, (255, 255, 255), -1)
            # plateMask = cv2.erode(img_pl, kernel, iterations=2)  # Perform Opening
            # plateMask = cv2.dilate(plateMask, kernel, iterations=2)
            #
            # plateMask = cv2.GaussianBlur(plateMask, (3, 3), 0).astype(dtype=np.uint8)
            # plateFinal = cv2.bitwise_and(imgO, imgO, mask=plateMask)
            # plateFinal = cv2.cvtColor(plateFinal,cv2.COLOR_BGR2GRAY)
            cropped = cv2.imread("cropped.jpg",0)
            label = myHands.recognition(cropped)
            labelGes = myGesture.recognition(cropped)
            pose = myEgoges.recognition(mask1)
            cv2.putText(imgContour, label, (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            cv2.putText(imgContour, labelGes, (x + w + 20, y + 100), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (255, 0, 0), 2)
            cv2.putText(imgContour, pose, (x + w + 20, y + 200), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 0, 255), 2)
            pos = (y + int(0.5*h))
            if pose == "Grab":
                throttlePos = pos
            cv2.putText(imgContour, str(pos), (x + w + 20, y ), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 255), 2)
            #return 1
        #else:
            #return 0

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    image = frame.array
    imgO = image.copy()
    imgCP = image.copy()
    pt1x = cv2.getTrackbarPos("pt1x", "Parameters")
    pt1y = cv2.getTrackbarPos("pt1y", "Parameters")
    pt2x = cv2.getTrackbarPos("pt2x", "Parameters")
    pt2y = cv2.getTrackbarPos("pt2y", "Parameters")
    pt3x = cv2.getTrackbarPos("pt3x", "Parameters")
    pt3y = cv2.getTrackbarPos("pt3y", "Parameters")
    pt4x = cv2.getTrackbarPos("pt4x", "Parameters")
    pt4y = cv2.getTrackbarPos("pt4y", "Parameters")
    pt1 = [pt1x, pt1y]
    pt2 = [pt2x, pt2y]
    pt4 = [pt4x, pt4y]
    pt3 = [pt3x, pt3y]
    cv2.circle(imgCP, pt1, 5, (0, 0, 255), -1)
    cv2.circle(imgCP, pt2, 5, (0, 255, 0), -1)
    cv2.circle(imgCP, pt3, 5, (255, 0, 0), -1)
    cv2.circle(imgCP, pt4, 5, (255, 255, 255), -1)
    cv2.imshow("show", imgCP)
    dst1 = [0, 0]
    dst2 = [640, 0]
    dst3 = [0, 480]
    dst4 = [650, 480]
    srcpts = np.float32([pt1, pt2, pt3, pt4])
    dstpts = np.float32([dst1, dst2, dst3, dst4])
    h, status = cv2.findHomography(srcpts, dstpts)
    image = cv2.warpPerspective(image, h, [image.shape[1], image.shape[0]])
    # To improve performance, optionally mark the image as not writeable to
    # image.flags.writeable = False
    # imgCP = image.copy()
    # # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # skin = skinDetection(image)
    # cv2.imshow('skin',skin)
    # imgContour = cv2.cvtColor(skin.copy(),cv2.COLOR_GRAY2BGR)
    # imgBlur = cv2.GaussianBlur(skin, (7, 7), 1)
    # imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)
    #
    # threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    # threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    # imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    # kernel = np.ones((5, 5))
    # imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    #
    # getContours(skin , imgContour,imgCP)
    # # cv2.imshow('canny',imgCanny)
    # if throttlePos >=180 and throttlePos <=380:
    #     throttle = int((abs(throttlePos - 380 ) / 200) * 100)
    # elif throttlePos < 180 :
    #     throttle = 100
    # elif throttlePos > 380 :
    #     throttle = 0
    # else:
    #     throttle = 0
    # throttleStr = "Throttle:" + str(throttle)
    # cv2.putText(imgContour, throttleStr, (350, 100 ), cv2.FONT_HERSHEY_COMPLEX, 1,
    #                     (255, 255, 255), 2)

    cv2.imshow('cont',image)
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break
    rawCapture.truncate(0)