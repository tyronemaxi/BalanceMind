#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: base.py
Time: 2025/3/9
"""
import ast
import re
from abc import ABC
from typing import Dict, List


class LLMResponse(ABC):
    def __init__(self, content: str, total_tokens: int) -> None:
        self.content = content
        self.total_tokens = total_tokens

    def __repr__(self):
        return f"{self.__class__}(content={self.content}, total_tokens={self.total_tokens})"

class BaseLLM(ABC):
    def __init__(self):
        pass

    def chat(self, messages: List[Dict]) -> LLMResponse:
        pass

    @staticmethod
    def literal_eval(response_content: str):
        response_content = response_content.strip()

        # remove content between <think> and </think>, especial for DeepSeek reasoning model
        if "<think>" in response_content and "</think>" in response_content:
            end_of_think = response_content.find("</think>") + len("</think>")
            response_content = response_content[end_of_think:]

        try:
            if response_content.startswith("```") and response_content.endswith("```"):
                if response_content.startswith("```python"):
                    response_content = response_content[9:-3]
                elif response_content.startswith("```json"):
                    response_content = response_content[7:-3]
                elif response_content.startswith("```str"):
                    response_content = response_content[6:-3]
                elif response_content.startswith("```\n"):
                    response_content = response_content[4:-3]
                else:
                    raise ValueError("Invalid code block format")
            result = ast.literal_eval(response_content.strip())
        except Exception:
            matches = re.findall(r"(\[.*?\]|\{.*?\})", response_content, re.DOTALL)

            if len(matches) != 1:
                raise ValueError(
                    f"Invalid JSON/List format for response content:\n{response_content}"
                )

            json_part = matches[0]
            return ast.literal_eval(json_part)

        return result