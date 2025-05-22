from src.burnout_detector.single_burnout_agent import SingleBurnoutAgent, SingleBurnoutAgentConfig
from src.burnout_detector.llm_utils import LLMConfig


def test_single_detector_agent():
    config = SingleBurnoutAgentConfig(
        llm_config=LLMConfig(
            model_id="gpt-4o-mini",
        )
    )
    agent = SingleBurnoutAgent(config)
    result = agent.detect_burnout("Sylvain")
    print(result)


if __name__ == "__main__":
    test_single_detector_agent()

