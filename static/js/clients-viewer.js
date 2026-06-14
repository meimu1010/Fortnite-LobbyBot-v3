console.log('Connecting to WebSocket');
const socket = new WebSocket(getWsAddr());

socket.addEventListener('open', handleWebSocketOpen);

socket.addEventListener('message', handleWebSocketMessage);

function handleWebSocketOpen(event) {
    console.log('Successfully connected to WebSocket');
}

function handleWebSocketMessage(event) {
    const data = JSON.parse(event.data);
    updateContent(data);
}

function updateContent(data) {
    const content = document.getElementById('content');
    content.innerHTML = '';

    data.forEach(client => {
        const link = createClientLink(client);
        content.appendChild(link);
    });
}

function createClientLink(client) {
    const link = document.createElement('a');
    link.href = `${location.pathname}/${client.num}`;
    
    const nameText = document.createTextNode(client.name);
    link.appendChild(nameText);
    
    return link;
}