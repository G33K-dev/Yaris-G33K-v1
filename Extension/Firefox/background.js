const DEFAULT_IDLE_MINUTES = 5;
const MIN_IDLE_SECONDS = 15;

let idleMinutes = DEFAULT_IDLE_MINUTES;
let isIdle = false;
let screensaverTabId;

function sendToTab(tabId, type) {
  chrome.tabs.sendMessage(tabId, { type }, () => {
    if (chrome.runtime.lastError) {
      console.debug(
        `YARIS could not reach tab ${tabId}: ${chrome.runtime.lastError.message}`
      );
    }
  });
}

function stopScreensaver() {
  if (screensaverTabId !== undefined) {
    sendToTab(screensaverTabId, "yaris:stop");
    screensaverTabId = undefined;
  }
}

function applyIdleState() {
  if (!isIdle) {
    stopScreensaver();
    return;
  }

  chrome.tabs.query({ active: true, lastFocusedWindow: true }, (tabs) => {
    if (chrome.runtime.lastError) {
      console.error(
        "YARIS could not find the active tab:",
        chrome.runtime.lastError.message
      );
      return;
    }

    const activeTabId = tabs[0]?.id;
    if (activeTabId === undefined) {
      stopScreensaver();
      return;
    }

    if (screensaverTabId !== undefined && screensaverTabId !== activeTabId) {
      sendToTab(screensaverTabId, "yaris:stop");
    }
    screensaverTabId = activeTabId;
    sendToTab(activeTabId, "yaris:start");
  });
}

function setIdleState(state) {
  isIdle = state === "idle";
  applyIdleState();
}

function refreshIdleState() {
  chrome.idle.queryState(
    Math.max(MIN_IDLE_SECONDS, idleMinutes * 60),
    (state) => {
      if (chrome.runtime.lastError) {
        console.error(
          "YARIS could not check idle state:",
          chrome.runtime.lastError.message
        );
        return;
      }
      setIdleState(state);
    }
  );
}

function configureIdleDetection(minutes) {
  if (!Number.isInteger(minutes) || minutes < 1 || minutes > 1440) {
    console.error("YARIS received an invalid idle time:", minutes);
    return;
  }

  idleMinutes = minutes;
  chrome.idle.setDetectionInterval(
    Math.max(MIN_IDLE_SECONDS, idleMinutes * 60)
  );
  refreshIdleState();
}

function loadSettings() {
  chrome.storage.local.get(
    { idleMinutes: DEFAULT_IDLE_MINUTES },
    (settings) => {
      if (chrome.runtime.lastError) {
        console.error(
          "YARIS could not load settings:",
          chrome.runtime.lastError.message
        );
        configureIdleDetection(DEFAULT_IDLE_MINUTES);
        return;
      }
      configureIdleDetection(Number(settings.idleMinutes));
    }
  );
}

chrome.idle.onStateChanged.addListener(setIdleState);

chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName === "local" && changes.idleMinutes) {
    configureIdleDetection(Number(changes.idleMinutes.newValue));
  }
});

chrome.tabs.onActivated.addListener(refreshIdleState);
chrome.windows.onFocusChanged.addListener(refreshIdleState);

chrome.runtime.onMessage.addListener((message, sender) => {
  if (message.type === "yaris:ready" && sender.tab?.id !== undefined && isIdle) {
    applyIdleState();
  }
});

loadSettings();
