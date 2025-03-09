#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: openai_llm.py
Time: 2025/3/9
"""
from typing import Dict, List

from app.llm.openai_llm.base import BaseLLM, ChatResponse


class OpenAI(BaseLLM):
    def __init__(self, model: str, api_base: str, api_key: str, **kwargs):
        super().__init__(model, api_base, api_key, **kwargs)

    def chat(self, messages: List[Dict]) -> ChatResponse:
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        return ChatResponse(
            content=completion.choices[0].message.content,
            total_tokens=completion.usage.total_tokens,
        )


if __name__ == '__main__':
    from conf.settings import OPENAI_API_BASE, OPENAI_API_KEY
    gpt_llm = OpenAI(model='gpt-4o', api_base=OPENAI_API_BASE, api_key=OPENAI_API_KEY)
    messages = [{"role": "user", "content": "你是谁？"}]
    result = gpt_llm.chat(messages)
    print(result.total_tokens)
    print(result.content)
