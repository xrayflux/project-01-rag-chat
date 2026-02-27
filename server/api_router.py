#!/usr/bin/env python3
# 指定解释器路径（Linux/macOS 直接执行脚本时使用）

# -*- coding: utf-8 -*-
# 指定文件编码为 UTF-8，避免中文乱码


# FastAPI 官方教程：https://fastapi.tiangolo.com/tutorial/first-steps/

from typing import Union  # 类型注解工具
from fastapi import FastAPI  # FastAPI 应用核心类
from chat.chat import chat  # 导入接口处理函数
import uvicorn  # ASGI 服务器，用于运行 FastAPI


# 创建 FastAPI 应用实例（整个 Web 服务的核心对象）
app = FastAPI(
    description="FuFan Chat Web API Server"  # 接口文档中的描述信息
)


# 注册 POST 路由：将 POST /api/chat 请求交给 chat 函数处理
# 使用函数调用方式定义路由（而非 @装饰器），在动态添加或运行时修改路由配置时更为灵活。
app.post(
    "/api/chat",               # 接口路径
    tags=["Chat"],             # 文档分类标签
    summary="大模型对话交互接口",  # 文档简要说明
)(chat)  # 等价于 @app.post(...)\ndef chat(...)


# 仅在直接运行该文件时启动服务
if __name__ == '__main__':

    # 启动 ASGI 服务
    # host=0.0.0.0 表示监听所有网络接口
    # port=8000 表示监听端口 8000
    uvicorn.run(app, host='0.0.0.0', port=8000)

