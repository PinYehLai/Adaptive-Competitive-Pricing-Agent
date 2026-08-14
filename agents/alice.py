import random
import pickle
import os
import numpy as np


'''
This template serves as a starting point for your agent.
'''


picklefile = open('agents/dealmakers/8_xgb.pkl', 'rb')
new_models = pickle.load(picklefile)

class Agent(object):
    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number  # index for this agent
        self.opponent_number = 1 - self.this_agent_number
        self.project_part = params['project_part'] 

       
        self.remaining_inventory = params['inventory_limit']
        self.inventory_replenish = params['inventory_replenish']
        self.PRICE_GRID = np.linspace(0.01, 500, 100)

        self.inv_limit = params['inventory_limit']
        self.last_opponent_price = None
        self.last_outcome = None

    
    def _calculate_expected_profit_vectorized(self, C1, C2, C3):
        # thresholds
        t1 = 2.7193025761078644
        t2 = 2.7215555543935457
        t3 = 7.262601783583493

        # determine which model to use
        key = (int(C1 > t1), int(C2 > t2), int(C3 > t3))
        model = new_models[key]

        # vectorized feature matrix: shape (100, 4)
        # price_item first
        X_batch = np.column_stack([
            self.PRICE_GRID,
            np.full_like(self.PRICE_GRID, C1),
            np.full_like(self.PRICE_GRID, C2),
            np.full_like(self.PRICE_GRID, C3),
        ])

    # one prediction call instead of 100
        probs = model.predict_proba(X_batch)[:, 1]

        # expected profit = price * prob
        return probs * self.PRICE_GRID
    
    def _calculate_price_multiplier(self, T):
        IOVH = self._compute_IOVH_adjustment(T)
        OLM = self._compute_OLM_adjustment()
        return (1 + IOVH) * (1 + OLM)

    def _process_last_sale(
            self, 
            last_sale,
            state,
            inventories,
            time_until_replenish
        ):
        '''
        This function updates your internal state based on the last sale that occurred.
        This template shows you several ways you can keep track of important metrics.
        '''
        ### keep track of who, if anyone, the customer bought from
        did_customer_buy_from_me = (last_sale[0] == self.this_agent_number)
        did_customer_buy_from_opponent = (last_sale[0] == self.opponent_number)

        ### keep track of the prices that were offered in the last sale
        my_last_prices = last_sale[1][self.this_agent_number]
        self.opponent_last_prices = last_sale[1][self.opponent_number]

        ### keep track of the profit for this agent after the last sale
        my_current_profit = state[self.this_agent_number]
        opponent_current_profit = state[self.opponent_number]

        ### keep track of the inventory levels after the last sale
        self.remaining_inventory = inventories[self.this_agent_number]
        opponent_inventory = inventories[self.opponent_number]

        ### keep track of the time until the next replenishment
        time_until_replenish = time_until_replenish

        # outcome tracking: +1 = we won, -1 = we lost, 0 = no purchase
        if did_customer_buy_from_me:
            self.last_outcome = +1
        elif did_customer_buy_from_opponent:
            self.last_outcome = -1
        else:
            self.last_outcome = 0

    def _compute_IOVH_adjustment(self, T):
        """
        Inventory Option Value Heuristic
        """
        I_t = self.remaining_inventory
        I_max = self.inv_limit['max']
        T_max = self.inventory_replenish

        alpha = 0.15  # tune this hyperparameter

        raw = alpha * ((T / T_max) - (I_t / I_max))

        # Clamp for safety
        raw = np.clip(raw, -0.3, 0.4)

        return raw
        
    def _compute_OLM_adjustment(self):
        """
        Opponent-Lead Margin:
        Punish if opponent undercut and won.
        Reward if opponent overpriced and lost.
        """
        if self.last_opponent_price is None or self.last_outcome is None:
            return 0.0

        gamma = 0.04

        # opponent undercut us and won
        if self.last_outcome == -1:
            return -gamma

        # opponent overpriced and lost
        if self.last_outcome == +1:
            return +gamma

        return 0.0


    def action(self, obs):
        '''
        This function is called every time the agent needs to choose an action by the environment.

        The input 'obs' is a 5 tuple, containing the following information:
        -- new_buyer_covariates: a vector of length 3, containing the covariates of the new buyer.
        -- last_sale: a tuple of length 2. The first element is the index of the agent that made the last sale, if it is NaN, then the customer did not make a purchase. The second element is a numpy array of length n_agents, containing the prices that were offered by each agent in the last sale.
        -- state: a vector of length n_agents, containing the current profit of each agent.
        -- inventories: a vector of length n_agents, containing the current inventory level of each agent.
        -- time_until_replenish: an integer indicating the time until the next replenishment, by which time your (and your opponent's, in part 2) remaining inventory will be reset to the inventory limit.

        The expected output is a single number, indicating the price that you would post for the new buyer.
        '''

        new_buyer_covariates, last_sale, state, inventories, time_until_replenish = obs
        self._process_last_sale(last_sale, state, inventories, time_until_replenish)

        if self.remaining_inventory <= 0:
            return 999.0

        C1, C2, C3 = new_buyer_covariates

        # 1. Base myopic optimal price
        profit_array = self._calculate_expected_profit_vectorized(C1, C2, C3)
        optimal_price = self.PRICE_GRID[np.argmax(profit_array)]

        # 2. Dynamic multiplier
        multiplier = self._calculate_price_multiplier(time_until_replenish)

        P_offer = optimal_price * multiplier
        return max(0.01, min(500, P_offer))
