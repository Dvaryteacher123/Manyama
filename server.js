const express = require("express");
const http = require("http");
const multer = require("multer");
const path = require("path");
const { Server } = require("socket.io");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static(__dirname));

// 📁 FILE UPLOAD
const storage = multer.diskStorage({
  destination: "./uploads",
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname));
  }
});
const upload = multer({ storage });

app.post("/upload", upload.single("file"), (req, res) => {
  res.json({ url: "/uploads/" + req.file.filename });
});

app.use("/uploads", express.static("uploads"));

let users = {};

// 🤖 BOT
function bot(msg) {
  msg = msg.toLowerCase();
  if (msg.includes("hi")) return "Mambo 😄";
  if (msg.includes("time")) return new Date().toLocaleTimeString();
  return null;
}

io.on("connection", (socket) => {

  socket.on("login", (user) => {
    users[socket.id] = user;
    io.emit("users", Object.values(users));
  });

  socket.on("chat", (data) => {
    io.emit("chat", data);

    let reply = bot(data.text);
    if (reply) {
      io.emit("chat", { user: "Bot", text: reply });
    }
  });

  socket.on("private", ({to, msg}) => {
    for (let id in users) {
      if (users[id] === to) {
        io.to(id).emit("private", msg);
      }
    }
  });

  socket.on("disconnect", () => {
    delete users[socket.id];
    io.emit("users", Object.values(users));
  });
});

server.listen(3000, () => console.log("🔥 Running"));
