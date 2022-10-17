import cv2
import numpy as np
import imageSharing
import classification
from threading import Timer

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)

cap.set(4, frameHeight)

def empty(a):
    pass
x2,y2,w2,h2=0,0,0,0
counter=0
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)
# cv2.createTrackbar("Threshold1", "Parameters", 110, 255, empty)
# cv2.createTrackbar("Threshold2", "Parameters", 55, 255, empty)
#cv2.createTrackbar("Area", "Parameters", 5000, 30000, empty)

threshold1 = 110
threshold2 = 55
global timeoutFlag
timeoutFlag = 0
global isStable
isStable=0
global categoryList
categoryList=[]
names = globals()
for i in range(20):
    names['x2_' + str(i)] = 0
    names['y2_' + str(i)] = 0
    names['h2_' + str(i)] = 0
    names['w2_' + str(i)] = 0
    names['counter_' + str(i)] = 0
    names['stable_' + str(i)] = 0
    names['category_' + str(i)] = ""


def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def findStable(x,y,h,w,i):
    global timeoutFlag
    global categoryList
    names=globals()
    x1_=names.get('x2_' + str(i))
    y1_ = names.get('y2_' + str(i))
    h1_ = names.get('h2_' + str(i))
    w1_ = names.get('w2_' + str(i))
    stabled_image = img[y1_:y1_+int(1.05*h1_), x1_:x1_+int(1.05*w1_)]
    if (x-x1_<=20) and (y-y1_<=20) and (h-h1_<=20) and (w-w1_<=20) and (x1_>1 and x>1 and y1_>1 and y>1):
        names['counter_' + str(i)] = names.get('counter_' + str(i)) + 1
        print(x,y,x1_,y1_)
        if names.get('counter_' + str(i))>=15:
            names['counter_' + str(i)]=0
            print("stable" + str(i))
            he, wi = stabled_image.shape[:2]
            if he>=10 and wi>=10:
                filename = "stabled%d.png" % (i)
                if names.get('stable_' + str(i)) == 0:
                    # imageSharing.sendImageClientRecon(stabled_image)
                    # names['category_' + str(i)] = classification.classificationCV2(stabled_image)
                    names['category_' + str(i)] = imageSharing.sendImageClientRecon(stabled_image)
                    categoryList.append(names['category_' + str(i)])
                    cv2.imwrite(filename,stabled_image)
                    #isStable=1
                    cv2.imshow(filename, stabled_image)
                    if timeoutFlag == 0:
                        print("timer started")
                        t = Timer(4.0,timeout)
                        t.start()
                        timeoutFlag = 1
                names['stable_' + str(i)] = 1
    else:
        names['counter_' + str(i)]=0
        names['stable_' + str(i)] = 0
        #isStable=0

    names['x2_' + str(i)] = x
    names['y2_' + str(i)] = y
    names['h2_' + str(i)] = h
    names['w2_' + str(i)] = w

def timeout():
    global timeoutFlag
    global categoryList
    print("*"*72)
    print("Timed Out")
    print(categoryList)
    print("*" * 72)
    flagRecyc= 0
    for items in categoryList:
        if items == "Trash":
            print("Unrecyclable")
            flagRecyc = 1
    if flagRecyc == 0:
        print("Recyclable")
    categoryList.clear()
    timeoutFlag = 0


def getContours(img, imgContour):

    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    global x1, y1, h1, w1
    x1, y1, h1, w1 = 2, 2, 3, 3
    i = 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #areaMin = cv2.getTrackbarPos("Area", "Parameters")
        areaMin = 6000
        if area>areaMin:
            i = i +1
            cv2.drawContours(imgContour, cnt, -1, (255, 0 , 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            print(len(approx))
            x , y ,w , h =cv2.boundingRect(approx)
            cv2.rectangle(imgContour, (x , y ), (x + w , y + h ),(0, 255, 0), 5)

            cv2.putText(imgContour, "Points: " + str(len(approx)), (x +w +20, y +20), cv2.FONT_HERSHEY_COMPLEX, .7, (0, 255, 0), 2)
            cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, .7,
                        (0, 255, 0), 2)
            x1, y1, h1, w1 = x, y, h, w
            findStable(x, y, h, w, i)
            if  names['stable_' + str(i)] == 1:
                 cv2.putText(imgContour, names['category_' + str(i)], (x + w , y + 155), cv2.FONT_HERSHEY_COMPLEX, .7,
                             (0, 0, 255), 2)
                 if area >= 200000:
                    cv2.putText(imgContour, "Oversize!", (x + 15, y + 155), cv2.FONT_HERSHEY_COMPLEX, .7,
                                (0, 0, 255), 4)
            #return 1
        #else:
            #return 0


while True:
    success, img = cap.read()
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img, (7, 7), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    # threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    # threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)
    kernel = np.ones((5, 5))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour)
    #getContours(imgDil, imgContour)

    cropped_image = img[y1:y1+h1, x1:x1+w1]

    # if (x2-x1<=10) and (y2-y1<=10) and (h2-h1<=10) and (w2-w1<=10) and (x1>1 and x2>1 and y1>1 and y2>1):
    #     counter=counter+1
    #     print(x2,y2,x1,y1)
    #     if counter>=25:
    #         counter=0
    #         print("stable")
    #         he, wi = cropped_image.shape[:2]
    #         if he>=10 and wi>=10:
    #             cv2.imwrite("stable.jpg",cropped_image)
    #             isStable=1
    #             cv2.imshow("Stable", cropped_image)
    # else:
    #     counter=0
    #     isStable=0
    # x2,y2,h2,w2=x1,y1,h1,w1

    imgStack = stackImages(0.8,([imgContour,cropped_image]))

    cv2.imshow("Result", imgStack)
    cv2.imshow("Cropped", cropped_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break