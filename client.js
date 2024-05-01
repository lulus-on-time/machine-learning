const socket = io.connect('http://localhost:5000');
console.log(socket)

socket.on('message', (data)=>{
  console.log(data)
});

socket.on('connect', function(msg) {
  console.log('Connected to the server');
  console.log(msg);
});

socket.on('disconnect', function(msg) {
    console.log('Disconnected from the server');
    console.log(msg);
  });

socket.on('prediction_result', (data)=>{
    console.log(data)
});

socket.on('connect_error', function(error) {
  console.log('Connection failed: ', error);
});