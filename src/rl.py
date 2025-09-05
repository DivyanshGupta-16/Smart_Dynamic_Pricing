
import numpy as np
import random
from collections import defaultdict

class DynamicPricingEnv:
    """
    Simple episodic environment walking rows of a dataframe-like object
    with the following columns present (strings allowed for levels):
    - Demand_Level
    - Supply_Level
    - Customer_Loyalty_Status
    - Historical_Cost_of_Ride
    """
    def __init__(self, df):
        self.df = df.reset_index(drop=True)
        # Allowed multipliers for price
        self.actions = [0.8, 1.0, 1.2, 1.4]
        self.reset()

    def reset(self):
        self.idx = 0
        self.done = False
        return self._state(self.df.iloc[self.idx])

    def _state(self, row):
        return (row["Demand_Level"], row["Supply_Level"], row.get("Customer_Loyalty_Status", "Regular"))

    def step(self, action_index: int):
        row = self.df.iloc[self.idx]
        multiplier = self.actions[action_index]
        # Derive a naive base_cost proxy
        base_cost = float(row["Historical_Cost_of_Ride"]) / 1.2
        revenue = base_cost * multiplier

        # Reward is (revenue - base), clipped to avoid runaway updates
        reward = max(-50.0, min(50.0, revenue - base_cost))

        self.idx += 1
        if self.idx >= len(self.df):
            self.done = True

        next_state = None if self.done else self._state(self.df.iloc[self.idx])
        return next_state, reward, self.done

class QLearningAgent:
    def __init__(self, n_actions: int, learning_rate: float = 0.1, discount: float = 0.95, epsilon: float = 0.2):
        self.q = defaultdict(lambda: np.zeros(n_actions))
        self.lr = learning_rate
        self.gamma = discount
        self.epsilon = epsilon
        self.n_actions = n_actions

    def act(self, state):
        if random.random() < self.epsilon:
            return random.randrange(self.n_actions)
        return int(np.argmax(self.q[state]))

    def learn(self, s, a, r, s_next):
        q_sa = self.q[s][a]
        target = r
        if s_next is not None:
            target = r + self.gamma * np.max(self.q[s_next])
        self.q[s][a] += self.lr * (target - q_sa)

def train_q_agent(env, episodes: int = 20, epsilon_decay: float = 0.97):
    agent = QLearningAgent(n_actions=len(env.actions), epsilon=0.3)
    for _ in range(episodes):
        s = env.reset()
        done = False
        while not done:
            a = agent.act(s)
            s_next, r, done = env.step(a)
            agent.learn(s, a, r, s_next)
            s = s_next
        agent.epsilon *= epsilon_decay
    return agent
