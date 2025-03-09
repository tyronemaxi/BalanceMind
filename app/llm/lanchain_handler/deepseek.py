#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: deepseek.py
Time: 2025/3/9
"""
from typing import Any

from app.llm.lanchain_handler.base import BaseLLMChat, BaseThreadGenerator, BaseStreamHandler
from app.core.log import logger
from conf.settings import OPENAI_API_BASE, OPENAI_API_KEY


class DeepSeekChat(BaseLLMChat):
    def __init__(self, api_base: str, api_key: str, callback_handler: BaseStreamHandler):
        super().__init__(api_base, api_key, callback_handler)

    def chat(self, messages: list, model: str = "deepseek-r1", max_tokens: int = 12800, temperature: float = 0.6,
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
