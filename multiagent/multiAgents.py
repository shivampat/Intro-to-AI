# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # print(successorGameState)
        # print("New Pos", newPos)
        # print("New food", newFood)
        # print("new ghost states", newGhostStates)
        # print("new scared times", newScaredTimes)

        """
        IDEAS:
        * penalize further food, emphasize closer food
        * penalize non-scared ghosts being close to state
        * emphasize closeness to scared ghosts with higher scared times.
        *
        """

        score = successorGameState.getScore()

        capsules = currentGameState.getCapsules()

        if newFood.asList():
            foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
            minFoodDistance = min(foodDistances)
            foodScore = 1.0 / (1 + minFoodDistance)  
        else:
            foodScore = 0

        ghostScore = 0
        minUnscaredDist = 10000000 
        for i, ghostState in enumerate(newGhostStates):
            ghostPos = ghostState.getPosition()
            distance = manhattanDistance(newPos, ghostPos)
            if newScaredTimes[i] == 0:
                minUnscaredDist = min(minUnscaredDist, distance)

            if newScaredTimes[i] > 0:
                ghostScore += 2.0 / (distance + 1) if distance > 0 else 10  #
            elif distance > 0:  
                ghostScore -= 1.5 / (distance + 1)

        capsulesScore = 0
        if capsules:
            capsuleDistances = [manhattanDistance(newPos, capsule) for capsule in capsules]
            minCapsuleDistance = min(capsuleDistances)

            if minUnscaredDist < 1 and minCapsuleDistance < 1: 
                capsulesScore += 5 * minCapsuleDistance 
            else: 
                capsulesScore += 1 / (minCapsuleDistance + 1)

        score += foodScore + capsulesScore + ghostScore
        return score


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def minMax(self, state, depth, agentNum=0):
        # end the thing
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state),  #tuple tuple
        num_agents = state.getNumAgents() #number of agents lol
        new_depth = depth - 1 if agentNum == num_agents - 1 else depth # make depth smol
        next_agent = (agentNum + 1) % num_agents
        legal_actions = state.getLegalActions(agentNum)
        action_evaluations = []
        # recursive evaluation
        for action in legal_actions:
            successor_state = state.generateSuccessor(agentNum, action)
            # go next
            eval_score = self.minMax(successor_state, new_depth, next_agent)[0]
            # add the thing
            action_evaluations.append((eval_score, action))
        if agentNum == 0:
            return max(action_evaluations)  # max dapacman
        else:
            return min(action_evaluations)  # min ghosts

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        #you love it chat im backkkk
        #ok so i need to create a minmax function.
        #and then the function

        return self.minMax(gameState, self.depth)[1]
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def minMax(self, state, depth, agentNum=0, alpha=float('-inf'), beta=float('inf')):
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state),  # tuple tuple
        num_agents = state.getNumAgents()  # number of agents lol
        new_depth = depth - 1 if agentNum == num_agents - 1 else depth  # make depth smol
        next_agent = (agentNum + 1) % num_agents
        legal_actions = state.getLegalActions(agentNum)
        action_evaluations = []
        # recursive evaluation
        for action in legal_actions:
            successor_state = state.generateSuccessor(agentNum, action)
            eval_score = self.minMax(successor_state, new_depth, next_agent, alpha, beta)[0]
            #max
            if agentNum == 0:
                action_evaluations.append((eval_score, action))
                alpha = max(alpha, eval_score)
                if alpha > beta:
                    break #prune
            #min
            else:
                action_evaluations.append((eval_score, action))
                beta = min(beta, eval_score)
                if alpha > beta:
                    break  #prune
        if agentNum == 0:
            return max(action_evaluations)  # max dapacman
        else:
            return min(action_evaluations)  # min ghosts

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.minMax(gameState, self.depth)[1]
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectiMax(self, state, depth, agentNum=0):
        if state.isWin() or state.isLose() or depth == 0:
            return self.evaluationFunction(state),  # tuple tuple
        num_agents = state.getNumAgents()  # number of agents lol
        new_depth = depth - 1 if agentNum == num_agents - 1 else depth  # make depth smol
        next_agent = (agentNum + 1) % num_agents
        legal_actions = state.getLegalActions(agentNum)
        # max
        if agentNum == 0:
            best_score = float('-inf')
            best_action = None
            # eval recursively
            for action in legal_actions:
                successor_state = state.generateSuccessor(agentNum, action)
                eval_score = self.expectiMax(successor_state, new_depth, next_agent)[0]
                if eval_score > best_score:
                    best_score = eval_score
                    best_action = action
            return best_score, best_action
        # min
        else:
            total_score = 0  #score of all ghosts
            #eval all ghosts
            for action in legal_actions:
                successor_state = state.generateSuccessor(agentNum, action)
                eval_score = self.expectiMax(successor_state, new_depth, next_agent)[0]
                total_score += eval_score
            # expected score
            expected_score = total_score / len(legal_actions) if legal_actions else 0
            return expected_score, random.choice(legal_actions)  # chose uniformly

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectiMax(gameState, self.depth)[1]
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION:

    Adding to score: 
    * closeness to capsule and unscared ghost
    * proximity to scared ghost 
    * winning the game (MOST REWARD)
        - isWin() func. or no pellets remaining. 
    * closeness to food pellet


    Removing from score: 
    * proximity to unscared ghost 
    * leaving food/capsules uneaten
    * being eaten (MOST PENALIZED)

    Constants to control how much proximity to food, proximity
    to ghosts, and proximity to capsules contributes to 
    state evaluation. 

    """
    "*** YOUR CODE HERE ***"

    # score variable being modified
    score = currentGameState.getScore()

    # State variables 
    pacmanPos = currentGameState.getPacmanPosition()
    foodList = currentGameState.getFood().asList()
    capsules = currentGameState.getCapsules()
    ghostStates = currentGameState.getGhostStates()

    ### Constants
     
    # Food 
    CLOSE_FOOD_CONST = 10
    REMAINING_FOOD_PENALIZER = 7

    # Ghosts
    SCARED_CONST = 200
    UNSCARED_CONST = 5

    # Capsules
    CLOSE_CAPSULE_CONST = 10
    REMAINING_CAPSULES_PENALIZER = 0.5

    # Food score 
    foodScore = 0
    if foodList:
        closestFoodDist = min([manhattanDistance(pacmanPos, foodPos) for foodPos in foodList])
        foodScore += CLOSE_FOOD_CONST / (closestFoodDist + 1) 
        foodScore -= REMAINING_FOOD_PENALIZER * len(foodList)
    
    # Ghosts (both scared and unscared)
    ghostScore = 0
    minGhostDist = float('inf')
    for ghost in ghostStates:
        ghostDist = manhattanDistance(pacmanPos, ghost.getPosition())
        minGhostDist = min(ghostDist, minGhostDist)
        scaredTimer = ghost.scaredTimer

        if ghostDist == 0 and scaredTimer == 0:
            return float('-inf')

        if scaredTimer == 0:
            ghostScore -= UNSCARED_CONST / (ghostDist + 1)
        else:
            ghostScore += SCARED_CONST * scaredTimer / (ghostDist + 1) 
 

    # Capsule score 
    capsuleScore = 0
    if capsules:
        closestCapsuleDist = min([manhattanDistance(pacmanPos, capsulePos) for capsulePos in capsules])
        capsuleScore += CLOSE_CAPSULE_CONST / (closestCapsuleDist + 1)
        capsuleScore -= REMAINING_CAPSULES_PENALIZER * len(capsules)

    # Final consts
    FOOD = 20
    GHOST = 30
    CAPSULE = 10

    MAKE_A_MOVE = 10 

    score += FOOD*foodScore + GHOST*ghostScore + CAPSULE*capsuleScore + MAKE_A_MOVE
    return score 

# Abbreviation
better = betterEvaluationFunction