import sys
import os
import io
import logging
import json
import greengrasssdk
import RPi.GPIO as GPIO
import pygame
from pygame.locals import *
import pygame.camera
import pygame.image
import boto3
import numpy as np
import time
from PIL import Image

CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080
DEVICE_ID = '/dev/video0'
IOT_DEVICE_NAME = 'AIKegerator'

gg_client = greengrasssdk.client('iot-data')
logger = logging.getLogger()

# This endpoint is pointed at tanmcrae@ local sagemaker endpoint currently.
SAGEMAKER_ENDPOINT = 'endpoint_defined_in_sagemaker'
SOLENOID_PIN = 18

# Configuration settings
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOLENOID_PIN, GPIO.OUT)
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
logger.setLevel(logging.INFO)

# Pygame requires a graphic environment to be enabled but we can just use a dummy screen to trick it. 
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.camera.init()
camera = pygame.camera.Camera(DEVICE_ID, (CANVAS_WIDTH, CANVAS_HEIGHT))

sm = boto3.client('sagemaker-runtime', region_name='us-east-1')


def pour_drink(event, context):
    logger.info('Pour drink function called, params: event={} & context={}'.format(event, context))
    status = 'COMPLETE'
    try:
        # Start pouring
        GPIO.output(SOLENOID_PIN, 0)
        # If valve open for more than 9 seconds, it's probably spilling
        timeout = 10
        timeout_start = time.time()
        while time.time() < timeout_start + timeout:
            image = capture_image()
            logger.info('captured image')
            prediction = get_prediction(image)
            logger.info('prediction is {}'.format(prediction))
            # If Prediction is 0 then it's full. If 1 then it's considered empty.
            if prediction == 1:
                break
    except Exception as e:
        status = 'FAILURE'
        logger.info('Failed to open solenoid with message: {}'.format(str(e)))
    finally:
        # Need to ensure the solenoid valve closes regardless of what happens in the loop
        logger.info('Closing solenoid valve')
        GPIO.output(SOLENOID_PIN, 1)


    logger.info('Emit completion message back to cloud')
    gg_client.publish(
        topic='aikegerator/{}/solenoid/response'.format(IOT_DEVICE_NAME),
        payload=json.dumps({
            'amount_poured': '280',
            'Status': status
        }).encode()
    )
    return

def get_prediction(image):
    start = time.time()

    logger.info('About to convert image to bytes')
    output = io.BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)

    logger.info('About to make sagemaker prediction')
    response = sm.invoke_endpoint(
        EndpointName=SAGEMAKER_ENDPOINT,
        Body=output,
        ContentType='image/jpeg'
    )
    logger.info('sagemaker took {}'.format(time.time()-start))
    result = response['Body'].read()
    result = json.loads(result)

    # the result will output the probabilities for all classes
    # find the class with maximum probability and print the class index
    logger.info('Probabilities: {}'.format(result))
    index = np.argmax(result)
    return int(index)


def capture_image(): 
    camera.start()
    pygame_surface = camera.get_image()
    camera.stop()

    pil_string_image = pygame.image.tostring(pygame_surface, 'RGB', False)
    image = Image.frombytes('RGB', (CANVAS_WIDTH, CANVAS_HEIGHT), pil_string_image)
    return image
