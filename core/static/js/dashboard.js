fetch("/dashboard/activity/")
  .then((res) => res.json())
  .then((data) => {
    const container = document.getElementById("heatmap");
    if (!container) return;

    const today = new Date();
    const weeks = 12;
    const days = weeks * 7;
    let html = '<div style="display:flex;gap:3px;flex-wrap:wrap;">';

    for (let i = days - 1; i >= 0; i--) {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      const key = d.toISOString().split("T")[0];
      const count = data[key] || 0;

      let color = "#F4F4F2";
      if (count === 1) color = "#5B88A5";
      if (count === 2) color = "#406183";
      if (count >= 3) color = "#243A69";

      html += `<div title="${key}: ${count} session(s)"
                          style="width:12px;height:12px;border-radius:2px;background:${color}"></div>`;
    }

    html += "</div>";
    html +=
      '<div class="mt-1"><small class="text-muted">less</small>' +
      ' <span style="display:inline-block;width:10px;height:10px;background:#F4F4F2;border-radius:2px"></span>' +
      ' <span style="display:inline-block;width:10px;height:10px;background:#5B88A5;border-radius:2px"></span>' +
      ' <span style="display:inline-block;width:10px;height:10px;background:#406183;border-radius:2px"></span>' +
      ' <span style="display:inline-block;width:10px;height:10px;background:#243A69;border-radius:2px"></span>' +
      ' <small class="text-muted">more</small></div>';

    container.innerHTML = html;
  });