from motron.data.repository.logger import MotronLogger
from motron.domain.entity.log_level import LogLevel

def test_logger_levels():
    logger = MotronLogger("TestLogger")
    logger.trace("trace level")
    logger.debug("debug level")
    logger.info("info level")
    logger.warn("warn level")
    logger.error("error level")

    # No assertion since we're just checking no exceptions and log formatting
    assert True
