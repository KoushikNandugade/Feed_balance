# 📱 Feed Balance Environment

## Overview & Motivation
Social media platforms face a constant struggle: maximizing ad revenue while preventing users from getting bored and leaving the app. This environment simulates that real-world problem. The agent acts as the recommendation algorithm, choosing whether to show the user engaging content (memes) or profitable content (ads). 

## Action & Observation Spaces
* **Action Space:** A text string where the agent dictates the next piece of content (e.g., "Show an Ad" or "Show a Meme").
* **Observation Space:** The agent receives a JSON payload containing the user's current `boredom_level` (0-10), the `total_profit` accumulated, and the `target_profit` required to win the episode.

## Task Difficulty Levels
The environment features 3 randomized task difficulties with a deterministic grader (0.0 to 1.0):
1. **Easy:** Target Profit = $5.0. Boredom increases at a normal rate.
2. **Medium:** Target Profit = $10.0. Boredom increases at 2x rate from ads.
3. **Hard:** Target Profit = $15.0. Boredom increases at 3x rate from ads.

## Meaningful Reward Function
* **+1.0** for showing an Ad (Profitable).
* **+0.5** for showing a Meme (Keeps user engaged).
* **-2.0 Penalty** for showing more than 2 ads in a row (Destructive behavior).
* **+10.0 / -10.0** terminal rewards for winning (reaching profit) or losing (user quits at 10/10 boredom).

## Setup and Usage Instructions
1. Clone the repository.
2. Start the server: `uv run uvicorn server.app:app --reload`
3. Run the baseline evaluation: `uv run python baseline.py`

## Baseline Performance
A simulated baseline agent using a strict "2 Memes, 1 Ad" pacing strategy successfully navigates the Medium difficulty task without triggering the user abandonment state, achieving a Grader Score of 1.0.