import random
import pickle
import os
import numpy as np


'''
This template serves as a starting point for your agent.
'''


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
        # self.opponent_number = 1 - agent_number  # index for opponent

        self.t1 = 2.7193025761078644
        self.t2 = 2.7215555543935457
        self.t3 = 7.262601783583493

        with open('agents/dealmakers/8_models_dict.pkl', 'rb') as f:
            self.models = pickle.load(f)

        with open('agents/dealmakers/dp_policy.pkl', 'rb') as f:
            self.dp_policy = pickle.load(f)

        self.seg_multipliers = {key: 1.0 for key in self.dp_policy.keys()}
        self.seg_sale_history = {key: [] for key in self.dp_policy.keys()}

        self.last_seg_key = None
        self.last_price = 100.0

        self.opponent_price_history = []
        self.my_price_history = []
        self.last_sale_winner = None

        self.PRICE_GRID = np.linspace(0.01, 500, 100)

    def _calculate_expected_profit(self, P, C1, C2, C3, seg_key):
        model = self.models[seg_key]
        prob = model.predict_proba([[C1, C2, C3, P]])[0, 1]
        return P * prob

    def _calculate_price_multiplier(self, T, I):
        diff = T - I
        if diff > 0:
            return 1 + diff * 0.03
        elif diff < 0:
            return 1 - abs(diff) * 0.02
        return 1.0

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
        # did_customer_buy_from_opponent = (last_sale[0] == self.opponent_number)

        ### keep track of the prices that were offered in the last sale
        my_last_prices = last_sale[1][self.this_agent_number]
        ### potentially useful for Part 2
        # opponent_last_prices = last_sale[1][self.opponent_number]

        ### keep track of the profit for this agent after the last sale
        my_current_profit = state[self.this_agent_number]
        ### potentially useful for Part 2
        # opponent_current_profit = state[self.opponent_number]

        ### keep track of the inventory levels after the last sale
        self.remaining_inventory = inventories[self.this_agent_number]
        ### potentially useful for Part 2
        # opponent_inventory = inventories[self.opponent_number]

        ### keep track of the time until the next replenishment
        time_until_replenish = time_until_replenish

        ### TODO - add your code here to potentially update your pricing strategy 
        ### based on what happened in the last round
        winner = last_sale[0]
        self.last_sale_winner = winner

        my_price = last_sale[1][self.this_agent_number]
        opp_price = last_sale[1][1 - self.this_agent_number]

        self.my_price_history.append(my_price)
        self.opponent_price_history.append(opp_price)

        if len(self.my_price_history) > 10:
            self.my_price_history.pop(0)
            self.opponent_price_history.pop(0)

        if self.last_seg_key is None:
            return

        seg_key = self.last_seg_key
        history = self.seg_sale_history[seg_key]

        did_buy = (winner == self.this_agent_number)
        history.append(1 if did_buy else 0)
        if len(history) > 5:
            history.pop(0)

        if len(history) >= 3:
            br = sum(history) / len(history)
            m = self.seg_multipliers[seg_key]

            if br >= 0.8:
                m *= 1.15
            elif br <= 0.2:
                m *= 0.90
            elif br >= 0.6:
                m *= 1.05
            elif br <= 0.4:
                m *= 0.97

            self.seg_multipliers[seg_key] = np.clip(m, 0.8, 1.3)

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
        C1, C2, C3 = new_buyer_covariates
        seg_key = (C1 > self.t1, C2 > self.t2, C3 > self.t3)
        self.last_seg_key = seg_key

        I = int(self.remaining_inventory)
        if I <= 0:
            return 999.0

        t = max(0, min(time_until_replenish, self.dp_policy[seg_key].shape[1] - 1))
        p_dp = self.dp_policy[seg_key][I][t]
        if p_dp <= 0:
            p_dp = 50.0

        m = self.seg_multipliers[seg_key]
        p_dp = p_dp * m

        best_p = 100
        best_rev = -1
        model = self.models[seg_key]

        for p_test in self.PRICE_GRID:
            rev = p_test * model.predict_proba([[C1, C2, C3, p_test]])[0, 1]
            if rev > best_rev:
                best_rev = rev
                best_p = p_test

        p_static = best_p * m

        prob_dp = model.predict_proba([[C1, C2, C3, p_dp]])[0, 1]
        prob_static = model.predict_proba([[C1, C2, C3, p_static]])[0, 1]

        rev_dp = p_dp * prob_dp
        rev_static = p_static * prob_static

        if rev_static > rev_dp * 1.03:
            p_final = p_static
        else:
            p_final = p_dp

        opp_last = last_sale[1][1 - self.this_agent_number]

        if opp_last > 0:

            if p_final >= opp_last:
                p_final = opp_last - 0.5

            elif self.last_sale_winner == self.this_agent_number:
                pass

            if len(self.opponent_price_history) >= 3:
                if (self.opponent_price_history[-1] < self.my_price_history[-1] and
                    self.opponent_price_history[-2] < self.my_price_history[-2] and
                    self.opponent_price_history[-3] < self.my_price_history[-3]):

                    p_final = min(p_final, opp_last - 2.0)


        p_final = float(np.clip(p_final, 5.0, 500.0))
        self.last_price = p_final

        return p_final

