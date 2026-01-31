from nautica.api.ws import (
    Packet,
    Reply
)
from src.lib.ServerList import Servers

@Packet.On("nr.list")
async def server_list(payload):
    out = []
    for k, v in Servers.data.items():
        server = v.copy()
        del server["accessKey"]
        
        out.append(server)
        
    return Reply(id="nr.list", servers=out)