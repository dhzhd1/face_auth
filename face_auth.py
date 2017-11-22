# coding=utf-8

import numpy as np
import dlib
import caffe
import os



def load_face_features(face_feature_file):
	pass

def save_face_features(face_feature, face_feature_file):
	pass

def remove_face_feature(face_feature_file):
	pass

def extract_face(frame):
	face_info = None
	face_detector = dlib.get_frontal_face_detector()
	detector_result = face_detector(frame, 0)
	if len(detector_result) < 0:
		print("No face detected! Please make sure your face are in the detect window.")
	else:
		biggest_face_size = 0.
		for idx, coord in enumerate(detector_result):
			if abs(coord.right() - coord.left()) * abs(coord.bottom() - coord.top()) > biggest_face_size:
				cropped_face = np.copy(frame[max(0, coord.top()): coord.bottom(), max(0, coord.left()):coord.right(), :])
				face_info = ([coord.left(), coord.top(), coord.right(), coord.bottom()], cropped_face)
	return face_info



