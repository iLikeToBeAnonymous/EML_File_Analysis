# Largely based on my previous file found here:
# https://github.com/iLikeToBeAnonymous/Category_Extraction_From_Product_Names/blob/separate_files/RakeTest_fileLoad.py

import string
import json # json lib for functions and prettifying things.
import re # so you co do regex matching and stuff.
import os # ChatGPT
import email # for parsing .eml files
from email.iterators import _structure
from os import path
from collections import Counter, OrderedDict # ChatGPT

# # Compile the regex used to match the field name
# fieldNmRegex = re.compile("^(?<fieldName>[A-Za-z0-9\-]+):.*$")

# myDir = path.abspath(path.dirname(__file__))
# targetFolder = 'ThunderbirdExports-TESTING'
# targetFilename = 'Mail delivery failed  returning message to sender - Mail Delivery System (Mailer-Daemon@se1-lax1.servconfig.com) - 2022-11-23 1649.eml'

# # JOIN THE THREE SEPARATE COMPONENTS TOGETHER TO MAKE A COMPLETE LITERAL PATH.
# literalPath = path.join(myDir, targetFolder, targetFilename)
# # print('My dir:  ' + literalPath)


# rawData = open(literalPath, 'r') # Opens the source data which contains the text from which to extract keywords

# # #REMEMBER! .read() reads the file as a blob, but readlines() reads the file into an array of strings, each row delimiting a line.
# # myText = rawData.read() # reads the complete source text into a variable
# myText = rawData.readlines()

# myctr = 0 # Set the line counter to zero
# for eachEle in myText:
#     myctr += 1
#     # print("Row " + str(myctr) + ":  " + eachEle)

###############################
### BEGIN CODE FROM ChatGPT ###
def extract_fields(eml_filepath):
    fields = []
    with open(eml_filepath, 'rb') as fileContents:
        msg = email.message_from_binary_file(fileContents)
        for part in msg.walk():
            for field in part.keys():
                fields.append(field)
    return fields

def extract_body(file_path):
    with open(file_path, 'rb') as f:
        msg = email.message_from_binary_file(f)
    body_fields = {}
    for part in msg.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            body_decoded = body.decode()
            # print("var body is of type: " + str(type(body))) # DEBUGGING AND INFO
            # print("var body_decoded is of type:  " + str(type(body_decoded))) # DEBUGGING AND INFO
    # print(str(body_decoded))
    # # print(json.dumps(body_fields, indent=4))
    print('Email addresses found in body: ' + str(re.findall(r'[\w\.-]+@[\w\.-]+', body_decoded)))
    # # print('Sudo fields found in body: ' + str(re.findall(r'\n[\u0020\w]+:', body_decoded)))
    # # print(_structure(msg))
    # print('Sudo-fields found in body: ' + str(re.findall(r'^\w[\u0020\w]+:.*', body_decoded)))

# # DEBUGGING AND TESTING
# def extract_fields(eml_file):
#     with open(eml_file, 'rb') as fileContents:
#         msg = email.message_from_binary_file(fileContents)
#         fields = []

#         if msg.is_multipart():
#             parts = msg.get_payload()
#             # print(parts[1].items())
#             # print(parts[1]['Content-type'])
#             # print(parts[1])
#             for part in parts:
#                 # print(part.items())
#                 # part_headers = part.items()
#                 part_payload = part.get_payload()
#                 # print(part_headers)
#                 print(part_payload)

#         for field in msg.keys():
#             fields.append(field)
#         return fields
# # END DEBUGGING AND TESTING        

# V1 from ChatGPT---------------------------------#
# def analyze_folder(folder):
#     fields_list = []
#     for eml_file in os.listdir(folder):
#         if eml_file.endswith('.eml'):
#             fields = extract_fields(os.path.join(folder, eml_file))
#             fields_list.extend(fields)
#     return fields_list
#-------- End V1 ---------------------------------#

# V2 from ChatGPT---------------------------------#
# def analyze_folder(folder):
#     fields_list = []
#     for eml_file in os.listdir(folder):
#         if eml_file.endswith('.eml'):
#             fields = extract_fields(os.path.join(folder, eml_file))
#             fields_list.extend(fields)
#     return Counter(fields_list)
#-------- End V2 ---------------------------------#

# V3 from ChatGPT---------------------------------#
def analyze_folder(folder):
    fields_list = []
    # DEPLOYMENT (ALL FILES IN FOLDER)
    for eml_file in os.listdir(folder):
        if eml_file.endswith('.eml'):
            fields = extract_fields(os.path.join(folder, eml_file))
            fields_list.extend(fields)
    # END DEPLOYMENT SECTION

    # # BEGIN TESTING OF SINGLE FILE (MINE) #
    # eml_file = os.listdir(folder)[5]
    # print(eml_file) # EML file name
    # fields = extract_fields(os.path.join(folder, eml_file))
    # fields_list.extend(fields)
    # # END TESTING OF SINGLE FILE (MINE)   #

    #----- Begin test of extract_body() -----#
            print(extract_body(os.path.join(folder, eml_file)))
    #------ End test of extract_body() ------#

    fields_counter = Counter(fields_list)
    fields_dict = {}
    for field, count in fields_counter.items():
        fields_dict[field] = count
    return fields_dict
#-------- End V3 ---------------------------------#

# folder = '/path/to/folder' # Original from ChatGPT. Below is my version.
#------------------BEGIN MINE ---------------------#
myDir = path.abspath(path.dirname(__file__)) # mine
targetFolder = 'ThunderbirdExports-TESTING' # mine
folder_path = path.join(myDir, targetFolder) # mine
#------------------ END MINE ----------------------#

# # Below two lines work with analyze_folder V1 and V2
# fields_list = analyze_folder(folder_path) 
# print(fields_list)

# Below two lines work with analyze_folder V3
fields_dict = analyze_folder(folder_path)
# print(json.dumps(fields_dict, indent=4))
# _______________________________________________________
# Replaced the version of the above line with a sorting option
# See https://www.geeksforgeeks.org/python-sort-python-dictionaries-by-key-or-value/
sorted_vs = OrderedDict(sorted(fields_dict.items()))
# print(json.dumps(sorted_vs, indent=4))

