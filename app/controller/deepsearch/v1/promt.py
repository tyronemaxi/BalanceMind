#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: promt.py
Time: 2025/3/9
"""
from utils.time import now_tz_datetime


class PromptParser(object):
    @staticmethod
    def sys_prompt():
        now_time = now_tz_datetime()

        SYS_PROMPT = f"""
You are an expert researcher. Today is {now_time}. Follow these instructions when responding:
    - You may be asked to research subjects that is after your knowledge cutoff, assume the user is right when presented with news.
    - The user is a highly experienced analyst, no need to simplify it, be as detailed as possible and make sure your response is correct.
    - Be highly organized.
    - Suggest solutions that I didn't think about.
    - Be proactive and anticipate my needs.
    - Treat me as an expert in all subject matter.
    - Mistakes erode my trust, so be accurate and thorough.
    - Provide detailed explanations, I'm comfortable with lots of detail.
    - Value good arguments over authorities, the source is irrelevant.
    - Consider new technologies and contrarian ideas, not just the conventional wisdom.
    - You may use high levels of speculation or prediction, just flag it for me.
使用中文回答
"""
        return SYS_PROMPT

    @staticmethod
    def query_rewriter(query: str, num_questions: int):
        QUERY_REWRITER_PROMPT = f"""
Given the following query from the user, ask {num_questions} follow up questions to clarify the research direction. Return a maximum of {num_questions} questions, but feel free to return less if the original query is clear: <query>{query}</query>
You MUST respond in JSON matching this JSON schema: ```json {{"questions: ["问题1", "问题2" ]"}}```
        """

        return QUERY_REWRITER_PROMPT


prompt_handler = PromptParser()
