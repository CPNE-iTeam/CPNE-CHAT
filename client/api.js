const messagesBox = document.getElementById("messagesBox");
const template = document.getElementById("msgTemplate");

async function LoadMessages() {
    try {
        const res = await fetch("http://cmb101-02/messages");
        const data = await res.json();

        if (data.status === "success") {
            messagesBox.innerHTML = "";
            
            data.messages.forEach(msg => {
                AddMessageToDOM(msg);
            });
        } else {
            console.log("Erreur requête");
        }
    } catch (error) {
        console.log("Erreur serveur :", error);
    }
}

function AddMessageToDOM(msg) {
    const clone = template.content.cloneNode(true);

    clone.querySelector(".user").textContent = msg.author;
    clone.querySelector(".tag").textContent = `#${msg.authorNameTag}:`;
    clone.querySelector(".msgTxt").textContent = msg.content;

    messagesBox.appendChild(clone);
}

LoadMessages();
setInterval(LoadMessages, 1500);

async function CreateMessages(content, author) {
    try {
        const res = await fetch("http://cmb101-02/new_message", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ content, author })
        });

        const data = await res.json();

        if (data.status === "success") {
            LoadMessages();
            messagesBox.scrollTop = messagesBox.scrollHeight;
        } else {
            console.log("Erreur requête");
        }
    } catch (error) {
        console.log("Erreur serveur :", error);
    }
}


function SendMessage() {
    const author = document.getElementById("username").value.trim();
    const content = document.getElementById("message").value.trim();

    if (author !== "" && content !== "") {
        document.getElementById("message").value = "";
        CreateMessages(content, author);
    }
}

sendBtn.addEventListener("click", SendMessage);

const messageInput = document.getElementById("message");

messageInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        SendMessage();
    }
});