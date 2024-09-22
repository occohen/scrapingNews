import pymongo
import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv

#load env vars
load_dotenv()

uri = os.getenv('DB_URI') # Make sure to create environment variable with the app-specific URI 
client = MongoClient(uri, server_api=ServerApi('1'))

db = client["Articles"] # open the client to the database called "Articles" 
collection = db["CNN"]  # open the collection - "CNN"

#add the directory in which you want to drop the .txt files 
txt_files_directory = 'files' 

# Loop through each file in the directory
for filename in os.listdir(txt_files_directory):
    if filename.endswith('.txt'): 

        #get the file's path if it is a txt
        file_path = os.path.join(txt_files_directory, filename)
        
        # Read the contents of the .txt file
        with open(file_path, 'r', encoding='utf-8') as file:
            storyname = file.readline().rstrip("\n")
            file_content = file.read()
        
        # Prepare the document for MongoDB
        document = {
            "storyname": storyname,
            "content": file_content
        }
        
        # Insert the document into the MongoDB collection
        collection.insert_one(document)
        print(f"Inserted: {filename}")

print("All files have been inserted.")
