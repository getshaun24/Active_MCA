from flask_login import UserMixin
import bcrypt
from password_generator import PasswordGenerator
from datetime import datetime
# from project.mongo import db



class User(UserMixin):
	# All users would have the below properties
	def __init__(self, email, db):
		userData = db.Credentials.Users.find_one({ "email": email })
		if userData is not None:
			self.id = userData['email']
			self.email = userData['email']
			self.access_status = userData['access_status']
			self.password = userData['password']
			self.two_factor_code = userData['two_factor_code']
			self.first_name = userData['first_name']
			self.last_name = userData['last_name']
			self.notification_count = userData['notification_count']
			if self.access_status != "master":
				# self.business_id = userData['business_id']
				pass
			if self.access_status == "admin":
				self.user_database = userData["metadata"]["funder_db"]
			if self.access_status == "syndicator" or self.access_status == "merchant":
				self.user_databases = userData['metadata']['funder_dbs']
		else:
			self.id = None

	def update_two_factor_code(self, code, db):
		db.Credentials.Users.update({"email": self.email}, {"$set": {"two_factor_code":code}})

	def check_password(self, entered_password):
		if not bcrypt.checkpw(entered_password.encode('utf8'), self.password):
			return False
		else:
			return True

	def generate_and_update_password(self, db):
		pwo = PasswordGenerator()
		pwo.minlen = 8
		pwo.maxlen = 12
		password = pwo.generate()
		hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(14))
		db.Credentials.Users.update({"email": self.email}, {"$set": {"password": hashed_password}})
		return password

	def update_reset_code(self, reset_code, db):
		db.Credentials.Users.update({"email": self.email}, {"$set": {"reset_code":reset_code}})

	def verify_reset_code(self, reset_code, db):
		userData = db.Credentials.Users.find_one({ 'email': self.email})
		if 'reset_code' in userData.keys():
			if userData['reset_code'] == reset_code:
				return True
			else:
				return False
		else:
			return False

	def update_password(self, password, db):
		db.Credentials.Users.update({"email": self.email}, {"$set": {"password":password}})

	def clear_reset_code(self, db):
		db.Credentials.Users.update({"email": self.email}, {"$set": {"reset_code":""}})

	def get_user_by_id(self, id, db):
		userData = db.Credentials.Users.find_one({ "_id": Object("'"+id+"'") })
		self.id = id
		self.email = userData['email']
		self.DB_name = userData["DB_name"]
		self.access_status = userData["access_status"]
		self.password = userData['password']
		self.two_factor_code = userData['two_factor_code']
		return self

	def get_dwolla_account(self, db):
		userData = db.Credentials.Users.find_one({ "_id": Object("'"+self.id+"'") })
		self.dwolla_funding_source_destination_account = userData['dwolla_funding_source_destination_account']
		return self

def generate_random_password():
	pwo = PasswordGenerator()
	pwo.minlen = 8
	pwo.maxlen = 12
	password = pwo.generate()
	hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt(14))
	return hashed_password

def create_new_user(db, email, access_status, first_name, last_name, business_id='', metadata={}):
	db.Credentials.Users.insert_one({
		"date_created": datetime.today(),
		"email": email,
		"password": generate_random_password(),
		"access_status": access_status,
		"reset_code":"",
		"two_factor_code":"",
		"first_name": first_name,
		"last_name": last_name,
		"notification_count": 0,
		"notfications":[],
		"metadata": metadata,
		"business_id": business_id
	})