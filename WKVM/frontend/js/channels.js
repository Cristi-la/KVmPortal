class Manager {
  constructor(url, sids = null) {
    this.url = url;
    this.socket = null;
    this.terminals = {};
    this.sids = sids;
  }

  createTerminals() {
    if (!this.sids.length) return;

    for (const sid of this.sids) {
      if (!(sid in this.terminals)) {
        this.terminals[sid] = new Terminal(sid, this);
      }
    }
  }

  connect() {
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log("WebSocket connection opened.");
      if (this.sids) {
        this.sendData(Message.load(this.sids));
        return;
      }

      // this.sendData(Message.session);
    };

    this.socket.onmessage = (event) => {
      console.log("WebSocket message received:", event.data);
      this.receiveData(event.data);
    };

    this.socket.onclose = (event) => {
      console.log("WebSocket connection closed:", event);
      // displayNotification();
    };

    // this.socket.onerror = (error) => {
    //   console.error("WebSocket error:", error);
    //   displayNotification();
    // };
  }

  sendData(data) {
    if (!this.socket || this.socket.readyState !== WebSocket.OPEN) {
      console.error("WebSocket is not open. Unable to send data:", data);
      return;
    }

    console.log(`Socket send: ${data}`);
    this.socket.send(data);
  }

  receiveData(data) {
    try {
      const parsedData = JSON.parse(data);
      console.log(`Socket receive: ${data}`);
      const { sid, data, action } = parsedData;

      if (
        action === Message.GET_DATA &&
        action === Message.GET_LOAD &&
        sid in this.terminals
      ) {
        this.terminals[sid].receiveData(data);
        return;
      }

      handleAction(action, data, sid);
    } catch (error) {
      console.error("Failed to parse incoming data:", error);
    }
  }

  handleAction(action, data, sid) {
    switch (action) {
      case Message.GET_RESIZE:
        break;

      case Message.GET_CLOSE:
        break;

      case Message.GET_SESSIONS:
        this.sids = data;
        createTerminals();
        break;

      default:
        console.error(`Unknow action: ${action}, data: ${data}, sid: ${sid}`);
        break;
    }
  }

  close() {
    if (this.socket) {
      this.socket.close();
    }
  }
}
