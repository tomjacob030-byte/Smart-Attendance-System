# import cv2
# import numpy as np
# import face_recognition
# import os
# from datetime import datetime
# # from PIL import ImageGrab
 
# path = 'ImagesAttendance'
# images = []
# classNames = []
# myList = os.listdir(path)
# print(myList)
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])
# print(classNames)
 
# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList
 
# def markAttendance(name):
#     with open('Attendance.csv','r+') as f:
#         myDataList = f.readlines()
#         nameList = []
#         for line in myDataList:
#             entry = line.split(',')
#             nameList.append(entry[0])
#         if name not in nameList:
#             now = datetime.now()
#             dtString = now.strftime('%H:%M:%S,%D')
#             f.writelines(f'n{name},{dtString}')

# #### FOR CAPTURING SCREEN RATHER THAN WEBCAM
# # def captureScreen(bbox=(300,300,690+300,530+300)):
# #     capScr = np.array(ImageGrab.grab(bbox))
# #     capScr = cv2.cvtColor(capScr, cv2.COLOR_RGB2BGR)
# #     return capScr
 
# encodeListKnown = findEncodings(images)
# print('Encoding Complete')
 
# cap = cv2.VideoCapture(0)
 
# while True:
#     success, img = cap.read()
#     #img = captureScreen()
#     # height, width, _ = img.shape
#     # imgS = cv2.resize(img, (0,0), None, (int(width * 0.25), int(height * 0.25)))
#     imgS = cv2.resize(img,(0,0),None,0.25,0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    
#     facesCurFrame = face_recognition.face_locations(imgS)
#     encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)
    
#     for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
#         #print(faceDis)
#         matchIndex = np.argmin(faceDis)
 
#         if matches[matchIndex]:
#             name = classNames[matchIndex].upper()
#             #print(name)
#             y1,x2,y2,x1 = faceLoc
#             y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
#             cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
#             cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
#             cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
#             markAttendance(name)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break
        
#     cv2.imshow('Webcam',img)
#     cv2.waitKey(1)

# import cv2
# import numpy as np
# import face_recognition
# import os
# from datetime import datetime

# # Path where images are stored
# path = 'ImagesAttendance'
# images = []
# classNames = []
# myList = os.listdir(path)
# print(myList)

# # Load images and class names
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])
# print(classNames)

# # Function to encode all known images
# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList

# # Function to mark attendance in CSV
# def markAttendance(name):
#     today = datetime.now().strftime('%Y-%m-%d')  # current date
#     with open('Attendance.csv', 'a+') as f:
#         f.seek(0)  # Go to start to read existing data
#         myDataList = f.readlines()
#         nameDateList = []

#         for line in myDataList:
#             entry = line.strip().split(',')
#             if len(entry) >= 3:
#                 nameDateList.append((entry[0], entry[2]))  # (name, date)

#         # Add only if not already present today
#         if (name, today) not in nameDateList:
#             now = datetime.now()
#             dtString = now.strftime('%H:%M:%S')
#             f.write(f'{name},{dtString},{today}\n')

# # Encode known images
# encodeListKnown = findEncodings(images)
# print('Encoding Complete')

# # Start webcam
# cap = cv2.VideoCapture(0)

# # Keep track of people already marked in this session
# marked_this_session = set()

# while True:
#     success, img = cap.read()
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     facesCurFrame = face_recognition.face_locations(imgS)
#     encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#     for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#         matchIndex = np.argmin(faceDis)

#         if matches[matchIndex]:
#             name = classNames[matchIndex].upper()

#             # Avoid duplicate entries in the same session
#             if name not in marked_this_session:
#                 markAttendance(name)
#                 marked_this_session.add(name)

#             # Draw rectangle & name on face
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, name, (x1 + 6, y2 - 6),
#                         cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     cv2.imshow('Webcam', img)
#     cv2.waitKey(1)

# import cv2
# import numpy as np
# import face_recognition
# import os
# from datetime import datetime, timedelta

# # Path where images are stored
# path = 'ImagesAttendance'
# images = []
# classNames = []
# myList = os.listdir(path)
# print(myList)

# # Load images and class names
# for cl in myList:
#     curImg = cv2.imread(f'{path}/{cl}')
#     images.append(curImg)
#     classNames.append(os.path.splitext(cl)[0])
# print(classNames)

