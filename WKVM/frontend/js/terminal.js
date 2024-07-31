class Terminal {
  constructor(sid, manager) {
    this.sid = sid;
    this.manager = manager;
    this.term = new window.Terminal(termOptions);
    this.fitAddon = new window.FitAddon.FitAddon();
    this.container = document.getElementById("terminal");

    if (!this.term || !this.fitAddon) {
      console.error("Terminal or FitAddon not initialized.");
      return;
    }

    this.term.loadAddon(this.fitAddon);
    this.init();
  }

  init() {
    if (!this.term || !this.container) {
      console.warn("Document body used as terminal frame.");
      return;
    }

    this.term.open(this.container);
    this.container.querySelector(".terminal").classList.toggle("fullscreen");
    this.fitAddon.fit();
    this.term.focus();
    // this._resize_setup();
  }

  receiveData(data) {
    console.log(`Terminal ${self.sid}, Received: ${data}`);
    if (this.term) this.term.write(data);
  }

  writeData(data) {
    if (!this.manager) return;

    console.log(`Terminal ${self.sid}, Write: ${data}`);
    const message = Message.data(data, this.sid);
    this.manager.sendData(message);
  }

  //   _resize_setup() {
  //     let resizeTimer;
  //     const resizeFunction = () => {
  //       clearTimeout(resizeTimer);
  //       resizeTimer = setTimeout(() => {
  //         if (this.term && this.fitAddon) {
  //           this.performResize();
  //         }
  //       }, 300);
  //     };

  //     window.addEventListener('resize', resizeFunction);
  //     window.addEventListener('beforeunload', resizeFunction);
  //   }

  // writeMessage(data_json) {
  //   const data = data_json.data;
  //   console.debug("Recive data: ", data);

  //   if (this.term) this.term.write(data);
  // }

  //   performResize() {
  //     if (!this.term || !this.fitAddon || !this.socket || this.stop_working.includes(this.status)) return;
  //     this._delTermSize();

  //     this.fitAddon.fit();

  //     const NewCols = this.term.cols;
  //     const NewRows = this.term.rows;
  //     this.sendData(
  //       JSON.stringify({
  //         action: "resize",
  //         type: "new",
  //         data: { cols: NewCols, rows: NewRows },
  //       })
  //     );
  //     console.log("Resize performed");
  //   }

  //   _delTermSize() {
  //     if (!this.term || !this.fitAddon || !this.socket) return;
  //     const Cols = this.term.cols;
  //     const Rows = this.term.rows;
  //     this.sendData(
  //       JSON.stringify({
  //         action: "resize",
  //         type: "del",
  //         data: { cols: Cols, rows: Rows },
  //       })
  //     );
  //   }
}
