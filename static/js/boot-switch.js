const CLOSED_COLOR = '#dc322f';
const START_COLOR = '#43b581';

function clearContent() {
    document.getElementById('content').textContent = '';
}

function createClientElement(client) {
    const div = document.createElement('div');
    div.className = 'client';

    div.appendChild(createElement('div', 'name', client.name));

    const infoDiv = div.appendChild(createElement('div', 'info'));

    const input = createElement('input', '', '', {
        type: 'button',
        value: client.state !== 'closed' ? texts.close : texts.start,
        onclick: function () {
            sendEvent(client.state !== 'closed' ? 'close' : 'start', client.num);
        },
        style: `border-left-color: ${client.state !== 'closed' ? CLOSED_COLOR : START_COLOR}`,
    });

    infoDiv.appendChild(input);
    infoDiv.appendChild(createElement('div', 'state', texts[client.state]));

    return div;
}

function createElement(tag, className, text, attributes) {
    const element = document.createElement(tag);
    if (className) element.className = className;
    if (text) element.appendChild(document.createTextNode(text));
    if (attributes) {
        for (const key in attributes) {
            if (attributes.hasOwnProperty(key)) {
                element[key] = attributes[key];
            }
        }
    }
    return element;
}

function updateContent(data) {
    clearContent();
    data.forEach(client => document.getElementById('content').appendChild(createClientElement(client)));
}

const socket = new WebSocket(getWsAddr());

function restart() {
    const request = new XMLHttpRequest();
    request.open('POST', `${location.pathname}/restart`);
    request.send(null);
}

function sendEvent(event, num) {
    socket.send(JSON.stringify({ event, num }));
}

function handleWebSocketOpen() {
    console.log('Successfully connected to WebSocket');
}

function handleWebSocketMessage(event) {
    const data = JSON.parse(event.data);
    updateContent(data);
}

socket.addEventListener('open', handleWebSocketOpen);
socket.addEventListener('message', handleWebSocketMessage);