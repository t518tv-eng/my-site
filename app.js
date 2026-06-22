const chat = document.getElementById("chat");

const me = "Gemini Gall";

function renderMessage(m) {
  const div = document.createElement("div");

  const isMe = m.author === me;
  div.className = "msg " + (isMe ? "me" : "other");

  let content = "";

  // TEXT
  if (m.type === "text") {
    content = `
      <div class="text">${m.text || ""}</div>
      <div class="meta">${m.dt}</div>
    `;
  }

  // PHOTO
  else if (m.type === "photo" && m.media) {
    content = `
      <img class="photo" src="../telegram/${m.media}" />
      <div class="meta">${m.dt}</div>
    `;
  }

  // VOICE
  else if (m.type === "voice" && m.media) {
    content = `
      <audio controls src="../telegram/${m.media}"></audio>
      <div class="meta">${m.dt}</div>
    `;
  }

  // 🎥 ROUND VIDEO (КРУЖОЧКИ)
  else if (m.type === "round_video" && m.media) {
    content = `
      <div class="round-wrapper">
        
        <video class="round"
          muted
          loop
          playsinline
          src="../telegram/${m.media}">
        </video>

        <!-- play / pause -->
        <button class="round-btn" onclick="
          const v = this.parentElement.querySelector('video');

          if (v.paused) {
            v.play();
            this.innerText = '⏸';
          } else {
            v.pause();
            this.innerText = '▶';
          }
        ">▶</button>

        <!-- sound toggle -->
        <button class="round-sound" onclick="
          const v = this.parentElement.querySelector('video');
          v.muted = !v.muted;
          this.innerText = v.muted ? '🔇' : '🔊';
        ">🔇</button>

        <div class="meta">${m.dt}</div>
      </div>
    `;
  }

  // VIDEO
  else if (m.type === "video" && m.media) {
    content = `
      <video controls src="../telegram/${m.media}"></video>
      <div class="meta">${m.dt}</div>
    `;
  }

  // fallback
  else {
    return;
  }

  div.innerHTML = `<div class="bubble">${content}</div>`;
  chat.appendChild(div);
}

messages.forEach(renderMessage);

chat.scrollTop = chat.scrollHeight;