from config.settings import get_settings

settings = get_settings()

# AI API 配置
AI_API_KEY = settings.AI_API_KEY
AI_API_ENDPOINT = settings.AI_API_ENDPOINT
AI_MODEL = settings.AI_MODEL

# 请求超时（秒）
AI_TIMEOUT = 60.0