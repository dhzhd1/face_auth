# coding=utf-8
import os
import configparser


def load_config(config_path):
	pass

def save_config(config):
	pass

def set_config(config, section, key, value):
	pass


def init_config(config_path):
	if not os.path.isfile(config_path):
		cfg = open(config_path, 'w')
		config = configparser.ConfigParser()
		section_list = ['App', 'Inference', 'Capture']
		for section_name in section_list:
			config.add_section(section_name)

		def_app_settings = {'template_folder': './templates',
		                    'assets_folder': './static',
		                    'database_path': './auth.db',
		                    'database_type': 'sqlite'}
		for key in def_app_settings.keys():
			config.set('App', key, def_app_settings[key])

		def_inference_settings = {'model_path': './model/snapshot_iter_123450.caffemodel',
		                          'net_define_path': './model/deploy.prototxt',
		                          'mean_file_path': './model/mean.binaryproto',
		                          'solver_mode': 'gpu',
		                          'gpu_id': '0',
		                          'feature_map_db': './gallery/features.npy',
		                          'score_threshold': '0.9',
		                          'feature_layer': 'pool5/drop_7x7_s1'}

		for key in def_inference_settings.keys():
			config.set('Inference', key, def_inference_settings[key])

		def_capture_settings = {'frame_width': '1024',
		                        'frame_height': '768',
		                        'face_width': '256',
		                        'face_height': '256',
		                        'device': 'video0',
		                        'fps': '25',
		                        'process_interval': '0.5'}
		for key in def_capture_settings.keys():
			config.set('Capture', key, def_capture_settings[key])


		config.write(cfg)
		cfg.close()

	config = configparser.ConfigParser()
	config.read(config_path)
	return config

if __name__ == '__main__':
	cfg_file_path = 'config.ini'
	init_config(cfg_file_path)

