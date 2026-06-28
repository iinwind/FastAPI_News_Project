from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

# 统一所有接口成功响应的格式的函数，并自动处理各种不能直接转 JSON 的复杂对象。
def success_response(message: str = "success", data = None):
    content = {
        "code": 200,
        "message": message,
        "data": data
    }
    return JSONResponse(content=jsonable_encoder(content))