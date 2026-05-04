const express = require("express");
const http = require("http");
const { Server } = require("socket.io");
const makeWASocket = require("@whiskeysockets/baileys").default;
const { useMultiFileAuthState } = require("@whiskeysockets/baileys");
const qrcode = require("qrcode");

const app = express();
const server = http.createServer(app);
const io = new Server(server);

app.use(express.static("public"));

let sock;

async function startBot() {

    const { state, saveCreds } = await useMultiFileAuthState("auth");

    sock = makeWASocket({
        auth: state,
        printQRInTerminal: true
    });

    sock.ev.on("connection.update", async (update) => {
        const { qr, connection } = update;

        if (qr) {
            const qrImage = await qrcode.toDataURL(qr);
            io.emit("qr", qrImage);
        }

        if (connection === "open") {
            io.emit("status", "Connected ✅");
        }

        if (connection === "close") {
            startBot(); // auto reconnect
        }
    });

    sock.ev.on("creds.update", saveCreds);
}

startBot();

// SEND MESSAGE
io.on("connection", (socket) => {
    socket.on("sendMessage", async (data) => {
        try {
            await sock.sendMessage(data.number + "@s.whatsapp.net", {
                text: data.message
            });
        } catch (err) {
            console.log(err);
        }
    });
});

server.listen(3000, () => {
    console.log("Server running...");
});
