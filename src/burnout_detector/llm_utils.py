from smolagents import LiteLLMModel
from dataclasses import dataclass
import os
import yaml
from typing import Optional


@dataclass
class LLMConfig:
    model_id: str  # the model identifier, e.g. "gpt-3.5-turbo"
    temperature: float = 0.2  # temperature for model inference


class LLMUtils:
    @staticmethod
    def get_llm_model(config: LLMConfig) -> LiteLLMModel:
        """Get the LLM model based on the model type.

        Args:
            config: Configuration data for the language model to load.
        Returns:
            LiteLLMModel: Configured model instance
        """
        model = config.model_id
        match model:
            case model if model.startswith("claude"):
                if os.environ["ANTHROPIC_API_KEY"] is None:
                    raise ValueError(
                        "ANTHROPIC_API_KEY is not set. "
                        "Either set it as an environment variable "
                        "or add it to a .env file in the directory "
                        "you are executing from."
                    )
                return LiteLLMModel(
                    model="anthropic/" + model,
                    api_key=os.environ["ANTHROPIC_API_KEY"],
                    temperature=0.2
                )
            case model if model.startswith("gpt"):
                if os.environ["OPENAI_API_KEY"] is None:
                    raise ValueError(
                        "OPENAI_API_KEY is not set. "
                        "Either set it as an environment variable "
                        "or add it to a .env file in the directory "
                        "you are executing from."
                    )
                return LiteLLMModel(
                    model_id=model,
                    api_base="https://api.openai.com/v1",
                    api_key=os.environ["OPENAI_API_KEY"],
                    temperature=0.2
                )
            case model if model.startswith("gemini"):
                if os.environ["GEMINI_API_KEY"] is None:
                    raise ValueError(
                        "GEMINI_API_KEY is not set. "
                        "Either set it as an environment variable "
                        "or add it to a .env file in the directory "
                        "you are executing from."
                    )
                return LiteLLMModel(
                    model="google/" + model,
                    api_key=os.environ["GEMINI_API_KEY"],
                    temperature=0.2
                )
            case _:
                raise ValueError(f"Unsupported model type: {model}")

    @staticmethod
    def load_prompt_template(prompt_path: Optional[str] = None) -> str:
        """
        Read the prompt template from the given path (YAML file).

        Args: 
            prompt_path: The path to the prompt template file. Optional.
            
        Returns:
            dict: A dictionary containing the prompt templates.
        """
        if prompt_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            prompt_path = os.path.join(current_dir, "prompt_templates.yaml")

        with open(prompt_path, "r") as file:
            prompt_templates = yaml.safe_load(file)

        return prompt_templates
