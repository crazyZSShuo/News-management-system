import uvicorn
from app.config.config import config


if __name__ == "__main__":
    uvicorn.run(
        "app.factory:create_app",
        host="127.0.0.1",
        port=8000,
        access_log=True,
        reload=config.app.debug,
        reload_dirs=["app"],
        factory=True
    )
