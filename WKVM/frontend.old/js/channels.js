class Manager {
  constructor(url, sids = null) {
    this.url = url;
    this.socket = null;
    this.terminals = {};
    this.sids = [];

    if (sids && sids.length) this.createTerminals(sids);
  }

  createTerminals(sids) {
    if (!sids.length) return;
    console.log(sids)

    for (const sid of sids) {
      if (sid in this.sids) return 

      this.terminals[sid] = new Terminal(sid, this);
      this.sids.push(sid);
    }
  }

  connect() {
    this.socket = new WebSocket(this.url);

    this.socket.onopen = () => {
      console.log("WebSocket connection opened.");
      if (this.sids && this.sids.length) {
        for (const sid of this.sids) {
          console.log(`Requesting session content for ${sid}`);
          this.sendData(Message.load(sid));
        }
        return;
      }

      this.sendData(Message.session);
    };

    this.socket.onmessage = (event) => this.receiveData(event.data);

    // this.socket.onclose = (event) => {
    //   console.log("WebSocket connection closed:", event);
    //   // displayNotification();
    // };

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

  receiveData(receiveData) {
    const parsedData = JSON.parse(receiveData);
    console.log(`Socket receive: ${receiveData}`);
    const sid = parsedData.sid;
    const action = parsedData.action;
    const data = parsedData.data;
    const vis = parsedData.vis;

    try {
      this.handleAction(action, data, sid, vis);
    } catch (error) {
      console.error("Failed to parse incoming data:", error);
    }
  }

  handleAction(action, data, sid, vis) {
    switch (action) {
      case Message.SEND_DATA:
        if(sid in this.terminals && data) 
          this.terminals[sid].receiveData(data);
        break;

      case Message.SEND_LOAD:
        this.terminals[sid].loadData(data, vis);
        break;

      case Message.SEND_SESSIONS:
        this.createTerminals(data);
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
