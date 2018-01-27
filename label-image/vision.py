from google.cloud import vision
from google.cloud.vision import types
from urllib import request

# Instantiates a client
client = vision.ImageAnnotatorClient()

def label_image(event, context):
	web_file = request.urlopen(event['uri']).read()
	image = types.Image(content=web_file)
	response = client.label_detection(image=image)
	labels = response.label_annotations
	return labels

if __name__ == '__main__':
	print(label_image({'uri': 'https://i0.wp.com/media2.slashfilm.com/slashfilm/wp/wp-content/images/Mulan1.jpg'}, {}))