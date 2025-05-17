import os
from dotenv import load_dotenv
from litestar import Litestar, get
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyPlugin
from litestar.openapi import OpenAPIConfig
from advanced_alchemy.extensions.litestar.plugins import SQLAlchemyAsyncConfig

from db.config import engine
from api.user import user_router
from db.config import create_tables

# Load environment variables
load_dotenv()

# Host and port settings
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

async def on_startup(app: Litestar) -> None:
    await create_tables()

# OpenAPI config
openapi_config = OpenAPIConfig(
    title="User Management API",
    version="1.0.0",
    description="A REST API for user management with LiteStar and PostgreSQL",
    use_handler_docstrings=True,
)

# SQLAlchemy plugin config
sqlalchemy_plugin = SQLAlchemyPlugin(
    config=SQLAlchemyAsyncConfig(
        engine_instance=engine,
        create_all=True  # create tables on startup
    )
)

# Health check
@get("/", description="Health check endpoint")
async def health_check() -> dict:
    return {"status": "ok", "message": "User Management API is running"}

# Create the application
app = Litestar(
    route_handlers=[health_check, user_router],
    openapi_config=openapi_config,
    plugins=[sqlalchemy_plugin],
    on_startup=[on_startup],  # 👈 вот это добавь
    debug=True,
)

# Run manually (only needed outside Docker)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=True,
    )
