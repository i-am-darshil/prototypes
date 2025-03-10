async function getWebSocket() {
    try {
        const response = await fetch("/get_ws_server");
        const data =  await response.json()
        const ws_server_url = data.ws_server
        console.log(`get_ws_server response: ${data}`)
        return {socket: new WebSocket(ws_server_url), ws_server_url: ws_server_url}
    } catch (error) {
        console.error(`Failed to connect to websocket server. Error: ${error}`)
    }
}

const socketData = await getWebSocket()

export {socketData}