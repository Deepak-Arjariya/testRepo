<!DOCTYPE html>
<html>
  <head>
    <title>Chat</title>
  </head>
  <body>
    <ul id="messages"></ul>
    <input id="m" autocomplete="off" /><button>Send</button>
    <script src="/socket.io/socket.io.js"></script>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
      const socket = io();

      // Send chat messages
      $('form').submit(function () {
        socket.emit('chat message', $('#m').val());
        $('#m').val('');
        return false;
      });

      // Receive and display chat messages
      socket.on('chat message', function (msg) {
        $('#messages').append($('<li>').text(msg));
      });
    </script>
  </body>
</html>
