import uuid
import random
from uuid import uuid4
from openenv_core import Environment, State
from models import FeedBalanceAction, FeedBalanceObservation

class FeedBalanceEnvironment(Environment):
    SUPPORTS_CONCURRENT_SESSIONS: bool = True

    def __init__(self):
        """Initialize the feed_balance environment."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._reset_count = 0
        
        # Our custom variables
        self.boredom_level = 0
        self.consecutive_ads = 0
        self.total_profit = 0.0
        self.difficulty = "easy"
        self.target_profit = 5.0
        self.boredom_multiplier = 1

    def reset(self) -> FeedBalanceObservation:
        """Reset the environment and assign a task difficulty."""
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self._reset_count += 1
        
        # REQ #3: Assign one of 3 Tasks (Easy, Medium, Hard)
        self.difficulty = random.choice(["easy", "medium", "hard"])
        
        if self.difficulty == "easy":
            self.target_profit = 5.0
            self.boredom_multiplier = 1
        elif self.difficulty == "medium":
            self.target_profit = 10.0
            self.boredom_multiplier = 2
        else: # hard
            self.target_profit = 15.0
            self.boredom_multiplier = 3

        # Reset variables
        self.boredom_level = 0
        self.consecutive_ads = 0
        self.total_profit = 0.0

        return FeedBalanceObservation(
            echoed_message=f"NEW USER LOGIN! Task Difficulty: {self.difficulty.upper()} | Goal: Reach ${self.target_profit} profit.",
            message_length=0,
            done=False,
            reward=0.0,
        )

    def step(self, action: FeedBalanceAction) -> FeedBalanceObservation: # type: ignore[override]
        """Process the AI's action, update state, and calculate rewards."""
        reward = 0.0
        done = False 
        ai_choice = action.message.lower().strip()

        # Action: AI shows an Ad
        if "ad" in ai_choice:
            self.total_profit += 1.50    
            self.boredom_level += (2 * self.boredom_multiplier) # Harder tasks = faster boredom     
            self.consecutive_ads += 1
            
            # REQ #4: Meaningful Reward Function (Penalize spamming)
            if self.consecutive_ads > 2:
                reward = -2.0 # Penalty for destructive behavior
            else:
                reward = 1.0 # Good incremental progress                 
        
        # Action: AI shows a Meme/Content
        else:
            self.boredom_level -= 3       
            self.consecutive_ads = 0      
            reward = 0.5 # Reward for keeping user engaged                  

        # Keep boredom from dropping below zero
        if self.boredom_level < 0:
            self.boredom_level = 0

        grader_score = 0.0

        # Win Condition: Reached target profit
        if self.total_profit >= self.target_profit:
            done = True
            reward += 10.0 # Big completion reward
            grader_score = 1.0 # REQ #3: Programmatic grader score (0.0 to 1.0)
            echo = f"WIN! You reached the ${self.target_profit} goal! Task: {self.difficulty.upper()}"
            
        # Lose Condition: User got too bored and quit
        elif self.boredom_level >= 10:
            done = True
            reward -= 10.0 # Penalty for losing user
            grader_score = min(1.0, self.total_profit / self.target_profit) # Partial credit
            echo = f"LOSE! User got bored and quit. Profit: ${self.total_profit} / ${self.target_profit}"
            
        # Game Continues
        else:
            echo = f"Action: {ai_choice} | Boredom: {self.boredom_level}/10 | Profit: ${self.total_profit} / ${self.target_profit}"

        self._state.step_count += 1

        # Add the grader score to the final output so the judges see it
        if done:
            echo += f" | Final Grader Score: {grader_score:.2f}"

        return FeedBalanceObservation(
            echoed_message=echo,
            message_length=len(ai_choice),
            done=done,
            reward=reward
        )

    @property
    def state(self) -> State:
        return self._state