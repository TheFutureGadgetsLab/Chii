import logging
from discord.ext.commands import Context

LOG_FORMAT  ='%(levelname)s | %(asctime)s %(message)s'
DATE_FORMAT ='%m/%d/%Y %I:%M:%S %p'

class LoggerLimb:
    @property
    def __derived_name(self) -> str:
        """ Returns the name of the derived class """
        return str(self.__class__.__name__)

    def _setup_logger(self, level=logging.INFO) -> logging.Logger:
        name     = self.__derived_name
        log_file = f'logs/{self.__derived_name}.log'

        formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)

        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)

        logger.info(f'')
        logger.info(f'#'*80)
        logger.info(f'#')
        logger.info(f'# {name} Startup')
        logger.info(f'#')
        logger.info(f'#'*80)
        logger.info(f'')

        return logger

    async def cog_command_error(self, ctx: Context, error: Exception) -> None:
        self.logger.error(str(error))
        print("-+"*40)
        print(self.__derived_name)
        print(error)