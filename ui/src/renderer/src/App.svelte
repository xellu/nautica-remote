<script lang="ts">
    import logo from "./assets/logo.svg";

    import List from "./tabs/List.svelte"
    import Shell from "./tabs/Shell.svelte";

    import { handlers } from "./scripts/Connector";
    import { Toaster } from '@skeletonlabs/skeleton-svelte';
    import { toaster } from "./scripts/Toast";

    let tab = "list";
    const tabs = [
        {label: "Server List", "id": "list"},
        {label: "Remote Shell", "id": "shell"},
        
    ]

    // handlers["auth"] = () => {
    //     tab = "shell"
    // }

    handlers["setPage"] = (page: string) => {
        tab = page;
    }
</script>

<div class="flex items-center justify-between h-8 w-full fixed top-0 left-0 bg-surface-900 {tab != tabs[0].id ? 'shadow-md' : ''} duration-150 select-none">
    <img src="{logo}" alt="" class="select-none h-8 p-2 drag-area" draggable="false">
    <div class="grow drag-area h-8"></div>
    <div class="flex">
        <button class="flex items-center justify-center w-8 btn" title="Minimize Window" aria-label="minimize" onclick={() => {
            window.api.windowControls.minimize();
        }}>
            ➖
        </button>
        <button class="flex items-center justify-center w-8 btn" title="Close" aria-label="close" onclick={() => {
            window.api.windowControls.close();
        }}>
            ❌
        </button>
    </div>
</div>

<div class="h-screen w-full pt-8 flex">
    <div class="h-full flex flex-col bg-surface-900 w-56 min-w-56 pl-8 select-none">
        {#each tabs as t, index}
            <div class="w-full {index > 0 && tabs[index-1].id == tab ? 'bg-surface-950' : ''} {index < tabs.length-1 && tabs[index+1].id == tab ? 'bg-surface-950' : ''} ">
                <button
                    class="p-1 px-3 w-full {t.id == tab ? 'bg-surface-950 text-primary-400 hover:text-primary-400/70 rounded-l-lg' : 'hover:text-white/70'}
                    {index > 0 && tabs[index-1].id == tab ? 'bg-surface-900 rounded-tr-lg' : ''}
                    {index < tabs.length-1 && tabs[index+1].id == tab ? 'bg-surface-900 rounded-br-lg' : ''}"
                    onclick={() => { tab = t.id; }}
                >
                    <p class="text-left w-full pr-5 font-medium">{t.label}</p>
                </button>
            </div>
        {/each}
        <div class="flex-grow w-full {tab == tabs[tabs.length-1].id ? 'bg-surface-950' : ''} {tab == tabs[tabs.length-1].id  ? 'bg-surface-950' : ''} ">
            <div class="h-full w-full {tab == tabs[tabs.length-1].id ? 'bg-surface-900 rounded-tr-lg' : ''}"></div>
        </div>
    </div>
    <div class="flex-grow overflow-y-scroll">
        {#if tab == "list"}
            <List />
        {:else if tab == "shell"}
            <Shell />
        {:else}
            <p class="p-3 text-error-500">❗ Tab not found</p>
        {/if}
    </div>
</div>


<Toaster {toaster}></Toaster>