# # Function to encode all known images
# def findEncodings(images):
#     encodeList = []
#     for img in images:
#         img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         encode = face_recognition.face_encodings(img)[0]
#         encodeList.append(encode)
#     return encodeList

# # Function to mark attendance in CSV
# def markAttendance(name):
#     today = datetime.now().strftime('%Y-%m-%d')  # current date
#     with open('Attendance.csv', 'a+') as f:
#         f.seek(0)
#         myDataList = f.readlines()
#         nameDateList = []

#         for line in myDataList:
#             entry = line.strip().split(',')
#             if len(entry) >= 3:
#                 nameDateList.append((entry[0], entry[2]))  # (name, date)

#         now = datetime.now()
#         dtString = now.strftime('%H:%M:%S')

#         # Always allow writing if it's the first time today
#         if (name, today) not in nameDateList:
#             f.write(f'{name},{dtString},{today}\n')
#             return True
#         else:
#             # Allow multiple entries per day if time gap met
#             last_time = None
#             for line in reversed(myDataList):
#                 parts = line.strip().split(',')
#                 if len(parts) >= 3 and parts[0] == name and parts[2] == today:
#                     last_time = datetime.strptime(parts[1], '%H:%M:%S')
#                     break
            
#             if last_time:
#                 if datetime.now() - last_time >= timedelta(minutes=5):
#                     f.write(f'{name},{dtString},{today}\n')
#                     return True
#         return False

# # Encode known images
# encodeListKnown = findEncodings(images)
# print('Encoding Complete')

# # Start webcam
# cap = cv2.VideoCapture(0)

# # Keep track of last marked time in session
# last_seen_time = {}

# while True:
#     success, img = cap.read()
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     facesCurFrame = face_recognition.face_locations(imgS)
#     encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

#     for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
#         matchIndex = np.argmin(faceDis)

#         if matches[matchIndex]:
#             name = classNames[matchIndex].upper()
#             now = datetime.now()

#             # Only mark if first time OR 5 minutes passed since last mark
#             if (name not in last_seen_time) or (now - last_seen_time[name] >= timedelta(minutes=5)):
#                 if markAttendance(name):
#                     last_seen_time[name] = now

#             # Draw rectangle & name
#             y1, x2, y2, x1 = faceLoc
#             y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
#             cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
#             cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
#             cv2.putText(img, name, (x1 + 6, y2 - 6),
#                         cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     cv2.imshow('Webcam', img)
#     cv2.waitKey(1)
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime, timedelta

# Configurable gap between two entries for the same person (in minutes)
ATTENDANCE_GAP_MINUTES = 5

# Path where images are stored
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print("Images found:", myList)

# Load images and class names
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print("Class names:", classNames)

# Function to encode all known images
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# Function to check CSV for today's last marked time
def getLastMarkedTime(name):
    today = datetime.now().strftime('%Y-%m-%d')
    last_time = None
    if os.path.exists('Attendance.csv'):
        with open('Attendance.csv', 'r') as f:
            for line in f.readlines():
                parts = line.strip().split(',')
                if len(parts) >= 3 and parts[0] == name and parts[2] == today:
                    last_time = datetime.strptime(parts[1], '%H:%M:%S')
    return last_time

# Function to mark attendance in CSV
def markAttendance(name):
    today = datetime.now().strftime('%Y-%m-%d')
    now_time = datetime.now().strftime('%H:%M:%S')
    with open('Attendance.csv', 'a') as f:
        f.write(f'{name},{now_time},{today}\n')

# Encode known images
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Start webcam
cap = cv2.VideoCapture(0)

# Store last marked time in memory for quick checks
last_seen_time = {}

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            now = datetime.now()

            # Get last marked time (from memory or CSV)
            last_time = last_seen_time.get(name) or getLastMarkedTime(name)

            # If first time today or gap passed → mark attendance
            if (last_time is None) or (now - last_time >= timedelta(minutes=ATTENDANCE_GAP_MINUTES)):
                markAttendance(name)
                last_seen_time[name] = now
                print(f"Marked attendance for {name} at {now.strftime('%H:%M:%S')}")

            # Draw rectangle & name
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    cv2.imshow('Webcam', img)
    cv2.waitKey(1)
