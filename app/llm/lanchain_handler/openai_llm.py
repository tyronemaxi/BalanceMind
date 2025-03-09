#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: openai_llm.py
Time: 2025/3/9
"""
from typing import Any

from app.llm.lanchain_handler.base import BaseLLMChat, BaseThreadGenerator, BaseStreamHandler
from app.core.log import logger


class OpenAIChat(BaseLLMChat):
    def __init__(self, api_base: str, api_key: str, callback_handler: BaseStreamHandler):
        super().__init__(api_base, api_key, callback_handler)

    def chat(self, messages: list, model: str, max_tokens: int = 4096, temperature: float = 0.5,
             streaming: bool = False, verbose: bool = False, **kwargs: Any):

        try:
            from langchain_openai import ChatOpenAI

            llm = ChatOpenAI(
                model_name=model,
                openai_api_key=self.api_key,
                openai_api_base=self.api_base,
                verbose=verbose,
                streaming=streaming,
                callbacks=[self.callback_handler],
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs)

            logger.debug(f"llm messages: {messages}")
            if streaming:
                llm.invoke(messages)
            else:
                resp = llm.invoke(messages)
                return resp

        except Exception as e:
            logger.error(f"[openai] call openai error: {e}")
            raise e


if __name__ == '__main__':
    from conf.settings import OPENAI_API_BASE, OPENAI_API_KEY
    gen = BaseThreadGenerator()
    callback = BaseStreamHandler(gen)
    openai_chat = OpenAIChat(api_base=OPENAI_API_BASE, api_key=OPENAI_API_KEY, callback_handler=callback)
    messages = [{"role": "user", "content": "你好"}]
    result = openai_chat.chat(messages, model="gpt-4o")
    print(result.content)
