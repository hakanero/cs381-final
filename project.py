from matplotlib import pyplot
import random as rd

class Agent:
	'''Agent class, represents each one of the players that want a certain amount of each resource'''
	def __init__(self, id, *demands) -> None:
		self.id = id 
		'''ID to identify the agents'''
		self.demand_vec = demands
		self.non_normal_demand = demands
		'''Demand vector of agent'''
		self.group_num = self.demand_vec.index(max(self.demand_vec))
		'''Which group does this agent belong to? The group is which resource this agent desires the most'''
	
	def get_demand(self, resource_num):
		return self.demand_vec[resource_num]

	def lowest_demand(self):
		return self.demand_vec[self.group_num]
	
	def normalize(self):
		normalizer = max(self.demand_vec)
		self.demand_vec = tuple(d/normalizer for d in self.demand_vec)
	
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
		#print(agent.id, amount, self.remaining)
	
	def visualize(self, fig_name=""):
		labels = [f"Agent {u}" for u in self.utilizers]
		amounts = [round(self.utilizers[u]*100) for u in self.utilizers]
		labels.append("Not Utilized")
		#print(self.remaining)
		amounts.append(round((self.remaining)*100))
		pyplot.figure(f"{self.name} {fig_name}")
		pyplot.pie(amounts, labels=labels)
	
	def get_utilization(self, agent):
		return self.utilizers[agent.id] if agent.id in self.utilizers else 0

	def __str__(self):
		return self.name

class Algorithm:
	'''Algorithm class, represents the base of a resource allocation algorithm'''
	def __init__(self, number_of_resources = 2, number_of_agents = 3) -> None:
		self.nor = number_of_resources
		self.n = number_of_agents
		self.resources = []
		self.agents = []
	
	def calc_values(self):
		self.g1 = [a for a in self.agents if a.demand_vec[0] == 1.0]
		self.g2 = [a for a in self.agents if a.demand_vec[0] < 1.0]
		self.p1 = self.get_P(self.g1, 1)
		self.p2 = self.get_P(self.g2, 0)
		self.r1 = 1.0 - len(self.g1)/self.n - sum([a.demand_vec[0] for a in self.g2])/self.n
		self.r2 = 1.0 - len(self.g2)/self.n - sum([a.demand_vec[1] for a in self.g1])/self.n
		self.d1,self.d2 = 0,0
		for agent in self.p1:
			self.d1 += (1.0/agent.demand_vec[1])
		for agent in self.p2:
			self.d2 += (1.0/agent.demand_vec[0])

	def add_agent(self, agent):
		agent.normalize()
		self.agents.append(agent)
	
	def share_function(self):
		'''the function that shares resources'''
		self.calc_values()
		#initially, give everyone 1/n of their demand
		for a in self.agents:
			for j,i in enumerate(a.demand_vec):
				self.resources[j].utilize(a, i/self.n)
	
	def calculate_alpha(self):
		l = min(len(self.g1), len(self.g2))
		return l*1.0/self.n
	
	def calculate_utility(self, res):
		#Allocation of that resource / demand of that resource
		cur_min = float("inf")
		for a in self.agents:
			if self.resources[res].get_utilization(a) < cur_min:
				cur_min = self.resources[res].get_utilization(a)
		return cur_min / a.get_demand(res)

	def get_P(self, g, r):
		P = []
		current_min = float("inf")
		smallest = None
		for a in g:
			if a.get_demand(r) < current_min:
				current_min = a.get_demand(r)
				smallest = a
		for a in g:
			if a.get_demand(r) == smallest.get_demand(r):
				P.append(a)
		return P

	def print_res(self):
		for r in self.resources:
			print(r)

	def show_resources(self, name = ""):
		for r in self.resources:
			r.visualize(name)

