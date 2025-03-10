import { socketData } from "./socketClient.js"
console.log(`From index.js, data: ${JSON.stringify(socketData)}`)

const socket = socketData.socket
const ws_server_url = socketData.ws_server_url

socket.onopen = function() {
    document.getElementById("wsStatus").textContent = `Connected to ${ws_server_url}`;
};

socket.onmessage = (event) => {
    console.log("Message from server:", event.data);
    const msgList = document.getElementById("messages");

    const message = JSON.parse(event.data)
    const body = message.body
    const created_at = message.created_at
    const sender_user_name = message.sender_user_name
    const channel_name = message.channel_name
    const msgItem = document.createElement("h4");
    const labelItem = document.createElement("p");
    const endItem = document.createElement("p");


    labelItem.textContent = `${channel_name}, ${created_at}`
    msgItem.textContent = `'${sender_user_name}' :  ${body}`;
    endItem.textContent = "================================="
    msgList.appendChild(labelItem);
    msgList.appendChild(msgItem);
    msgList.appendChild(endItem);
};

socket.onclose = function() {
    document.getElementById("wsStatus").textContent = "Disconnected";
}

document.getElementById("userNameButton").onclick = async() => {
    await createUser()
}

document.getElementById("channelButton").onclick = async() => {
    await createChannel()
}

document.getElementById("membershipButton").onclick = async() => {
    await createMembership()
}

document.getElementById("userMembershipButton").onclick = async() => {
    await getMembershipForUser()
}

document.getElementById("messageButton").onclick = async() => {
    await sendMessage()
}

async function createUser() {
    const userName = document.getElementById("userNameInput").value;

    const response = await fetch(`/users/${userName}`, {
        method: "POST",
    });

    const data = await response.json()
    console.log(`createUser data: ${JSON.stringify(data)}`)
    const register_msg = {user_name: data.user_name, type: "register"}
    socket.send(JSON.stringify(register_msg))
    const userEl = document.getElementById("user");
    const userInfo = document.createElement("p");
    userInfo.textContent = `Welcome ${data.user_name}`;
    userEl.appendChild(userInfo)
}

async function createChannel() {
    const channelName = document.getElementById("channelInput").value;

    const response = await fetch(`/channels/${channelName}`, {
        method: "POST",
    });

    const data = await response.json()
    console.log(`createChannel data: ${JSON.stringify(data)}`)
    const channelEl = document.getElementById("channel");
    const channelInfo = document.createElement("p");
    channelInfo.textContent = `${new Date().toLocaleString()}: ${JSON.stringify(data)}`;
    channelEl.appendChild(channelInfo)
}

async function createMembership() {
    const userName = document.getElementById("membershipUsernameInput").value;
    const channelName = document.getElementById("membershipChannelInput").value;

    const response = await fetch(`/membership`, {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"user_name": userName, "channel_name": channelName})
    });

    const data = await response.json()
    console.log(`createMembaership data: ${JSON.stringify(data)}`)
    const membershipEl = document.getElementById("membership");
    const membershipInfo = document.createElement("p");
    membershipInfo.textContent = `${new Date().toLocaleString()}: ${JSON.stringify(data)}`;
    membershipEl.appendChild(membershipInfo)
}

async function getMembershipForUser() {
    const userName = document.getElementById("userMembershipInput").value;

    const response = await fetch(`/membership?user_name=${userName}`);

    const data = await response.json()
    console.log(`getMembershipForUser data: ${JSON.stringify(data)}`)
    const userMembershipEl = document.getElementById("userMembership");
    const channels = data.channels

    for (let channelInfo of channels) {
        let channelName = channelInfo["channel_name"]
        let userName = channelInfo["user_name"]

        let channelId = `${userName} - ${channelName}`

        let channelNameEl = document.getElementById(channelId)
        if (channelNameEl) {
            channelNameEl.remove()
        }

        channelNameEl = document.createElement("div");
        channelNameEl.setAttribute("id", channelId);

        const channelP = document.createElement("h3");
        channelP.textContent = channelId;
        channelNameEl.appendChild(channelP)

        userMembershipEl.appendChild(channelNameEl)
    }
}

async function sendMessage() {
    const userName = document.getElementById("messageUsernameInput").value;
    const channelName = document.getElementById("messageChannelInput").value;
    const messageBody = document.getElementById("messageInput").value;

    const response = await fetch(`/message`, {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({"sender_user_name": userName, "channel_name": channelName, "body": messageBody})
    });

    const data = await response.json()
    console.log(`sendMessage data: ${JSON.stringify(data)}`)
    // const membershipEl = document.getElementById("message");
    // const membershipInfo = document.createElement("p");
    // membershipInfo.textContent = `${new Date().toLocaleString()}: ${JSON.stringify(data)}`;
    // membershipEl.appendChild(membershipInfo)
}