#!/usr/bin/env python3
# 指定解释器路径（Linux/macOS 直接执行时使用）

# -*- coding: utf-8 -*-
# 指定文件编码为 UTF-8，避免中文乱码


from fastapi import Body, HTTPException
# Body：声明请求体参数
# HTTPException：用于主动抛出 HTTP 错误响应

from typing import List, Union, Optional
# 类型注解工具

# 使用 LangChain 调用 ChatGLM3 / GLM4 服务
from langchain.chains.llm import LLMChain   # 当前未使用（可删除）
from langchain_community.llms.chatglm3 import ChatGLM3
from langchain_core.messages import AIMessage  # 当前未使用（可删除）
from langchain_core.prompts import PromptTemplate

from loguru import logger
# 日志库，用于打印运行信息


def chat(
    query: str = Body("", description="用户的输入"),
    # model_name: str = Body("chatglm3-6b", description="基座模型的名称"),
    model_name: str = Body("glm4-9b-chat", description="基座模型的名称"),
    temperature: float = Body(0.8, description="大模型参数：采样温度", ge=0.0, le=2.0),
    max_tokens: Optional[int] = Body(None, description="大模型参数：最大输入Token限制"),
):
    """
    接收用户请求 → 调用大模型服务 → 返回模型结果
    """

    # ===== 记录请求参数=====
    logger.info("Received query: {}", query)
    logger.info("Model name: {}", model_name)
    logger.info("Temperature: {}", temperature)
    logger.info("Max tokens: {}", max_tokens)

    # ===== 调用大模型服务 =====
    try:
        # 构造提示模板
        template = """{query}"""
        prompt = PromptTemplate.from_template(template)

        # 后端推理服务地址（OpenAI 兼容接口风格）
        endpoint_url = "http://192.168.110.131:9091/v1/chat/completions"

        # 创建 LLM 对象
        llm = ChatGLM3(
            endpoint_url=endpoint_url,
            model_name=model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # LCEL 语法：将 Prompt 与 LLM 组合为一条执行链
        llm_chain = prompt | llm

        # 执行链，发送请求到模型服务
        response = llm_chain.invoke(query)

        # 空值检查
        if response is None:
            raise ValueError("Received null response from LLM")

        # 正常返回 JSON 响应
        return {"LLM Response": response}

    except ValueError as ve:
        # 参数或返回值异常 → 400
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        # 其他异常（网络错误 / 服务异常 / 代码错误）→ 500
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error: " + str(e)
        )