class UNB(Algorithm):
	'''UNB algorithm stands for UNBalanced. When groups are unbalanced, only increase the share of the agent with lowest share in the smallest group.'''
	def step2(self):
		'''when group 1 is bigger we look at group 2 and give resource 1 to the smallest agents of group 2'''
		#need to find new smallest agent each iteration
		P = self.get_P(self.g2, 0)
		#this one we find the smallest agent of resource 1 thats not in P (basically the second lowest frac) minus the smallest frac in P
		n_subP = [a for a in self.agents if a not in P]
	
		minAgentVal = float("inf") #smallest agent outside of P
		for agent in n_subP:
			if self.resources[0].get_utilization(agent) < minAgentVal:
				minAgentVal = self.resources[0].get_utilization(agent)
		
		s0 = minAgentVal - 0 if len(P) == 0 else self.resources[0].get_utilization(P[0])
		s1 = float("inf") if len(P) == 0 else self.resources[0].remaining / len(P) 
		#denominator for s2
		s2_denom = 0
		for j in P:
			cur = 1.0 / j.demand_vec[0]
			s2_denom += cur
		s2 = float("inf") if len(P) == 0 else self.resources[1].remaining / s2_denom	
		#print(s0,s1,s2)
		s = min(s0,s1,s2)
		for agent in P:
			#increase agents share by some rate
			self.resources[0].utilize(agent, s)
			self.resources[1].utilize(agent, s/agent.get_demand(0))
		return self.agents

	def process(self):
		while self.resources[0].remaining > 0 and self.resources[1].remaining > 0.2:
			self.step2()


class BAL(Algorithm):
	def step2(self):
		#thıs needs to be outsıde of the loop 
		#get s1,s2 calcStep is on page 13
		s1,s2 = self.calcStep()
		#add things to every agent in p1
		for agent in self.p1:
			#scalar we add to allocation and subtract from remaining resources
			val = s1/agent.demand_vec[1]
			self.resources[1].utilize(agent, val*agent.get_demand(1))
			self.resources[0].utilize(agent, val*agent.get_demand(0))
		#add things to every agent in p2
		for agent in self.p2:
			#scalar we add to allocation and subtract from remaining resources
			val = s2/agent.demand_vec[0]
			self.resources[1].utilize(agent, val*agent.get_demand(1))
			self.resources[0].utilize(agent, val*agent.get_demand(0))
		
	def calcStep(self):
		s1,s2 = 0,0
		#calculate s1 and s2
		p1_sub = [a for a in self.agents if a not in self.p1]
		minAgentVal1 = float("inf") #smallest agent outside of P1
		for agent in p1_sub:
			if self.resources[1].get_utilization(agent) < minAgentVal1:
				minAgentVal1 = self.resources[1].get_utilization(agent)

		minAgentVal2 = float("inf") #smallest agent outside of P1
		for agent in self.p1:
			if self.resources[1].get_utilization(agent) < minAgentVal2:
				minAgentVal2 = self.resources[1].get_utilization(agent)
		s1a = minAgentVal1 - minAgentVal2 
		s1b = self.resources[1].remaining / (len(self.p1) + (self.d1*(self.r2/self.r1)))
		
		s1 = min(s1a,s1b)
		
		#calculate s2
		p2_sub = [a for a in self.agents if a not in self.p2]
		minAgentVal1 = float("inf") #smallest agent outside of P1
		for agent in p2_sub:
			if self.resources[0].get_utilization(agent) < minAgentVal1:
				minAgentVal1 = self.resources[0].get_utilization(agent)

		minAgentVal2 = float("inf") #smallest agent outside of P1
		for agent in self.p2:
			if self.resources[0].get_utilization(agent) < minAgentVal2:
				minAgentVal2 = self.resources[0].get_utilization(agent)
		s2a = minAgentVal1 - minAgentVal2
		
		s2b = self.resources[0].remaining / (len(self.p2) + (self.d2*(self.r1/self.r2)))

		s2 = min(s2a,s2b)
		#adjusts s1 and s2
		if (s1*self.d1)/(s2*self.d2) <= self.r1/self.r2:
			s2 = s1 * (self.d1/self.d2) * (self.r2/self.r1)
		else:
			s1 = s2 * (self.d2/self.d1) * (self.r1/self.r2)

		return (s1,s2)
	
	def process(self):
		while self.resources[0].remaining > 0 and self.resources[1].remaining > 0:
			self.step2()
	
