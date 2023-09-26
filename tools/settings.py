import logging
import os

from pydantic_settings import BaseSettings, SettingsConfigDict

from proto import hw_pb2


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    
    BASE_DIR: str = os.path.dirname(__file__)
    
    HOST: str = "localhost"
    PORT: int = 50051
    WORKERS: int = 1
    JAEGER_SERVER_ADDR: str = "0.0.0.0:14250"
    
    SERVICE_NAME:str = hw_pb2.DESCRIPTOR.services_by_name["Greeter"].full_name
       
    @property
    def grpc_channel(self) -> str:
        return f"{self.HOST}:{self.PORT}"
    
    @property
    def logger(self):
        logger = logging.getLogger()
        logger.setLevel("DEBUG")
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt="%(asctime)s: %(levelname)-8s %(message)s")
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        return logger


settings = Settings()
logger = settings.logger
