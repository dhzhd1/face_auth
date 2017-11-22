# coding=utf-8

import numpy as np
import caffe
import configparser
import sys
from caffe.proto import caffe_pb2
import time
from google.protobuf import text_format

class Inference():
	def __init__(self, config):
		"""
		Init Inference Class
		:param config:
		"""
		''' Configuration parameter initialization'''
		self.config = config
		self.caffe_model = self.config.get('Inference', 'model_path')
		self.caffe_deploy = self.config.get('Inference', 'net_define_path')
		self.mean_file = self.config.get('Inference', 'mean_file_path')
		self.use_gpu = True if self.config.get('Inference', 'solver_mode') == 'gpu' else False
		self.gpu_id = self.config.get('Inference', 'gpu_id') if self.use_gpu else None
		self.feature_layer = self.config.get('Inference', 'feature_layer')

		'''set caffe solver model, gpu or cpu'''
		if self.use_gpu:
			caffe.set_device(self.gpu_id)
			caffe.set_mode_gpu()
		else:
			caffe.set_mode_cpu()

		'''Loading Caffe model and define the transform'''
		self.net = caffe.Net(self.caffe_deploy, self.caffe_model, caffe.TEST)
		self.transform = self.get_transformer()

	def get_transformer(self):
		"""
		create a transformer for each input image
		:return: a transformer instance
		"""
		'''Load network parameters from caffe network deploy file'''
		network = caffe_pb2.NetParameter()
		with open(self.caffe_deploy) as caffe_deploy_file:
			text_format.Merge(caffe_deploy_file.read(), network)

		'''
		Load the input image shape. Since need to be compatiabled with old syntax we need to check 
		if there is 'input_shape' or 'input_dim' 
		'''
		if network.input_shape:
			dims = network.input_shape[0].dim
		else:
			dims = network.input_dim[:4]

		t = caffe.io.Transformer(inputs={'data': dims})
		'''
		Image read from opencv is (H, W, C). It should be changed (C, H, W) 
		C= Channel, W= Width, H= Height
		'''
		t.set_transpose('data', (2, 0, 1))

		'''The Channel is (B, G, R) if the image read from OpenCV, then it should be changed to R, G, B'''
		if dims[1] == 3:
			t.set_channel_swap('data', (2, 1, 0))

		'''Set image mean. If mean_file existed, use the mean file to caculate the mean, otherwise use a nornal mean array'''
		if self.mean_file:
			with open(self.mean_file, 'rb') as mean_file:
				blob = caffe_pb2.BlobProto()
				blob.MergeFromString(mean_file.read())
				if blob.HasField('shape'):
					blob_dims = blob.shape.dim
					assert len(blob_dims) == 4, 'Shape should have 4 dimmensiions - shape is %s' % blob.shape
				elif blob.HasField('num') and blob.HasField('channels') and blob.HasField('height') and blob.HasField('width'):
					blob_dims = (blob.num, blob.channel, blob.height, blob.width)
				else:
					raise ValueError('Blob does not provide shape or 4d dimensions')

				pixel = np.reshape(blob.data, blob.dims[1:]).mean(1).mean(1)
				t.set_mean('data', pixel)
		else:
			pixel = [129, 104, 93]
			t.set_mean('data', np.array(pixel))

		return t

	def forward_pass(self, images, batch_size=1, feature_layer=None):
		scores = None
		features = None

		caffe_images = []
		for image in images:
			if image.ndim == 2:
				'''
					If image.ndim == 2 which means the image only have one Channel with (Height, width)
					Use np.newaxis with add a new axis on to make the np array as (h, w, c).
					This array will transposed in the transformer function
				'''
				caffe_images.append(image[:, :, np.newaxis])
			else:
				caffe_images.append(image)

		'''Change caffe_image list to numpy array'''
		caffe_images = np.array(caffe_images)
		dims = self.transform.inputs['data'][1:]

		for chunk in [caffe_images[x:x + batch_size] for x in xrange(0, len(caffe_images), batch_size)]:
			chunk_shape = (len(chunk), ) + tuple(dims)
			if self.net.blobs['data'].data.shape != chunk_shape:
				self.net.blobs['data'].reshape(*chunk_shape)
			for idx, image in enumerate(chunk):
				image_data = self.transform.preprocess('data', image)
				self.net.blobs['data'].data[idx] = image_data
			output = self.net.forward()[self.net.outputs[-1]]
			# I only need feed forward to extract feature not for classification score

			if feature_layer is not None:
				if features is None:
					features = np.copy(self.net.blobs[feature_layer].data)
				else:
					features = np.vstack((features, self.net.blobs[feature_layer].data))

			if scores is None:
				scores = np.copy(output)
			else:
				scores = np.vstack((scores, output))

		return scores, features

def validation():
	pass

def extract_face_feature(cropped_face_frame):
	pass


