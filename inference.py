import os
from openai import OpenAI
from client import FeedBalanceEnv
from models import FeedBalanceAction

# --- EXACT CODE FROM THE HACKATHON CHECKLIST ---
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")

# Optional - if you use from_docker_image():
LOCAL_IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")
# -----------------------------------------------

def run_inference():
    print("🚀 Starting OpenEnv LLM Inference...")
    
    # Configure the OpenAI client using the required variables
    # (The hackathon grader will automatically inject the real HF_TOKEN here)
    llm_client = OpenAI(
        base_url=API_BASE_URL,
        api_key=HF_TOKEN or "dummy-key-for-testing" 
    )

    # Connect to your running server
    with FeedBalanceEnv(base_url="http://localhost:8000").sync() as env_client:
        result = env_client.reset()
        done = False
        step_count = 0
        
        while not done and step_count < 20:
            obs_text = result.observation.echoed_message
            
            # --- MAKE THE LLM CALL ---
            response = llm_client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are playing a game. You must balance a social media feed to make profit without boring the user. Respond with ONLY ONE of these two phrases: 'ad' or 'meme'."},
                    {"role": "user", "content": f"Current Status: {obs_text}. What is your next action?"}
                ],
                max_tokens=10
            )
            
            # Extract the AI's choice
            ai_action = response.choices[0].message.content.strip()
            print(f"🤖 LLM chose: {ai_action}")
            
            # Send the AI's choice to your game environment
            result = env_client.step(FeedBalanceAction(message=ai_action))
            print(f"📊 Env Response: {result.observation.echoed_message}")
            print(f"⭐ Step Reward: {result.reward}\n")
            
            done = result.done
            step_count += 1

if __name__ == "__main__":
    run_inference()