# Adaptive Competitive Pricing Agent

An adaptive multi-agent pricing system that combines **machine learning-based demand estimation, inventory-aware pricing, dynamic programming, and opponent-aware strategy selection** in a competitive marketplace.

Developed as a three-person Cornell Tech team project, the system first learns personalized customer demand and then extends the pricing policy to a two-agent competitive environment where prices, inventory, and opponent behavior evolve over time.

The final competitive agent uses an **80-step observation phase** to characterize the opponent's pricing behavior and then selects between two specialized pricing strategies for the remainder of the game.

---

## Overview

The project consists of two stages:

### Part 1 — Demand Estimation and Price Optimization

The first stage considers pricing without competition.

Given customer covariates, the objective is to estimate purchase probability and choose a price that maximizes expected revenue while accounting for limited inventory and periodic replenishment.

We evaluated several approaches, including:

* Global vs. segmented demand models
* Logistic regression and tree-based models
* Static revenue-maximizing prices
* Inventory-aware price adjustments

The strongest approach divided customers into **8 segments** using the three customer covariates and trained a separate **XGBoost demand model** for each segment.

For each customer, the pricing agent evaluates a grid of 100 candidate prices and estimates

$$
\text{Expected Revenue}(p)
==========================

p \times P(\text{purchase}\mid p, x)
$$

where (x) represents customer covariates.

The segmented XGBoost approach substantially outperformed the best global model:

| Approach                       |    Revenue |
| ------------------------------ | ---------: |
| Global LightGBM                |     ~2.49M |
| 8-Segment XGBoost — Expected   |     ~3.10M |
| **8-Segment XGBoost — Actual** | **~3.23M** |

The selected price is then adjusted using inventory pressure so that the agent can balance immediate revenue against future inventory availability.

---

## Part 2 — Pricing Under Competition

The second stage introduces another pricing agent competing for the same sequence of customers.

This changes the problem fundamentally.

A pricing strategy that performs well independently may perform poorly when interacting repeatedly with another adaptive strategy. In particular, our simulations showed that **strategy interaction mattered as much as the quality of the individual pricing policy**.

We therefore moved from selecting one universally "best" agent to building an **adaptive meta-agent**.

---

## Strategy Interaction Analysis

We performed repeated head-to-head simulations between two major strategy families:

* **DP Agent** — an inventory-aware Dynamic Programming strategy
* **Multiplier Agent** — an XGBoost demand model with adaptive inventory and market-based price multipliers

The simulations revealed a highly asymmetric payoff structure:

| Matchup                   | Approximate Revenue              |
| ------------------------- | -------------------------------- |
| Multiplier vs. Multiplier | ~10K–12K each                    |
| Multiplier vs. DP         | DP: ~10K–11K, Multiplier: ~7K–8K |
| **DP vs. DP**             | **~3K–4K each**                  |

The most important result was not simply which agent won a single matchup.

The **DP-vs-DP interaction created a destructive price war**, reducing revenue for both agents far more severely than the loss suffered by a Multiplier strategy against DP.

This led to a broader strategic insight:

> In repeated competitive environments, maximizing performance requires considering the distribution of opponent strategies and avoiding low-payoff interactions—not simply choosing the agent with the highest isolated win rate.

Because DP-based approaches had performed strongly in the earlier phase of the competition, we expected similar strategies to be common in the final environment. This motivated the design of an adaptive controller instead of committing to a single strategy.

---

## Adaptive Strategy Selector

The final system is a **meta-agent** composed of two independent pricing sub-agents and an opponent-classification layer.

```text
                         Incoming Customers
                                │
                                ▼
                  ┌───────────────────────────┐
                  │    Observation Phase      │
                  │      First 80 Steps       │
                  └─────────────┬─────────────┘
                                │
                    Opponent Price History
                                │
                                ▼
                  ┌───────────────────────────┐
                  │ Behavior Classification   │
                  │                           │
                  │ • Price volatility        │
                  │ • Frequency of changes    │
                  └─────────────┬─────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
             DP Sub-Agent            XGBoost / Multiplier
                                         Sub-Agent
                    │                       │
                    └───────────┬───────────┘
                                ▼
                          Final Price
```

During the first **80 interactions**, the controller records opponent prices and computes two behavioral statistics:

### Price Volatility

```python
price_std = np.std(opponent_prices)
```

This measures how widely the opponent changes its quoted prices.

### Small-Move Ratio

```python
frac_small_move = np.mean(
    np.abs(np.diff(opponent_prices)) < 1.0
)
```

This measures how frequently the opponent keeps its price nearly unchanged between consecutive rounds.

The final implementation uses these statistics to distinguish relatively stable pricing behavior from more dynamic, reactive behavior. Once the observation period is complete, the selected sub-agent remains active for the rest of the game.

The controller and both pricing strategies are implemented in:

[`agents/dealmakers.py`](agents/dealmakers.py)

---

## XGBoost Multiplier Sub-Agent

I designed and implemented the project's **NewSubAgent**, an XGBoost-based competitive pricing strategy.

The agent uses the segmented XGBoost demand models developed from the first stage but extends them for a competitive environment.

### 1. Customer-Specific Demand Prediction

The customer's three covariates determine one of eight demand segments.

For a grid of 100 possible prices, the corresponding XGBoost model estimates:

[
P(\text{purchase}\mid p, C_1,C_2,C_3)
]

The agent then computes expected revenue for every candidate price:

[
R(p)=p\times P(\text{purchase})
]

and selects the revenue-maximizing baseline price.

The computation is vectorized so that the entire candidate price grid can be evaluated efficiently.

### 2. Competitive Inventory Adjustment

The baseline price is then modified according to two market-state variables.

**Market Saturation**

