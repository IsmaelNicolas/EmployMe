from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
import pymongo
from pydantic import BaseModel
from typing import List
import os

app = FastAPI()
mongodb_uri = os.environ.get("MONGODB_URI")
if not mongodb_uri:
    raise ValueError("MONGODB_URI environment variable not set")

# MongoDB configuration
client = MongoClient(
       mongodb_uri
    )
db = client["microservices"]
messages_collection = db["messages"]
user_collection = db["users"]
# Pydantic model for message


class MessageCreate(BaseModel):
    sender_id: str
    reciver_id: str
    content: str


class Message(MessageCreate):
    id: str

# API endpoint to create a new message


@app.post("/messages/", response_model=Message)
def create_message(message: MessageCreate):
    message_data = message.dict()

    inserted = messages_collection.insert_one(message_data)
    message_data['id'] = str(inserted.inserted_id)
    return message_data

# API endpoint to retrieve a specific message by ID


@app.get("/messages/{message_id}", response_model=Message)
def get_message(message_id: str):
    message = messages_collection.find_one({"_id": message_id})
    if message:
        message['id'] = str(message['_id'])
        return message
    raise HTTPException(status_code=404, detail="Message not found")

# API endpoint to get all the chat messages of a particular user with another user


@app.get("/messages/{reciver_id}/{sender_id}")
def get_chat(reciver_id, sender_id):
    try:
        messages = list(messages_collection.find(
            {"reciver_id": reciver_id,  "sender_id": sender_id}))
        if not messages:
            messages = list(messages_collection.find(
            {"reciver_id": sender_id,  "sender_id": reciver_id}))
        
        for message in messages:
            message['_id'] = str(message['_id'])
        return messages

    except:
        raise HTTPException(
            status_code=500, detail="Error while retriving chat")
