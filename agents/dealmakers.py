import pickle
import os
import numpy as np
import xgboost
from functools import lru_cache
from collections import deque


'''
Unified Agent: Meta-Agent Strategy
Integrates David (DP) and NewAgent (Inventory/Saturation Heuristic)
'''

picklefile = open('agents/dealmakers/8_models_dict.pkl', 'rb')
MODELS_LOGREG = pickle.load(picklefile)

picklefile = open('agents/dealmakers/dp_policy.pkl', 'rb')
DP_POLICY = pickle.load(picklefile)

picklefile = open('agents/dealmakers/8_xgb.pkl', 'rb')
MODELS_XGB = pickle.load(picklefile)

PRICE_GRID = np.linspace(0.01, 500, 100)

XGRID_LOGREG_TEMPLATE = np.zeros((PRICE_GRID.shape[0], 4), dtype=float)
XGRID_LOGREG_TEMPLATE[:, 3] = PRICE_GRID

XGRID_XGB_TEMPLATE = np.zeros((PRICE_GRID.shape[0], 4), dtype=float)
XGRID_XGB_TEMPLATE[:, 0] = PRICE_GRID


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

X_SINGLE_LOGREG = np.zeros((1, 4), dtype=np.float32)
X_SINGLE_XGB = np.zeros((1, 4), dtype=np.float32)


@lru_cache(maxsize=200000)
def cached_logreg_grid_pred(seg_key, C1, C2, C3):
    if not MODELS_LOGREG or seg_key not in MODELS_LOGREG:
        return tuple([0.5] * PRICE_GRID.size)

    model = MODELS_LOGREG[seg_key]
    X = XGRID_LOGREG_TEMPLATE.copy()
    X[:, 0] = C1
    X[:, 1] = C2
    X[:, 2] = C3

    probs = model.predict_proba(X)[:, 1]
    return tuple(probs.astype(np.float32))


@lru_cache(maxsize=200000)
def cached_single_logreg(seg_key, C1, C2, C3, price):
    if not MODELS_LOGREG or seg_key not in MODELS_LOGREG:
        return 0.5

    model = MODELS_LOGREG[seg_key]
    X_SINGLE_LOGREG[0, 0] = C1
    X_SINGLE_LOGREG[0, 1] = C2
    X_SINGLE_LOGREG[0, 2] = C3
    X_SINGLE_LOGREG[0, 3] = price
    prob = model.predict_proba(X_SINGLE_LOGREG)[0, 1]
    return float(prob)


@lru_cache(maxsize=200000)
def cached_xgb_grid_pred(seg_key, C1, C2, C3):
    if not MODELS_XGB or seg_key not in MODELS_XGB:
        return tuple([0.5] * PRICE_GRID.size)

    model = MODELS_XGB[seg_key]
    X = XGRID_XGB_TEMPLATE.copy()
    X[:, 1] = C1
    X[:, 2] = C2
    X[:, 3] = C3

    probs = model.predict_proba(X, validate_features=False)[:, 1]
    return tuple(probs.astype(np.float32))


class DavidSubAgent(object):
    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number
        self.remaining_inventory = params['inventory_limit']

        self.models = MODELS_LOGREG
        self.dp_policy = DP_POLICY

        self.t1 = 2.7193025761078644
        self.t2 = 2.7215555543935457
        self.t3 = 7.262601783583493

        if self.dp_policy:
            self.seg_multipliers = {key: 1.0 for key in self.dp_policy.keys()}
            self.seg_sale_history = {key: deque(maxlen=5) for key in self.dp_policy.keys()}
        else:
            self.seg_multipliers = {}
            self.seg_sale_history = {}

        self.last_seg_key = None
        self.last_sale_winner = None

        self.opponent_price_history = deque(maxlen=10)
        self.my_price_history = deque(maxlen=10)

        self.PRICE_GRID = PRICE_GRID

    def _process_last_sale(self, last_sale, state, inventories, time_until_replenish):
        self.remaining_inventory = inventories[self.this_agent_number]

        if last_sale[0] is None:
            return

        winner = last_sale[0]
        self.last_sale_winner = winner

        my_price = last_sale[1][self.this_agent_number]
        opp_price = last_sale[1][1 - self.this_agent_number]

        self.my_price_history.append(my_price)
        self.opponent_price_history.append(opp_price)

        if self.last_seg_key is None or self.last_seg_key not in self.seg_sale_history:
            return

        seg_key = self.last_seg_key
        history = self.seg_sale_history[seg_key]

        did_buy = (winner == self.this_agent_number)
        history.append(1 if did_buy else 0)

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

            self.seg_multipliers[seg_key] = float(np.clip(m, 0.8, 1.3))

    def action(self, obs):
        new_buyer_covariates, last_sale, state, inventories, time_until_replenish = obs
        self._process_last_sale(last_sale, state, inventories, time_until_replenish)

        if self.remaining_inventory <= 0:
            return 999.0

        C1, C2, C3 = new_buyer_covariates

        seg_key = (C1 > self.t1, C2 > self.t2, C3 > self.t3)
        self.last_seg_key = seg_key

        models = self.models
        if not models or seg_key not in models:
            return 50.0

        model = models[seg_key]

        I = int(self.remaining_inventory)
        dp_policy = self.dp_policy

        if dp_policy and seg_key in dp_policy:
            max_t = dp_policy[seg_key].shape[1] - 1
            max_i = dp_policy[seg_key].shape[0] - 1
            t = max(0, min(time_until_replenish, max_t))
            i_idx = max(0, min(I, max_i))

            p_dp = dp_policy[seg_key][i_idx][t]
            if p_dp <= 0:
                p_dp = 50.0
        else:
            p_dp = 50.0

        m = self.seg_multipliers.get(seg_key, 1.0)
        p_dp = p_dp * m

        price_grid = self.PRICE_GRID

        probs_grid = np.fromiter(
            cached_logreg_grid_pred(seg_key, float(C1), float(C2), float(C3)),
            dtype=np.float32
        )
        rev_grid = price_grid * probs_grid
        best_idx = int(np.argmax(rev_grid))
        best_p = float(price_grid[best_idx])

        p_static = best_p * m

        prob_dp = cached_single_logreg(seg_key, float(C1), float(C2), float(C3), float(p_dp))
        prob_static = cached_single_logreg(seg_key, float(C1), float(C2), float(C3), float(p_static))

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

            if len(self.opponent_price_history) >= 3:
                if (self.opponent_price_history[-1] < self.my_price_history[-1] and
                    self.opponent_price_history[-2] < self.my_price_history[-2] and
                    self.opponent_price_history[-3] < self.my_price_history[-3]):
                    p_final = min(p_final, opp_last - 2.0)

        return float(np.clip(p_final, 5.0, 500.0))


