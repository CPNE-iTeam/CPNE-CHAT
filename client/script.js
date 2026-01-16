const app = document.querySelector(".app");
const sendBtn = document.getElementById("sendBtn");

let pending = false;

document.addEventListener("mousemove", (e) => {
    if (!pending) {
        pending = true;
        requestAnimationFrame(() => {
            update3D(e);
            pending = false;
        });
    }
});

function update3D(e) {
    const centerX = window.innerWidth / 2;
    const centerY = window.innerHeight / 2;

    const relX = (e.clientX - centerX) / centerX;
    const relY = (e.clientY - centerY) / centerY;

    app.style.transform = `rotateY(${relX * 8}deg) rotateX(${-relY * 8}deg)`;
}


sendBtn.addEventListener("mousemove", (e) => {
    const rect = sendBtn.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    sendBtn.style.setProperty("--btn-light-x", `${x}%`);
    sendBtn.style.setProperty("--btn-light-y", `${y}%`);
});

sendBtn.addEventListener("click", () => {
    sendBtn.classList.remove("sending");
    void sendBtn.offsetWidth; 
    sendBtn.classList.add("sending");
});
