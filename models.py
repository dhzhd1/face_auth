# coding=utf-8

from datetime import datetime
import json
from sqlalchemy import Boolean, Column
from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class RegisteredUsers(Base):
	__tablename__ = 'tb_users'

	user_id = Column(Integer, primary_key=True)
	login_name = Column(String(255), unique=True)
	first_name = Column(String(255), nullable=False)
	last_name = Column(String(255), nullable=False)
	job_title = Column(String(255), nullable=True)
	manager = Column(String(255), nullable=True)
	# status should be one of below condition: ['enabled', 'disabled']
	account_status = Column(String(20), nullable=False)
	user_password = Column(String(255), nullable=False)
	created = Column(DateTime, default=datetime.now)
	modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
	memo = Column(String(1024), nullable=True)

	@property
	def get_user_status(self):
		return self.account_status

	@property
	def get_password(self):
		return self.user_password

	@property
	def get_op_timestamps(self):
		return self.created, self.modified

	@property
	def get_full_name(self):
		return self.first_name, self.last_name

	@property
	def get_title(self):
		return self.job_title

	@property
	def get_manager(self):
		return self.manager

	@property
	def get_memo(self):
		return self.memo

	@property
	def get_user_id(self):
		return self.user_id

	# @property
	# def set_user_status(self, status):
	# 	if status.strip() in ['enabled', 'disabled']:
	# 		self.account_status = status

	# @property
	# def set_password(self, passwd):
	# 	self.user_password = passwd



class UserRights(Base):
	__tablename__ = 'tb_rights'

	user_id = Column(Integer, unique=True, primary_key=True)
	rights = Column(String(1024), default="{all:False}")
	modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
	memo = Column(String(1024), nullable=True)


class FaceFeatureMap(Base):
	__tablename__ = 'tb_feature_map'

	user_id = Column(Integer, unique=True, primary_key=True)
	feature_map_1 = Column(String(255), nullable=True)
	feature_map_2 = Column(String(255), nullable=True)
	feature_map_3 = Column(String(255), nullable=True)
	modified = Column(DateTime, default=datetime.now, onupdate=datetime.now)
	memo = Column(String(1024), nullable=True)

def init_data(session):
	try:
		session.add(RegisteredUsers(
			user_id = 0,
			login_name = 'admin',
			first_name = 'admin',
			last_name = 'admin',
			job_title = 'admin',
			account_status = 'enabled',
			user_password = 'admin',
		))
		session.commit()
	except IntegrityError:
		print("ERROR: The user id was existed!")

	try:
		dict_rights = {'all': True}
		session.add(UserRights(
			user_id = 0,
			rights = json.dumps(dict_rights)
		))
		session.commit()
	except IntegrityError:
		print("ERROR: The user id was existed!")

	try:
		session.add(FaceFeatureMap(
			user_id = 0
		))
		session.commit()
	except IntegrityError:
		print("ERROR: The user id was existed!")



if __name__ == "__main__":
	from datetime import timedelta
	from sqlalchemy import create_engine
	from sqlalchemy.orm import sessionmaker
	from models import Base

	engine = create_engine('sqlite:///auth.db', echo=True)
	Base.metadata.create_all(engine)
	Session = sessionmaker(bind=engine)
	session = Session()
	init_data(session)




