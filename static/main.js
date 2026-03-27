document.addEventListener("DOMContentLoaded", () => {

    const socket = io();

    const localVideo = document.getElementById("localVideo");
    const remoteVideo = document.getElementById("remoteVideo");
    const statusText = document.getElementById("status");

    let localStream;
    let peerConnection;
    let room = null;
    let role = null;
    let pendingCandidates = [];
    let remoteDescriptionSet = false;

    const config = {
        iceServers: [
            { urls: "stun:stun.l.google.com:19302" }
        ]
    };

    document.getElementById("joinBtn").onclick = async () => {
        console.log("Button clicked");

        room = document.getElementById("roomInput").value.trim();

        if (!room) {
            alert("Enter a room name");
            return;
        }

        statusText.innerText = "Waiting for another user...";
        await startCall();
    };

    socket.on("role", (data) => {
        role = data.role;
        console.log("My role:", role);
        statusText.innerText = "Role: " + role + " | Waiting for connection...";
    });

    socket.on("ready", async () => {
        if (role !== "caller") return;

        console.log("Creating offer");

        const offer = await peerConnection.createOffer();
        await peerConnection.setLocalDescription(offer);

        socket.emit("signal", { room, offer });
    });

    socket.on("signal", async (data) => {
        console.log("Signal:", data);

        if (data.offer) {
            console.log("Got offer");

            await peerConnection.setRemoteDescription(
                new RTCSessionDescription(data.offer)
            );

            remoteDescriptionSet = true;

            // Flush queued ICE candidates
            pendingCandidates.forEach(c =>
                peerConnection.addIceCandidate(c)
            );
            pendingCandidates = [];

            const answer = await peerConnection.createAnswer();
            await peerConnection.setLocalDescription(answer);

            socket.emit("signal", { room, answer });
        }

        if (data.answer) {
            console.log("Got answer");

            await peerConnection.setRemoteDescription(
                new RTCSessionDescription(data.answer)
            );

            remoteDescriptionSet = true;

            // Flush queued ICE
            pendingCandidates.forEach(c =>
                peerConnection.addIceCandidate(c)
            );
            pendingCandidates = [];
        }

        if (data.candidate) {
            const candidate = new RTCIceCandidate(data.candidate);

            if (remoteDescriptionSet) {
                await peerConnection.addIceCandidate(candidate);
            } else {
                pendingCandidates.push(candidate);
            }
        }
    });

    async function startCall() {
        localStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: true
        });

        localVideo.srcObject = localStream;

        createPeer(); // MUST happen before signaling

        socket.emit("join", { room });
    }

    function createPeer() {
        peerConnection = new RTCPeerConnection(config);

        localStream.getTracks().forEach(track => {
            peerConnection.addTrack(track, localStream);
        });

        peerConnection.ontrack = (event) => {
            console.log("Remote stream received");
            remoteVideo.srcObject = event.streams[0];
        };

        peerConnection.onicecandidate = (event) => {
            if (event.candidate) {
                socket.emit("signal", {
                    room,
                    candidate: event.candidate
                });
            }
        };

        peerConnection.onconnectionstatechange = () => {
            console.log("Connection state:", peerConnection.connectionState);
            statusText.innerText = "Role: " + role + " | " + peerConnection.connectionState;
        };
    }

});