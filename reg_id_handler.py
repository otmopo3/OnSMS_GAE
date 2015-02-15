from datastore import GcmRegistration

class RegIdHandler():
	def getRegId(self, email):
		keyname = email
		return GcmRegistration.get(keyname).registration_id
	
	def register(self, email, regId):
		registration = GcmRegistration.get_or_insert(email)
		registration.registration_id = regId
		registration.put()
		
		
		