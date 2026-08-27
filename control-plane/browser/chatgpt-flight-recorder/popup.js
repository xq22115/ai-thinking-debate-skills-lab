const KEY="ordinaryChatUxEventsV1";
const status=document.getElementById("status");
function showCount(){chrome.storage.local.get({[KEY]:[]},o=>{status.textContent=`events: ${Array.isArray(o[KEY])?o[KEY].length:0}`;});}
document.getElementById("clear").addEventListener("click",()=>chrome.storage.local.set({[KEY]:[]},showCount));
document.getElementById("export").addEventListener("click",()=>chrome.storage.local.get({[KEY]:[]},o=>{
  const payload={schemaVersion:1,exportedAt:new Date().toISOString(),contentCapture:"metadata_only",events:Array.isArray(o[KEY])?o[KEY]:[]};
  const url=URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{type:"application/json"}));
  const a=document.createElement("a");a.href=url;a.download=`ordinary-chat-ux-${Date.now()}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
}));
showCount();
