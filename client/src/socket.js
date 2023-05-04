import io from 'socket.io-client'

const socket = io("http://127.0.0.1:3001/", {
      transportOptions: {
        polling: {
          extraHeaders: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,OPTIONS",
            "Access-Control-Allow-Headers":
            "Content-Type, Authorization, Content-Length, X-Requested-With",
          },
        },
      },
    });
    
function emitAsync(event, ...args) {
  return new Promise((resolve, reject) => {
    socket.emit(event, ...args, (response) => {
      if (response.error) {
        reject(response.error);
      } else {
        resolve(response.data);
      }
    });
  });
}

export default socket
