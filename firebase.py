from keys import FIREBASE_CONFIG
import pyrebase

class Firebase:
    def __init__(self, name):
        self.firebase = pyrebase.initialize_app(FIREBASE_CONFIG)
        self.db = self.firebase.database()

        # Initializing a section for these specific tweets
        self.db.child(name)

    def push(self, data):
        self.db.push(data)


# firebase = Firebase("users")
# firebase.push({"hi": "test"})