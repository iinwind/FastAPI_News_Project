from pydantic import BaseModel
from typing import List

# 用 Pydantic 校验前端发来的数据格式，防止恶意输入
class ChatMessage(BaseModel):
    role: str  # "user" 或 "assistant"
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]