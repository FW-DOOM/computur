const ERRORS = [
  ["Microsoft Windows","Windows has detected a hard disk problem.\n\nBack up files immediately.\nError: 0x00000024  NTFS_FILE_SYSTEM"],
  ["Windows Security","Threat: Trojan:Win32/Wacatac.H!ml\nSeverity: SEVERE | Status: Active\nRegistry changes detected."],
  ["Drive Health Warning","SMART Failure — WDC WD10EZEX\nFailure imminent. Error: 0x800701E3"],
  ["System — Critical","Stop: 0x0000007E (0xFFFFFFFFC0000005)\nntoskrnl.exe failed. Dump saved."],
  ["Windows Update","Error 0x800f0900 — Update failed.\nChanges being reverted."],
  ["Security Alert","Unauthorized access: 185.220.101.47\nFirewall breach: svchost.exe PID 4812"],
  ["Boot Config Error","File: ntfs.sys\nStatus: 0xc000014c — Volume error."],
  ["Application Error","chrome.exe stopped working.\nFault offset: 0x0325c5c4"],
  ["System32 Alert","hal.dll — Hash mismatch.\nSystem integrity compromised."],
  ["Windows Activation","Error 0xC004F074 — Not genuine.\nFiles deleted in 3 days."],
  ["Memory Diagnostic","Corruption at 0xFFFFFA8003B2C000\nHardware failure imminent."],
  ["Event Viewer","Bugcheck: 0x0000009f\nDump: C:\\Windows\\MEMORY.DMP"],
  ["Windows Defender","Ransom:Win32/Petya.A active.\nFile: C:\\Windows\\System32\\lsass.exe"],
  ["Network Alert","DNS server not responding.\nAdapter may be permanently damaged."],
  ["Disk Error","winload.exe missing or corrupt.\nStatus: 0xc000000e"],
];

let spawning = false;
let spawnInterval = null;
const MAX_POPUP_WINDOWS = 12;   // Chrome windows are heavy — cap them
let openPopupCount = 0;

chrome.runtime.onMessage.addListener((msg) => {
  if (msg.type === 'START_CHAOS') {
    spawning = true;
    spawnErrors();
  }
  if (msg.type === 'STOP_CHAOS') {
    spawning = false;
    if (spawnInterval) clearInterval(spawnInterval);
  }
  if (msg.type === 'SHOW_WARNED') {
    spawning = false;
    spawnWarned();
  }
  if (msg.type === 'SPAWN_ONE') {
    spawnOneError();
  }
});

function rand(min, max) { return Math.floor(Math.random() * (max - min)) + min; }

async function spawnOneError() {
  if (openPopupCount >= MAX_POPUP_WINDOWS) return;  // hard cap
  const [title, msg] = ERRORS[rand(0, ERRORS.length)];
  const W = 400, H = 185;
  const screens = await getScreenSize();
  const x = rand(0, Math.max(50, screens.w - W));
  const y = rand(40, Math.max(50, screens.h - H));
  const params = new URLSearchParams({ title, msg });
  openPopupCount++;
  chrome.windows.create({
    url: chrome.runtime.getURL('error.html') + '?' + params.toString(),
    type: 'popup',
    width: W, height: H,
    left: x, top: y,
    focused: false
  }, () => {});
}

// track when popup windows close so the cap stays accurate
chrome.windows.onRemoved.addListener(() => {
  if (openPopupCount > 0) openPopupCount--;
});

function spawnErrors() {
  if (!spawning) return;
  spawnOneError();
  // 2 per second — enough to feel chaotic without freezing Chrome
  setTimeout(() => { if (spawning) spawnErrors(); }, 500);
}

async function spawnWarned() {
  const screens = await getScreenSize();
  chrome.windows.create({
    url: chrome.runtime.getURL('warned.html'),
    type: 'popup',
    width: screens.w,
    height: screens.h,
    left: 0, top: 0,
    focused: true
  });
}

async function getScreenSize() {
  return new Promise(resolve => {
    chrome.windows.getCurrent(w => {
      // use a generous default
      resolve({ w: w.width || 1920, h: w.height || 1080 });
    });
  });
}
