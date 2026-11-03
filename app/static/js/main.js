"use strict";

const menuButton = document.querySelector(".menu-toggle");
const nav = document.querySelector("#main-nav");
function closeMenu() {
  nav.classList.remove("is-open");
  menuButton.setAttribute("aria-expanded", "false");
}
menuButton.addEventListener("click", () => {
  const open = menuButton.getAttribute("aria-expanded") !== "true";
  menuButton.setAttribute("aria-expanded", String(open));
  nav.classList.toggle("is-open", open);
});
nav.addEventListener("click", (event) => {
  if (event.target.closest("a")) closeMenu();
});
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
    closeMenu();
    menuButton.focus();
  }
});
window.matchMedia("(min-width: 761px)").addEventListener("change", closeMenu);

const navLinks = [...nav.querySelectorAll('a[href^="#"]')];
const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (!entry.isIntersecting) continue;
    for (const link of navLinks) {
      const active = link.hash === `#${entry.target.id}`;
      link.classList.toggle("active", active);
      if (active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    }
  }
}, { rootMargin: "-15% 0px -60% 0px", threshold: 0 });
navLinks.forEach((link) => observer.observe(document.querySelector(link.hash)));

const refreshButton = document.querySelector("#refresh-status");
const healthLabel = document.querySelector("#app-health");
const statusMessage = document.querySelector("#status-message");
const fields = ["version", "environment", "commit", "platform"];
async function refreshStatus() {
  refreshButton.disabled = true;
  refreshButton.textContent = "↻ CHECKING…";
  healthLabel.textContent = "CHECKING";
  healthLabel.dataset.state = "checking";
  statusMessage.textContent = "Contacting this application's endpoints…";
  fields.forEach((field) => { document.querySelector(`#app-${field}`).textContent = "—"; });
  const controller = new AbortController();
  const timer = window.setTimeout(() => controller.abort(), 6000);
  try {
    const responses = await Promise.all([
      fetch("/health", { cache: "no-store", signal: controller.signal }),
      fetch("/api/version", { cache: "no-store", signal: controller.signal }),
    ]);
    if (responses.some((response) => !response.ok)) throw new Error("Endpoint unavailable");
    const [health, metadata] = await Promise.all(responses.map((response) => response.json()));
    if (fields.some((field) => typeof metadata[field] !== "string" || !metadata[field].trim())) {
      throw new Error("Invalid metadata");
    }
    fields.forEach((field) => {
      const node = document.querySelector(`#app-${field}`);
      node.textContent = field === "commit" && /^[a-f0-9]{40}$/i.test(metadata[field]) ? metadata[field].slice(0, 12) : metadata[field];
      node.title = metadata[field];
    });
    const healthy = health.status === "healthy";
    healthLabel.textContent = healthy ? "HEALTHY" : "DEGRADED";
    healthLabel.dataset.state = healthy ? "healthy" : "degraded";
    statusMessage.textContent = healthy
      ? `Application responded. Checked at ${new Date().toLocaleTimeString()}.`
      : "The endpoint responded but did not report a healthy application.";
  } catch {
    healthLabel.textContent = "UNAVAILABLE";
    healthLabel.dataset.state = "unavailable";
    statusMessage.textContent = "Could not verify application health and metadata. Try refreshing.";
    fields.forEach((field) => { const node = document.querySelector(`#app-${field}`); node.textContent = "—"; node.removeAttribute("title"); });
  } finally {
    window.clearTimeout(timer);
    refreshButton.disabled = false;
    refreshButton.textContent = "↻ REFRESH STATUS";
  }
}
refreshButton.addEventListener("click", refreshStatus);
refreshStatus();
