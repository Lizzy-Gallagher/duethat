class CalItem:
	def __init__(self, query, action, action_target, location, start_time):
		self.query = query
		self.action = action
		self.action_target = action_target
		self.location = location
		self.start_time = start_time

	def create_description(self):
		return self.action + " " + self.action_target

