class WebSocketManager {
    constructor(url, terminal = null, editor = null) {
        this.websocket = new WebSocket(url);
        this.terminal = terminal;
        this.setupWebSocketEvents();
    }

    setupWebSocketEvents() {
        this.websocket.onerror = (e) => {
            if (!this.terminal) return;
            this.terminal.writeMessage('WebSocket connection error\n\r');
            console.error('WebSocket connection error:', e);
        };

        this.websocket.onopen = () => {
            if (!this.terminal) return;
            this.terminal.setWebSocket(this.websocket);
            this.terminal.performResize();
            console.log('WebSocket connection established');
        };

        this.websocket.onmessage = (e) => {

            try {
                let data = JSON.parse(e.data);
                if (!data.message) return;

                switch (data.message.type) {
                    case 'error':
                    case 'info':
                        this.handleTerminalMessage(data.message);
                        break;
                    case 'action':
                        this.handleActionMessage(data.message);
                        break;
                }
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };
    }

    handleTerminalMessage(message) {
        if (!this.terminal) return;
        let content = message.content + (message.type === 'error' ? '\n\r' : '');
        this.terminal.writeMessage(content);
    }

    handleActionMessage(message) {
        console.log('Action message:', message.content);


        if (!message || !message.content || !message.content.data) return;

        if (message.content.type === 'load_content') {
            this.terminal.writeMessage(message.content.data)
        }
    }
}
