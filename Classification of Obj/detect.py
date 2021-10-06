
import cv2
import csv
import boto3
import time
import pyttsx3
import keyboard

# computer voice initializing and settings for rate of speech, volume and female voice

engine = pyttsx3.init()
engine.setProperty('rate', 125) 
engine.setProperty('volume',1)
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)


# Reads in user credentials for amaxon rekognition API
with open("new_user_credentials.csv","r") as input:
        next(input)
        reader = csv.reader(input)
        for lines in reader:
                ack = lines[2]
                sk = lines[3]
# starts the initiation of AR API
client =boto3.client("rekognition",aws_access_key_id = ack, aws_secret_access_key=sk, region_name='us-west-2')


# selecting webcam 0 as video Read source
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 1)

# While Loop so it always continue streaming
cntr = 0
value = 0
alert = False
while True:


    if keyboard.is_pressed('q'):  # if key 'q' is pressed 
            print('You Pressed A Key!')
            break  # finishing the loop
    if not cap.isOpened():
        print("Cannot open camera")
        exit()  

    time.sleep(.5)

    ret,frame = cap.read()

    cntr = cntr+1
    if value >= 300:
      alert = True
    if ((cntr%1)==0):
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break


        # iterates through all frames captured
        for i in range(0, len(frame)):
            # convert to jpeg and save in variable
            _,image_bytes = cv2.imencode('.jpg', frame)

            # converts frame to bytes so AR can read it
            image_bytes = image_bytes.tobytes()
            
            
            # checks for what labels can be found on the frame
            response = client.detect_labels(Image={'Bytes':image_bytes},MaxLabels=10, MinConfidence=95)
            
            # checks for what text Word can be found on the frame          
            response_text=client.detect_text(Image={'Bytes':image_bytes},Filters={ 'WordFilter': {'MinConfidence':90}})
            textDetections = response_text['TextDetections']

            # list of outcomes to check for that could match what we need in text
            possible_outcomes_text = ["amazon","amazon...","amazon.rr","amazon.co.uk","FedEx","ups","yemeksepeti","Jumia","konga","DHL","getir","etir","ACDI EXPRESS","DSV","Ptt","KARGO","Yemeksepeti","TNT"]
            
            # a dirty control for ringing the alert


            print('Detected text\n----------')
            for text in textDetections:
                        print ('Detected text:' + text['DetectedText'])
                        print()
                        if text[u'DetectedText'] in possible_outcomes_text:
                           print("-----> Detected Word {} ".format(text[u"DetectedText"]))
                           value += 50
                           print(value)
                   
            # list of outcomes to check for that could match what we need
            possible_outcomes_labels = ["Package Delivery","Package","Delivery","Courier"]


            for n in response[u"Labels"]:
                print(n[u"Name"])
                if n[u'Name'] in possible_outcomes_labels:
                    print("-----> Detectedlabel {} ".format(n[u"Name"]))
                    value += 50
                    print(value)
            break      
            # ring alert
        if alert == True:
            engine.say("THE POST PERSON HAS ARRIVED, YOU HAVE A PACKAGE AT THE DOOR")
            engine.runAndWait()

        

        


cap.release()




def main():

    print("Finding Post agents ")


if __name__ == "__main__":
    main()