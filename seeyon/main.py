import uvicorn

from seeyon.config.config import settings
from seeyon.utils.database import init_db_engine
from seeyon.utils.http_client import init_http_client

# -*- coding: utf-8 -*-
# ==============================================================================
# Package:
# File: main.py
# Description:
# Date: 2026/9/8 14:03
#
# @author WangLei
# @version 1.0
# @email WangLei1578@outlook.com
# @since Python 3.14.5
# ==============================================================================

if __name__ == '__main__':
    # init_db_engine()
    # init_http_client()
    # asyncio.run(init_db_engine())
    uvicorn.run(app="seeyon.api.app:app",
                host=settings.app_host,
                port=settings.app_port)
