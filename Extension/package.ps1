$ErrorActionPreference = "Stop"

$extensionRoot = $PSScriptRoot
$downloads = Join-Path $extensionRoot "..\website\downloads"
$downloads = [System.IO.Path]::GetFullPath($downloads)
$staging = Join-Path ([System.IO.Path]::GetTempPath()) (
  "YARIS-extensions-" + [guid]::NewGuid().ToString("N")
)
$chromiumStage = Join-Path $staging "chrome-opera"
$firefoxStage = Join-Path $staging "firefox"
$bundleStage = Join-Path $staging "bundle"

$chromiumFiles = @(
  "manifest.json",
  "service-worker.js",
  "content.js",
  "popup.html",
  "popup.css",
  "popup.js",
  "yaris.gif",
  "README.md"
)

try {
  New-Item -ItemType Directory -Path $downloads -Force | Out-Null
  New-Item -ItemType Directory -Path $chromiumStage, $firefoxStage, $bundleStage -Force | Out-Null

  foreach ($file in $chromiumFiles) {
    Copy-Item -LiteralPath (Join-Path $extensionRoot $file) -Destination $chromiumStage
  }

  $firefoxFiles = @(
    "manifest.json",
    "README.md"
  )
  foreach ($file in $firefoxFiles) {
    Copy-Item -LiteralPath (Join-Path $extensionRoot "Firefox\$file") -Destination $firefoxStage
  }
  foreach ($file in @("content.js", "popup.html", "popup.css", "popup.js", "yaris.gif")) {
    Copy-Item -LiteralPath (Join-Path $extensionRoot $file) -Destination $firefoxStage
  }
  Copy-Item -LiteralPath (Join-Path $extensionRoot "service-worker.js") `
    -Destination (Join-Path $firefoxStage "background.js")

  $releaseNotes = Join-Path $extensionRoot "RELEASE_NOTES.md"
  Copy-Item -LiteralPath $releaseNotes -Destination (Join-Path $bundleStage "RELEASE_NOTES.md")

  $chromiumZip = Join-Path $downloads "YARIS-Chrome-Opera.zip"
  $firefoxZip = Join-Path $downloads "YARIS-Firefox.zip"
  $bundleZip = Join-Path $downloads "YARIS-extensions.zip"

  Compress-Archive -Path (Join-Path $chromiumStage "*") -DestinationPath $chromiumZip -Force
  Compress-Archive -Path (Join-Path $firefoxStage "*") -DestinationPath $firefoxZip -Force
  Copy-Item -LiteralPath $chromiumZip, $firefoxZip -Destination $bundleStage
  Compress-Archive -Path (Join-Path $bundleStage "*") -DestinationPath $bundleZip -Force

  Get-Item -LiteralPath $chromiumZip, $firefoxZip, $bundleZip |
    Select-Object Name, Length
}
finally {
  if (Test-Path -LiteralPath $staging) {
    Remove-Item -LiteralPath $staging -Recurse -Force
  }
}
