class TerminalManager {
    constructor() {
        this.term = null
        // this.fitAddon = null
        // this.termContentLoadedFromDb = false
        // this.socket = null
    }

    init() {
        let termOptions = {
            cursorBlink: true,
            theme: {
                background: 'black',
                foreground: 'white',
                cursor: 'white'
            }
        };

        let term = new window.Terminal(termOptions)

        this.fitAddon = new window.FitAddon.FitAddon()
        term.loadAddon(this.fitAddon)

        this.term = term;
    }

    createQui(container){
        if (!this.term || !container) {
            console.warn('Document body used as terminal frame.')
            container = document.body
        }

        this.term.open(container);
        document.querySelector('#terminal .terminal').classList.toggle('fullscreen');
        this.fitAddon.fit();
        this.term.focus()
        this.setupResizeListener();
        
    }

    _reside_setup(){
        xterm.onResize(function (evt) {
        const terminal_size = {
            Width: evt.cols,
            Height: evt.rows,
        };
        // websocket.send("\x04" + JSON.stringify(terminal_size));
        });

        const xterm_resize_ob = new ResizeObserver(function (entries) {
            try {
              fitAddon && fitAddon.fit();
            } catch (err) {
              console.log(err);
            }
          });

        xterm_resize_ob.observe(document.querySelector("#xterm"));
    }

}


window.addEventListener('load', () => {
    const frame = document.getElementById('terminal')
    const terminal = new TerminalManager()

    terminal.init()
    terminal.createQui(frame)

})

