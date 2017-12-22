var socket = io.connect('http://127.0.0.1:5000');

socket.on('connect', function() {
    socket.send('I am now connected!');

    // socket.emit('custom event', 'my string')
    // the JS object will be converted to JSON data
    socket.emit('custom event', {'name': 'Paul'});

    socket.on('from flask', function(msg) {
        alert(msg['extension']);
    });

    socket.on('message', function(msg) {
        alert(msg);
    });
});