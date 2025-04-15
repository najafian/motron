from dataclasses import dataclass
from motron import UseCase, ConfigurationProperties, Profile, Bean


@ConfigurationProperties()
@dataclass
class AppConfig:
    title = "default title"
    debug = False
    port = 8080

@Profile("dev")
@UseCase
class DevService:
    def __init__(self):
        print("Loaded DevService")

@Profile("prod")
@UseCase
class ProdService:
    def __init__(self):
        print("Loaded ProdService")

@Bean
def appInfo():
    print("Creating custom bean `appInfo`")
    return {
        "author": "motron",
        "version": "1.0.0"
    }