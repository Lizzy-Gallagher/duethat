class TaskItem:
	def __init__(self, query, action, action_target, location, due_date):
		self.query = query 
		self.action = action
		self.action_target = action_target
		self.location = location
		self.due_date = due_date

	def create_title(self):
		return self.action + " " + self.action_target
