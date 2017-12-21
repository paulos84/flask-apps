// connects to the flask server running on localhost:5000
var socket = io.connect('http://127.0.0.1:5000');

// socket listens to event, in this case the event listened for is the connect event (client connected to server)
// callback function to send a message
socket.on('connect', function() {
    socket.send('I am now connected!');
});



