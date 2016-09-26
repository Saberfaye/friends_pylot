from system.core.controller import *

class Friends(Controller):
    def __init__(self, action):
        super(Friends, self).__init__(action)

        self.load_model('Friend')
        self.db = self._app.db
   
    def index(self):
        if not "id" in session:
            return redirect("/")
    	friends = self.models["Friend"].get_friends(session["id"])
    	not_friends = self.models["Friend"].get_not_friends(session["id"])
        return self.load_view('friends/index.html', all_friends = friends, all_not_friends = not_friends)

    def add(self, id):
        if not "id" in session:
            return redirect("/")
    	self.models["Friend"].add_friend(id, session["id"])
    	return redirect("/friends")

    def delete(self, id):
        if not "id" in session:
            return redirect("/")
    	self.models["Friend"].delete_friend(id, session["id"])
    	return redirect("/friends")