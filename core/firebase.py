import firebase_admin
import os
import json
from firebase_admin import db
import urllib
from datetime import datetime
if "FIREBASE_CREDS" in os.environ:
    firebase_creds = os.getenv("FIREBASE_CREDS")
else:
    configJson = json.loads(open("config.json", "r").read())
    firebase_creds = configJson["FIREBASE_CREDS"]

if "DATABASE_URL" in os.environ:
    databaseURL = os.getenv("DATABASE_URL")
else:
    configJson = json.loads(open("config.json", "r").read())
    databaseURL = configJson["DATABASE_URL"]
response = urllib.request.urlopen(firebase_creds)
firebase_creds = json.loads(response.read())
cred_obj = firebase_admin.credentials.Certificate(firebase_creds)
default_app = firebase_admin.initialize_app(cred_obj, {
    'databaseURL': databaseURL
})


def startChallenge(user):
    ref = db.reference("/challengers/"+str(user.id))
    #  check if the user has already been added
    if ref.get():
        events = ref.child("events").get()
        events.append({
            "type": "Start Command",
            "time": str(datetime.now())})
        ref.child("events").set(events)
    else:
        ref.set({
            "name": user.name,
            "created_at": str(user.created_at),
            "discriminator": user.discriminator,
            "mention": user.mention,
            "avatar": str(user.avatar),
            "avatar_url": str(user.avatar_url),
            "events": [{
                "type": "Start Command",
                "time": str(datetime.now())}],
        })


def submittedSuccessfully(user, code, part_number):
    if not code:
        code = "First_Hint"
    ref = db.reference("/challengers/"+str(user.id))
    #  check if the user has already been added
    participant = ref.get()
    if participant:
        events = ref.child("events").get()
        events.append({
            "type": "Hint Submitted Successfully",
            "code": code,
            "time": str(datetime.now())
        })
        if "score" not in participant:
            ref.child("score").set(part_number)
        else:
            if participant["score"] < part_number:
                ref.child("score").set(part_number)
        ref.child("events").set(events)
    else:
        ref.set({
            "name": user.name,
            "created_at": str(user.created_at),
            "discriminator": user.discriminator,
            "mention": user.mention,
            "avatar": str(user.avatar),
            "avatar_url": str(user.avatar_url),
            "score": part_number,
            "events": [{
                "code": code,
                "time": str(datetime.now())
            }]
        })


def validatedCode(user, code, correct):
    ref = db.reference("/challengers/"+str(user.id))
    #  check if the user has already been added
    participant = ref.get()
    if participant:
        events = ref.child("events").get()
        events.append({
            "type": "Submission Full Code",
            "code": code,
            "correct": correct,
            "time": str(datetime.now())
        })
        ref.child("events").set(events)
        if correct:
            ref.child("Winner").set(True)
            if "won_at" not in participant:
                ref.child("won_at").set(str(datetime.now()))
                return False
            else:
                return True

    else:
        ref.set({
            "name": user.name,
            "created_at": str(user.created_at),
            "discriminator": user.discriminator,
            "mention": user.mention,
            "avatar": str(user.avatar),
            "avatar_url": str(user.avatar_url),
            "events": [{
                "code": code,
                "correct": correct,
                "time": str(datetime.now())
            }],
        })
        return False


def show_leaderboard():
    ref = db.reference("/challengers")
    participants = ref.get()
    for participant in participants:
        print(participant.child('won_at').get())
