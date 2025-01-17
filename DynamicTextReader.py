import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np


cap= cv2.VideoCapture(0)
detector=FaceMeshDetector(maxFaces=1)

TextList=["Hello Everyone","Iam Rakesh","a Recent Graduate","in B.TECH computer Science"
          ,"with a Specialization","in AI & ML"]
sens=10

while True:
    success,img=cap.read()
    imgText=np.zeros_like(img)
    img,faces=detector.findFaceMesh(img,draw=False)
    if faces:
        face=faces[0]
        pointLeft=face[145]
        pointRight=face[374]

        w,_ =detector.findDistance(pointLeft,pointRight)
        # finding the distance:
        W = 6.3
        f = 310
        d=(W*f)/w
        print(d)

        cvzone.putTextRect(img,f'Distance{int(d)} cm',
            (face[10][0]-75,face[10][1]-50),scale=2)
        for i,text in enumerate(TextList):
            singleheight=20+int((int(d/sens)*sens)/4)
            scale=0.4+(int(d/sens)*sens)/75
            cv2.putText(imgText,text,(50,50+(i*singleheight)),
            cv2.FONT_ITALIC,scale,(255,255,255),2)

    imgStacked=cvzone.stackImages([img,imgText],2,1)

    cv2.imshow("image",imgStacked)
    cv2.waitKey(1)