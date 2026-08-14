import random
import pickle
import os
import numpy as np


'''
This template serves as a starting point for your agent.
'''


#picklefile = open('agents/dealmakers/8_models_dict.pkl', 'rb')
#new_models = pickle.load(picklefile)

picklefile = open('agents/dealmakers/8_xgb.pkl', 'rb')
new_models = pickle.load(picklefile)

class Agent(object):
    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number  # index for this agent
        
        self.project_part = params['project_part'] 

        ### starting remaining inventory and inventory replenish rate are provided
        ## every time the inventory is replenished, it is set to the inventory limit
        ## the inventory_replenish rate is how often the inventory is replenished
        ## for example, we will run with inventory_replenish = 20, with the limit of 11. Then, the inventory will be replenished every 20 time steps (time steps 0, 20, 40, ...) and the inventory will be set to 11 at those time steps. 
        self.remaining_inventory = params['inventory_limit']
        self.inventory_replenish = params['inventory_replenish']

        ### useful if you want to use a more complex price prediction model
        ### note that you will need to change the name of the path and this agent file when submitting
        ### complications: pickle works with any machine learning models defined in sklearn, xgboost, etc.
        ### however, this does not work with custom defined classes, due to the way pickle serializes objects
        ### refer to './yourteamname/create_model.ipynb' for a quick tutorial on how to use pickle
        # self.filename = './[yourteamname]/trained_model'
        # self.trained_model = pickle.load(open(self.filename, 'rb'))

        ### potentially useful for Part 2 -- When competition is between two agents
        ### and you want to keep track of the opponent's status
        self.opponent_number = 1 - agent_number  # index for opponent
        
        self.PRICE_GRID = np.linspace(0.01, 500, 100)
    
    def _calculate_expected_profit(self, P, C1, C2, C3):
        # Calculate the expect profit from the single costomer
        t1 = 2.7193025761078644
        t2 = 2.7215555543935457
        t3 = 7.262601783583493

        key = (int(C1 > t1), int(C2 > t2), int(C3 > t3))
        model = new_models[key]

        X = [[P, C1, C2, C3]]
        prob_buy = model.predict_proba(X)[0, 1]

        return float(P * prob_buy)
    
    def _calculate_competitive_multiplier(self, T, I_self, I_opp):
        """
        根據 市場飽和度 (Saturation) 與 庫存位勢 (Inventory Position) 
        計算價格調整係數 (Multiplier)
        """
        if T <= 0: return 0.5 
        if I_self <= 0: return 1.0 


        total_inventory = I_self + I_opp
        market_saturation = total_inventory / float(T)

        inventory_ratio = I_self / (I_opp + 0.01)

        alpha = 1.0


        if market_saturation > 1.0:
            if inventory_ratio > 1.0: 

                alpha = 0.85 
            elif inventory_ratio < 1.0:

                alpha = 0.95
            else:

                alpha = 0.90


        else: 
            if inventory_ratio > 1.0:

                alpha = 0.98 
            elif inventory_ratio < 1.0:

                alpha = 1.10 
            else:

                alpha = 1.0

        return alpha

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
        ### potentially useful for Part 2
        did_customer_buy_from_opponent = (last_sale[0] == self.opponent_number)

        ### keep track of the prices that were offered in the last sale
        my_last_prices = last_sale[1][self.this_agent_number]
        ### potentially useful for Part 2
        opponent_last_prices = last_sale[1][self.opponent_number]

        ### keep track of the profit for this agent after the last sale
        my_current_profit = state[self.this_agent_number]
        ### potentially useful for Part 2
        opponent_current_profit = state[self.opponent_number]

        ### keep track of the inventory levels after the last sale
        self.remaining_inventory = inventories[self.this_agent_number]
        ### potentially useful for Part 2
        self.opponent_inventory = inventories[self.opponent_number]

        ### keep track of the time until the next replenishment
        time_until_replenish = time_until_replenish

        ### TODO - add your code here to potentially update your pricing strategy 
        ### based on what happened in the last round
        pass

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

        ### currently output is just a deterministic price for the item
        ### but you are expected to use the new_buyer_covariates
        ### combined with models you come up with using the training data 
        ### and history of prices from each team to set a better price for the item
        if self.remaining_inventory <= 0:
            return 1000.0
        
        T = time_until_replenish

        I_t = self.remaining_inventory
        I_opp = self.opponent_inventory
        
        C1, C2, C3 = new_buyer_covariates

        max_profit = -1.0
        optimal_price = 1000.0

        for P_test in self.PRICE_GRID:
            current_profit = self._calculate_expected_profit(P_test, C1, C2, C3)
            
            if current_profit > max_profit:
                max_profit = current_profit
                optimal_price = P_test

        multiplier = self._calculate_competitive_multiplier(T, I_t, I_opp)

        P_offer = optimal_price * multiplier

        P_offer = max(0.01, P_offer)

        return P_offer
        # return optimal_price

