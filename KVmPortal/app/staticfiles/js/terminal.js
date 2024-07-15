class TerminalManager {
    constructor() {
        this.term = null
        this.fitAddon = null
        this.socket = null
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
        container.querySelector('.terminal').classList.toggle('fullscreen');
        this.fitAddon.fit();
        this.term.focus()
        this._reside_setup();
    }

    setWebSocket(socket) {
        this.socket = socket;

        if (!this.term) return;

        this.term.onData(data => {
            this.sendData(JSON.stringify({'action': 'execute', 'data': data}));
        });     
    }

    
    _reside_setup() {
        let resizeTimer;
        const resizeFunction = () => {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(() => {
                if (this.term && this.fitAddon) {
                    this.performResize();
                }
            }, 300);
        };

        const observer = new MutationObserver(resizeFunction);
        observer.observe(document.body, { attributes: true, childList: true, subtree: true });

        window.addEventListener('beforeunload', () => {
            observer.disconnect();
        });
    }

    sendData(data_json) {
        this.socket.send(data_json);
    }

    writeMessage(message) {
        this.term.write(message)
    }

    performResize() {
        if (!this.term || !this.fitAddon || !this.socket) return;
        this._delTermSize()

        this.fitAddon.fit();

        const NewCols = this.term.cols;
        const NewRows = this.term.rows;
        this.sendData(JSON.stringify({'action': 'resize', 'type': 'new', 'data': {'cols': NewCols, 'rows': NewRows}}));
        console.log('Resize performed')
    }

    _delTermSize() {
        if (!this.term || !this.fitAddon || !this.socket) return;
        const Cols = this.term.cols;
        const Rows = this.term.rows;
        this.sendData(JSON.stringify({'action': 'resize', 'type': 'del', 'data': {'cols': Cols, 'rows': Rows}}));
    }
}



