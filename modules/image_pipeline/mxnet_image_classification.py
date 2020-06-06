#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 6 14:41:37 2018

@author: "Anirban Das"
"""

import sys, csv
import os
import load_model
import cv2
import json
from iothub_client import IoTHubMessage
from timeit import default_timer as timer
import datetime, logging
import cifar10 as data

logging.basicConfig(format='%(asctime)s %(name)-20s %(levelname)-5s %(message)s')

# Initialize global variables -----------------------------------------------------------
# We don't use ImageNet pictures any more
#IMAGE_DIRECTORY = os.getenv('IMAGE_DIRECTORY', default='/home/moduleuser/Images')
STATS_DIRECTORY = os.getenv('STATS_DIRECTORY', default='/home/moduleuser/Statistics')
model_path = './mxnet_models/squeezenetv1.1/'
global_model = load_model.ImagenetModel(model_path + 'synset.txt', model_path + 'squeezenet_v1.1')  
SEND_CALLBACKS = 0

csvfilename = "Image_recognition_local_stats_{}_{}.csv".format(str(datetime.datetime.now().date()), "Azure")

# Get all the file paths from the directory specified
def get_file_paths(dirname):
    file_paths = []  
    for root, directories, files in os.walk(dirname):
        for filename in files:
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  
    return file_paths

# write local stats in a csv file
def write_local_stats(filename, stats_list):
    global STATS_DIRECTORY
    try:
        filepath = STATS_DIRECTORY.rstrip(os.sep) + os.sep + filename
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))
        with open(filepath, 'w') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(stats_list)
    except :
        e = sys.exc_info()[0]
        filepath = STATS_DIRECTORY.rstrip(os.sep) + os.sep + filename
        print(filepath)
        print("Exception occured during writting Statistics File: %s" % e)        
        #sys.exit(0)

def stall_for_connectivity():
    import time
    """
        Implements a stalling function so that message
        sending starts much after edgeHub is initialized
    """
    if os.getenv('STALLTIME'):
        stalltime=int(os.getenv('STALLTIME'))
    else:
        stalltime=60
    print("Stalling for {} seconds for all TLS handshake and other stuff to get done!!! ".format(stalltime))
    for i in range(stalltime):
        print("Waiting for {} seconds".format(i))
        time.sleep(1)
    print("\n\n---------------Will Start in another 5 seconds -------------------\n\n")
    time.sleep(5)

# changed the 'reshape' parameter
#def mxnet_image_classification(outputQueueName, hubManager, callback_function, context, N=5, reshape=(224, 224)):
def mxnet_image_classification(outputQueueName, hubManager, callback_function, context, N=5, reshape=(32, 32)):
    #global IMAGE_DIRECTORY # only for ImageNet
    global global_model
    global csvfilename
    stall_for_connectivity()
    if global_model is not None:
        try:
            #all_file_paths = get_file_paths(IMAGE_DIRECTORY) # only for ImageNet 
            '''
            local_stats = [['filename', 'payloadsize', 'imagefilesize', 'imagefileobjectsize',
                        'imagewidth', 'imageheight','count',
                        'f_t0','f_t1','f_t2','f_t3','f_t4', 'f_t5']]
            '''
            local_stats = [['payloadsize', 
                        'imagewidth', 'imageheight','count',
                        'f_t0','f_t1','f_t2','f_t3','f_t4', 'f_t5']]
            
            count = 1
            all_images = data.get_CIFAR10_data()
            for index, im in enumerate(all_images):
            #for filepath in all_file_paths: # only for ImageNet
                f_t0 = timer()
                dictionary = {}
                # no longer need to keep track of filename
                #filename = filepath.split(os.sep)[-1]
                
                # Read the image from the folder
                f_t1 = timer()
                #im = cv2.imread(filepath) # only for ImageNet
                length, width = im.shape[0:2]
                f_t2 = timer()
                                
                # Predict the classification from the image
                prediction = global_model.predict_from_image(im, reshape, N)
                f_t3 = timer()

                # Create the Payload JSON with the necessary fields
                for idx, elem in enumerate(prediction):
                    temp_dict = {}
                    temp_dict["probability"] = float(elem[0])
                    temp_dict["wordnetid"], temp_dict["classification"] = elem[1].split(" ", 1)                    
                    dictionary["classification_{}".format(idx)] = temp_dict
                # no longer need to keep track of filename
                # dictionary["imagefilename"] = filename
                dictionary["messagesendutctime"] = datetime.datetime.utcnow().isoformat()
                json_payload = json.dumps(dictionary)
                f_t4 = timer()
               
                # Publish the Payload in the specific topic
                message = IoTHubMessage(bytearray(json_payload, 'utf8'))
                hubManager.client.send_event_async(outputQueueName, message, callback_function, 0)
                
                f_t5 = timer()
                print("All procedure for {} done in {} seconds. \n".format(index, f_t5 - f_t0))
                #print("All procedure for {} done in {} seconds. \n".format(filename, f_t5 - f_t0))
                '''
                local_stats.append([filename, sys.getsizeof(json_payload), os.path.getsize(filepath), *some_method_i_don_t_remember, 
                            width, length, count, 
                            f_t0, 
                            f_t1, 
                            f_t2, 
                            f_t3, 
                            f_t4,
                            f_t5])

                '''
                local_stats.append([sys.getsizeof(json_payload), 
                            width, length, count, 
                            f_t0, 
                            f_t1, 
                            f_t2, 
                            f_t3, 
                            f_t4,
                            f_t5])

                # write local stats to csv file
                if count%200==0:
                    write_local_stats(csvfilename, local_stats)
                    local_stats = []
                count+=1
        except :
            e = sys.exc_info()[0]
            print("Exception occured during prediction: %s" % e)        
            sys.exit(0)

        finally:
            write_local_stats(csvfilename, local_stats)
