class WebSocketManager {
  constructor(url, terminal = null) {
    this.websocket = new WebSocket(url);
    this.terminal = terminal;
    this.setupWebSocketEvents();
  }

  setupWebSocketEvents() {
    this.websocket.onerror = (e) => {
      if (!this.terminal) return;
      this.terminal.writeMessage("WebSocket connection error\n\r");
      console.error("WebSocket connection error:", e);
      this.terminal.status = "Failing";
    };

    this.websocket.onopen = () => {
      if (!this.terminal) return;
      this.terminal.setWebSocket(this.websocket);
      console.log("WebSocket connection established");
      this.terminal.performResize();
      
    };

    this.websocket.onmessage = (e) => {
      try {
        let data = JSON.parse(e.data);
        console.log("WebSocket message:", data);

        if (!data.message) return;

        console.log("Terminal status:", data.message.status);
        this.terminal.status = data.message.status;

        switch (data.message.type) {
          case "error":
          case "info":
            this.handleTerminalMessage(data.message);
            break;
          case "load_content":
            this.handleLoadContent(data.message);
            break;
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };
  }

  handleTerminalMessage(message) {
    if (!this.terminal) return;
    let content = message.content + (message.type === "error" ? "\n\r" : "");
    this.terminal.writeMessage(content);
  }

  handleLoadContent(message) {
    if (!message || !message.content) return;

    this.terminal.writeMessage(message.content);
  }
}
