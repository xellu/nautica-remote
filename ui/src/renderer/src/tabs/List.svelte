<script lang="ts">
    import PopUp from "../components/PopUp.svelte";
  
    import { send, handlers } from "../scripts/Bridge"
    import { RemoteConfig } from "../scripts/Config";
    import { connect, disconnect } from "../scripts/Connector";

    import { onMount } from "svelte"
    import { toaster } from "../scripts/Toast"
  
  
    let servers: {
        _id: string,
        label: string,
        node: string,

        ip: string,
        port: number,
        accessKey: string
    }[] = [
        // {
        //     label: "api-public",
        //     node: "nc-main",

        //     ip: "nc-main.nightcube.net",
        //     port: 3711
        // }
    ]

    let createServer = {
        open: false,
        blocked: false,

        label: "",
        node: "",
        ip: "",
        port: undefined,
        accessKey: ""
    }

    async function addServer() {
        if (createServer.blocked) { return; }

        createServer.blocked = true;

        let r;
        let data: any;
        try {
            r = await fetch(`http://${RemoteConfig.ip}:${RemoteConfig.port.http}/api/v1/servers/create`, {
                method: "POST",
                body: JSON.stringify({
                    label: createServer.label,
                    node: createServer.node,

                    ip: createServer.ip, port: parseInt(createServer.port),
                    accessKey: createServer.accessKey
                })
            });
            data = await r.json();
        } catch (e) {
            console.error(e)
            toaster.create({
                title: `${e}`,
                type: "error"
            })
            createServer.blocked = false;
            return;
        }

        createServer.blocked = false;

        if (!r.ok) {
            toaster.create({
                title: data.error || "Failed to add server",
                type: "error"
            })
            return
        }

        toaster.create({
            title: "Server added"
        })
        createServer.open = false
        createServer.label = ""
        createServer.node = ""
        createServer.ip = ""
        createServer.port = undefined
        createServer.accessKey = ""

        send({id: "nr.list"})
    }

    onMount(() => {
        handlers["nr.list"] = (data: any) => {
            // console.log(data)
            servers = data.servers;
        }

        send({
            id: "nr.list"
        })
    })
</script>

<div class="h-full flex flex-col gap-1 p-3">
    <div class="flex gap-3 p-1.5 bg-surface-900 rounded-xl mb-5">
        <button class="btn preset-filled-primary-500" onclick={() => {createServer.open = true;}}>Add</button>
    </div>

    <p class="uppercase font-bold text-surface-500 text-sm">Server List</p>
    {#each servers as s}
        <div class="border border-surface-900 rounded-2xl p-3 flex justify-between items-start group">
            <div>
                <div class="flex items-center gap-2 flex-wrap">
                    <h2>{s.label}</h2>
                    <span class="chip preset-tonal-primary py-0.5">{s.node}</span>
                </div>
                <p class="font-mono text-sm text-surface-300">{s.ip}:{s.port}</p>
            </div>
            <div class="flex items-center gap-1">
                <button class="btn preset-filled-surface-200-800">
                    Edit
                </button>
                <button class="btn preset-filled-primary-500" onclick={() => {
                    disconnect();
                    connect(s.ip, s.port, s.accessKey);
                }}>
                    Connect
                </button>
            </div>
        </div>
    {/each}
</div>

<PopUp
    bind:open={createServer.open}
    title = "Add Server"
>
    <p class="text-sm">Label</p>
    <input type="text" class="input" bind:value={createServer.label} placeholder="api-public">

    <p class="text-sm mt-3">Node</p>
    <input type="text" class="input" bind:value={createServer.node} placeholder="eu-main">

    <p class="text-sm mt-3">Server Address</p>
    <div class="flex gap-1">
        <input type="text" class="input" bind:value={createServer.ip} placeholder="192.168.0.0">
        <p>:</p>
        <input type="number" class="input w-32" bind:value={createServer.port} placeholder="1-65535">
    </div>

    <p class="text-sm mt-3">Access Key</p>
    <input type="password" class="input" bind:value={createServer.accessKey}>

    <button class="btn preset-filled-primary-500 mt-5 w-full" disabled={createServer.blocked} onclick={() => {
        addServer()
    }}>Add</button>
</PopUp>