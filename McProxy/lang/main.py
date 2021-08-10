import json

class Lang:
    def __init__(self):
         file = open('lang.json', mode='r')
         text = file.readlines()
         self.js = json.loads(text)
