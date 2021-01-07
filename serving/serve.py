import json
import tensorflow as tf
import numpy as np
import PIL.Image
import bentoml
from bentoml.adapters import JsonInput
from bentoml.frameworks.tensorflow import TensorflowSavedModelArtifact

model = tf.keras.models.load_model("/models/tftransfer")

# region functions
def load_img(imgPath):
	"""Load an image for the DNN model. Returns the tensor-image."""
	max_dim = 512
	img = tf.io.read_file(imgPath)
	img = tf.image.decode_image(img, channels=3)
	img = tf.image.convert_image_dtype(img, tf.float32)
	
	shape = tf.cast(tf.shape(img)[:-1], tf.float32)
	long_dim = max(shape)
	scale = max_dim / long_dim
	
	new_shape = tf.cast(shape * scale, tf.int32)
	
	img = tf.image.resize(img, new_shape)
	img = img[tf.newaxis, :]
	return img

def save_img(prediction:tf.Tensor, imgPath:str):
	"""Save converts the DNN output from tensor to PIL.Image and save the image into the imgPath given."""
	prediction = prediction*255
	prediction = np.squeeze(np.array(prediction, dtype=np.uint8))
	prediction = PIL.Image.fromarray(prediction)
	prediction.save(imgPath)
# endregion functions

@bentoml.artifacts([TensorflowSavedModelArtifact('model')])
class TfModelService(bentoml.BentoService):
	@bentoml.api(input=JsonInput(), batch=False)
	def predict(self, jsonIn):
		jsonIn = json.loads(jsonIn)
		# print(f"\n\n\tjsonIn -> {type(jsonIn)}")
		# print(f"\tjsonIn -> {list(jsonIn.keys())} -> {list(jsonIn[list(jsonIn.keys())[0]].keys())}\n")
		prediction = self.artifacts.model(
			load_img(jsonIn["inputs"]["contentPath"]),
			load_img(jsonIn["inputs"]["stylePath"])
		)[0]
		save_img(
			prediction=prediction, 
			imgPath=jsonIn["outputPath"]
		)
		return True

svc = TfModelService()
svc.pack('model', model)
svc.save()