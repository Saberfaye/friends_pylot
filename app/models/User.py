from system.core.model import Model
import re, datetime, time

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def get_user(self, user_id):
		query = "SELECT * from users WHERE id = :id"
		data = { "id": user_id }
		return self.db.query_db(query, data)[0]

	def create_user(self, user):
		NAME_REGEX = re.compile(r"^[A-Z][a-z]+ [A-Z][a-z]+$")
		EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

		errors = []

		if not user["name"]:
			errors.append(("User name cannot be blank", "name"))
		elif not NAME_REGEX.match(user['name']):
			errors.append(("User name should start with a upper case letter and consists with letters only and at least 2 letters for first&last name", "name"))
		if not user["alias"]:
			errors.append(("User alias cannot be blank", "alias"))
		else:
			query = "SELECT * from users WHERE alias = :alias"
			data = { "alias": user["alias"] }
			alias = self.db.query_db(query, data)
			if alias:
				errors.append(("User alias is already used, please select a new one", "alias"))
		if not user["date_of_birth"]:
			errors.append(("User date of birth cannot be blank", "date_of_birth"))
		else:
			date_item = user["date_of_birth"].split("/")
			if int(date_item[2]) > datetime.datetime.now().year:
				errors.append(("User date of birth is invalid", "date_of_birth"))
			elif int(date_item[0]) >datetime.datetime.now().month:
				errors.append(("User date of birth is invalid", "date_of_birth"))
			elif int(date_item[1]) > datetime.datetime.now().day:
				errors.append(("User date of birth is invalid", "date_of_birth"))
		if not user["email"]:
			errors.append(("User email cannot be blank", "email"))
		elif not EMAIL_REGEX.match(user["email"]):
			errors.append(("Invalid Email Address", "email"))
		else:
			query = "SELECT * from users WHERE email = :email"
			data = { "email": user["email"] }
			email = self.db.query_db(query, data)
			if email:
				errors.append(("User email is already used, please select a new one", "email"))
		if not user["password1"]:
			errors.append(("Password cannot be blank", "password1"))
		elif len(user["password1"]) < 8:
			errors.append(("Password need to be at least 8 characters", "password1"))
		if not user["password2"]:
			errors.append(("You need to confirm password", "password2"))
		elif user["password2"] != user["password1"]:
			errors.append(("Password does not match!", "password2"))

		if errors:
			return {"status" : False, "errors" : errors}
		else:
			hashed_pw = self.bcrypt.generate_password_hash(user["password1"])
			query = "INSERT into users (name, alias, email, password, date_of_birth) VALUES(:name, :alias, :email, :password, :date_of_birth)"
			data = {'name': user['name'], 'alias': user['alias'], 'email': user['email'], 'password': hashed_pw, 'date_of_birth': user['date_of_birth']}
			user_id = self.db.query_db(query, data)

			return { "status" : True, "user_id" : user_id}

	def login_user(self, user):
		query = "SELECT * FROM users WHERE email = :email"
		data = { "email" : user["email"]}
		user_data = self.db.query_db(query, data)

		errors = []
		if not user_data:
			errors.append(("User does not exist", "login"))
		elif not self.bcrypt.check_password_hash(user_data[0]["password"], user["password"]):
			errors.append(("Email and password does not match", "login"))

		if errors:
			return {"status" : False, "errors" : errors}
		else:
			return { "status" : True, "user_id" : user_data[0]["id"], "user_alias" : user_data[0]["alias"]}
