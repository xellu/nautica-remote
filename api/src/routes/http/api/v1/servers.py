from nautica.api.http import (
    Request,
    Require,
    
    Context,
    
    Reply,
    Error
)
from src.lib.ServerList import Servers

@Request.POST("create")
@Require.body(label=str, node=str, ip=str, port=int, accessKey=str)
def create_server(ctx: Context):
    if ctx.args.body["port"] > 65535 or ctx.args.body["port"] <= 0:
        return Error("Invalid port"), 400
    
    if len(ctx.args.body["node"]) > 40:
        return Error("Node label too long (max 40 chars allowed)")
    if len(ctx.args.body["label"]) > 128:
        return Error("Server label too long (max 128 chars allowed)")
    
    Servers.create(
        label = ctx.args.body["label"],
        node = ctx.args.body["node"],
        
        ip = ctx.args.body["ip"],
        port = ctx.args.body["port"],
        accessKey = ctx.args.body["accessKey"]
    )
    Servers.save()
    
    return Reply(), 200