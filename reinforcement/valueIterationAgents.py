# valueIterationAgents.py
# -----------------------
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


# valueIterationAgents.py
# -----------------------
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


import mdp
import util

from learningAgents import ValueEstimationAgent
import collections


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp: mdp.MarkovDecisionProcess, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0
        self.runValueIteration()

    def runValueIteration(self):
        """
          Run the value iteration algorithm. Note that in standard
          value iteration, V_k+1(...) depends on V_k(...)'s.
        """
        "*** YOUR CODE HERE ***"

        "Reference markov decision process as markov"
        markov = self.mdp

        "Grab first state in MDP and create reference to all states"
        states = self.mdp.getStates()

        "Value dictionary"
        values = self.values

        """
        Algorithm:
            1. Get possible actions (getPossibleActions()) for current state.
            2. Create temporary value dictionary for current iteration.
            3. Run through accepted actions for current state and find
               max value action.
            4. Update temp dictionary with value, and move to that state.
            5. Repeat steps 2-4 until all states reached.
            6. Update values with temp dictionary, reset state.
        """
        for i in range(self.iterations):
            new_values = values.copy()
            for state in states:
                # Skip terminal state
                if markov.isTerminal(state):
                    new_values[state] = 0
                    continue
                max_val = float("-inf")
                for action in markov.getPossibleActions(state):
                    max_val = max(
                        max_val, self.computeQValueFromValues(state, action))
                new_values[state] = max_val
            self.values = new_values

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        values = self.values
        markov = self.mdp

        q = 0

        for nextState, prob in markov.getTransitionStatesAndProbs(state, action):
            reward = markov.getReward(state, action, nextState)

            # Q(s,a) = sigma T(s,a,s') [R(s,a,s') + discount * V(s')]
            q += prob * (reward + self.discount * values[nextState])

        return q
        # util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        if self.mdp.isTerminal(state):
            return None

        max_val = float("-inf")
        best_action = None

        for action in self.mdp.getPossibleActions(state):
            q_value = 0

            for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                reward = self.mdp.getReward(state, action, nextState)
                q_value += prob * (reward + self.discount *
                                   self.values[nextState])

            if q_value > max_val:
                max_val = q_value
                best_action = action

        return best_action

        """
        "*** YOUR CODE HERE ***"
        if self.mdp.isTerminal(state):
            return None

        max_val = float("-inf")
        next = None

        # print(self.values[state], state)

        for action in self.mdp.getPossibleActions(state):
            q = 0
            for nextState, prob in self.mdp.getTransitionStatesAndProbs(state, action):
                q = self.getQValue(nextState, action)
                if q > max_val:
                    max_val = q
                    next = action
        return next
        """

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
