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
		self.utilizers = {} #key is agent value is amount of resource given
		self.utilization_rate = 0
		self.remaining = 1

	def utilize(self, agent, amount):
		agent_id = agent.id
		if agent_id in self.utilizers:
			self.utilizers[agent_id] += amount
		else:
			self.utilizers[agent_id] = amount
		self.utilization_rate = sum([self.utilizers[k] for k in self.utilizers])
		self.remaining = 1.0-self.utilization_rate
	
	def visualize(self, unique=False):
		labels = [f"Agent {u}" for u in self.utilizers]
		amounts = [round(self.utilizers[u]*100) for u in self.utilizers]
		labels.append("Not Utilized")
		amounts.append(round((1-self.utilization_rate)*100))
		pyplot.figure(self.name + "1" if unique else self.name)
		pyplot.pie(amounts, labels=labels)
	
	def get_utilization(self, agent):
		return self.utilizers[agent.id]

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

	def smallest_agents_of_resource(self, resource_num) -> list:
		current_min = 10000000.0 #arbitrarily large number
		current_agents = []
		smallest = None
		for a in self.agents:
			if a.get_demand(resource_num) < current_min:
				current_min = a.get_demand(resource_num)
				smallest = a
		for a in self.agents:
			if a.get_demand(resource_num) == smallest.get_demand(resource_num):
				current_agents.append(a)
		return current_agents

	def length(self):
		return len(self.agents)

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
				self.resources[j].utilize(a,d/self.n)

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
				current_min_value = g.length()
				current_group = g
		return current_group
		"""
		current_group = None
		current_min_value = 1000000000.0 #arbitrarily large number
		for i in range(self.nor):
			g = self.groups[i]
			if g.total_value() < current_min_value:
				current_min_value = g.total_value()
				current_group = g
		return current_group
		"""

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
		super().share_function() #Give everyone 1/n of their demand to satisfy SI.
		super().group_agents() #Group agents
		#self.lesser = self.lowest_group() #which group is the lesser one (0 for group 1, 1 for group 2)

	#UNB algorithim when group 1 is bigger
	def step2group1(self):
		'''when group 1 is bigger we look at group 2 and give resource 1 to the smallest agents of group 2'''
		#find the agents with the smallest fraction share of resource 1 in group 2
		lesser = self.lowest_group()
		#need to find new smallest agent each iteration
		P = lesser.smallest_agents_of_resource(1)
		for a in P:
			print(a)
		
		#self.smallestFrac = self.lesser.utilizers[smallestAgent]
		#p = []
		#for agent in self.lesser.agents:
		#	if self.resources[0].utilizers[agent] == self.smallestFrac:
		#		p.append(agent)
		
		#calculate the rates
		
		#this one we find the smallest agent of resource 1 thats not in P (basically the second lowest frac) minus the smallest frac in P
		n_subP = [a for a in self.agents if a not in P]
	
		minAgentVal = float("inf") #smallest agent outside of P
		for agent in n_subP:
			if self.resources[0].get_utilization(agent) < minAgentVal:
				minAgentVal = self.resources[0].get_utilization(agent)
		print(minAgentVal)
		s0 = minAgentVal + self.resources[0].get_utilization(P[0])
		s1 = self.resources[0].remaining / len(P) 
		#denominator for s2
		s2_denom = 0
		for j in P:
			cur = 1.0 / j.demand_vec[0]
			s2_denom += cur
		s2 = self.resources[1].remaining / s2_denom	
		print(s0,s1,s2)
		s = min(s0,s1,s2)
		for agent in P:
			#increase agents share by some rate
			self.resources[0].utilize(agent, s)
			self.resources[1].utilize(agent, s/agent.get_demand(0))
		return self.agents
	
	#the UNB algorithim when group 2 is bigger basically the same method as above but switch the numbers 
	def step2group2(self):
		#find the agents with the smallest fraction share of resource 1 in group 2
		lesser = self.lowest_group()
		#need to find new smallest agent each iteration
		P = lesser.smallest_agents_of_resource(0)
		for a in P:
			print(a)
		
		#self.smallestFrac = self.lesser.utilizers[smallestAgent]
		#p = []
		#for agent in self.lesser.agents:
		#	if self.resources[0].utilizers[agent] == self.smallestFrac:
		#		p.append(agent)
		
		#calculate the rates
		
		#this one we find the smallest agent of resource 1 thats not in P (basically the second lowest frac) minus the smallest frac in P
		n_subP = [a for a in self.agents if a not in P]
		
		minAgentVal = float("inf") #smallest agent outside of P
		for agent in n_subP:
			if self.resources[1].get_utilization(agent) < minAgentVal:
				minAgentVal = self.resources[1].get_utilization(agent)
		s0 = minAgentVal + self.resources[1].get_utilization(P[0])
		s1 = self.resources[1].remaining / len(P) 
		#denominator for s2
		s2_denom = 0
		for j in P:
			cur = 1.0 / j.demand_vec[1]
			s2_denom += cur
		s2 = self.resources[1].remaining / s2_denom
		print(s0,s1,s2)
		s = min(s0,s1,s2)
		for agent in P:
			#increase agents share by some rate
			self.resources[1].utilize(agent, s)
			self.resources[0].utilize(agent, s/agent.get_demand(1))
		return self.agents
		
	
	def share_function(self):
		super().share_function() #Give everyone 1/n of their demand to satisfy EF.
		super().group_agents() #Group the agents based on their most demanded resource.
		
	def process(self):
		while self.resources[0].remaining > 0 and self.resources[1].remaining > 0.2:
			#if group1 bigger
			if self.groups[0].length() > self.groups[1].length():
				self.step2group1()
			else:
				self.step2group2()


class BAL(Algorithm):
	'''BAL algorithm stands for BALanced. When groups are balanced, increase the share of the smallest in both groups'''
	def __init__(self, number_of_resources=2, number_of_agents=3) -> None:
		super().__init__(number_of_resources, number_of_agents)
	
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

	def step2(self):

		while self.resources[0].remaining > 0 and self.resources[1].remaining > 0:
			
			#find the agents with the smallest fraction share of resource 1 in group 2
			p1,p2 = [],[]
			#need to find new smallest agent each iteration
			smallestAgent = self.lesser.smallest_agent()
			self.smallestFrac = self.lesser.utilizers[smallestAgent]
			p = []
			for agent in self.lesser.agents:
				if self.resources[0].utilizers[agent] == self.smallestFrac:
					p.append(agent)
				
			#calculate the rates
			
			
			s1,s2 = self.calcStep()
			for k in [0,1]:
				if k == 0:
					for agent in p1:
						self.resource[0]
						self.resource[1]

			for agent in p:
				#increase agents share by some rate
				self.resources[give].utilizers[agent] += s
				#decrement overall resource by the rate 
				self.resources[0].remaining -= s
				self.resources[1].remaining -= (s/self.resources[0].utilizers[agent])
			
		return self.agents

		super().group_agents() #Group the agents based on their most demanded resource.


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
	alg.agents.append(Agent("A", 0.2,0.3))
	alg.agents.append(Agent("B", 0.4,0.1))
	alg.agents.append(Agent("C", 0.4,0.2))
	alg.share_function()
	alg.show_resources()
	for r in alg.resources:
		for i in r.utilizers:
			print("resource",r,"agent",i,r.utilizers[i])
	alg.process()
	for r in alg.resources:
		for i in r.utilizers:
			print("resource",r,"agent",i,r.utilizers[i])
	alg.show_resources(True)
	pyplot.show()

unb_test()