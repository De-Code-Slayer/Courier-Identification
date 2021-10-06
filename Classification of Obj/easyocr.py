# import csv
# import boto3

# with open("new_user_credentials.csv","r") as input:
#         next(input)
#         reader = csv.reader(input)
#         for lines in reader:
#                 ack = lines[2]
#                 sk = lines[3]

# photo = "_104765502_amazonparcel.jpg"
# client =boto3.client("rekognition",aws_access_key_id = ack, aws_secret_access_key=sk, region_name='us-west-2')
# with open(photo,"rb") as source_image:
#         sbyte = source_image.read()

# # response = client.detect_labels(Image={'Bytes':sbyte},MaxLabels=10, MinConfidence=95)
# response=client.detect_text(Image={'Bytes':sbyte})

# textDetections=response['TextDetections']


# print('Detected text\n----------')
# for text in textDetections:
#             print ('Detected text:' + text['DetectedText'])
#             print ('Confidence: ' + "{:.2f}".format(text['Confidence']) + "%")
#             print ('Id: {}'.format(text['Id']))
#             if 'ParentId' in text:
#                 print ('Parent Id: {}'.format(text['ParentId']))
#             print ('Type:' + text['Type'])
#             print()
# print( len(textDetections))



import pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 125) 

engine.setProperty('volume',1)
voices = engine.getProperty('voices') 
engine.setProperty('voice', voices[1].id)
engine.say("THE POST PERSON HAS ARRIVED, YOU HAVE A PACKAGE AT THE DOOR")

engine.runAndWait()