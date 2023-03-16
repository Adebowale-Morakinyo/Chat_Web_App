async function appendMessage(img, msg, side="left") {
  if (typeof msg.name !== "undefined") {
    var time = formatDate(new Date())

    if (typeof msg.time !== "undefined") {
      var date = msg.time;
    } else {
      var date = time;
    }

  var global_name = await load_name();
  if (global_name == msg.name) {
     side = "right"
    }

  //   Simple solution for small apps
  const msgHTML = `
  <div class="msg ${side}-msg">
    <div class="msg-img" style="background-image: url(${img})"></div>

    <div class="msg-bubble">
      <div class="msg-info">
        <div class="msg-info-name ${side}-name">${msg.name}</div>
        <div class="msg-info-time">${date}</div>
      </div>

      <div class="msg-text">${msg.message}</div>
    </div>
  </div>
`;

  var msgerChat = document.getElementById("messages");

  msgerChat.insertAdjacentHTML("beforeend", msgHTML);
  msgerChat.scrollTop += 500;
  }
}

async function load_name() {
  return await fetch("/get_name")
    .then(async function (response) {
      return await response.json();
    })
    .then(function (text) {
      return text["name"];
    });
}

async function load_messages() {
  return await fetch("/get_messages")
    .then(async function (response) {
      return await response.json();
    })
    .then(function (text) {
      console.log(text);
      return text;
    });
}

// Utils
function get(selector, root = document) {
  return root.querySelector(selector);
}

function formatDate(date) {
  const h = "0" + date.getHours();
  const m = "0" + date.getMinutes();

  return `${h.slice(-2)}:${m.slice(-2)}`;
}

var socket = io.connect("http://127.0.0.1:5000");
var PERSON_IMG = "https://cdn-icons-png.flaticon.com/512/4575/4575970.png";

socket.on("connect", async function () {
  var usr_name = await load_name();
  if (usr_name != "") {
    socket.emit("event", {
      message: usr_name + " just connected to the server!",
      name: usr_name,
      date: formatDate(new Date()),
      connect: true,
    });
  }
  var form = $("form#msgForm").on("submit", async function (e) {
    e.preventDefault();

    // get input from message box
    let msg_input = document.getElementById("msg");
    let user_input = msg_input.value;
    let user_name = await load_name();

    // add date
    let date = formatDate(new Date())

    // clear msg box value
    msg_input.value = "";

    // send message to other users
    socket.emit("event", {
      message: user_input,
      name: user_name,
      date: date
    });
  });
});
socket.on("disconnect", async function (msg) {
  var usr_name = await load_name();
  socket.emit("event", {
    message: usr_name + " just left the server...",
    name: usr_name,
    date: formatDate(new Date())
  });
  socket.disconnect();
});
socket.on("message response", function (msg) {
  appendMessage(PERSON_IMG, msg);
});

window.onload = async function () {
  var msgs = await load_messages();
  for (i = 0; i < msgs.length; i++) {
    appendMessage(PERSON_IMG, msgs[i]);
  }

  let name = await load_name();
  if (name != "") {
    $("#login").hide();
  } else {
    $("#logout").hide();
  }
};

