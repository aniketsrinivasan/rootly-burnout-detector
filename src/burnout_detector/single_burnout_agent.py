from dataclasses import dataclass
from llm_utils import LLMConfig, LLMUtils
from typing import List, Optional
from logging import Logger
from halo import Halo
import os
from smolagents import CodeAgent as Agent, LogLevel

from src.burnout_detector.tools.rootly_tools.users_tool import UsersTool
from src.burnout_detector.tools.rootly_tools.shifts_tool import ShiftsTool
from src.burnout_detector.tools.rootly_tools.incidents_tool import IncidentsTool


@dataclass
class SingleBurnoutAgentConfig:
    llm_config: LLMConfig
    tools: Optional[List[str]] = None
    batch_size: int = 8
    log_level: LogLevel = LogLevel.OFF


class SingleBurnoutAgent:
    """
    Agent for detecting burnout.
    """

    def __init__(self, config: Optional[SingleBurnoutAgentConfig] = None):
        self.config = config
        self.logger = Logger("default")

    def detect_burnout(self, burnout_candidate: str, config_override: Optional[SingleBurnoutAgentConfig] = None):
        """
        Detect whether a candidate is burnt out.

        Args:
            burnout_candidate: The name of the burnout candidate.
            config_override: Optionally override the configuration used during initialization.
        """
        llm_config = self.config.llm_config if config_override is None else config_override
        assert llm_config is not None, "Must provide an LLM config, but got None."

        model = LLMUtils.get_llm_model(llm_config)
        tools = []
        if os.getenv("ROOTLY_API_KEY"):
            tools.append(UsersTool())
            tools.append(ShiftsTool())
            tools.append(IncidentsTool())

        agent = Agent(
            model=model, 
            tools=tools,
            additional_authorized_imports=[
                "datetime",
                "requests"
            ]
        )

        if (single_burnout_detection := LLMUtils.load_prompt_template()["single_burnout_detection"]["template"]):
            prompt = single_burnout_detection.format(
                burnout_candidate=burnout_candidate
            )
        else:
            raise ValueError("No prompt template found for single burnout detection.")
        
        spinner = Halo(text="Detecting burnout...", spinner="dots")
        self.logger.info(prompt)
        spinner.start()

        try:
            result = agent.run(prompt)
            spinner.stop()
            self.logger.info(result)
        except Exception as e:
            spinner.fail("Analysis failed.")
            self.logger.error(f"Error detecting burnout: {e}")

        return result


