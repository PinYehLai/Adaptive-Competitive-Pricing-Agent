import random
import pickle
import os
import numpy as np

"""
Improved DP-based dynamic pricing agent with:

1. Dynamic-programming shadow values for inventory (DP).
2. Soft competition model using last opponent price (logistic).
3. High-valuation boost so we capture more buyer surplus.

Compatible with the Part 2 environment and 8_xgb.pkl segment models.
"""

picklefile = open('agents/dealmakers/8_xgb.pkl', 'rb')
new_models = pickle.load(picklefile)


class Agent(object):
    def __init__(self, agent_number, params={}):
        # Basic identifiers
        self.this_agent_number = agent_number
        self.opponent_number = 1 - self.this_agent_number
        self.project_part = params.get('project_part', 2)

        # Inventory / replenishment parameters
        inv_param = params['inventory_limit']
        # inventory_limit may be an int or a dict with min/max
        if isinstance(inv_param, dict):
            self.inv_limit = int(inv_param.get('max', max(inv_param.values())))
        else:
            self.inv_limit = int(inv_param)

        self.inventory_replenish = int(params['inventory_replenish'])  # e.g. 20
        self.remaining_inventory = self.inv_limit

        # Price grid
        self.PRICE_GRID = np.linspace(0.01, 500.0, 100)

        # Opponent tracking
        self.last_opponent_price = None
        self.last_outcome = None  # +1: we sold, -1: opp sold, 0: no sale

        # ---------------- DP parameters (tunable) ----------------
        # base sale prob in simplified DP model
        self.dp_base_p = 0.4
        # scale DP shadow value into price space (key knob to reduce leftover utility)
        self.dp_lambda_scale = 100.0

        # ---------------- Competition parameters ----------------
        # softness of logistic competition response
        self.competition_k = 1.0

        # Precompute DP shadow table once
        self._precompute_dp_shadow_table()


        self.is_fixed_opponent = False
        self.fixed_price_estimate = None
        self.fixed_counter = 0

    # ============================================================
    # Dynamic Programming Precomputation
    # ============================================================
    def _precompute_dp_shadow_table(self):
        """
        Precompute a DP value function V[i, k] and shadow values lambda_dp[i, k]:

        i = 0..inv_limit          (inventory)
        k = 0..inventory_replenish (customers left in cycle)

        Simplified single-seller DP:
          - Each step: can "offer" or "hold".
          - If offer: sell w.p. p, reward=1, then V[i-1,k-1]; else V[i,k-1].
          - If hold: V[i,k-1].
        """
        I_max = self.inv_limit
        T_max = self.inventory_replenish
        p = self.dp_base_p

        V = np.zeros((I_max + 1, T_max + 1), dtype=float)

        # DP recursion
        for k in range(1, T_max + 1):          # customers left
            for i in range(1, I_max + 1):      # inventory
                offer_value = p * (1.0 + V[i - 1, k - 1]) + (1.0 - p) * V[i, k - 1]
                hold_value = V[i, k - 1]
                V[i, k] = max(offer_value, hold_value)

        lambdas = np.zeros_like(V)
        for i in range(1, I_max + 1):
            lambdas[i, :] = V[i, :] - V[i - 1, :]

        self.V_dp = V
        self.lambda_dp = lambdas

    def _get_shadow_price(self, inventory, time_until_replenish):
        """
        Shadow price = scaled marginal value of one more unit of inventory at (i, k).
        """
        i = int(max(0, min(inventory, self.inv_limit)))
        k = int(max(0, min(time_until_replenish, self.inventory_replenish)))
        base_lambda = self.lambda_dp[i, k]
        return self.dp_lambda_scale * base_lambda

    # ============================================================
    # Demand / Profit with XGBoost
    # ============================================================
    def _calculate_expected_profit_vectorized(self, C1, C2, C3):
        """
        Compute solo purchase probabilities across PRICE_GRID using the correct
        XGBoost segment model. Return (expected_profit, solo_probs).
        """
        # Segment thresholds (same as your Part 1)
        t1, t2, t3 = 2.7193025761078644, 2.7215555543935457, 7.262601783583493

        key = (int(C1 > t1), int(C2 > t2), int(C3 > t3))
        model = new_models[key]

        prices = self.PRICE_GRID
        X_batch = np.column_stack([
            prices,
            np.full_like(prices, C1),
            np.full_like(prices, C2),
            np.full_like(prices, C3),
        ])

        probs = model.predict_proba(X_batch)[:, 1]  # P(buy | price, covariates)
        expected_profit = probs * prices
        return expected_profit, probs

    # ============================================================
    # Opponent Tracking
    # ============================================================
    def _process_last_sale(self, last_sale, state, inventories, time_until_replenish):
        """
        Update internal state based on last sale info.
        """
        winner = last_sale[0]
        last_prices = last_sale[1]  # np.array of length n_agents

        # Update inventory from environment state
        self.remaining_inventory = inventories[self.this_agent_number]

        # Update opponent price if available and not NaN
        if last_prices is not None and len(last_prices) > self.opponent_number:
            opp_price = last_prices[self.opponent_number]
            if opp_price is not None and not (isinstance(opp_price, float) and np.isnan(opp_price)):
                self.last_opponent_price = float(opp_price)

        # Outcome tracking
        if winner == self.this_agent_number:
            self.last_outcome = +1
        elif winner == self.opponent_number:
            self.last_outcome = -1
        else:
            self.last_outcome = 0

    # ============================================================
    # Soft Competition Model
    # ============================================================
    def _compute_effective_probs_with_competition(self, solo_probs):
        """
        Soft competition adjustment using last opponent price.

        Let diff = opp_price - my_price.
        Win probability multiplier ≈ sigmoid(k * diff):

          - If we undercut strongly: diff > 0 → multiplier ~ 1
          - If we overprice: diff < 0 → multiplier smoothly → 0

        Effective prob = solo_prob * multiplier.
        """
        if self.last_opponent_price is None:
            return solo_probs

        prices = self.PRICE_GRID
        opp = self.last_opponent_price
        diff = opp - prices

        k = self.competition_k
        comp_factor = 1.0 / (1.0 + np.exp(-k * diff))

        # numerical safety
        comp_factor = np.clip(comp_factor, 0.0, 1.0)

        return solo_probs * comp_factor

    # ============================================================
    # High-Valuation Boost
    # ============================================================
    def _apply_high_valuation_boost(self, base_idx, solo_probs):
        """
        Heuristic: if inferred buyer valuation is much higher than the chosen base
        price, gently boost our chosen price towards that valuation.

        - Compute valuation_est ≈ E[WTP] from the demand curve.
        - If valuation_est > 1.3 * base_price, boost to min(1.15 * base_price, valuation_est).
        - Snap boosted_price back to nearest grid point.
        """
        base_price = self.PRICE_GRID[base_idx]

        total_prob = solo_probs.sum()
        if total_prob <= 1e-9:
            # demand is almost zero everywhere, no boost
            return base_idx

        # approximate valuation from demand curve
        valuation_est = float((solo_probs * self.PRICE_GRID).sum() / total_prob)

        # only boost if clearly underpricing
        if valuation_est > 1.15 * base_price:
            target_price = min(valuation_est, base_price * 1.35)
            # snap to nearest grid price
            new_idx = int(np.argmin(np.abs(self.PRICE_GRID - target_price)))
            return new_idx

        return base_idx

    # ============================================================
    # Main Action
    # ============================================================
    def action(self, obs):
        """
        obs = (
            new_buyer_covariates: np.array of length 3,
            last_sale: (winner_index, np.array of prices),
            state: profit per agent,
            inventories: inventory per agent,
            time_until_replenish: int,
        )
        """
        new_buyer_covariates, last_sale, state, inventories, time_until_replenish = obs

        # Update internal state
        self._process_last_sale(last_sale, state, inventories, time_until_replenish)

        # If out of inventory, effectively don't sell
        if self.remaining_inventory <= 0:
            return 1000.0

        C1, C2, C3 = new_buyer_covariates

        # 1) Solo demand across price grid
        _, solo_probs = self._calculate_expected_profit_vectorized(C1, C2, C3)

        # 2) Competition-adjusted effective probabilities
        eff_probs = self._compute_effective_probs_with_competition(solo_probs)

        # 3) DP shadow price for current (inventory, time)
        shadow_price = self._get_shadow_price(self.remaining_inventory, time_until_replenish)

        # 4) DP-adjusted profit objective: eff_probs * (price - shadow_price)
        margins = self.PRICE_GRID - shadow_price
        adj_profit = eff_probs * margins

        # If all adjusted profits are non-positive, choose a very high price (skip selling)
        best_idx = int(np.argmax(adj_profit))
        if adj_profit[best_idx] <= 0:
            return 1000.0

        # 5) High-valuation boost (only if demand curve suggests much higher WTP)
        boosted_idx = self._apply_high_valuation_boost(best_idx, solo_probs)

        P_offer = float(self.PRICE_GRID[boosted_idx])

        # ------------------------------------------------------------
        # Special rule: Exploit fixed-price opponent (smart version)
        # ------------------------------------------------------------
        if self.is_fixed_opponent and self.fixed_price_estimate is not None:
            fixed_p = self.fixed_price_estimate

            # Only consider undercut if our price is > fixed price
            if P_offer > fixed_p:

                # Inventory & time ratios for smarter decision
                inv_ratio = self.remaining_inventory / self.inv_limit['max']  # 0 → empty, 1 → full
                time_ratio = time_until_replenish / self.inventory_replenish  # 1 → cycle start, 0 → end

                # Decision: Only undercut when we actually need volume
                should_undercut = (
                    inv_ratio > 0.55   # lots of inventory → need to push volume
                    or time_ratio < 0.25  # late in cycle → unload inventory
                )

                if should_undercut:
                    # Undercut by tiny amount
                    P_offer = max(0.01, fixed_p - 0.001)
                # else: keep P_offer (high DP price is more profitable)

        # Safety clamp
        return max(0.01, P_offer)
