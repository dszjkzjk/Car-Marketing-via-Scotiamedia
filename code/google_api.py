
"""
Created on Tue Mar 26 17:43:21 2019

@author: junkangzhang
"""


from google.cloud import vision
import pandas as pd
import time
import os 

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/A2/My First Project-2725394ab802.json"
df = pd.read_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/url_file.csv')
df = df.drop('Unnamed: 0',axis=1)

def detect_labels_uri(uri):
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations

    return labels


# Count the time
start_time = time.time()

google_tags_list = []      
for url in df['media_url']:
    google_tags = detect_labels_uri(url)
    google_tags_list.append(google_tags)
    
elapsed_time = time.time() - start_time
#print("Total time used in second is {0}".format(str(elapsed_time)))
df['google_api'] = google_tags_list

df_new = df.copy()

df_new['google_api'] = df_new['google_api'].apply(lambda x: [item.description for item in x])
df_new.to_csv('/Users/junkangzhang/Downloads/MMA 2019/Courses/INSY670/Final/google_tags.csv')
