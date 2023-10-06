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

// Create an object to encapsulate variables
const chatApp = {
  socket: io.connect("http://127.0.0.1:5000"),
  PERSON_IMG: "https://cdn-icons-png.flaticon.com/512/4575/4575970.png",
  initialConnectionHandled: false, // New property to track initial connection
};

chatApp.socket.on("connect", async function () {
  var usr_name = await load_name();
  if (usr_name != "") {
    chatApp.socket.emit("event", {
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
    let date = formatDate(new Date());

    // clear msg box value
    msg_input.value = "";

    // send message to other users
    chatApp.socket.emit("event", {
      message: user_input,
      name: user_name,
      date: date,
    });
  });
});

// Handle the leave button click event
$("#leave-btn").on("click", async function () {
  // Get the username
  var usr_name = await load_name();

  // Emit the "event" to notify that the user left the server
  chatApp.socket.emit("event", {
    message: usr_name + " just left the server...",
    name: usr_name,
    date: formatDate(new Date()),
  });
  console.log("disconnected");
  // Disconnect cleanly
  chatApp.socket.disconnect();

  // Redirect to the home page
  window.location.href = "/";  // Change this to the desired home page URL
});

chatApp.socket.on("message response", function (msg) {
  // Skip the initial connection message when processing other messages
  if (chatApp.initialConnectionHandled && msg.message.includes("just connected to the server!")) {
    return;
  }
  appendMessage(chatApp.PERSON_IMG, msg);
});

window.onload = async function () {
  var msgs = await load_messages();
  for (i = 0; i < msgs.length; i++) {
    // Skip the initial connection message when loading messages
    if (!chatApp.initialConnectionHandled && msgs[i].message.includes("just connected to the server!")) {
      continue;
    }
    appendMessage(chatApp.PERSON_IMG, msgs[i]);
  }

  let name = await load_name();
  if (name != "") {
    $("#login").hide();
  } else {
    $("#logout").hide();
  }
};
