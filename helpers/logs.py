import logging

logging.basicConfig(level=logging.INFO, 
                    filename="log.log", filemode="w", 
                    format="%(asctime)s - %(levelname)s - %(message)s - %(created)f")

logging.debug("debug")
logging.info("info")
logging.warning("warning")
logging.error("error")
logging.critical("critical")