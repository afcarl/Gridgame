import random as r

class gridQController():

	def __init__(self,gridSize):
		self.treasurePlaces = 5
		self.damagedStates = 2
		self.nbrActions = 4

		self.greed = 0.2 #epsilon. greedy constant

		self.initQmatrix = 10


		self.discount = 0.9	#Gamma
		self.stepSize = 0.8 	#Alpha

		self.alphaFixed = True
		
		self.gridWidth = gridSize	
		self.gridHeight = gridSize
		self.totalStates = self.gridHeight*self.gridWidth*self.treasurePlaces*self.damagedStates
		self.initQ()

		print("Controller created")
	

	def initQ(self):
		tmp = [0]*self.totalStates
		x = 0
		for i in range(0,self.gridWidth):
			for j in range(0,self.gridHeight):
				for k in range(0,self.treasurePlaces):
					for l in range(0,self.damagedStates):
						tmp[x] = (i,j,k,l)
						x+=1
		self.Q = [tmp,
				  [self.initQmatrix]*self.totalStates,
				  [self.initQmatrix]*self.totalStates,
				  [self.initQmatrix]*self.totalStates,
				  [self.initQmatrix]*self.totalStates]
		self.visits = [[0]*self.totalStates,
				  [0]*self.totalStates,
				  [0]*self.totalStates,
				  [0]*self.totalStates]


	def getBestAction(self,state):
		
		if r.random() < self.greed:
			index = self.Q[0].index(state)
			nextAction = 1
			bestVal = self.Q[nextAction][index]
			for i in range(2,5):
				if self.Q[i][index] > bestVal:
					bestVal = self.Q[i][index]
					nextAction = i
			nextAction -= 1
			
		else:
			nextAction = r.randint(0,3)
		
		return nextAction
		
	def updateQmatrix(self,currentState,action,reward,previousState):
		prevStateIndex = self.Q[0].index(previousState)
		nextStateIndex = self.Q[0].index(currentState)
		newDatum = reward+self.discount*self.getMaxValue(currentState)

		self.visits[action][prevStateIndex] += 1
		if not self.alphaFixed:
			self.stepSize = 1.0/self.visits[action][prevStateIndex]
		tmp = (1-self.stepSize)*self.Q[action+1][prevStateIndex]+self.stepSize*newDatum
		self.Q[action+1][prevStateIndex] = tmp

	def getMaxValue(self,state):
		index = self.Q[0].index(state)
		actions = [self.Q[1][index],self.Q[2][index],self.Q[3][index],self.Q[4][index]]
		tmp = actions[actions.index(max(actions))]
		return tmp

	def setGreed(self,newGreed):
		self.greed = newGreed