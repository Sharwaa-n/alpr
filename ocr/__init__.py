from google.cloud import vision
import os, re
from os.path import dirname, abspath


class OCR:

    def __init__(self, credFile):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.resolveFilePath(credFile)
        self.client = vision.ImageAnnotatorClient()

    def resolveFilePath(self, name):
        return f'{dirname(abspath(__file__))}/{name}'

    def Process(self, content):
        image = vision.Image(content=content)
        response = self.client.text_detection(image=image)

        texts = response.text_annotations
        # for text in texts:
        #     print('\n -> "{}"'.format(text.description))
        if len(texts) > 0:
            return self.plateNumberFinalize(texts[0].description.replace('\n','').replace(' ', ''))
        
    def plateNumberFinalize(self, str):
        #to remove all characters before the 1st A
        str = re.sub(r'^.*?A','A',str)
        finalPlate = ""
        newCharacter = '0'
        newCharacter2 = '1'
        position = 2
        for character in str:
            #remove all characters except alphanumerics
            if character.isalnum():
                finalPlate += character
        #Replacing 3rd character with 0 if it is either O or D and as 1 if its I or L
        if finalPlate[2] == 'O':
            finalPlate = finalPlate[:position] + newCharacter + finalPlate[position + 1:]
        elif finalPlate[2] == 'o':
            finalPlate = finalPlate[:position] + newCharacter + finalPlate[position + 1:]
        elif finalPlate[2] == 'D':
            finalPlate = finalPlate[:position] + newCharacter + finalPlate[position + 1:]
        elif finalPlate[2] == 'I':
            finalPlate = finalPlate[:position] + newCharacter2 + finalPlate[position + 1:]
        elif finalPlate[2] == 'L':
            finalPlate = finalPlate[:position] + newCharacter2 + finalPlate[position + 1:]

        position1 = None
        #verifying that there is no D and O in the last 4 positions and if present replacing them with 0
        for i in range(6, len(finalPlate)):
            if finalPlate[i] == "O":
                position1 = i
                finalPlate = finalPlate[:position1] + newCharacter + finalPlate[position1 + 1:]
            elif finalPlate[i] == "D":
                position1 = i
                finalPlate = finalPlate[:position1] + newCharacter + finalPlate[position1 + 1:]

        newchar3 = ''
        if len(finalPlate) > 9:
            if finalPlate[5] == 'P':
                finalPlate = finalPlate[:4] + newchar3 + finalPlate[4 + 1:]
            if finalPlate[5] == 'C':
                finalPlate = finalPlate[:4] + newchar3 + finalPlate[4 + 1:]
        # while len(finalPlate) > 9:
        #     finalPlate = finalPlate[:4] + newchar3 + finalPlate[4 + 1:]


        return finalPlate

