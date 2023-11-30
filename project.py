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
		self.remaining = 1

	def utilize(self, agent_id, amount):
		if agent_id in self.utilizers:
			self.utilizers[agent_id] += amount
		else:
			self.utilizers[agent_id] = amount
		self.utilization_rate = sum([self.utilizers[k] for k in self.utilizers])
		self.remaining = 1-self.utilization_rate
	
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
	'''UNB algorithm stands for UNBalanced. When groups are unbalanced, only increase the share of the agent with lowest share in the smallest group.'''
	def __init__(self, number_of_resources=2, number_of_agents=3) -> None:
		super().__init__(number_of_resources, number_of_agents)
		self.groups = [] #number of groups (default should be 2)
		self.lesser = 0 #which group is the lesser one (0 for group 1, 1 for group 2)
		self.smallestFrac = float("inf") #the smallest fraction of a resource given to an agent
		self.smallestAgents = [] #the group of agents with the smallest resource fraction

	def share_function(self):
		super().share_function() #Give everyone 1/n of their demand to satisfy EF.
		self.groups = [[] for _ in range(self.nor)]
		for r in range(self.n):
			self.groups[self.agents[r].group_num].append(self.agents[r])
		for i in range(self.nor):
			print(f"Group {self.resources[i]}:")
			for k in self.groups[i]:
				print(k)

	#UNB algorithim when 
	def step2group1(self):
		#find the smallest group
		minIndex = float("inf")
		for i in range(len(self.groups)):
			if len(self.groups[i]) < minIndex:
				minIndex = i
		#find the smallest fraction demand of the other resource 
		self.lesser = minIndex
		if self.lesser == 0:
			give = 1 #
		else:
			give = 0

		#finds the smallest fraction of resource
		self.smallestFrac = min(self.groups[self.lesser].demand[give])

		#makes sure we get all agents with the smallest fraction
		for i in range(len(self.groups[minIndex])):
			if self.groups[minIndex][i].demand[minIndex] == self.smallestFrac:
				self.smallestAgents.append(self.groups[minIndex][i])


		while self.resources[0] > 0 and self.resources[1] > 0:
			
			#find the agents with the smallest fraction share here
			for agent in self.groups[]
			p = []


			#calculate the rate
			s0 = 
			s1 = 
			s2 = 
			s = min(s0,s1,s2)

			for agent in self.smallestAgents:
				#increase agents share by some rate
				self.resources[give].utilizers[agent] += s
				#decrement overall resource by the rate 
				self.resources[give].remaining -= s
		
		#the UNB algorithim when group 2 is lesser
		def step2group2():


class BAL(Algorithm):
	'''BAL algorithm stands for BALanced. When groups are balanced, increase the share of the smallest in both groups'''
	def __init__(self, number_of_resources=2, number_of_agents=3) -> None:
		super().__init__(number_of_resources, number_of_agents)
		self.groups = []
	
	def share_function(self):
		super().share_function() #Give everyone 1/n of their demand to satisfy EF.
		self.groups = [[] for _ in range(self.nor)]
		for r in range(self.n):
			self.groups[self.agents[r].group_num].append(self.agents[r])
		for i in range(self.nor):
			print(f"Group {self.resources[i]}:")
			for k in self.groups[i]:
				print(k)
	
	def calcStep():
		return 

	def step2():
		return

class BALStar(BAL):
	def __init__(self, number_of_resources=2, number_of_agents=3) -> None:
		super().__init__(number_of_resources, number_of_agents)
		self.groups = []
	
	def share_function(self):
		super().share_function() #Give everyone 1/n of their demand to satisfy EF.
		self.groups = [[] for _ in range(self.nor)]
		for r in range(self.n):
			self.groups[self.agents[r].group_num].append(self.agents[r])
		for i in range(self.nor):
			print(f"Group {self.resources[i]}:")
			for k in self.groups[i]:
				print(k)
	
	def calcStep():
		return 

	def step2():
		return


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

unb_test()