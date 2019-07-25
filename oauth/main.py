
from google.appengine.api import users
from oauth2client.contrib.appengine import StorageByKeyName


user = users.get_current_user()
storage = StorageByKeyName(CredentialsModel, user.user_id(), 'credentials')
credentials = storage.get()


# hi dewdadssddsaad