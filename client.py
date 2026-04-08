# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.

"""Feed Balance Environment Client."""

from typing import Dict

from openenv.core import EnvClient
from openenv.core.client_types import StepResult
from openenv.core.env_server.types import State

from models import FeedBalanceAction, FeedBalanceObservation


class FeedBalanceEnv(
    EnvClient[FeedBalanceAction, FeedBalanceObservation, State]
):
    """
    Client for the Feed Balance Environment.

    This client maintains a persistent WebSocket connection to the environment server,
    enabling efficient multi-step interactions with lower latency.
    Each client instance has its own dedicated environment session on the server.

    Example:
        >>> # Connect to a running server
        >>> with FeedBalanceEnv(base_url="http://localhost:8000") as client:
        ...     result = client.reset()
        ...     print(result.observation.echoed_message)
        ...
        ...     result = client.step(FeedBalanceAction(message="Hello!"))
        ...     print(result.observation.echoed_message)

    Example with Docker:
        >>> # Automatically start container and connect
        >>> client = FeedBalanceEnv.from_docker_image("feed_balance-env:latest")
        >>> try:
        ...     result = client.reset()
        ...     result = client.step(FeedBalanceAction(message="Test"))
        ... finally:
        ...     client.close()
    """

    def _step_payload(self, action: FeedBalanceAction) -> Dict:
        """
        Convert FeedBalanceAction to JSON payload for step message.

        Args:
            action: FeedBalanceAction instance

        Returns:
            Dictionary representation suitable for JSON encoding
        """
        return {
            "message": action.message,
        }

    def _parse_result(self, payload: Dict) -> StepResult[FeedBalanceObservation]:
        """
        Parse server response into StepResult[FeedBalanceObservation].

        Args:
            payload: JSON response data from server

        Returns:
            StepResult with FeedBalanceObservation
        """
        obs_data = payload.get("observation", {})
        observation = FeedBalanceObservation(
            echoed_message=obs_data.get("echoed_message", ""),
            message_length=obs_data.get("message_length", 0),
            done=payload.get("done", False),
            reward=payload.get("reward"),
            metadata=obs_data.get("metadata", {}),
        )

        return StepResult(
            observation=observation,
            reward=payload.get("reward"),
            done=payload.get("done", False),
        )

    def _parse_state(self, payload: Dict) -> State:
        """
        Parse server response into State object.

        Args:
            payload: JSON response from state request

        Returns:
            State object with episode_id and step_count
        """
        return State(
            episode_id=payload.get("episode_id"),
            step_count=payload.get("step_count", 0),
        )
    



if __name__ == "__main__":
    print("🤖 Starting the AI Player...")
    
    # Connect to your running server
    with FeedBalanceEnv(base_url="http://localhost:8000").sync() as client:
        
        # 1. Reset/Start the game
        result = client.reset()
        print("✅ Game Started!")
        
        # 2. Make the AI take an action
        my_action = FeedBalanceAction(message="Hello Hackathon!")
        print(f"➡️  AI is sending action: {my_action.message}")
        result = client.step(my_action)
        
        # 3. Print the results to the screen!
        print("\n📊 --- RESULTS ---")
        print(f"Server Echo: {result.observation.echoed_message}")
        print(f"Reward: {result.reward}")
        print(f"Game Over (Done): {result.done}")
        print("------------------\n")
