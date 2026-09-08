# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: http_client.py
# Description:工具模块,创建远程调用httpx工具
# Date: 2026/9/8 19:31
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
import asyncio

import httpx
from httpx import AsyncClient

# import requests
# requests.get("https://www.baidu.com/s?ie=UTF-8&wd=%E4%BB%80%E4%B9%88%E6%98%AFlangchain")
# 以上方法也是可行的,只不过没法直接调用异步

http_client: AsyncClient | None = None

# 创建httpx异步客户端
async def get_http_client():
    global http_client
    if http_client is None:
        http_client = httpx.AsyncClient(timeout=10.0)
    return http_client

# 关闭httpx异步客户端
async def close_http_client():
    global http_client
    if http_client is not None:
        await http_client.aclose()
        http_client = None

# 测试方法
async def test():
    # 创建httpx异步客户端
    await get_http_client()
    # 发送GET请求
    result = await http_client.get("http://127.0.0.1:18081/users/u1001/orders")
    print(result.json())
    print(result.text)
    # 关闭httpx异步客户端
    await close_http_client()

if __name__ == '__main__':
    asyncio.run(test())