[
\text{Market Saturation}
========================

\frac{I_{\text{self}}+I_{\text{opponent}}}
{T}
]

where (T) is the remaining time before inventory replenishment.

**Inventory Position**

[
\text{Inventory Ratio}
======================

\frac{I_{\text{self}}}
{I_{\text{opponent}}+\epsilon}
]

When supply is high relative to remaining selling opportunities, the agent lowers prices to capture more orders.

When supply is scarce, the agent can increase prices to preserve inventory and extract greater revenue from remaining demand.

This produces a pricing policy that responds simultaneously to:

* Customer purchase probability
* Candidate price
* Remaining inventory
* Opponent inventory
* Time until replenishment
* Overall market saturation

---

## DP Sub-Agent

The second strategy uses a precomputed **Dynamic Programming policy** as an inventory-aware pricing baseline.

Its pricing logic combines:

* Customer segmentation
* Inventory level
* Time until replenishment
* DP policy lookup
* Demand-model expected revenue
* Segment-level sales feedback
* Opponent price response
* Price-war detection

Rather than relying exclusively on a fixed DP value, the agent compares its DP-based price with a greedy demand-based alternative and incorporates recent competitive information before selecting the final quote.

---

## Why a Meta-Agent?

An important lesson from the project was that there was no universally dominant pricing strategy.

Suppose Strategy A beats Strategy B in a direct matchup. That does **not** imply Strategy A will produce the highest total revenue in a tournament containing many different competitors.

Our payoff experiments demonstrated this clearly.

The DP strategy could outperform the Multiplier strategy head-to-head, yet repeated DP-vs-DP interactions could destroy substantially more revenue through aggressive competition.

The final architecture therefore optimizes at two levels:

```text
Customer Level
    ↓
What price maximizes expected revenue?

Game Level
    ↓
Which pricing strategy is best suited to this opponent?
```

This separation between **pricing optimization** and **strategy selection** became the central design idea of the final system.

---

## My Contributions — Pin-Yeh Lai

This was a three-person Cornell Tech team project. The analysis of competitive results and the conclusions drawn from the payoff experiments were developed collaboratively by the team.

My primary contributions focused on **competitive strategy design and implementation**.

### XGBoost Competitive Pricing Agent

I designed and implemented the `NewSubAgent` competitive pricing mechanism:

* Reused segmented XGBoost demand prediction to estimate customer purchase probabilities across candidate prices.
* Designed the expected-revenue price search used to select a customer-specific baseline quote.
* Developed the market-saturation and inventory-position multiplier used to adapt prices to the competitive environment.
* Integrated opponent inventory, remaining time, and market supply into real-time pricing decisions.
* Implemented vectorized price evaluation to reduce inference overhead.

### Adaptive Meta-Agent

Based on the team's cross-agent simulation results, I designed and implemented the final opponent-aware strategy selection mechanism:

* Proposed using an observation period before committing to a pricing strategy.
* Designed the **80-step detection phase**.
* Selected opponent price volatility and adjacent-price movement frequency as behavioral signals.
* Implemented the classification and strategy-switching controller.
* Integrated the DP and XGBoost-based pricing agents into a single meta-agent.
* Designed the system around the strategic objective of avoiding unfavorable repeated interactions rather than optimizing only for individual head-to-head wins.

The resulting implementation allows the agent to **observe, classify, and adapt** rather than committing to one pricing policy before seeing its opponent.

---

## Core Implementation

The final submitted competitive agent is:

```text
agents/dealmakers.py
```

Supporting models and experiments are located under:

```text
agents/dealmakers/
├── 8_xgb.pkl
├── 8_models_dict.pkl
├── dp_policy.pkl
├── 8_xgb.ipynb
├── create_model.ipynb
├── new_agent.py
├── andrew_v2.py
└── ...
```

The repository also contains the local head-to-head simulation environment used to evaluate different agent combinations.

---

## Project Structure

```text
.
├── agents/
│   ├── dealmakers.py            # Final adaptive competitive agent
│   │
│   └── dealmakers/
│       ├── 8_xgb.pkl            # Segmented XGBoost models
│       ├── 8_models_dict.pkl    # Demand models used by DP agent
│       ├── dp_policy.pkl        # Precomputed DP policy
│       ├── 8_xgb.ipynb          # XGBoost experiments
│       ├── create_model.ipynb   # Model / policy construction
│       ├── new_agent.py         # Multiplier-agent development
│       └── andrew_v2.py         # Meta-agent development
│
├── data/
├── algopricing_opy/
├── run_gym_headtohead_localcomputer_2025.ipynb
├── make_env_2025.py
├── settings.py
└── requirements.txt
```

---

## Running Locally

Install the required dependencies:

```bash
pip install -r requirements.txt
```

The repository includes a local head-to-head simulation notebook:

```text
run_gym_headtohead_localcomputer_2025.ipynb
```

which can be used to load agents and simulate competitive pricing interactions.

---

## Key Takeaways

This project highlighted three broader lessons:

**1. Segmentation can matter more than model complexity.**
Customer-specific demand structure produced a larger improvement than simply switching algorithms.

**2. The best standalone policy may not be the best competitive policy.**
Agent performance depends on interactions with other adaptive agents.

**3. Strategy selection can be an optimization problem itself.**
When opponent behavior is heterogeneous, identifying the competitive environment and selecting an appropriate policy can outperform relying on a single fixed strategy.

---

## Team

**DealMakers — Cornell Tech**

* Alice Lee
* Pin-Hsuan Lai
* Pin-Yeh Lai

Competitive analysis and strategic conclusions were developed collaboratively by the team. Individual contributions described above reflect my primary design and implementation responsibilities.

For a detailed discussion of the experiments, strategy evolution, and final competitive system, see the project report.
