from dataclasses import dataclass
from llm_utils import LLMConfig, LLMUtils
from typing import List, Optional
from logging import Logger

from utils import Utils


@dataclass
class MultiBurnoutAgentConfig:
    llm_config: LLMConfig
    tools: Optional[List[str]] = None
    batch_size: int = 8


class MultiBurnoutAgent:
    """
    Agent for detecting burnout.
    """

    def __init__(self, config: Optional[MultiBurnoutAgentConfig] = None):
        self.config = config
        self.logger = Logger("default")

    @staticmethod
    def _process_burnout_candidates(burnout_candidates: List[dict]) -> List[str]:
        """
        Process the burnout candidates and return their data as structured strings.
        """
        processed_candidates = []
        for candidate in burnout_candidates:
            _name = candidate["name"]
            _on_call_schedule = candidate["on_call_schedule"]
            _most_recent_incident = candidate["most_recent_incident"]
            processed = f"Name: {_name}\nOn-call schedule: {_on_call_schedule}\nMost recent incident: {_most_recent_incident}"
            processed_candidates.append(processed)
        return processed_candidates

    def detect_burnout(self, burnout_candidates: List[dict], config_override: Optional[MultiBurnoutAgentConfig] = None):
        """
        Detect whether a set of candidates are burnt out.

        Args:
            burnout_candidates: List of dictionaries containing "name", "on_call_schedule", and information on the
                most recent incidents handled by the burnout candidate.
            config_override: Optionally override the configuration used during initialization.
        """
        llm_config = self.config.llm_config if config_override is None else config_override
        assert llm_config is not None, "Must provide an LLM config, but got None."

        model = LLMUtils.get_llm_model(llm_config)

        processed_candidates = self._process_burnout_candidates(burnout_candidates)
        batched_candidates = Utils.batchify(processed_candidates, self.config.batch_size)

        pass