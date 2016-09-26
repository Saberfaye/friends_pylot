from __future__ import print_function
from system.core.model import Model
import re, datetime, time, sys

class Friend(Model):
	def __init__(self):
		super(Friend, self).__init__()

	def get_friends(self, user_id):
		query = "SELECT user2.id, user2.alias FROM users JOIN friendships ON users.id = friendships.user_id JOIN users AS user2 ON friendships.friend_id = user2.id WHERE users.id = :user_id"
		data = { "user_id": user_id }
		print (self.db.query_db(query, data), file=sys.stderr)
		return self.db.query_db(query, data)

	def get_not_friends(self, user_id):
		query = "SELECT id, alias FROM users WHERE id NOT IN (SELECT user2.id FROM users JOIN friendships ON users.id = friendships.user_id JOIN users AS user2 ON friendships.friend_id = user2.id WHERE users.id = :user_id UNION ALL SELECT id FROM users WHERE users.id = :user_id)"
		data = { "user_id": user_id }
		return self.db.query_db(query, data)

	def add_friend(self, friend_id, user_id):
		query = "INSERT INTO friendships (user_id, friend_id) VALUES(:user_id, :friend_id);"
		data = { "user_id" : user_id, "friend_id" : friend_id}
		self.db.query_db(query, data)
		data = { "user_id" : friend_id, "friend_id" : user_id}
		return self.db.query_db(query, data)

	def delete_friend(self, friend_id, user_id):
		query = "DELETE FROM friendships WHERE user_id = :user_id AND friend_id = :friend_id"
		data = { "user_id" : user_id, "friend_id" : friend_id}
		self.db.query_db(query, data)
		data = { "user_id" : friend_id, "friend_id" : user_id}
		return self.db.query_db(query, data)
