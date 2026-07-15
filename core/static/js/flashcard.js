let currentIndex = 0;
const total = CARDS.length;

function updateCounter() {
    const remaining = total - currentIndex;
    document.getElementById("counter-text").textContent =
        `${remaining} remaining of ${total}`;

    const pct = (currentIndex / total) * 100;
    document.getElementById("session-progress").style.width = pct + "%";
}

function loadCard(index) {
    if (index >= total) {
        // All cards reviewed — show conclusion screen
        document.getElementById("card-scene").classList.add("d-none");
        document.getElementById("done-screen").classList.remove("d-none");
        document.getElementById("counter-text").textContent = "Completed!";
        return;
    }

    const card = CARDS[index];

    // Reset the flip state before changing the content
    const flipCard = document.getElementById("flip-card");
    flipCard.classList.remove("is-flipped");

    // Wait for the reset animation before changing the text
    setTimeout(() => {
        document.getElementById("card-subject").textContent = card.subject;
        document.getElementById("card-front").textContent   = card.front;
        document.getElementById("card-back").textContent    = card.back;
    }, 280);

    updateCounter();
}

// Button "See Answer" — makes the card flip
document.getElementById("btn-flip").addEventListener("click", function () {
    document.getElementById("flip-card").classList.add("is-flipped");
});

// Click on the card (UX extra)
document.getElementById("flip-card").addEventListener("click", function (e) {
    // Don't trigger if clicked on a button inside the card
    if (e.target.tagName === "BUTTON") return;
    this.classList.toggle("is-flipped");
});

// Rating buttons (Easy / Hard / Forgot)
document.querySelectorAll(".rating-btn").forEach(btn => {
    btn.addEventListener("click", function () {
        const rating = this.dataset.rating;
        const card   = CARDS[currentIndex];
        const url    = SUBMIT_URL.replace("{id}", card.id);

        // Visual feedback immediately — disable buttons while processing
        document.querySelectorAll(".rating-btn").forEach(b => b.disabled = true);

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": CSRF_TOKEN,
            },
            body: JSON.stringify({ rating: rating }),
        })
        .then(res => res.json())
        .then(() => {
            currentIndex++;
            document.querySelectorAll(".rating-btn").forEach(b => b.disabled = false);
            loadCard(currentIndex);
        })
        .catch(err => {
            console.error("Error saving review:", err);
            document.querySelectorAll(".rating-btn").forEach(b => b.disabled = false);
        });
    });
});

// Initial load 
if (total === 0) {
    document.getElementById("counter-text").textContent = "No cards to review today!";
    document.getElementById("card-scene").classList.add("d-none");
    document.getElementById("done-screen").classList.remove("d-none");
} else {
    loadCard(0);
}