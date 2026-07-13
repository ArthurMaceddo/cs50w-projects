// Conclusion Toggle of topic via fetch
document.querySelectorAll(".topic-toggle").forEach((checkbox) => {
  checkbox.addEventListener("change", function () {
    const id = this.dataset.topicId;
    const url = TOGGLE_URL.replace("{id}", id);

    fetch(url, {
      method: "POST",
      headers: { "X-CSRFToken": CSRF_TOKEN },
    })
      .then((res) => res.json())
      .then((data) => {
        // Update topic visual
        const nameEl = document.querySelector(`#topic-${id} .topic-name`);
        if (data.completed) {
          nameEl.classList.add("text-decoration-line-through", "text-muted");
        } else {
          nameEl.classList.remove("text-decoration-line-through", "text-muted");
        }
        // Update progress bar
        document.getElementById("progress-bar").style.width =
          data.progress + "%";
        document.getElementById("progress-badge").textContent =
          data.progress + "%";
      });
  });
});

document.querySelectorAll(".topic-delete").forEach((btn) => {
  btn.addEventListener("click", function () {
    if (!confirm("Delete this topic?")) return;
    const id = this.dataset.topicId;
    const url = DELETE_URL.replace("{id}", id);

    fetch(url, {
      method: "DELETE",
      headers: { "X-CSRFToken": CSRF_TOKEN },
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.deleted) {
          document.getElementById(`topic-${id}`).remove();
          document.getElementById("progress-bar").style.width =
            data.progress + "%";
          document.getElementById("progress-badge").textContent =
            data.progress + "%";
        }
      });
  });
});
