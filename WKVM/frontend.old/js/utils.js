class Message {
  static SEND_DATA = "sd";          // client, server

  static SEND_SESSIONS = "ss";      // server
  // static SEND_RESIZE = "sr";
  // static SEND_CLOSE = "sc";
  static SEND_LOAD = "sl";          // server

  // static GET_DATA = "gd";
  static GET_SESSIONS = "gs";       // client
  // static GET_RESIZE = "gr";
  // static GET_CLOSE = "gc";
  static GET_LOAD = "gl";           // client

  constructor(data, sid, action) {
    this.data = data;
    this.sid = sid;
    this.action = action;
  }

  toJSON() {
    return JSON.stringify({
      data: this.data,
      sid: this.sid,
      action: this.action,
    })
  }

  static create(data, sid, action) {
    const msg = new Message(data, sid, action);

    return msg.toJSON();
  }

  static data(...args) {
    return Message.create(args[0], args[1], Message.SEND_DATA);
  }
  static session = Message.create(
    "get_all_sessions",
    null,
    Message.GET_SESSIONS
  );

  // static resize(data, sid) {
  //   return Message.create(data, sid, Message.SEND_RESIZE);
  // }
  // static close(sid) {
  //   return Message.create("close_session", sid, Message.SEND_CLOSE);
  // }
  static load(sids) {
    return Message.create("get_session_content", sids, Message.GET_LOAD);
  }
}

function displayNotification(msg) {
  alert(msg);
}



function getSessionIDsFromURL(url) {
  const urlObj = new URL(url);
  const params = new URLSearchParams(urlObj.search);
  const sessions = params.get('sessions');

  // Check if 'sessions' parameter exists and split it into an array if it does
  if (sessions) {
      return sessions.split(',');
  }

  // Always return an array, even if no sessions are found
  return [];
}