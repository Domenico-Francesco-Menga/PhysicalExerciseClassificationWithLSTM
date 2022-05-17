import numpy as np
import cv2
import mediapipe as mp
import angleSquat
from time import ctime

def log (eventName):
  with open("logFile.txt","a+") as logFile:
    try:
      logFile.write("["+str(ctime())+"]"+"  "+eventName+"\n")
    except:
      pass

def writeFile(nameFile,typeFile,listOfListOfAngle):
  with open(nameFile+typeFile+".txt","a+") as file:
    try:
      for row in listOfListOfAngle:
        file.write(str(row) + "\n")

      log(f"Scittura su file {nameFile+typeFile+'.txt'} eseguita")
    except:
      log(f"Errore in scrittura file {nameFile+typeFile+'.txt'}")
      pass




def createTarget(numberOfRow,typeOfClass):
  listOflist = list()
  row = 0
  while row < numberOfRow:
    if typeOfClass == "squat":
      listOflist.append([1.0,0.0,0.0,0.0,0.0,0.0])
    elif typeOfClass == "affondiFrontali":
      listOflist.append([0.0, 1.0, 0.0, 0.0, 0.0, 0.0])
    elif typeOfClass == "jumpSquat":
      listOflist.append([0.0, 0.0, 1.0, 0.0, 0.0, 0.0])
    elif typeOfClass == "recupero":
      listOflist.append([0.0, 0.0, 0.0, 1.0, 0.0, 0.0])
    elif typeOfClass == "bicipiti":
      listOflist.append([0.0, 0.0, 0.0, 0.0, 1.0, 0.0])
    elif typeOfClass == "alzateLaterali":
      listOflist.append([0.0, 0.0, 0.0, 0.0, 0.0, 1.0])
    row +=1
  return listOflist

#dict with key = ex name and value =  number of videos for that ex type
typeOfExerciseTraining = {
  "squat": 18,  #
  "affondiFrontali": 17,
  "jumpSquat" : 23,
  "recupero": 7,
  "bicipiti": 11,
  "alzateLaterali": 17
}
typeOfExerciseTest = {
  "squat": 6,  #
  "affondiFrontali": 5,
  "jumpSquat" : 7,
  "recupero": 3,
  "bicipiti":4,
  "alzateLaterali": 5
}
typeOfExerciseValidation = {
  "squat": 2,  #
  "affondiFrontali": 2,
  "jumpSquat" : 3,
  "recupero": 1,
  "bicipiti":2,
  "alzateLaterali": 2
}


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose  # dichiarazione di uso del modello di pose estimation
lisaAngoli = list()
listOfListOfAngle = list()
numberOfFrame = 0
emptyList = [0.0]*12

for isFlip in range(0,2):
  ##########################################################################
  ####################### FOR PER IL VALIDATION SET #########################
  ##########################################################################

  for key in typeOfExerciseValidation:
    for index in range(1, typeOfExerciseValidation[key] + 1):
      videoPath = r"C:\Users\menga\OneDrive\Desktop\VideoEsercizi"
      videoPath = videoPath + "\\" + key + "\\" + "validation"+ "\\" + key + str(index) + ".mp4"
      if isFlip == 0:
        nameFile = key + str(index)
      else:
        nameFile = key +"Flipped"+ str(index)
      print(videoPath)
      cap = cv2.VideoCapture(videoPath)

      with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
          while cap.isOpened():
            ret, frame = cap.read()

            if isFlip == 0:
              frame = cv2.flip(frame, 1)

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # conversione dell'frame da BGR to RGB
            results = pose.process(image)  # process dell' array RGB , ritorna un array

            if results.pose_landmarks:
              landmarks = results.pose_landmarks.landmark
              listaAngoli = angleSquat.getAllAngle(landmarks, mp_pose)
              #print(listaAngoli)
              listOfListOfAngle.append(listaAngoli)


            #numberOfFrame += 1
        except:
            pass

    # Il codice sottostante verifica che prendendo matrici 35x12 con una differenza di 3 frame tra due matrici non si vadano a creare matrici cobn meno righe,
    # se dal calcolo del modulo risulta una situazione tale => aggiungo righe = 0.0
    numberOfFrame = len(listOfListOfAngle)
    tempNumbOfFrame = numberOfFrame - 35
    rowToAdd = 0
    if tempNumbOfFrame % 3 != 0:
      if tempNumbOfFrame % 3 == 1:
        rowToAdd = 2
      elif tempNumbOfFrame % 3 == 2:
        rowToAdd = 1

      # ciclo per il numero di righe da aggiungere per rendere tempNumbOfFrame divisibile per 3
      for j in range(0, (rowToAdd)):
        listOfListOfAngle.append(emptyList)

    # scrittura su file degli esempi di training
    writeFile(nameFile, "Training", listOfListOfAngle)

    # conteggio output e scrittura su file
    numeroOutput = ((len(listOfListOfAngle) - 35) / 3) + 1
    listOfTarget = createTarget(numeroOutput, key)
    writeFile(nameFile, "Target", listOfTarget)

    # clear delle liste
    listOfTarget.clear()
    listOfListOfAngle.clear()


log("############################ FINE SCRITTURA ###################################")
