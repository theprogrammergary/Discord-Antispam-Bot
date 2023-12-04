from loguru import logger

logger.remove()
logger.add(
    "./logs/{time:YYYY-MM-DD}.log",
    rotation="00:00",
    retention="14 days",
    compression="zip",
    backtrace=True,
    format='\n{time:YYYY-MM-DD HH:mm:ss} {level.icon} {level} \n{file}>"{function}">{line} \n    {message} \n',
)