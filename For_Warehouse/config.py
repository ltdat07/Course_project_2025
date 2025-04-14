from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = "TOKEN_BOT"
    EXCEL_FILE: str = "ESP_sklad_2.xlsx"
    SHEET_MOVE: str = "Движение_склад"
    SHEET_REST: str = "Склад_остатки"
    SHEET_PRICE: str = "Справочник_товаров"
    LOG_FILE: str = "warehouse.log"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Экземпляр настроек, который будет импортироваться в других модулях
settings = Settings()
