from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from app.api.routes import router

app = FastAPI(title="企业知识库智能问答 Agent", version="1.0.0")
app.include_router(router, prefix="/api")

# 自定义 /docs 路由，将 JS 和 CSS 换成国内极速 CDN
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        # 这里改成了国内的 jsdelivr 镜像源（或者直接使用 unpkg 的国内缓存）
        swagger_js_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.15.5/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.bootcdn.net/ajax/libs/swagger-ui/4.15.5/swagger-ui.css",
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)