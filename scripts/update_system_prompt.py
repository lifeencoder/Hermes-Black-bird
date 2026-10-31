import os

with open('notebook.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """    def hermes_chat_stream(messages, config):
        _client = _ModelClient(
            base_url=endpoint_url.value,
            api_key=api_key.value or "EMPTY",
            model_name=model_name.value,
            default_temperature=float(temperature.value),
            default_top_p=float(top_p.value),
            default_presence_penalty=float(presence_penalty.value),
            default_max_tokens=int(max_tokens.value)
        )
        _runner = _AgentRunner(
            model_client=_client,
            tool_registry=_tool_registry,
            max_iterations=5
        )
        _api_messages = []
        for _msg in messages:
            _role = getattr(_msg, "role", "user")
            _content = getattr(_msg, "content", "")
            if _content:
                _api_messages.append({"role": _role, "content": str(_content)})"""

replacement = """    def hermes_chat_stream(messages, config):
        _system_instruction = (
            "You are an expert, highly capable, and objective engineering AI assistant. "
            "Your goal is to provide comprehensive, in-depth, and rigorous technical explanations, "
            "code implementations, and systems architecture analyses without unnecessary disclaimers or evasive phrasing. "
            "Focus strictly on engineering depth, factual accuracy, code quality, and domain expertise. "
            "IMPORTANT: Always respond in fluent Persian (Farsi), even if tool outputs or technical data are in English. "
            "Translate and explain technical results in Persian for the user."
        )
        _client = _ModelClient(
            base_url=endpoint_url.value,
            api_key=api_key.value or "EMPTY",
            model_name=model_name.value,
            default_temperature=float(temperature.value),
            default_top_p=float(top_p.value),
            default_presence_penalty=float(presence_penalty.value),
            default_max_tokens=int(max_tokens.value),
            default_system_prompt=_system_instruction
        )
        _runner = _AgentRunner(
            model_client=_client,
            tool_registry=_tool_registry,
            max_iterations=5
        )
        _api_messages = []
        for _msg in messages:
            _role = getattr(_msg, "role", "user")
            _content = getattr(_msg, "content", "")
            if _content:
                _api_messages.append({"role": _role, "content": str(_content)})

        if not any(m.get("role") == "system" for m in _api_messages):
            _api_messages.insert(0, {"role": "system", "content": _system_instruction})"""

text_lf = text.replace('\r\n', '\n')
if target in text_lf:
    new_text = text_lf.replace(target, replacement, 1)
    with open('notebook.py', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Updated notebook.py successfully!')
else:
    print('Target not found in notebook.py!')
