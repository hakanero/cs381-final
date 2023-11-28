from matplotlib import pyplot

class Agent:
	'''Agent class, represents each one of the players that want a certain amount of each resource'''
	def __init__(self, id, *demands) -> None:
		self.id = id 
		'''ID to identify the agents'''
		self.demand_vec = (demands)
		'''Demand vector of agent'''
		self.group_num = self.demand_vec.index(max(self.demand_vec))
		'''Which group does this agent belong to? The group is which resource this agent desires the most'''
	
	def get_demand(self, resource_num):
		return self.demand_vec[resource_num]

	def lowest_demand(self):
		return self.demand_vec[self.group_num]
	
	def __str__(self) -> str:
		return self.id

class Resource:
	'''Resource class, represents the resources we share among agents. '''
	def __init__(self, name = "Resource") -> None:
		self.name = name
		self.utilizers = {}
		self.utilization_rate = 0
		self.remaining = 1

	def utilize(self, agent_id, amount):
		if agent_id in self.utilizers:
			self.utilizers[agent_id] += amount
		else:
			self.utilizers[agent_id] = amount
		self.utilization_rate = sum([self.utilizers[k] for k in self.utilizers])
		self.remaining = 1-self.utilization_rate
	
	def visualize(self, unique=False):
		labels = [f"Agent {u}" for u in self.utilizers]
		amounts = [round(self.utilizers[u]*100) for u in self.utilizers]
		labels.append("Not Utilized")
		amounts.append(round((1-self.utilization_rate)*100))
		pyplot.figure(self.name + "1" if unique else self.name)
		pyplot.pie(amounts, labels=labels)
	
	def __str__(self):
		return self.name

class Group:
	def __init__(self, resource_num) -> None:
		self.resource_num = resource_num
		self.agents = []
	
	def add_agent(self, agent: Agent):
		self.agents.append(agent)

	def total_value(self):
		res = 0.0
		for a in self.agents:
			res += a.demand_vec[self.resource_num]
		return res

	def smallest_agent(self) -> Agent:
		current_min = 10000000.0 #arbitrarily large number
		current_agent = None
		for a in self.agents:
			if a.get_demand(self.resource_num) < current_min:
				current_min = a.get_demand(self.resource_num)
				current_agent = a
		return current_agent

class Algorithm:
	'''Algorithm class, represents the base of a resource allocation algorithm'''
	nor : int #number_of_resources
	n : int #number_of_agents
	resources = []
	agents = []
	groups = []

	def __init__(self, number_of_resources = 2, number_of_agents = 3) -> None:
		self.nor = number_of_resources
		self.n = number_of_agents
	
	def share_function(self):
		'''the function that shares resources'''
		#initially, give everyone 1/n of their demand
		for a in self.agents:
			for j,d in enumerate(a.demand_vec):
				self.resources[j].utilize(a.id,d/self.n)

	def group_agents(self, verbose : bool = False):
		self.groups = [Group(i) for i in range(self.nor)]
		for a in range(self.n):
			self.groups[self.agents[a].group_num].add_agent(self.agents[a])
		if verbose:
			for i in range(self.nor):
				print(f"Group {self.resources[i]}:")
				for k in self.groups[i]:
					print(k)
	
	def lowest_group(self):
		current_group = None
		current_min_value = 1000000000.0 #arbitrarily large number
		for i in range(self.nor):
			g = self.groups[i]
			if g.total_value() < current_min_value:
				current_min_value = g.total_value()
				current_group = g
		return current_group

	def print_res(self):
		for r in self.resources:
			print(r)

	def show_resources(self, unique=False):
		for r in self.resources:
			r.visualize(unique)

class UNB(Algorithm):
	'''UNB algorithm stands for UNBalanced. When groups are unbalanced, only increase the share of the agent with lowest share in the smallest group.'''
	def __init__(self, number_of_resources=2, number_of_agents=3) -> None:
		super().__init__(number_of_resources, number_of_agents)
	
	def share_function(self):
		super().share_function() #Give everyone 1/n of their demand to satisfy EF.
		super().group_agents() #Group the agents based on their most demanded resource.
		
	def process(self):
		lowest_group = self.lowest_group()
		smallest_agent = lowest_group.smallest_agent()

		increase_amount = 0.1 # change this to second smallest - smallest

		self.resources[lowest_group.resource_num].utilize(smallest_agent.id, increase_amount)

class BAL(Algorithm):
	'''BAL algorithm stands for BALanced. When groups are balanced, increase the share of the smallest in both groups'''
	def __init__(self, number_of_resources=2, number_of_agents=3) -> None:
		super().__init__(number_of_resources, number_of_agents)
	
	def share_function(self):
		super().share_function() #Give everyone 1/n of their demand to satisfy EF.
		super().group_agents() #Group the agents based on their most demanded resource.

class BALStar(BAL):
	pass


#TESTS BELOW

def alg_test():
	alg = Algorithm()
	alg.resources.append(Resource("CPU"))
	alg.resources.append(Resource("Memory"))
	alg.agents.append(Agent("A", 0.1,0.7))
	alg.agents.append(Agent("B", 1.0,0.3))
	alg.agents.append(Agent("C", 0.2,0.4))
	alg.share_function()
	alg.show_resources()

def unb_test():
	alg = UNB()
	alg.resources.append(Resource("CPU"))
	alg.resources.append(Resource("Memory"))
	alg.agents.append(Agent("A", 0.1,0.7))
	alg.agents.append(Agent("B", 1.0,0.3))
	alg.agents.append(Agent("C", 0.2,0.4))
	alg.share_function()
	alg.show_resources()
	alg.process()
	alg.show_resources(True)
	pyplot.show()

unb_test()