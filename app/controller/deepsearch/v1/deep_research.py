#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: deep_research.py
Time: 2025/3/9
"""
from app.llm.lanchain_handler.base import BaseThreadGenerator, BaseStreamHandler
from app.llm.lanchain_handler.deepseek import DeepSeekChat
from app.controller.deepsearch.v1.promt import prompt_handler
from conf.settings import OPENAI_API_BASE, OPENAI_API_KEY


class DeepResearchCtrl(object):
    @staticmethod
    def chat(gen: BaseThreadGenerator, messages: list, streaming: bool):
        callback = BaseStreamHandler(gen)
        deepseek_chat = DeepSeekChat(api_base=OPENAI_API_BASE, api_key=OPENAI_API_KEY, callback_handler=callback)

        deepseek_chat.chat(messages=messages, streaming=streaming)

        return gen

    def query_rewrite(self, query: str):
        gen = BaseThreadGenerator()
        sys_prompt = prompt_handler.sys_prompt()
        query_prompt = prompt_handler.query_rewriter(query, 3)
        messages = [{"role": "system", "content": sys_prompt}, {"role": "user", "content": query_prompt}]

        import threading
        thread = threading.Thread(target=self.chat, args=(gen, messages, True))
        thread.start()

        return gen


deepseek_research_ctrl = DeepResearchCtrl()

if __name__ == '__main__':
    gen = deepseek_research_ctrl.query_rewrite(query="中国人工智能发展")
    answer = ""
    for i in gen:
        answer += i
        print(i)

    print(answer)
