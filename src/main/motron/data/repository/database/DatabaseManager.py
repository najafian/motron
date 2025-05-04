import os
from typing import Dict

from pymongo import MongoClient
from mongita import MongitaClientDisk
from motron.core.config_loader import get_config
from motron.data.repository.logger import MotronLogger

logger = MotronLogger("motron.database")


class DatabaseManager:
    _instances: Dict[str, object] = {}

    @classmethod
    def get_db(cls):
        config = get_config()
        db_config = config.get("database", {})
        db_type = db_config.get("type", "mongo")
        mode = db_config.get("mode", "server")
        mongo_conf = db_config.get("mongo", {})
        db_name = mongo_conf.get("name", "test")

        # Return cached instance if exists
        if db_name in cls._instances:
            return cls._instances[db_name]

        # Initialize Mongo or Mongita instance
        if db_type == "mongo":
            if mode == "standalone":
                mongita_path = os.path.join(os.getcwd(), "database", "mongo")
                os.makedirs(mongita_path, exist_ok=True)

                logger.info(f"Starting embedded MongoDB (Mongita) at: {mongita_path}")
                client = MongitaClientDisk(path=mongita_path)
                cls._instances[db_name] = client[db_name]
                logger.info(f"Mongita started with DB: {db_name}")
            elif mode == "server":
                uri = mongo_conf.get("uri", "mongodb://localhost:27017")
                username = mongo_conf.get("username")
                password = mongo_conf.get("password")

                if username and password and "@" not in uri:
                    uri = uri.replace("mongodb://", f"mongodb://{username}:{password}@")

                logger.info(f"Connecting to MongoDB server at {uri}")
                client = MongoClient(uri)
                cls._instances[db_name] = client[db_name]
                logger.info(f"MongoDB connection established with DB: {db_name}")
            else:
                raise ValueError(f"Unknown mongo mode: {mode}")
        else:
            raise NotImplementedError(f"Database type '{db_type}' is not supported")

        return cls._instances[db_name]
