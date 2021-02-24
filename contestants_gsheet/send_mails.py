#!/usr/bin/env python3
import os
from sendgrid.helpers.mail import Mail
from sendgrid import SendGridAPIClient
from  config import HASHCODE_EMAIL_TOKEN,HASHCODE_TEMPLATE_ID


def SendDynamic(participants):
    """ Send a dynamic email to a list of email addresses

    :returns API response code
    :raises Exception e: raises an exception """

    try:
        sg = SendGridAPIClient(HASHCODE_EMAIL_TOKEN)
    except Exception as e:
        print("Error: {0}".format(e))
        return 
    
    # from address we pass to our Mail object, edit with your name
    FROM_EMAIL = 'gdg.algiers@esi.dz'
    print(participants)
    participants_dict = {}
    for key,_, mail,name, last_name,team_name in participants:
        participants_dict.setdefault(team_name, []).append((mail,key,last_name, name))
    for team_name in participants_dict.keys():
        # list of emails and preheader names, update with yours
        TO_EMAILS = [(member[0], member[2]+ " "+ member[3]) for member in participants_dict[team_name]]
        # create Mail object and populate
        message = Mail(
            from_email=FROM_EMAIL,
            to_emails=TO_EMAILS)
        # pass custom values for our HTML placeholders
        message.dynamic_template_data = {
            'subject': 'Testing Hashcode mail',
            'place': 'GDG Algiers',
            'participant_uuid':participants_dict[team_name][0][1],
            'team_name':team_name
        }
        message.template_id = HASHCODE_TEMPLATE_ID
        # create our sendgrid client object, pass it our key, then send and return our response objects
        try:
            print("MESSSSAAAAGGGGEEE")
            print(message)
            response = sg.send(message)
            code, body, headers = response.status_code, response.body, response.headers
            print(f"Response code: {code}")
            print(f"Response headers: {headers}")
            print(f"Response body: {body}")
            print("Dynamic Messages Sent!")
        except Exception as e:
            print("Error: {0}".format(e))

