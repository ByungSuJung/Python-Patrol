from road import Road
class Car:
	def __init__(self,start,dest,modified=False):
		self.id=None
		self.start = start
		self.current_position = start
		self.dest = dest
		self.ts_on_current_position=0
		self.paths = None
		self.total_ts = 0
		self.total_dist = 0
		self.total_nodes_traveled = 0
		self.modified = modified
		#start.add(self)

	def set_path(self,paths):
		self.paths = paths