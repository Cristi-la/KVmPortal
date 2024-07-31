class Terminal {
  static counter = 100;
  static OPTIONS = {
      cursorBlink: true,
      theme: {
          background: 'black',
          foreground: 'white',
          cursor: 'white'
      }
  };

  upScaleContainerZIndex() {
      Terminal.counter = Terminal.counter + 1;
      this.container.style.zIndex = Terminal.counter;
  }

  LOADED = false;

  constructor(sid, manager) {
    this.sid = sid;
    this.manager = manager;
    this.term = new window.Terminal(Terminal.OPTIONS);
    this.fitAddon = new window.FitAddon.FitAddon();
    this.container = this.get_container();
    this.upScaleContainerZIndex();

    if (!this.term || !this.fitAddon) {
      console.error("Terminal or FitAddon not initialized.");
      return;
    }

    this.term.loadAddon(this.fitAddon);
    this.init();
    this.setupEvents();
  }

  get_container(){
    const box = document.getElementById("terminal");
    const newDiv = document.createElement("div");
    newDiv.classList.add("window");
    box.appendChild(newDiv);
    
    return newDiv;
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
    console.log(`Terminal ${this.sid}, Received: ${data}`);
    if (this.term) this.term.write(data);
  }

  loadData(data) {  
    this.LOADED = true; 
    this.receiveData(data)
    this.upScaleContainerZIndex();
   }

  writeData(data) {
    if (!this.LOADED) {
      console.warn(`Terminal ${this.sid} not loaded yet. Received data will be ignored.`);
      return;
    }

    if (!this.manager) return;

    console.log(`Terminal ${this.sid}, Write: ${data}`);
    const message = Message.data(data, this.sid);
    this.manager.sendData(message);
  }

  setupEvents() {
    this.term.onData(data => this.writeData(data));
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
