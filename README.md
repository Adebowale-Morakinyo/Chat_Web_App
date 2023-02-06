# Chat_Web_App

### For development use, not production (simplifying development workflow)
This code is a simple chat application that uses Flask, Flask-SocketIO, and Flask-CORS on the server side, and JavaScript, HTML, and CSS on the client side. The server side is responsible for handling the communication between clients, by using the WebSocket protocol provided by SocketIO. The clients use the browser's WebSocket API to communicate with the server.

On the server side, a Flask app is created and a blueprint is registered for handling views. CORS is also set up to allow for cross-origin resource sharing. A SocketIO instance is then created, with the app and a wildcard origin. The server has one event handler that listens for a 'event' event, and when it receives one, it appends the message to a database and then emits the same message to all clients connected to the server.

On the client side, the code uses JavaScript to create an asynchronous function that appends a message to the chat window. The function takes in an image, a message, and a side argument, which can be left or right. The function also uses the fetch API to load the user's name and previous messages from the server. The code also includes several utility functions for formatting dates and getting elements from the DOM.

Finally, the client side code creates a WebSocket connection to the server using the socket.io library, and sets up event listeners for the 'connect' and 'disconnect' events, which are emitted by the server when a client connects or disconnects from the server. When the user submits a message, the message is sent to the server via the WebSocket connection.
## Setup

Ensure you have python 3.8+ installed.

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
python server.py
```

Flask_cors used because of Werkzeug limitation issues.

## Screenshot
| | | |
|:-------------------------:|:-------------------------:|:-------------------------:|
|<img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Home%20Page.PNG">  Home Page|  <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Login%20Page%202.PNG" > Login Page|<img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Chatting%201.PNG"> Chatting(1)|
|<img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Chatting%202.PNG"> Chatting(2)|  <img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Chatting%203.PNG"> Chatting(3)|<img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Chatting%204.PNG"> Chatting(4)|
|<img width="1604" src="https://github.com/Adebowale-Morakinyo/Chat_Web_App/blob/main/Screenshot/Logging%20out.PNG"> Logging Out|

## Reference
[UI Chat Idea](https://codepen.io/sajadhsm/pen/odaBdd), [Chat Avatar image](https://www.flaticon.com/free-icon/chat_4575970?term=avatar+chat&page=1&position=13&origin=search&related_id=4575970)