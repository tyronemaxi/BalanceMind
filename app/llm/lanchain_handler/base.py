#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: base.py
Time: 2025/3/9
"""
from typing import List, Any, Dict
from queue import Queue, Empty
from abc import ABC

from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import LLMResult

from app.core.log import logger


class BaseThreadGenerator(object):
    """
    generator for thread which store tokens
    """

    def __init__(self, gen_id: str = None):
        self.queue = Queue()
        self.closed = False
        self.stop = "[DONE]"
        self.gen_id = gen_id

    def __iter__(self):
        return self

    def __next__(self):
        if self.closed and self.queue.empty():
            raise StopIteration

        try:
            item = self.queue.get()

            if item == self.stop:
                self.queue.task_done()
                raise StopIteration

            return item

        except Empty:
            if self.closed:
                raise StopIteration

            return next(self)

    def close(self):
        if not self.closed:
            self.queue.put(self.stop)
            self.closed = True


class BaseStreamHandler(StreamingStdOutCallbackHandler):
    """
    基础调用类
    Custom Stream Handler for llm
    refers: https://python.langchain.com/docs/modules/callbacks/multiple_callbacks
    """

    def __init__(self, gen: Any):
        super().__init__()
        self.gen = gen

    def on_llm_start(
            self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Run when LLM starts running."""
        pass

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        self.gen.send(token)

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        self.gen.close()

    def on_llm_error(self, error: Exception, **kwargs: Any) -> None:
        logger.error(f"[llm error] call llm error: {error}")
        err_msg = "(* / ω＼*)被发现开小差啦......，请重试一下"
        self.gen.send(err_msg)
        self.gen.close()


class BaseLLMChat(ABC):
    def __init__(self, api_base: str, api_key: str, callback_handler: BaseStreamHandler):
        self.api_base = api_base
        self.api_key = api_key
        self.callback_handler = callback_handler

    def chat(self, messages: list, model: str, max_tokens: int = 4096, temperature: float = 0.5,
             streaming: bool = False, verbose: bool = False, **kwargs: Any):
        # try:
        #     llm = ChatOpenAI(
        #         model_name=model,
        #         openai_api_key=self.api_key,
        #         openai_api_base=self.api_base,
        #         verbose=verbose,
        #         streaming=streaming,
        #         callbacks=[self.callback_handler],
        #         temperature=temperature,
        #         max_tokens=max_tokens,
        #         **kwargs)
        #
        #     logger.debug(f"llm messages: {messages}")
        #     if streaming:
        #         llm.invoke(messages)
        #     else:
        #         resp = llm.invoke(messages)
        #         return resp
        #
        # except Exception as e:
        #     logger.error(f"[openai_llm] call openai_llm error: {e}")
        #     raise e
        pass
