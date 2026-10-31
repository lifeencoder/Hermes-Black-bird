#!/usr/bin/env python3
"""
Hermes Black Bird - Core Model Client
Independent, portable client for interacting with vLLM OpenAI-compatible endpoints.
Supports default technical system_prompt, dynamic tool calling, customized inference parameters, and streaming.
Pure Python - strictly decoupled from any UI frameworks (Marimo, Gradio, Streamlit).
"""

import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Union
import yaml
from openai import OpenAI

DEFAULT_SYSTEM_PROMPT = """You are an expert, highly capable, and objective engineering AI assistant. Your goal is to provide comprehensive, in-depth, and rigorous technical explanations, code implementations, and systems architecture analyses without unnecessary disclaimers or evasive phrasing. Focus strictly on engineering depth, factual accuracy, code quality, and domain expertise. IMPORTANT: Always respond in fluent Persian (Farsi), even if tool outputs or technical data are in English. Translate and explain technical results in Persian for the user."""


class ModelClient:
    """
    Portable client encapsulating inference requests to the Hermes-3 vLLM server.
    """

    def __init__(
        self,
        config_path: Optional[Union[str, Path]] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        default_temperature: Optional[float] = None,
        default_max_tokens: Optional[int] = None,
        default_system_prompt: Optional[str] = None,
        default_top_p: Optional[float] = None,
        default_presence_penalty: Optional[float] = None,
    ):
        """
        Initialize the ModelClient with config file or parameter overrides.
        """
        # Load configuration from YAML
        self.config = self._load_config(config_path)

        # Apply parameters with priority: Explicit argument -> Config file -> Hardcoded default
        self.base_url = (
            base_url
            or self.config.get("base_url")
            or os.getenv("VLLM_BASE_URL", "http://localhost:8000/v1")
        )

        loaded_key = api_key or self.config.get("api_key") or os.getenv("VLLM_API_KEY", "EMPTY")
        # Check for MoLab key file if present and default key is empty
        if loaded_key == "EMPTY" and os.path.exists("/marimo/vllm_api_key.txt"):
            try:
                with open("/marimo/vllm_api_key.txt", "r", encoding="utf-8") as f:
                    file_key = f.read().strip()
                    if file_key:
                        loaded_key = file_key
            except Exception:
                pass
        self.api_key = loaded_key

        self.model_name = (
            model_name
            or self.config.get("model_name")
            or "NousResearch/Hermes-3-Llama-3.1-70B-FP8"
        )
        self.default_temperature = float(
            default_temperature
            if default_temperature is not None
            else self.config.get("default_temperature", 0.8)
        )
        self.default_max_tokens = int(
            default_max_tokens
            if default_max_tokens is not None
            else self.config.get("default_max_tokens", 2048)
        )
        self.default_system_prompt = (
            default_system_prompt
            if default_system_prompt is not None
            else self.config.get("default_system_prompt", DEFAULT_SYSTEM_PROMPT)
        )
        self.default_top_p = float(
            default_top_p
            if default_top_p is not None
            else self.config.get("default_top_p", 0.95)
        )
        self.default_presence_penalty = float(
            default_presence_penalty
            if default_presence_penalty is not None
            else self.config.get("default_presence_penalty", 0.1)
        )

        # Initialize the underlying OpenAI client
        self.client = OpenAI(base_url=self.base_url, api_key=self.api_key)

    def _load_config(self, config_path: Optional[Union[str, Path]]) -> Dict[str, Any]:
        """
        Locate and parse config/model.yaml safely.
        """
        candidate_paths: List[Path] = []
        if config_path:
            candidate_paths.append(Path(config_path))

        # Check relative to this file: ../config/model.yaml
        current_file_dir = Path(__file__).resolve().parent
        candidate_paths.append(current_file_dir.parent / "config" / "model.yaml")

        # Check relative to working directory
        candidate_paths.append(Path.cwd() / "config" / "model.yaml")

        # Check standard MoLab package location
        candidate_paths.append(Path("/marimo/model_package/config/model.yaml"))

        for path in candidate_paths:
            if path.is_file():
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if isinstance(data, dict):
                            return data
                except Exception as err:
                    print(f"[ModelClient] Warning: Failed to read config at {path}: {err}")

        # Fallback default empty dictionary
        return {}

    def chat(
        self,
        messages: List[Dict[str, Any]],
        tools: Optional[List[Dict[str, Any]]] = None,
        stream: bool = True,
        system_prompt: Optional[str] = None,
        **kwargs,
    ) -> Any:
        """
        Send a chat completion request to Hermes-3.

        Args:
            messages: List of message objects ({'role': 'user', 'content': ...})
            tools: Optional tool/function specifications for tool calling
            stream: Whether to stream tokens incrementally
            system_prompt: Optional system prompt to prepend as the initial instruction
            **kwargs: Extra parameters passed to client.chat.completions.create

        Returns:
            Stream generator (if stream=True) or ChatCompletion object (if stream=False)
        """
        temperature = kwargs.pop("temperature", self.default_temperature)
        max_tokens = kwargs.pop("max_tokens", self.default_max_tokens)
        top_p = kwargs.pop("top_p", self.default_top_p)
        presence_penalty = kwargs.pop("presence_penalty", self.default_presence_penalty)
        model = kwargs.pop("model", self.model_name)

        # Apply system_prompt: explicit argument takes precedence over default
        effective_system = system_prompt if system_prompt is not None else self.default_system_prompt

        formatted_messages = list(messages)
        if effective_system:
            if formatted_messages and formatted_messages[0].get("role") == "system":
                formatted_messages[0] = {"role": "system", "content": effective_system}
            else:
                formatted_messages.insert(0, {"role": "system", "content": effective_system})

        payload: Dict[str, Any] = {
            "model": model,
            "messages": formatted_messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": top_p,
            "presence_penalty": presence_penalty,
            "stream": stream,
            **kwargs,
        }

        if tools:
            payload["tools"] = tools
            if "tool_choice" not in payload:
                payload["tool_choice"] = "auto"

        return self.client.chat.completions.create(**payload)

    def check_connection(self) -> bool:
        """
        Check if the vLLM server is reachable and active.
        """
        try:
            models = self.client.models.list()
            return len(models.data) > 0
        except Exception:
            return False

    def list_models(self) -> List[str]:
        """
        List available model IDs from the server.
        """
        try:
            models = self.client.models.list()
            return [m.id for m in models.data]
        except Exception as err:
            print(f"[ModelClient] Error listing models: {err}")
            return []


if __name__ == "__main__":
    client = ModelClient()
    print("Base URL:", client.base_url)
    print("Model Name:", client.model_name)
    print("Temperature:", client.default_temperature)
    print("Top P:", client.default_top_p)
    print("Presence Penalty:", client.default_presence_penalty)
    print("System Prompt Preview:", client.default_system_prompt[:60] if client.default_system_prompt else "None")
    print("Connected:", client.check_connection())
