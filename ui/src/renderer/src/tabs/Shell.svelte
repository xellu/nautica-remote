<script lang="ts">
    import { handlers, send, stateStore } from "../scripts/Connector";

    let state: "idle" | "connecting" | "connected" | "disconnected" = "idle";
    let serverLogs: {timestamp: {formatted: string, raw: number}, name: string, type:string, message: string, colors: {name: string, message: string}}[] = []

    stateStore.subscribe((value) => {
        state = value;
    })

    const states = {
        idle: {
            text: "No server selected",
            css: "opacity-50"
        },
        connecting: {
            text: "Connecting to Daemon...",
            css: "animate-pulse"
        },
        connected: {
            text: "Connected",
            css: "opacity-0"
        },
        disconnected: {
            text: "❗ Disconnected",
            css: "text-error-500"
        }
    }

    const colors = {
        INFO: {name: "text-primary-500", msg: "text-surface-100"},
        OK: {name: "text-success-500", msg: "text-surface-100"},
        WARN: {name: "text-warning-500", msg: "text-surface-100"},
        ERROR: {name: "text-error-500", msg: "text-surface-100"},
        CRITICAL: {name: "text-error-500", msg: "text-error-300"},
        DEBUG: {name: "text-purple-500", msg: "text-surface-100"},
        TRACE: {name: "text-white", msg: "text-surface-300"}
    }

    let command: string = "";
    handlers["log"] = (packet: any) => {
        serverLogs = serverLogs.concat(packet.buffer);
    }
</script>

{#if state == "connected"}
<div class="h-full w-full p-3 flex flex-col font-mono text-sm">
    {#each serverLogs as log}
        <pre class="whitespace-pre-wrap"><span class="text-surface-500">({log.timestamp.formatted})</span> <span class="{colors[log.type]?.name}">[{log.name}/{log.type}]</span> <span class="{colors[log.type]?.msg}">{log.message}</span></pre>
    {/each}
</div>

<div class="z-10 flex p-3 gap-1 fixed bottom-0 w-[calc(100vw-14rem-16px)]">
    <input type="text" class="input bg-surface-900" placeholder="Enter a command"
        bind:value={command}
        onkeypress={(event) => {
            if (["clear", "cls"].includes(command.toLocaleLowerCase())) {
                command = "";
                serverLogs = [];
                return;
            }

            // console.log(event)
            if (event.key == "Enter") {
                send({id: "command", command: command});
                command = "";
            }
        }}
    >
    <button class="btn preset-filled-primary-500" onclick={() => {
        if (["clear", "cls"].includes(command.toLocaleLowerCase())) {
            command = "";
            serverLogs = []
            return;
        }
        send({id: "command", command: command});
        command = "";
    }}>Send</button>
</div>


{:else}
    <div class="h-full w-full flex items-center justify-center {states[state].css}">
        <p>{states[state].text}</p>
    </div>
{/if}