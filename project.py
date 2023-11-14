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
	def __str__(self) -> str:
		return self.id

class Resource:
	'''Resource class, represents the resources we share among agents. '''
	def __init__(self, name = "Resource") -> None:
		self.name = name
		self.utilizers = {}
		self.utilization_rate = 0

	def utilize(self, agent_id, amount):
		if agent_id in self.utilizers:
			self.utilizers[agent_id] += amount
		else:
			self.utilizers[agent_id] = amount
		self.utilization_rate = sum([self.utilizers[k] for k in self.utilizers])
	
	def visualize(self):
		labels = [f"Agent {u}" for u in self.utilizers]
		amounts = [round(self.utilizers[u]*100) for u in self.utilizers]
		labels.append("Not Utilized")
		amounts.append(round((1-self.utilization_rate)*100))
		pyplot.figure(self.name)
		pyplot.pie(amounts, labels=labels)
	
	def __str__(self):
		return self.name

class Algorithm:
	'''Algorithm class, represents the base of a resource allocation algorithm'''
	nor : int #number_of_resources
	n : int #number_of_agents
	resources = []
	agents = []

	def __init__(self, number_of_resources = 2, number_of_agents = 3) -> None:
		self.nor = number_of_resources
		self.n = number_of_agents
	
	def share_function(self):
		'''the function that shares resources'''
		#initially, give everyone 1/n of their demand
		for a in self.agents:
			for j,d in enumerate(a.demand_vec):
				self.resources[j].utilize(a.id,d/self.n)

	def print_res(self):
		for r in self.resources:
			print(r)

	def show_resources(self):
		for r in self.resources:
			r.visualize()
		pyplot.show()

class UNB(Algorithm):
	def __init__(self, number_of_resources=2, number_of_agents=3) -> None:
		super().__init__(number_of_resources, number_of_agents)
		self.groups = []
	'''UNB algorithm stands for UNBalanced. When groups are unbalanced, only increase the share of the agent with lowest share in the smallest group.'''
	def share_function(self):
		super().share_function() #Give everyone 1/n of their demand to satisfy EF.
		self.groups = [[] for _ in range(self.nor)]
		for r in range(self.n):
			self.groups[self.agents[r].group_num].append(self.agents[r])
		for i in range(self.nor):
			print(f"Group {self.resources[i]}:")
			for k in self.groups[i]:
				print(k)
	def process(self):
		pass

class BAL(Algorithm):
	def __init__(self, number_of_resources=2, number_of_agents=3) -> None:
		super().__init__(number_of_resources, number_of_agents)
		self.groups = []
	'''BAL algorithm stands for BALanced. When groups are balanced, only increases the share of the agent with lowest share in the smallest groups.'''
	def share_function(self):
		super().share_function() #Give everyone 1/n of their demand to satisfy EF.
		self.groups = [[] for _ in range(self.nor)]
		for r in range(self.n):
			self.groups[self.agents[r].group_num].append(self.agents[r])
		for i in range(self.nor):
			print(f"Group {self.resources[i]}:")
			for k in self.groups[i]:
				print(k)

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

alg_test()