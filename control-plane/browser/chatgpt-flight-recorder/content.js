(() => {
  "use strict";
  const KEY = "ordinaryChatUxEventsV1", MAX_EVENTS = 5000;
  const assistantState = new WeakMap();
  let navStart = null, lastHref = location.href;
  const nowEpochMs = () => Date.now();
  const monoMs = () => performance.now();
  function add(type, fields = {}) {
    const event = {schemaVersion:1,type,epochMs:nowEpochMs(),monoMs:Math.round(monoMs()*1000)/1000,...fields};
    chrome.storage.local.get({[KEY]:[]}, obj => {
      const items = Array.isArray(obj[KEY]) ? obj[KEY] : [];
      items.push(event); if (items.length > MAX_EVENTS) items.splice(0, items.length-MAX_EVENTS);
      chrome.storage.local.set({[KEY]:items});
    });
  }
  const routeKind = () => location.pathname.startsWith("/c/") ? "conversation" : "other";
  function markPaintAfterRouteChange(trigger) {
    const started = navStart;
    requestAnimationFrame(() => requestAnimationFrame(() => {
      if (started !== null) { add("chat_switch_to_paint",{trigger,durationMs:Math.max(0,monoMs()-started),routeKind:routeKind()}); navStart=null; }
    }));
  }
  document.addEventListener("click", event => {
    const target = event.target instanceof Element ? event.target.closest("a[href]") : null;
    if (target && typeof target.getAttribute("href") === "string" && target.getAttribute("href").startsWith("/c/")) {
      navStart=monoMs(); add("chat_switch_click",{routeKind:routeKind()});
    }
  }, {capture:true,passive:true});
  setInterval(() => {
    if (location.href !== lastHref) { lastHref=location.href; add("route_change",{routeKind:routeKind()}); markPaintAfterRouteChange("url_change"); }
  },100);
  try { new PerformanceObserver(list => { for (const entry of list.getEntries()) add("long_animation_frame",{durationMs:entry.duration}); }).observe({type:"long-animation-frame",buffered:true}); } catch (_) {}
  try { new PerformanceObserver(list => { for (const entry of list.getEntries()) add("long_task",{durationMs:entry.duration}); }).observe({type:"longtask",buffered:true}); } catch (_) {}
  try { new PerformanceObserver(list => { for (const entry of list.getEntries()) if (entry.name === "first-contentful-paint") add("paint",{name:entry.name,startTimeMs:entry.startTime}); }).observe({type:"paint",buffered:true}); } catch (_) {}
  const observer = new MutationObserver(mutations => {
    const touched = new Set();
    for (const mutation of mutations) {
      const element = mutation.target instanceof Element ? mutation.target : mutation.target.parentElement;
      if (!element) continue;
      const assistant = element.closest('[data-message-author-role="assistant"]'); if (assistant) touched.add(assistant);
    }
    for (const node of touched) {
      const length = (node.textContent || "").length, t = monoMs(), previous = assistantState.get(node);
      if (!previous) { assistantState.set(node,{length,t,first:t}); add("assistant_first_observed",{charCount:length}); }
      else if (length !== previous.length) { add("assistant_stream_delta",{charCount:length,deltaChars:length-previous.length,streamGapMs:Math.max(0,t-previous.t),sinceFirstMs:Math.max(0,t-previous.first)}); assistantState.set(node,{length,t,first:previous.first}); }
    }
  });
  function startObserver() {
    if (!document.documentElement) { requestAnimationFrame(startObserver); return; }
    observer.observe(document.documentElement,{subtree:true,childList:true,characterData:true});
    add("recorder_started",{routeKind:routeKind(),userAgentMajor:navigator.userAgent.match(/Chrome\/(\d+)/)?.[1] || "unknown"});
  }
  startObserver();
})();
