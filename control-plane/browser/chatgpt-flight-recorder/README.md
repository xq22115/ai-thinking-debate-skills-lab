# Ordinary Chat UX Flight Recorder

A local Chrome MV3 extension for diagnosing ordinary ChatGPT responsiveness without recording prompt/response text.

It measures metadata only: chat-switch click → route/paint latency, assistant stream gaps and character-count deltas, Long Animation Frames, long tasks, and paint timing. Data stays in `chrome.storage.local` until you export or clear it; the extension makes no network requests.

This is a diagnostic layer, not a claim that repository code can change ChatGPT server latency. Use it to separate server/stream stalls from browser main-thread/render/navigation stalls before changing the execution architecture.

## Live acceptance

Live PASS requires an authorized device and real ChatGPT session. Repository tests can validate schema/reporting only and must not be labeled live UX proof.
