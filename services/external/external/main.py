from typing import Optional

from fastapi import FastAPI

from pydantic import BaseModel
import requests

import external.messages as messages

import random

import time


import logging

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.Logger(__name__)


class ExternalRequest(BaseModel):
    patientId: str
    description: str
    processInstanceId: str


def sendRequestToSiddhi(json: dict) -> None:
    requests.post(
        url="http://siddhi.local:8283/external",
        json=json,
        headers={"Content-Type": "application/json"},
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/external/patient/")
async def external(externalRequest: ExternalRequest):

    # Print new line for readability
    print("")

    jsonObj = {
        "patientId": externalRequest.patientId,
        "description": externalRequest.description,
        "processInstanceId": externalRequest.processInstanceId,
        "value": "",
    }

    # Api is too fast
    time.sleep(1)

    if externalRequest.description == messages.KETOACIDOSIS_EVAL_RISK:
        if externalRequest.patientId == "A":
            jsonObj["value"] = "True"
        elif externalRequest.patientId == "B":
            jsonObj["value"] = "False"
        else:
            randomBit = bool(random.getrandbits(1))
            level = "True" if randomBit else "False"
            jsonObj["value"] = level
            print(jsonObj["value"])

        sendRequestToSiddhi(jsonObj)

    elif (
        externalRequest.description
        == messages.KETOACIDOSIS_MEASURE_KETONE_CONCENTRATION
    ):
        var = random.random()
        randomConcentration = float(var) * float(10)
        jsonObj["value"] = randomConcentration

        sendRequestToSiddhi(jsonObj)

    elif externalRequest.description == messages.KETOACIDOSIS_CALL_DOCTOR_NOTIFICATION:
        print("Calling doctor...")

        sendRequestToSiddhi(jsonObj)

    elif externalRequest.description == messages.HYPOGLYCEMIA_SEND_NOTIFICATION_EAT:
        print("Received eat food Notification")

        # To send or not to send
        if bool(random.getrandbits(1)):
            print("\tReplying")
            jsonObj["description"] = messages.HYPOGLYCEMIA_RECORD_FOOD_EATEN
            sendRequestToSiddhi(jsonObj)

        else:
            print("\tNot replying")

    elif (
        externalRequest.description == messages.HYPOGLYCEMIA_SEND_NOTIFICATION_GLUCAGON
    ):
        print("Received inject glucagon Notification")

        # To send or not to send
        if bool(random.getrandbits(1)):
            print("\tReplying")
            jsonObj["description"] = messages.HYPOGLYCEMIA_RECORD_GLUCAGON_INJECTION
            sendRequestToSiddhi(jsonObj)

        else:
            print("\tNot replying")

    elif (
        externalRequest.description
        == messages.HYPERGLYCEMIA_NOTIFICATION_HIGH_BLOOD_SUGAR
    ):
        print("Received Notify patient about high blood sugar notification")

        # To send or not to send
        if bool(random.random() > 0.2):
            jsonObj[
                "description"
            ] = messages.HYPERGLYCEMIA_SEND_NOTIFICATION_BLOOD_SUGAR_MEASUREMENT

            # Glucose too high or glucose normal
            if bool(random.random() > 0.25):
                print("\tReplying High Glucose")
                jsonObj["value"] = "10.0"
            else:
                print("\tReplying Low Glucose")
                jsonObj["value"] = "7.0"

            print(jsonObj)
            sendRequestToSiddhi(jsonObj)

        else:
            print("\tNot replying")
    elif (
        externalRequest.description
        == messages.HYPERGLYCEMIA_NOTIFY_PATIENT_TAKE_INSULIN
    ):
        print("Received notification to inject insulin!")
        # To send or not to send
        if bool(random.random() > 0.2):
            print("\tReplying")
            jsonObj["description"] = messages.HYPERGLYCEMIA_SEND_INSULIN_INJECTED
            sendRequestToSiddhi(jsonObj)

        else:
            print("\tNot replying")
    elif (
        externalRequest.description
        == messages.GENERATE_REPORT_PATIENT_NOTIFIED
    ):
        print("Received notification about report being generated with priority")
    elif (
        externalRequest.description
        == messages.GENERATE_REPORT_PATIENT_NOTIFIED_NON_PRIOR
    ):
        print("Received notification about report being generated without priority")

    # Print new line for readability
    print("")


@app.post("/external/doctor/")
async def doctor(externalRequest: ExternalRequest):
    # Log the info

    if (
        externalRequest.description
        == messages.KETOACIDOSIS_DOCTOR_NOTIFICATION_KETOACIDOSIS
    ):
        print(messages.KETOACIDOSIS_DOCTOR_NOTIFICATION_KETOACIDOSIS)
    elif (
        externalRequest.description
        == messages.KETOACIDOSIS_HIGH_KETONE_MEASUREMENT_DOCTOR_NOTIFICATION
    ):
        print(messages.KETOACIDOSIS_HIGH_KETONE_MEASUREMENT_DOCTOR_NOTIFICATION)
    elif externalRequest.description == messages.HYPOGLYCEMIA_NOTIFY_MEDICAL_EXPERT:
        print(messages.HYPOGLYCEMIA_NOTIFY_MEDICAL_EXPERT)
    # Print new line for readability
    print("")
    return {"patientId": externalRequest.patientId}
