"use strict";

// A shuffled deck shows every subject before repeating. Only artwork IDs are
// saved on this device; nothing is sent to a server or tracked.
(() => {
  const art = document.querySelector(".ghost");
  if (!art) return;
  const gallery = JSON.parse(art.dataset.gallery);
  const key = "portfolio-ascii-deck-v1";
  let state = {};
  try { state = JSON.parse(localStorage.getItem(key)) || {}; } catch { /* Storage may be disabled. */ }
  const ids = gallery.map((item) => item.id);
  let remaining = Array.isArray(state.remaining)
    ? [...new Set(state.remaining)].filter((id) => ids.includes(id) && id !== state.last)
    : [];
  if (!remaining.length) {
    remaining = [...ids];
    for (let i = remaining.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [remaining[i], remaining[j]] = [remaining[j], remaining[i]];
    }
    // Avoid a repeat at the boundary between two shuffled decks, too.
    if (remaining[remaining.length - 1] === state.last) {
      [remaining[0], remaining[remaining.length - 1]] = [remaining[remaining.length - 1], remaining[0]];
    }
  }
  const nextId = remaining.pop();
  const chosen = gallery.find((item) => item.id === nextId);
  art.textContent = chosen.art;
  art.setAttribute("aria-label", `ASCII illustration: ${chosen.name}`);
  document.querySelector("#art-subject").textContent = chosen.name.toUpperCase();
  document.querySelector("#art-render").textContent = `RENDER_${chosen.render_id}`;
  try { localStorage.setItem(key, JSON.stringify({last: chosen.id, remaining})); } catch { /* Still render without storage. */ }
})();
