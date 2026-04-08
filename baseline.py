import os
from client import FeedBalanceEnv
from server.models import FeedBalanceAction

def run_baseline():
    print("🚀 Starting OpenEnv Baseline Evaluation...")
    
    # Connect to your running server
    with FeedBalanceEnv(base_url="http://localhost:8000").sync() as client:
        result = client.reset()
        print(f"\n{result.observation.echoed_message}\n")
        
        done = False
        step_count = 0
        total_rewards = 0.0
        
        # Keep playing until the game is over (or max 20 steps)
        while not done and step_count < 20:
            
            # --- AI LOGIC: 2 Memes to lower boredom, then 1 Ad for profit ---
            if step_count % 3 == 2:
                action_msg = "Show an Ad to the user"
            else:
                action_msg = "Show a funny Meme to the user"
            
            print(f"🤖 Step {step_count + 1} | Agent Action: {action_msg}")
            
            # Send action to environment
            result = client.step(FeedBalanceAction(message=action_msg))
            total_rewards += result.reward
            
            print(f"📊 Env Response: {result.observation.echoed_message}")
            print(f"⭐ Step Reward: {result.reward}\n")
            
            done = result.done
            step_count += 1

        print("🏁 EVALUATION COMPLETE!")
        print(f"Total Accumulated Reward: {total_rewards}")

if __name__ == "__main__":
    run_baseline()