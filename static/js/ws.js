function getWsAddr() {
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    return `${protocol}${window.location.host}${window.location.pathname}/ws`;
}