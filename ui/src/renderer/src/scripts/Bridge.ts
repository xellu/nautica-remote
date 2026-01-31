// import { writable, type Writable } from "svelte/store";
import { RemoteConfig } from "./Config";

import { writable, type Writable } from "svelte/store";

let ws: WebSocket;

const stateStore: Writable<"idle" | "connecting" | "connected" | "disconnected"> = writable("idle");
const wsTrafficStore: Writable<{in: string[], out: string[]}> = writable({in: [], out: []});
const errorHandlers: Function[] = [];

const handlers: {[key: string]: (data: any) => void} = {
    error: (packet: any) => { //handles errors
        errorHandlers.forEach((fn) => fn(packet.content));
    },
}

const onError = (fn: Function) => {
    errorHandlers.push(fn);
}

const onPacket = (data: any) => {
    // console.log(data)
    wsTrafficStore.update((value) => { //push to incoming traffic
        value.in.push(JSON.stringify(data));
        return value;
    });

    if (handlers[data.id]) {
        handlers[data.id](data);
    } else {
        console.error("Unhandled message", data.id);
    }
}

const send = (data: any) => {
    data = JSON.stringify(data);
    
    ws.send(data);
    wsTrafficStore.update((value) => { //push to outcoming traffic
        value.out.push(data);
        return value;
    });
}

const connect = () => {
    stateStore.set("connecting");
    ws = new WebSocket(`ws://${RemoteConfig.ip}:${RemoteConfig.port.ws}/nautica-remote`);
    
    ws.onopen = () => {
        stateStore.set("connected");

        send({id: "nr.list"})
    }

    ws.onmessage = (event) => {
        onPacket(JSON.parse(event.data));
    }

    ws.onclose = () => {
        wsTrafficStore.set({in: [], out: []});
        stateStore.set("disconnected");

        setTimeout(() => connect(), 1000)
    }

    ws.onerror = (error) => {
        console.error(error);
    }
}

const disconnect = () => {
    ws.close();
}

export {
    connect,
    disconnect,
    send,
    
    onError,

    handlers,
    stateStore,
    wsTrafficStore,   
}