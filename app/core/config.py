from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Класс настроек приложения.

    Attributes:
        database_url (str): URL базы данных.
        secret (str): Секретный ключ для JWT.
        model_config (SettingsConfigDict): Конфигурация модели, указывающая файл
                                           переменных окружения и его кодировку.
    """
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8'
    )


settings = Settings()
