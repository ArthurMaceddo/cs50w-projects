fetch("/dashboard/activity/")
  .then((res) => res.json())
  .then((data) => {
    const container = document.getElementById("heatmap");
    if (!container) return;

    const today = new Date();
    const weeks = 12;
    const days = weeks * 7;

    let html = `<div style="
      display: grid;
      grid-template-rows: repeat(7, 12px);
      grid-template-columns: repeat(${weeks}, 12px);
      grid-auto-flow: column;
      gap: 3px;
    ">`;

    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const key = d.toISOString().split("T")[0];
      const count = data[key] || 0;

      let color = "#D4CDC5";
      if (count === 1) color = "#5B88A5";
      if (count === 2) color = "#406183";
      if (count >= 3) color = "#243A69";

      html += `<div title="${key}: ${count} session(s)"
        style="width:12px;height:12px;border-radius:2px;background:${color}"></div>`;
    }

    html += "</div>";

    html +=
      '<div class="mt-2 d-flex align-items-center gap-1">' +
      '<small class="text-muted me-1">less</small>' +
      '<span style="display:inline-block;width:10px;height:10px;background:#D4CDC5;border-radius:2px"></span>' +
      '<span style="display:inline-block;width:10px;height:10px;background:#5B88A5;border-radius:2px"></span>' +
      '<span style="display:inline-block;width:10px;height:10px;background:#406183;border-radius:2px"></span>' +
      '<span style="display:inline-block;width:10px;height:10px;background:#243A69;border-radius:2px"></span>' +
      '<small class="text-muted ms-1">more</small>' +
      "</div>";

    container.innerHTML = html;
  });
