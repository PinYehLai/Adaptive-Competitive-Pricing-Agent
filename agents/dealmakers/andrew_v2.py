import random
import pickle
import os
import numpy as np
import sys

# 嘗試匯入 XGBoost，避免環境沒安裝導致 Crash
try:
    import xgboost
except ImportError:
    pass  # 如果沒有 XGBoost，但在 Pickle Load 時可能會報錯，需確保環境有安裝

'''
Unified Agent: Meta-Agent Strategy
Integrates David (DP) and NewAgent (Inventory/Saturation Heuristic)
'''

# --- 1. 全局載入模型 (避免重複載入) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_pickle_safe(filename):
    """安全載入 Pickle，嘗試不同路徑組合"""
    paths_to_try = [
        os.path.join(BASE_DIR, filename),               # 絕對路徑
        os.path.join('agents', 'dealmakers', filename), # 相對路徑 1
        os.path.join('dealmakers', filename),           # 相對路徑 2
        filename                                       # 當前路徑
    ]
    for p in paths_to_try:
        if os.path.exists(p):
            try:
                with open(p, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                print(f"Error loading {p}: {e}")
    return None


# 載入 David 需要的模型 (Logistic Regression & DP Policy)
MODELS_LOGREG = load_pickle_safe('8_models_dict.pkl')
DP_POLICY = load_pickle_safe('dp_policy.pkl')

# 載入 NewAgent 需要的模型 (XGBoost)
MODELS_XGB = load_pickle_safe('8_xgb.pkl')


# --- 2. 定義 Sub-Agent: David (DP Strategy) ---
class DavidSubAgent(object):
    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number
        self.remaining_inventory = params['inventory_limit']

        # 引用全局載入的模型
        self.models = MODELS_LOGREG
        self.dp_policy = DP_POLICY

        # 分群閾值
        self.t1 = 2.7193025761078644
        self.t2 = 2.7215555543935457
        self.t3 = 7.262601783583493

        # 內部狀態
        if self.dp_policy:
            self.seg_multipliers = {key: 1.0 for key in self.dp_policy.keys()}
            self.seg_sale_history = {key: [] for key in self.dp_policy.keys()}
        else:
            self.seg_multipliers = {}
            self.seg_sale_history = {}

        self.last_seg_key = None
        self.last_sale_winner = None
        self.opponent_price_history = []
        self.my_price_history = []
        self.PRICE_GRID = np.linspace(0.01, 500, 100)

    def _process_last_sale(self, last_sale, state, inventories, time_until_replenish):
        self.remaining_inventory = inventories[self.this_agent_number]

        if last_sale[0] is None:  # No sale
            return

        winner = last_sale[0]
        self.last_sale_winner = winner

        my_price = last_sale[1][self.this_agent_number]
        opp_price = last_sale[1][1 - self.this_agent_number]

        self.my_price_history.append(my_price)
        self.opponent_price_history.append(opp_price)

        if len(self.my_price_history) > 10:
            self.my_price_history.pop(0)
            self.opponent_price_history.pop(0)

        if self.last_seg_key is None or self.last_seg_key not in self.seg_sale_history:
            return

        seg_key = self.last_seg_key
        history = self.seg_sale_history[seg_key]

        did_buy = (winner == self.this_agent_number)
        history.append(1 if did_buy else 0)
        if len(history) > 5:
            history.pop(0)

        # 根據最近銷售成功率調整 multiplier
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
        new_buyer_covariates, last_sale, state, inventories, time_until_replenish = obs
        self._process_last_sale(last_sale, state, inventories, time_until_replenish)

        if self.remaining_inventory <= 0:
            return 999.0

        C1, C2, C3 = new_buyer_covariates
        t1 = self.t1
        t2 = self.t2
        t3 = self.t3

        seg_key = (C1 > t1, C2 > t2, C3 > t3)
        self.last_seg_key = seg_key

        # 防呆：如果模型沒載入成功
        models = self.models
        if not models or seg_key not in models:
            return 50.0

        model = models[seg_key]

        # DP Policy Look up
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

        # === 向量化搜尋最佳 Greedy 價格 (邏輯不變) ===
        price_grid = self.PRICE_GRID
        # 建立特徵矩陣 [[C1, C2, C3, p] for p in grid]
        X_grid = np.column_stack([
            np.full_like(price_grid, C1, dtype=float),
            np.full_like(price_grid, C2, dtype=float),
            np.full_like(price_grid, C3, dtype=float),
            price_grid.astype(float)
        ])
        probs_grid = model.predict_proba(X_grid)[:, 1]
        rev_grid = price_grid * probs_grid
        best_idx = int(np.argmax(rev_grid))
        best_p = price_grid[best_idx]
        best_rev = rev_grid[best_idx]

        p_static = best_p * m

        # 比較 DP 價格和 Static 價格的預期收益
        # p_dp 可能不在 grid 上，所以單獨預測
        prob_dp = model.predict_proba([[C1, C2, C3, p_dp]])[0, 1]
        prob_static = model.predict_proba([[C1, C2, C3, p_static]])[0, 1]

        rev_dp = p_dp * prob_dp
        rev_static = p_static * prob_static

        if rev_static > rev_dp * 1.03:
            p_final = p_static
        else:
            p_final = p_dp

        # 對手價格競爭邏輯
        opp_last = last_sale[1][1 - self.this_agent_number]
        if opp_last > 0:
            if p_final >= opp_last:
                p_final = opp_last - 0.5

            # 檢查對手是否連續降價 (Price War Detection)
            if len(self.opponent_price_history) >= 3:
                if (self.opponent_price_history[-1] < self.my_price_history[-1] and
                    self.opponent_price_history[-2] < self.my_price_history[-2] and
                    self.opponent_price_history[-3] < self.my_price_history[-3]):
                    p_final = min(p_final, opp_last - 2.0)

        return float(np.clip(p_final, 5.0, 500.0))


# --- 3. 定義 Sub-Agent: NewAgent (Inventory/Saturation Heuristic) ---
class NewSubAgent(object):
    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number
        self.opponent_number = 1 - agent_number
        self.remaining_inventory = params['inventory_limit']
        self.opponent_inventory = params['inventory_limit']  # 估計值，會更新

        # 引用全局載入的模型 (XGBoost)
        self.models = MODELS_XGB

        # 閾值 (跟 David 一樣，用於 XGBoost 字典鍵值)
        self.t1 = 2.7193025761078644
        self.t2 = 2.7215555543935457
        self.t3 = 7.262601783583493

        self.PRICE_GRID = np.linspace(0.01, 500, 100)

    def _calculate_expected_profit(self, P, C1, C2, C3):
        # 原本單點版本 (保留邏輯，必要時仍可調用)
        key = (int(C1 > self.t1), int(C2 > self.t2), int(C3 > self.t3))

        if not self.models or key not in self.models:
            return P * 0.5

        model = self.models[key]
        X = [[P, C1, C2, C3]]
        try:
            prob_buy = model.predict_proba(X)[0, 1]
        except Exception:
            prob_buy = 0.5

        return float(P * prob_buy)

    def _calculate_expected_profit_vectorized(self, P_array, C1, C2, C3):
        """
        向量化版本：對一整個 PRICE_GRID 一次性預測。
        邏輯上等價於對每個 P 呼叫 _calculate_expected_profit。
        """
        key = (int(C1 > self.t1), int(C2 > self.t2), int(C3 > self.t3))

        if not self.models or key not in self.models:
            # 與單點版本一致：fallback 用 0.5
            return P_array * 0.5

        model = self.models[key]
        # XGBoost input: [[P, C1, C2, C3], ...]
        X = np.column_stack([
            P_array.astype(float),
            np.full_like(P_array, C1, dtype=float),
            np.full_like(P_array, C2, dtype=float),
            np.full_like(P_array, C3, dtype=float),
        ])
        try:
            probs = model.predict_proba(X)[:, 1]
        except Exception:
            probs = np.full_like(P_array, 0.5, dtype=float)

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

        # Market Saturation Logic
        if market_saturation > 1.0:  # 供過於求
            if inventory_ratio > 1.0:
                alpha = 0.85  # Dump
            elif inventory_ratio < 1.0:
                alpha = 0.95
            else:
                alpha = 0.90
        else:  # 供不應求
            if inventory_ratio > 1.0:
                alpha = 0.98
            elif inventory_ratio < 1.0:
                alpha = 1.10  # Markup
            else:
                alpha = 1.0

        return alpha

    def action(self, obs):
        new_buyer_covariates, last_sale, state, inventories, time_until_replenish = obs

        # Update State
        self.remaining_inventory = inventories[self.this_agent_number]
        self.opponent_inventory = inventories[self.opponent_number]

        if self.remaining_inventory <= 0:
            return 1000.0

        T = time_until_replenish
        I_t = self.remaining_inventory
        I_opp = self.opponent_inventory
        C1, C2, C3 = new_buyer_covariates

        # === 向量化 Greedy 搜尋最佳價格 (邏輯不變) ===
        price_grid = self.PRICE_GRID
        max_profit = -1.0
        optimal_price = 1000.0

        if self.models:
            profits = self._calculate_expected_profit_vectorized(price_grid, C1, C2, C3)
            best_idx = int(np.argmax(profits))
            max_profit = profits[best_idx]
            optimal_price = float(price_grid[best_idx])
        else:
            # 模型載入失敗時的 fallback (保持原邏輯)
            optimal_price = 50.0

        # Apply Competitive Logic
        multiplier = self._calculate_competitive_multiplier(T, I_t, I_opp)
        P_offer = optimal_price * multiplier

        return max(0.01, P_offer)


# --- 4. Main Meta-Agent (The Controller) ---
class Agent(object):
    """
    Meta-agent:
    - 整合 DavidSubAgent 和 NewSubAgent
    - 前期觀察對手，決定最終策略模式
    """

    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number
        self.opponent_number = 1 - agent_number
        self.project_part = params.get("project_part", 2)

        # 初始化兩個子 Agent
        self.na_agent = NewSubAgent(agent_number, params)   # Saturation Strategy
        self.dp_agent = DavidSubAgent(agent_number, params) # DP Strategy

        # 偵測相關狀態
        self.step = 0
        self.DETECT_STEPS = 80
        self.opp_prices = []
        self.mode = "detect"  # "detect" / "use_na" / "use_dp"

    def _update_detection_stats(self, last_sale):
        if last_sale is None or last_sale[0] is None:
            return

        # last_sale[1] is prices array
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

        # 若資料不足，保守選擇 new_agent (反應型)
        if len(self.opp_prices) < 10:
            self.mode = "use_na"
            return

        prices = np.array(self.opp_prices)
        diffs = np.abs(np.diff(prices))

        frac_small_move = np.mean(diffs < 1.0)
        price_std = np.std(prices)

        # 判斷對手是否為 "Static/Passive"
        if frac_small_move > 0.7 and price_std < 15.0:
            self.mode = "use_dp"  # 對手很呆，用 DP 宰割
        else:
            self.mode = "use_na"  # 對手是動態的，用庫存策略抗衡

    def action(self, obs):
        # 1. 讓兩個子 agent 更新內部狀態並各自給出價格
        price_na = self.na_agent.action(obs)
        price_dp = self.dp_agent.action(obs)

        new_buyer_covariates, last_sale, state, inventories, time_until_replenish = obs

        # 2. 偵測期邏輯
        if self.mode == "detect":
            self._update_detection_stats(last_sale)
            self.step += 1
            self._decide_mode_if_ready()

        # 3. 輸出決策
        if self.mode == "detect":
            chosen_price = price_na
        elif self.mode == "use_na":
            chosen_price = price_na
        else:
            chosen_price = price_dp

        return float(chosen_price)
