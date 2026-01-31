from nautica.services.database.xeldb import XelDB
from nautica.services.logger import LogManager

Servers = XelDB("servers")
logger = LogManager("Lib.ServerList")

# Core.Eventer.on("shutdown")
# def on_exit(*args, **kwargs):
#     Servers.stop()
#     logger.ok("Server list saved") 
#not needed - framework already handles it apparently