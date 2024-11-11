#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: tyrone
File: tools.py
Time: 2024/11/3
"""
import json

from openai import OpenAI

from app.client.outer.weather import weather_cli, city_codes_cli
from conf.settings import OPENAI_API_KEY, OPENAI_API_BASE
from app.core.log import logger


def get_city_code(query: str):
    """
    获取城市 acode
    """
    city_code = city_codes_cli.get_adcode(query)

    return city_code


def parse_weather_response(response):

    if response['status'] != '1':
        return "无法获取天气信息"

    forecasts = response['forecasts'][0]  # 获取第一个城市的天气预报
    city = forecasts['city']
    province = forecasts['province']
    report_time = forecasts['reporttime']

    weather_info = [f"{city}, {province} 天气预报（数据更新时间：{report_time}）:\n"]

    for cast in forecasts['casts']:
        date = cast['date']
        week = cast['week']
        day_weather = cast['dayweather']
        night_weather = cast['nightweather']
        day_temp = cast['daytemp']
        night_temp = cast['nighttemp']
        day_wind = cast['daywind']
        night_wind = cast['nightwind']

        weather_info.append(
            f"{date}（周{week}）: "
            f"白天气温 {day_temp}°C，天气：{day_weather}，风向：{day_wind}; "
            f"夜间气温 {night_temp}°C，天气：{night_weather}，风向：{night_wind}\n"
        )

    return ''.join(weather_info)


def get_weather(query: str):
    """
    获取天气
    """
    try:
        a_code = get_city_code(query)
    except Exception as e:
        return "无法获取城市信息"

    try:
        resp = weather_cli.get_weather(a_code)
        data = parse_weather_response(resp)
    except Exception as e:
        return "无法获取天气信息"

    return data


def get_stock_price(query: str):
    """
    获取实时股价
    """
    msg = "东吴证券的实时股价是 7.00 元"
    return msg


def get_news(query: str):
    """
    实时热点新闻
    """
    msg = "特朗普大选获胜"
    return msg


def travel_assistant(query: str):
    """
    获取旅游信息
    """
    msg = '最近的天气特别适合去海边旅行，例如厦门，宁波，三亚这些城市，美食推荐去吃海鲜大餐，还有各种好玩的景点，例如鼓浪屿，杭州西湖，上海外滩等，祝你旅行愉快！'
    return msg


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "根据用户的问题，回答天气类问题。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户问题"
                    }
                },
                "required": ["query"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "根据用户的问题，回答对应公司的实时股价信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户问题"
                    }
                },
                "required": ["query"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "get_news",
            "description": "根据用户的问题，回答热点新闻信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户问题"
                    }
                },
                "required": ["query"]
            }
        }
    }, {
        "type": "function",
        "function": {
            "name": "travel_assistant",
            "description": "根据用户的问题，回答热点旅游信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户问题"
                    }
                },
                "required": ["query"]
            }
        }
    }
]


def get_completion(messages, model):
    client = OpenAI(base_url=OPENAI_API_BASE,
                    api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
        max_tokens=1024,
        tools=tools
    )

    return response.choices[0].message


def chat(prompt, model='gpt-4'):
    messages = [
        {"role": "system", "content": "你是一名问答助手, 能专业，简洁的回答用户问题"},
        {"role": "user", "content": prompt}
    ]

    resp = get_completion(messages, model)
    print(messages)
    messages.append(resp)

    while resp.tool_calls:
        for tool in resp.tool_calls:
            args = json.loads(tool.function.arguments)

            if tool.function.name == "get_weather":
                result = get_weather(**args)
                logger.info(f"{result}")

            elif tool.function.name == "get_news":
                result = get_news(**args)
                logger.info(f"{result}")

            elif tool.function.name == "get_stock_price":
                result = get_stock_price(**args)
                logger.info(f"{result}")

            elif tool.function.name == "travel_assistant":
                result = travel_assistant(**args)
                logger.info(f"{result}")

            else:
                result = "抱歉，我无法提供帮助。"

            messages.append(
                {
                    "tool_call_id": tool.id,
                    "role": "tool",
                    "name": tool.function.name,
                    "content": result,
                }
            )  # extend conversation with function response

            resp = get_completion(messages, model)
            messages.append(resp)

    # resp = get_completion(messages, model)
    print(resp.content)


if __name__ == '__main__':
    history = []
    prompt = "最近的热点新闻"
    chat(prompt)
    # resp = get_city_code("今天天气怎么样")
    # print(resp)
