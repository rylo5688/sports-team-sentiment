from keys import FIREBASE_CONFIG
import pyrebase

class Firebase:
    def __init__(self, filter_by):
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.db = self.firebase.database()
        self.filter_by = filter_by

    # Push tweet object for this topic
    def push(self, data):
        return self.db.child(self.filter_by).push(data)

    # Get all tweets for this topic
    def get(self):
        return self.db.child(self.filter_by).get()

# firebase = Firebase("users")
# # firebase.push({"wee": "wut"})
# print(firebase.get().val())
