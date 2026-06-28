import json
import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse

from config.ai_conf import AI_API_KEY, AI_API_ENDPOINT, AI_MODEL, AI_TIMEOUT
from models.users import User
from schemas.ai import ChatRequest
from utils.auth import get_current_user

router = APIRouter(prefix="/api/ai", tags=["ai"])

# 向 DashScope 发起流式请求，逐块 yield SSE 数据给前端。
async def stream_dashscope(messages: list[dict]):
    # 准备请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AI_API_KEY}",
        "X-DashScope-SSE": "enable", # 开启流式输出
    }
    # 准备请求体
    payload = {
        "model": AI_MODEL,
        "messages": messages,
        "stream": True,
    }
    # 创建一个异步 HTTP 客户端
    async with httpx.AsyncClient() as client:
        # 发起流式请求
        async with client.stream(
            "POST",
            AI_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=AI_TIMEOUT,
        ) as response:
            # 检查是否出错，把错误状态码包装成 SSE 数据返回给前端
            if response.status_code != 200:
                yield f"data: {json.dumps({'error': f'AI 请求失败: {response.status_code}'})}\n\n"
                return
            # 逐行处理响应，过滤并转发给前端
            async for line in response.aiter_lines():
                if line.startswith("data:"):
                    yield line + "\n\n"

@router.post("/chat")
async def chat(
    request: ChatRequest,
    user: User = Depends(get_current_user),
):
    # 将 Pydantic 模型转为普通字典列表
    messages = [{"role": m.role, "content": m.content} for m in request.messages]
    # 调用 DashScope 流式接口，返回 SSE 流
    return StreamingResponse(
        stream_dashscope(messages),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # 防止 Nginx 缓冲 SSE 流
        },
    )