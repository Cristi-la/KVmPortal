class Terminal {
  Failing = 'Failing' 
  Work = 'Work'
  Init = 'Init'
  Undefined = 'Undefined'
  Stopped = 'Stopped'
  Abborted = 'Abborted'

  stop_working = Array('Failing', 'Stopped', 'Abborted')

  constructor() {
    this.term = null;
    this.fitAddon = null;
    this.socket = null;
    this.container = null;  
    this.status = null;
  }

  init() {
    let termOptions = {
      cursorBlink: true,
      theme: {
        background: "black",
        foreground: "white",
        cursor: "white",
      },
    };

    this.term = new window.Terminal(termOptions);
    this.fitAddon = new window.FitAddon.FitAddon();

    if (!this.term || !this.fitAddon) {
      console.error("Terminal or FitAddon not initialized.");
      return;
    }

    this.term.loadAddon(this.fitAddon);
  }

  createQui(container) {
    if (!this.term || !container) {
      console.warn("Document body used as terminal frame.");
      return;
    }
    this.container = container
    this.term.open(container);
    this.container.querySelector(".terminal").classList.toggle("fullscreen");
    this.fitAddon.fit();
    this.term.focus();
    // this._resize_setup();
  }

  setWebSocket(socket) {
    this.socket = socket;

    if (!this.term) return;

    this.term.onData((data) => {
      this.sendData(JSON.stringify({ action: "execute", data: data }));
    });

    this.socket.onmessage = (e) => {
        let data = JSON.parse(e.data);
        this.writeMessage(data);
    }
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
  

  sendData(data_json) {
    if (!this.socket) return;

    console.debug("Sending data: ", data_json);
    this.socket.send(data_json);
  }

  writeMessage(data_json) {
    const data = data_json.data;
    console.debug("Recive data: ", data);

    if (this.term) this.term.write(data);
  }

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
