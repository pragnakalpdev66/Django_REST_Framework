document.addEventListener("DOMContentLoaded", () => {
  // Animataion
  const circles = document.querySelectorAll(".progress-circle");
  circles.forEach(circle => {
    let c = circle.querySelector(".progress-value")?.textContent || "0";
    c = String(c).trim().replace("%", "");
    // percent = Number(c)
    const percent = Math.max(0, Math.min(100, Number(c)));

    const progress = circle.querySelector(".progress");
    const radius = 45;
    const stroke = 2 * Math.PI * radius;

    // delay
    setTimeout(() => {
      const offset = stroke - (percent / 100) * stroke;
      progress.style.strokeDashoffset = offset;
    }, 250);
    

  });
});

document.getElementById('theme-toggle')?.addEventListener('click', () => {
  document.body.classList.toggle('dark');
});