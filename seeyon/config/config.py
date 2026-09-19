# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: config.py
# Description:
# Date: 2026/9/8 11:30
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_DIR = Path(__file__).parents[2]
ENV_FILE = ENV_DIR / ".env"

class Settings(BaseSettings):
    # 加载配置文件，读取值，赋值当前对应变量里面
    # 使用变量接受，特殊：变量名称固定的 model_config
    model_config = SettingsConfigDict(
        # 文件位置
        env_file=ENV_FILE,
        # 编码方式，中文
        env_file_encoding='utf-8',
        # 配置文件属性和类属性不一致
        extra='ignore'
    )
    # 对应配置文件，创建对应属性:类型
    LLM_MODEL: str

    llm_api_key: str
    llm_base_url: str

    # 数据库
    database_url: str
    # 商城 API
    commerce_api_base_url: str
    # 服务器
    app_host: str
    app_port: int


settings = Settings()

if __name__ == '__main__':
    print(settings.LLM_MODEL)
    print(settings.app_host)