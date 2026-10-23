const DEFAULT_IDLE_MINUTES = 5;
const form = document.querySelector("#settings-form");
const input = document.querySelector("#idle-minutes");
const status = document.querySelector("#status");

chrome.storage.local.get(
  { idleMinutes: DEFAULT_IDLE_MINUTES },
  (settings) => {
    if (chrome.runtime.lastError) {
      status.textContent = "Could not load your saved setting.";
      return;
    }
    input.value = settings.idleMinutes;
  }
);

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const minutes = Number(input.value);
  if (!Number.isInteger(minutes) || minutes < 1 || minutes > 1440) {
    status.textContent = "Enter a whole number from 1 to 1440.";
    return;
  }

  chrome.storage.local.set({ idleMinutes: minutes }, () => {
    if (chrome.runtime.lastError) {
      status.textContent = "Could not save your setting.";
      return;
    }
    status.textContent = `Saved. YARIS starts after ${minutes} minute${minutes === 1 ? "" : "s"} idle.`;
  });
});
