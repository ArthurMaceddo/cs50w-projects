// ── Setting ────────────────────────────────────
const FOCUS_MINUTES = 25;
const SHORT_BREAK   = 5;
const LONG_BREAK    = 15;
const CYCLES_BEFORE_LONG = 4;

// ── State ──────────────────────────────────────────
let totalSeconds    = FOCUS_MINUTES * 60;
let remainingSeconds = totalSeconds;
let timerInterval   = null;
let isRunning       = false;
let isFocus         = true;   // true = focus, false = pause
let cycleCount      = 1;

// ── DOM Elements ───────────────────────────────────
const display      = document.getElementById("timer-display");
const label        = document.getElementById("timer-label");
const progressBar  = document.getElementById("timer-progress");
const cycleBadge   = document.getElementById("cycle-badge");
const btnStart     = document.getElementById("btn-start");
const btnPause     = document.getElementById("btn-pause");
const btnReset     = document.getElementById("btn-reset");
const subjectSelect = document.getElementById("subject-select");

// ── Utility Functions ─────────────────────────────
function formatTime(seconds) {
    const m = String(Math.floor(seconds / 60)).padStart(2, "0");
    const s = String(seconds % 60).padStart(2, "0");
    return `${m}:${s}`;
}

function updateDisplay() {
    display.textContent = formatTime(remainingSeconds);
    const elapsed = totalSeconds - remainingSeconds;
    progressBar.style.width = ((elapsed / totalSeconds) * 100) + "%";
}

function requestNotificationPermission() {
    if ("Notification" in window && Notification.permission === "default") {
        Notification.requestPermission();
    }
}

function sendNotification(title, body) {
    if ("Notification" in window && Notification.permission === "granted") {
        new Notification(title, { body: body, icon: "📚" });
    }
}

function saveSession(durationMinutes) {
    const subjectId = subjectSelect.value;
    if (!subjectId) return;  //  dont save if no subject is selected

    fetch(SAVE_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN,
        },
        body: JSON.stringify({
            subject_id: subjectId,
            duration_minutes: durationMinutes,
        }),
    })
    .then(res => res.json())
    .then(() => console.log("Saved Session!"))
    .catch(err => console.error("Error trying to save session:", err));
}

function onTimerEnd() {
    clearInterval(timerInterval);
    isRunning = false;
    btnStart.disabled = false;
    btnPause.disabled = true;

    if (isFocus) {
        // Focus Cycle ended — save session
        saveSession(FOCUS_MINUTES);

        const isLongBreak = cycleCount % CYCLES_BEFORE_LONG === 0;
        const breakMinutes = isLongBreak ? LONG_BREAK : SHORT_BREAK;
        const breakLabel   = isLongBreak ? "Long Break ☕" : "Short Break 😌";

        sendNotification("Focus completed! 🎉", `Time to rest. ${breakLabel}`);

        // Configure pause
        isFocus          = false;
        totalSeconds     = breakMinutes * 60;
        remainingSeconds = totalSeconds;
        label.textContent = breakLabel;
        progressBar.classList.replace("bg-success", "bg-info");

    } else {
        // Pause ended — next focus cycle 
        cycleCount++;
        sendNotification("Ended Pause! 🎯", "Time to focus again.");

        isFocus          = true;
        totalSeconds     = FOCUS_MINUTES * 60;
        remainingSeconds = totalSeconds;
        label.textContent = "Focus 🎯";
        cycleBadge.textContent = `Cycle ${cycleCount} / ${CYCLES_BEFORE_LONG}`;
        progressBar.classList.replace("bg-info", "bg-success");
    }

    updateDisplay();
}

// ── Controls ───────────────────────────────────────
btnStart.addEventListener("click", function () {
    if (!subjectSelect.value) {
        alert("Select a subject before starting!");
        return;
    }
    requestNotificationPermission();
    isRunning = true;
    btnStart.disabled = true;
    btnPause.disabled = false;

    timerInterval = setInterval(() => {
        if (remainingSeconds <= 0) {
            onTimerEnd();
            return;
        }
        remainingSeconds--;
        updateDisplay();
    }, 1000);
});

btnPause.addEventListener("click", function () {
    if (isRunning) {
        clearInterval(timerInterval);
        isRunning = false;
        btnStart.disabled = false;
        btnPause.disabled = true;
        label.textContent = "Paused ⏸️";
    }
});

btnReset.addEventListener("click", function () {
    clearInterval(timerInterval);
    isRunning        = false;
    isFocus          = true;
    cycleCount       = 1;
    totalSeconds     = FOCUS_MINUTES * 60;
    remainingSeconds = totalSeconds;
    btnStart.disabled = false;
    btnPause.disabled = true;
    label.textContent = "Focus 🎯";
    cycleBadge.textContent = `Cycle 1 / ${CYCLES_BEFORE_LONG}`;
    progressBar.style.width = "0%";
    progressBar.classList.replace("bg-info", "bg-success");
    updateDisplay();
});

// ── Initialization ───────────────────────────────────
updateDisplay();