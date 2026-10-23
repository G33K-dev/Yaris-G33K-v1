# YARIS Screensaver for Chrome, Opera, and Firefox

This Manifest V3 extension displays the project's animated Toyota Yaris GIF as
a DVD-style screensaver on the active webpage after a configurable period
without computer input. The default delay is 5 minutes. Any mouse or keyboard
activity resets the timer, and the animation stops when activity resumes.

## Browser support

- **Chrome:** load this folder from `chrome://extensions`.
- **Opera:** load this folder from `opera://extensions`.
- **Firefox:** load the `Firefox` folder from `about:debugging#/runtime/this-firefox`
  using **Load Temporary Add-on** and select its `manifest.json`.

For Chrome and Opera, enable Developer mode and choose **Load unpacked**.
Open the extension's popup to set the idle time from 1 to 1440 minutes.

The extension uses the browser's idle-detection permission and needs webpage
access to display the overlay. It cannot inject into browser-internal pages,
the Chrome Web Store, or pages where site access is disabled. For local files,
enable **Allow access to file URLs** in the extension details.

The Firefox build uses its own Manifest V3 background-script manifest. Firefox
temporary add-ons are removed when Firefox closes; use Firefox Add-ons signing
for a persistent installation.

## Create release downloads

From PowerShell, run `.\package.ps1`. It creates Chrome/Opera and Firefox
packages plus the combined `website\downloads\YARIS-extensions.zip` bundle.
The combined bundle is suitable as a GitHub release asset.
