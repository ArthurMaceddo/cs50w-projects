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

      let color = "#ebedf0";
      if (count === 1) color = "#9be9a8";
      if (count === 2) color = "#40c463";
      if (count >= 3) color = "#216e39";

      html += `<div title="${key}: ${count} session(s)"
                          style="width:12px;height:12px;border-radius:2px;background:${color}"></div>`;
    }

    html += "</div>";
    html +=
      '<div class="mt-1"><small class="text-muted">menos</small>' +
      ' <span style="display:inline-block;width:10px;height:10px;background:#ebedf0;border-radius:2px"></span>' +
      ' <span style="display:inline-block;width:10px;height:10px;background:#9be9a8;border-radius:2px"></span>' +
      ' <span style="display:inline-block;width:10px;height:10px;background:#40c463;border-radius:2px"></span>' +
      ' <span style="display:inline-block;width:10px;height:10px;background:#216e39;border-radius:2px"></span>' +
      ' <small class="text-muted">mais</small></div>';

    container.innerHTML = html;
  });
