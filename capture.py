# coding=utf-8

import cv2
import numpy as np
import configparser
import threading
from time import sleep



class Capture:
	def __init__(self, config):
		self.config = config
		self.device = self.config.get('Capture', 'device')
		self.frame = None
		self.width = self.config.get('Capture', 'frame_width')
		self.height = self.config.get('Capture', 'frame_height')
		self.face_width = self.config('Capture', 'face_width')
		self.face_height = self.config('Capture', 'face_height')
		self.fps = self.config.get('Capture', 'fps')
		self.process_interval = self.config.get('Capture', 'process_interval')

		self.cap = cv2.VideoCapture(self.device)
		self.capture_status = True
		self.in_processing = False


	def __del__(self):
		self.cap.release()


	def start(self):
		"""
		Frame capture only return the central (256, 256) part image
		:return:
		"""
		while self.capture_status:
			_, frame = self.cap.read()
			c_frame = frame[self.width / 2 - self.face_width / 2: self.width / 2 + self.face_width / 2,
			          self.height / 2 - self.face_width / 2: self.height / 2 + self.face_height / 2, :]
			if not self.in_processing:
				self.frame = frame
				self.in_processing = True
			sleep(0.2)
		yield cv2.imdecode('png', c_frame)


	def stop(self):
		self.capture_status = False