class NewSubAgent(object):
    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number
        self.opponent_number = 1 - agent_number
        self.remaining_inventory = params['inventory_limit']
        self.opponent_inventory = params['inventory_limit']

        self.models = MODELS_XGB

        self.t1 = 2.7193025761078644
        self.t2 = 2.7215555543935457
        self.t3 = 7.262601783583493

        self.PRICE_GRID = PRICE_GRID

    def _calculate_expected_profit(self, P, C1, C2, C3):
        key = (int(C1 > self.t1), int(C2 > self.t2), int(C3 > self.t3))

        if not self.models or key not in self.models:
            return P * 0.5

        model = self.models[key]
        X_SINGLE_XGB[0, 0] = P
        X_SINGLE_XGB[0, 1] = C1
        X_SINGLE_XGB[0, 2] = C2
        X_SINGLE_XGB[0, 3] = C3
        try:
            prob_buy = model.predict_proba(X_SINGLE_XGB, validate_features=False)[0, 1]
        except Exception:
            prob_buy = 0.5

        return float(P * prob_buy)

    def _calculate_expected_profit_vectorized(self, P_array, C1, C2, C3):
        key = (int(C1 > self.t1), int(C2 > self.t2), int(C3 > self.t3))

        if not self.models or key not in self.models:
            return P_array * 0.5

        probs = np.fromiter(
            cached_xgb_grid_pred(key, float(C1), float(C2), float(C3)),
            dtype=np.float32
        )

        return P_array * probs

    def _calculate_competitive_multiplier(self, T, I_self, I_opp):
        if T <= 0:
            return 0.5
        if I_self <= 0:
            return 1.0

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

    def action(self, obs):
        new_buyer_covariates, last_sale, state, inventories, time_until_replenish = obs

        self.remaining_inventory = inventories[self.this_agent_number]
        self.opponent_inventory = inventories[self.opponent_number]

        if self.remaining_inventory <= 0:
            return 1000.0

        T = time_until_replenish
        I_t = self.remaining_inventory
        I_opp = self.opponent_inventory
        C1, C2, C3 = new_buyer_covariates

        price_grid = self.PRICE_GRID
        optimal_price = 1000.0

        if self.models:
            profits = self._calculate_expected_profit_vectorized(price_grid, C1, C2, C3)
            best_idx = int(np.argmax(profits))
            optimal_price = float(price_grid[best_idx])
        else:
            optimal_price = 50.0

        multiplier = self._calculate_competitive_multiplier(T, I_t, I_opp)
        P_offer = optimal_price * multiplier

        return max(0.01, P_offer)


class Agent(object):
    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number
        self.opponent_number = 1 - agent_number
        self.project_part = params.get("project_part", 2)

        self.na_agent = NewSubAgent(agent_number, params)
        self.dp_agent = DavidSubAgent(agent_number, params)

        self.step = 0
        self.DETECT_STEPS = 80
        self.opp_prices = []
        self.mode = "detect"

    def _update_detection_stats(self, last_sale):
        if last_sale is None or last_sale[0] is None:
            return

        try:
            opp_price = float(last_sale[1][self.opponent_number])
            if opp_price > 0 and not np.isnan(opp_price):
                self.opp_prices.append(opp_price)
        except Exception:
            pass

    def _decide_mode_if_ready(self):
        if self.mode != "detect":
            return
        if self.step < self.DETECT_STEPS:
            return

        if len(self.opp_prices) < 10:
            self.mode = "use_na"
            return

        prices = np.array(self.opp_prices, dtype=np.float32)
        if prices.size <= 1:
            self.mode = "use_na"
            return

        diffs = np.abs(np.diff(prices))

        frac_small_move = float(np.mean(diffs < 1.0))
        price_std = float(np.std(prices))

        if frac_small_move > 0.7 and price_std < 15.0:
            self.mode = "use_dp"
        else:
            self.mode = "use_na"

    def action(self, obs):
        price_na = self.na_agent.action(obs)
        price_dp = self.dp_agent.action(obs)

        new_buyer_covariates, last_sale, state, inventories, time_until_replenish = obs

        if self.mode == "detect":
            self._update_detection_stats(last_sale)
            self.step += 1
            self._decide_mode_if_ready()

        if self.mode == "detect":
            chosen_price = price_na
        elif self.mode == "use_na":
            chosen_price = price_na
        else:
            chosen_price = price_dp

        return float(chosen_price)
