from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "旧物改造灵感交换站"
    DATABASE_URL: str = "mysql+pymysql://root:password@mysql:3306/upcycle"
    UPLOAD_DIR: str = "/app/uploads"
    ALLOWED_EXTENSIONS: set[str] = {"jpg", "jpeg", "png", "gif", "webp"}
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB

    class Config:
        env_file = ".env"


settings = Settings()
