// content.js

// ========================
// 1. ĐẾM THỜI GIAN TRÊN TRANG
// ========================

let startTime = Date.now();
let timerInterval = null;

function formatTime(ms) {
  const totalSeconds = Math.floor(ms / 1000);
  const h = String(Math.floor(totalSeconds / 3600)).padStart(2, "0");
  const m = String(Math.floor((totalSeconds % 3600) / 60)).padStart(2, "0");
  const s = String(totalSeconds % 60).padStart(2, "0");
  return `${h}:${m}:${s}`;
}

function createTimerOverlay() {
  if (document.getElementById("__time_on_page_overlay")) return;

  const box = document.createElement("div");
  box.id = "__time_on_page_overlay";

  Object.assign(box.style, {
    position: "fixed",
    bottom: "10px",
    left: "10px",
    padding: "6px 25px 6px 10px", // Tăng padding-right để chừa chỗ cho nút x
    background: "rgba(0,0,0,0.5)",
    color: "#52ff66ff",
    fontSize: "24px",
    fontFamily: "sans-serif",
    borderRadius: "6px",
    zIndex: 999999,
    pointerEvents: "none",
  });

  const timeText = document.createElement("span");
  timeText.textContent = "00:00:00";
  box.appendChild(timeText);

  const closeBtn = document.createElement("div");
  closeBtn.textContent = "×";
  Object.assign(closeBtn.style, {
    position: "absolute",
    top: "0",
    right: "0",
    padding: "2px 6px",
    cursor: "pointer",
    color: "#fff",
    fontSize: "16px",
    pointerEvents: "auto", // Cho phép click vào nút
    lineHeight: "1",
  });

  closeBtn.onclick = () => {
    box.remove();
    if (timerInterval) clearInterval(timerInterval);
  };

  box.appendChild(closeBtn);
  document.body.appendChild(box);

  // Cập nhật mỗi giây
  timerInterval = setInterval(() => {
    const now = Date.now();
    const elapsed = now - startTime;
    timeText.textContent = formatTime(elapsed);
  }, 1000);
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", createTimerOverlay);
} else {
  createTimerOverlay();
}
