<script lang="ts">
    import PopUp from "../components/PopUp.svelte";
  
    import { handlers } from "../scripts/Connector";
    // import { RemoteConfig } from "../scripts/Config";
    import { connect, disconnect } from "../scripts/Connector";
    import { randomString } from "../scripts/Utils"


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
        editId: null,

        label: "",
        node: "",
        ip: "",
        port: undefined,
        accessKey: ""
    }

    function getServers() {
        return JSON.parse(localStorage.getItem("servers") || "[]");
    }

    function addServer(): any {
        if (!createServer.label || !createServer.ip || !createServer.accessKey || !createServer.port) {
            return toaster.create({
                title: "Missing fields",
                type: "error"
            })
        }

        let port: number = parseInt(createServer.port)
        if (port > 65535 || port < 0) {
            return toaster.create({
                title: "Invalid port",
                type: "error"
            })
        }

        if (createServer.node.length > 40)
            return toaster.create({
                title: "Node label too long (max 40 chars allowed)",
                type: "error"
            })

        if (createServer.label.length > 128)
            return toaster.create({
                title: "Server label too long (max 128 chars allowed)",
                type: "error"
            })

        let _servers = getServers()
        _servers.push({
            _id: randomString(64),
            label: createServer.label,
            node: createServer.node,

            ip: createServer.ip, port: createServer.port,
            accessKey: createServer.accessKey
        })
        localStorage.setItem("servers", JSON.stringify(_servers));


        toaster.create({
            title: "Server added"
        })
        createServer.open = false
        createServer.label = ""
        createServer.node = ""
        createServer.ip = ""
        createServer.port = undefined
        createServer.accessKey = ""
        createServer.editId = null

        servers = getServers()
    }

    function deleteServer() {
        if (!createServer.editId) return;
        if (!confirm("Are you sure?")) return;

        servers = servers.filter((s) => { return s._id != createServer.editId })
        localStorage.setItem("servers", JSON.stringify(servers));

        createServer.open = false
        createServer.label = ""
        createServer.node = ""
        createServer.ip = ""
        createServer.port = undefined
        createServer.accessKey = ""
        createServer.editId = null
    }

    function editServer(): any {
        if (!createServer.editId) return;

        if (!createServer.label || !createServer.ip || !createServer.accessKey || !createServer.port) {
            return toaster.create({
                title: "Missing fields",
                type: "error"
            })
        }

        let port: number = parseInt(createServer.port)
        if (port > 65535 || port < 0) {
            return toaster.create({
                title: "Invalid port",
                type: "error"
            })
        }

        if (createServer.node.length > 40)
            return toaster.create({
                title: "Node label too long (max 40 chars allowed)",
                type: "error"
            })

        if (createServer.label.length > 128)
            return toaster.create({
                title: "Server label too long (max 128 chars allowed)",
                type: "error"
            })

        let _servers = getServers()

        const index = _servers.findIndex(s => s._id === createServer.editId)
        if (index === -1) {
            return toaster.create({
                title: "Server not found",
                type: "error"
            })
        }

        _servers[index] = {
            _id: createServer.editId,
            label: createServer.label,
            node: createServer.node,
            ip: createServer.ip,
            port: port,
            accessKey: createServer.accessKey
        }

        localStorage.setItem("servers", JSON.stringify(_servers))

        toaster.create({
            title: "Server updated"
        })

        createServer.open = false
        createServer.label = ""
        createServer.node = ""
        createServer.ip = ""
        createServer.port = undefined
        createServer.accessKey = ""
        createServer.editId = null

        servers = getServers()
    }


    onMount(() => {
        servers = getServers()
    })
</script>

<div class="h-full flex flex-col gap-1 p-3">
    <div class="flex gap-3 p-1.5 bg-surface-900 rounded-xl mb-5">
        <button class="btn preset-filled-primary-500" onclick={() => {
            createServer.editId = null
            createServer.label = ""
            createServer.node = ""
            createServer.ip = ""
            createServer.port = undefined
            createServer.accessKey = ""
            createServer.open = true
    }}>Add</button>
    </div>

    <p class="uppercase font-bold text-surface-500 text-sm">Server List</p>
    {#each servers as s}
        <div class="border border-surface-900 rounded-2xl p-3 flex justify-between items-start group">
            <div>
                <div class="flex items-center gap-2 flex-wrap">
                    <h2>{s.label}</h2>
                    {#if s.node}
                        <span class="chip preset-tonal-primary py-0.5">{s.node}</span>
                    {/if}    
                </div>
                <p class="font-mono text-sm text-surface-300">{s.ip}:{s.port}</p>
            </div>
            <div class="flex items-center gap-1">
                <button class="btn preset-filled-surface-200-800" onclick={() => {
                    createServer.editId = s._id
                    createServer.label = s.label
                    createServer.node = s.node
                    createServer.ip = s.ip
                    createServer.port = s.port
                    createServer.accessKey = s.accessKey
                    createServer.open = true
                }}>
                    Edit
                </button>
                <button class="btn preset-filled-primary-500" onclick={() => {
                    disconnect();
                    connect(s.ip, s.port, s.accessKey);
                    handlers["setPage"]("shell")
                }}>
                    Connect
                </button>
            </div>
        </div>
    {/each}
</div>

<PopUp
    bind:open={createServer.open}
    title = {createServer.editId == null ? "Add Server" : "Edit Server"}

    
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

    {#if createServer.editId == null}
        <button class="btn preset-filled-primary-500 mt-5 w-full" onclick={() => {
            addServer()
        }}>Add</button>
    {:else}
        <div class="mt-5 flex gap-3">
            <button class="btn preset-filled-error-500 w-1/3" onclick={() => {
                deleteServer()
            }}>Delete</button>

            <button class="btn preset-filled-primary-500 w-2/3" onclick={() => {
                editServer()
            }}>Save Changes</button>
        </div>
    {/if}
</PopUp>