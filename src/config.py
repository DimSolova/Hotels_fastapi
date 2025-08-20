from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DB_HOST : str
    DB_PORT : int
    DB_USER : str
    DB_PASS : str
    DB_NAME: str


    #декоратор делает функцию как свойство
    #этот адрес так же называют DSN
    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


    #.env стоит и так по умолчанию , в extra задается чтобы он игнорировал ,
    # если вдруг в .env есть переменная , в классе нет
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

setting = Settings()