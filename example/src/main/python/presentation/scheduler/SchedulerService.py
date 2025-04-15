from motron import UseCase, Scheduled
from motron.data.repository.logger import MotronLogger

@UseCase
class SchedulerService:
    logger: MotronLogger

    def __init__(self):
        self.logger.info("SchedulerService initialized")

    @Scheduled(cron="*/1 * * * *")  # Runs every 1 minute
    def run_every_minute(self):
        self.logger.info("⏰ Cron job: Executed every 1 minute")

    @Scheduled(fixedDelay=5)  # Runs every 5 seconds after last execution finishes
    def run_every_5_seconds(self):
        self.logger.debug("⏱️ Fixed delay: Executed every 5 seconds")

    @Scheduled(initialDelay=10)  # Runs once after 10 seconds
    def run_after_10_seconds(self):
        self.logger.warn("🚀 Initial delay: Ran after 10 seconds")
