import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector

cap= cv2.VideoCapture(0)
detector=FaceMeshDetector(maxFaces=1)

while True:
    success,img=cap.read()
    img,faces=detector.findFaceMesh(img,draw=False)
    if faces:
        face=faces[0]
        pointLeft=face[145]
        pointRight=face[374]
        #cv2.circle(img,pointLeft,5,(255,0,255),cv2.FILLED)
        #cv2.line(img, pointLeft, pointRight, (0, 255, 255))
        #cv2.circle(img, pointRight, 5, (255, 0, 255), cv2.FILLED)

        w,_ =detector.findDistance(pointLeft,pointRight)
        # finding the distance:
        W = 6.3
        f = 310
        d=(W*f)/w
        print(d)

        cvzone.putTextRect(img,f'Distance{int(d)} cm',(face[10][0]-75,face[10][1]-50),scale=2)
        #finding Focal Length:
        #d=25
        #W=6.3
        #f=(w*d)/W
    cv2.imshow("image",img)
    cv2.waitKey(1)