class BALStar(BAL):
	"""Same as BAL, but with just a single change in values"""
	def calc_values(self):
		super().calc_values()
		self.r1 = self.r1 + self.d1/self.n
		self.r2 = self.r2 + self.d2/self.n

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
	alg = UNB(2,3)
	alg.resources.append(Resource("CPU"))
	alg.resources.append(Resource("Memory"))
	alg.add_agent(Agent("A", 0.2,0.3))
	alg.add_agent(Agent("B", 0.5,0.2))
	alg.add_agent(Agent("C", 0.4,0.1))
	alg.share_function()
	alg.show_resources("initial")
	for r in alg.resources:
		for i in r.utilizers:
			print("resource",r,"agent",i,r.utilizers[i])
	alg.process()
	for r in alg.resources:
		for i in r.utilizers:
			print("resource",r,"agent",i,r.utilizers[i])
	alg.show_resources("after UNB")
	pyplot.show()

def bal_test():
	alg = BAL(2,4)
	alg.resources.append(Resource("CPU"))
	alg.resources.append(Resource("Memory"))
	alg.add_agent(Agent("A", 0.2,0.3))
	alg.add_agent(Agent("B", 0.4,0.1))
	alg.add_agent(Agent("C", 0.4,0.2))
	alg.add_agent(Agent("D", 0.4,0.1))
	alg.share_function()
	alg.show_resources("initial")
	for r in alg.resources:
		for i in r.utilizers:
			print("resource",r,"agent",i,r.utilizers[i])
	alg.process()
	for r in alg.resources:
		for i in r.utilizers:
			print("resource",r,"agent",i,r.utilizers[i])
	alg.show_resources("after BAL")
	pyplot.show()

def bal_star_test():
	alg = BALStar(2,5)
	alg.resources.append(Resource("CPU"))
	alg.resources.append(Resource("Memory"))
	alg.add_agent(Agent("A", 0.2,0.3))
	alg.add_agent(Agent("B", 0.4,0.1))
	alg.add_agent(Agent("C", 0.4,0.2))
	alg.add_agent(Agent("D", 0.1,0.1))
	alg.add_agent(Agent("E", 1.0,1.0))
	alg.share_function()
	alg.show_resources("initial")
	for r in alg.resources:
		for i in r.utilizers:
			print("resource",r,"agent",i,r.utilizers[i])
	alg.process()
	for r in alg.resources:
		for i in r.utilizers:
			print("resource",r,"agent",i,r.utilizers[i])
	alg.show_resources("after BAL*")
	pyplot.show()

def unb_random_viz():
	no_of_agents = 10
	alg = UNB(2,no_of_agents)
	alg.resources.append(Resource("CPU"))
	alg.resources.append(Resource("Memory"))
	for i in range(no_of_agents):
		alg.add_agent(Agent(f"{i}", rd.uniform(0.001, 1.0), rd.uniform(0.4,0.9)))
	alg.share_function()
	alg.show_resources("initial")
	alg.process()
	alg.show_resources("after UNB")
	pyplot.show()

def bal_random_viz():
	no_of_agents = 10
	alg = BAL(2,no_of_agents)
	alg.resources.append(Resource("CPU"))
	alg.resources.append(Resource("Memory"))
	for i in range(no_of_agents):
		alg.add_agent(Agent(f"{i}", rd.uniform(0.001, 0.9), rd.uniform(0.4,0.9)))
	alg.share_function()
	alg.show_resources("initial")
	alg.process()
	alg.show_resources("after UNB")
	pyplot.show()

"""
We are just observing lol
Who performs better under what values
How well the algorithms perform on making the smallest agent happy
Who got the least utility from the resource -> social utility
"""

def randomize():
	no_of_agents = 20
	alg = UNB(2,no_of_agents)
	alg.resources.append(Resource("CPU"))
	alg.resources.append(Resource("Memory"))
	for i in range(no_of_agents):
		alg.add_agent(Agent(f"{i}", rd.uniform(0.001,1.0), rd.uniform(0.001,1.0)))
	alg.share_function()
	alpha = alg.calculate_alpha()
	alg.process()
	util = alg.calculate_utility(0)
	print("alpha is",alpha,"utility is",util)
	return alpha, util


x,y = [],[]
for i in range(1000):
	a, u = randomize()
	x.append(a)
	y.append(u)

pyplot.scatter(x,y)
pyplot.show()

#bal_random_viz()