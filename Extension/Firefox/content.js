(() => {
  let animationFrame;
  let overlay;
  let car;
  let lastFrameTime;
  let x = 0;
  let y = 0;
  let dx = 240;
  let dy = 180;

  function stopScreensaver() {
    if (animationFrame) {
      cancelAnimationFrame(animationFrame);
      animationFrame = undefined;
    }
    overlay?.remove();
    overlay = undefined;
    car = undefined;
    lastFrameTime = undefined;
  }

  function animate(timestamp) {
    if (!car || !overlay) {
      return;
    }

    const elapsed = lastFrameTime
      ? Math.min((timestamp - lastFrameTime) / 1000, 0.05)
      : 0;
    lastFrameTime = timestamp;

    const maxX = Math.max(0, window.innerWidth - car.offsetWidth);
    const maxY = Math.max(0, window.innerHeight - car.offsetHeight);
    x += dx * elapsed;
    y += dy * elapsed;

    if (x <= 0 || x >= maxX) {
      x = Math.min(Math.max(x, 0), maxX);
      dx *= -1;
    }
    if (y <= 0 || y >= maxY) {
      y = Math.min(Math.max(y, 0), maxY);
      dy *= -1;
    }

    car.style.transform = `translate(${x}px, ${y}px)`;
    animationFrame = requestAnimationFrame(animate);
  }

  function startScreensaver() {
    if (overlay || !document.documentElement) {
      return;
    }

    overlay = document.createElement("div");
    overlay.setAttribute("aria-hidden", "true");
    Object.assign(overlay.style, {
      position: "fixed",
      inset: "0",
      zIndex: "2147483647",
      overflow: "hidden",
      pointerEvents: "none"
    });

    car = document.createElement("img");
    car.src = chrome.runtime.getURL("yaris.gif");
    car.alt = "";
    Object.assign(car.style, {
      position: "absolute",
      left: "0",
      top: "0",
      width: "180px",
      height: "auto",
      maxWidth: "40vw",
      maxHeight: "40vh",
      objectFit: "contain",
      willChange: "transform"
    });

    overlay.append(car);
    document.documentElement.append(overlay);
    x = Math.max(0, (window.innerWidth - car.offsetWidth) / 2);
    y = Math.max(0, (window.innerHeight - car.offsetHeight) / 2);
    animationFrame = requestAnimationFrame(animate);
  }

  chrome.runtime.onMessage.addListener((message) => {
    if (message.type === "yaris:start") {
      startScreensaver();
    } else if (message.type === "yaris:stop") {
      stopScreensaver();
    }
  });

  window.addEventListener("resize", () => {
    if (!car) {
      return;
    }
    x = Math.min(x, Math.max(0, window.innerWidth - car.offsetWidth));
    y = Math.min(y, Math.max(0, window.innerHeight - car.offsetHeight));
  });

  chrome.runtime.sendMessage({ type: "yaris:ready" });
})();
