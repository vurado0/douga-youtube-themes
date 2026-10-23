# Installing DOUGA — the complete guide

Pick your browser, follow the steps, open YouTube. Every route installs **all five volumes**; you switch between them with <kbd>⌥ Option</kbd> + <kbd>⇧ Shift</kbd> + <kbd>T</kbd> (<kbd>Alt</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> on Windows/Linux).

- [Which method should I use?](#which-method-should-i-use)
- [Safari — Userscripts app (recommended for Safari)](#safari--userscripts-app)
- [Arc, Chrome, Edge, Brave — extension](#arc-chrome-edge-brave--extension)
- [Firefox — Violentmonkey](#firefox--violentmonkey)
- [Firefox — temporary extension (for testing)](#firefox--temporary-extension)
- [Any browser — Stylus](#any-browser--stylus)
- [Safari — native extension with Xcode](#safari--native-extension-with-xcode)
- [Choosing a volume](#choosing-a-volume)
- [Updating](#updating)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)

---

## Which method should I use?

| Browser | Method | Theme switcher | Auto-updates |
|---|---|---|---|
| Safari (Mac) | [Userscripts app](#safari--userscripts-app) | Shortcut | Yes, via the script's update URL |
| Arc · Chrome · Edge · Brave · Opera · Vivaldi | [Extension](#arc-chrome-edge-brave--extension) | Toolbar menu + shortcut | Re-download a release |
| Firefox | [Violentmonkey](#firefox--violentmonkey) | Shortcut | Yes |
| Any browser with Stylus | [Stylus](#any-browser--stylus) | One style per volume (toggle in Stylus) | Re-import |
| Safari, no add-on app | [Native extension](#safari--native-extension-with-xcode) | Toolbar menu + shortcut | Rebuild |

Download links used below:

- **Userscript:** [`dist/douga.user.js`](../dist/douga.user.js) — [raw link for installing](https://raw.githubusercontent.com/vurado0/douga-youtube-themes/main/dist/douga.user.js)
- **Extension:** [`douga-extension-v1.0.0.zip`](https://github.com/vurado0/douga-youtube-themes/raw/main/dist/douga-extension-v1.0.0.zip)
- **Stylus styles:** [`dist/stylus/`](../dist/stylus)

---

## Safari — Userscripts app

Safari has no Chrome-style "load unpacked". The free, open-source **Userscripts** app by quoid adds userscript support to Safari, and DOUGA runs inside it.

1. **Install the app.** Open the Mac App Store, search for **"Userscripts"** (by quoid, open source on [GitHub](https://github.com/quoid/userscripts)) and install it. It is free.
2. **Open Userscripts once.** Launch it from Applications. It shows the folder where your scripts live — the default folder is fine.
3. **Turn it on in Safari.** Safari ▸ **Settings…** ▸ **Extensions** ▸ tick **Userscripts**.
4. **Allow it on YouTube.** Still in the Extensions pane, click **Edit Websites…** (or the Userscripts icon in the toolbar) and set **www.youtube.com** to **Allow**.
5. **Add DOUGA.** Pick one:
   - **A — from the link:** open the [raw userscript link](https://raw.githubusercontent.com/vurado0/douga-youtube-themes/main/dist/douga.user.js) in Safari, click the **Userscripts** icon in the toolbar and install it from there.
   - **B — paste:** click the **Userscripts** icon ▸ **Open Extension Page** ▸ **+** ▸ **New JS**, delete the template, paste the whole contents of `douga.user.js`, press <kbd>⌘</kbd> <kbd>S</kbd>.
   - **C — drop the file:** copy `douga.user.js` into the scripts folder you chose in step 2.
6. **Open YouTube** and reload the tab. The logo turns into the どうが mascot.

> Tip: the userscript's `@updateURL` points at this repo, so Userscripts can check it for updates from its extension page.

---

## Arc, Chrome, Edge, Brave — extension

Works in every Chromium browser: Arc, Chrome, Edge, Brave, Opera, Vivaldi.

1. **Download** [`douga-extension-v1.0.0.zip`](https://github.com/vurado0/douga-youtube-themes/raw/main/dist/douga-extension-v1.0.0.zip).
2. **Unzip it.** On a Mac a double-click does it. You get a folder called **`douga-extension`** — keep it somewhere permanent (e.g. `Documents/`), the browser loads it from there.
3. **Open the extensions page:**

   | Browser | Address |
   |---|---|
   | Arc | `arc://extensions` |
   | Chrome | `chrome://extensions` |
   | Edge | `edge://extensions` |
   | Brave | `brave://extensions` |

4. **Turn on Developer mode** (switch in the top-right corner; in Edge it is in the left sidebar).
5. Click **Load unpacked** and select the **`douga-extension`** folder (the one containing `manifest.json`).
6. **Pin it** (optional): click the puzzle-piece icon in the toolbar and pin **DOUGA**. Its menu lists all five volumes and an on/off button.
7. **Open YouTube** and reload the tab.

> Arc users: Arc shares Chrome's extension system, so the steps are identical. If you use several Arc profiles, load the extension in each profile you want it in.

---

## Firefox — Violentmonkey

1. Install **Violentmonkey** from [addons.mozilla.org](https://addons.mozilla.org/firefox/addon/violentmonkey/) (Tampermonkey works too).
2. Open the [raw userscript link](https://raw.githubusercontent.com/vurado0/douga-youtube-themes/main/dist/douga.user.js). Violentmonkey shows an install screen — click **Confirm installation**.
3. Open YouTube and reload.

The same steps work in Chrome/Edge with Tampermonkey or Violentmonkey if you prefer userscripts over the extension.

---

## Firefox — temporary extension

For testing the extension build itself. Firefox removes temporary add-ons when it quits; for everyday use take the Violentmonkey route above.

1. Unzip `douga-extension-v1.0.0.zip`.
2. Open `about:debugging#/runtime/this-firefox`.
3. Click **Load Temporary Add-on…** and select `douga-extension/manifest.json`.

---

## Any browser — Stylus

Stylus loads one fixed volume per style, without the switcher or the search-box text.

1. Install **Stylus** for your browser ([Chrome Web Store](https://chromewebstore.google.com/detail/stylus/clngdbkpkpeebahjckkjfobafhncgmne), [Firefox Add-ons](https://addons.mozilla.org/firefox/addon/styl-us/)).
2. Open one file from [`dist/stylus/`](../dist/stylus) as **Raw**, e.g. `douga-shirokuro.user.css`. Stylus offers to install it — click **Install style**.
3. Install more volumes the same way and switch them on/off in the Stylus menu (keep only one enabled).

---

## Safari — native extension with Xcode

A real Safari extension with the toolbar menu, built on your own Mac. It needs the **full Xcode app** (about 10 GB, free in the App Store); the Command Line Tools alone are not enough.

1. Install **Xcode** from the App Store and open it once to finish setup.
2. Point the developer tools at it:
   ```bash
   sudo xcode-select -s /Applications/Xcode.app/Contents/Developer
   ```
3. Get the code and build:
   ```bash
   git clone https://github.com/vurado0/douga-youtube-themes.git
   cd douga-youtube-themes
   ./scripts/build-safari.sh
   ```
   The script converts `dist/extension` into an Xcode project, builds a locally signed app and opens it once.
4. In Safari: **Settings ▸ Advanced ▸** tick **Show features for web developers**.
5. Menu bar **Develop ▸** tick **Allow Unsigned Extensions** (asks for your password).
6. **Settings ▸ Extensions ▸** enable **DOUGA** and allow it on `www.youtube.com`.

> Safari turns "Allow Unsigned Extensions" off whenever it quits. Re-tick it after a restart, or use the Userscripts route, which has no such limit. Distributing a signed build requires an Apple Developer account.

---

## Choosing a volume

| Where | How |
|---|---|
| On YouTube | <kbd>⌥ Option</kbd> + <kbd>⇧ Shift</kbd> + <kbd>T</kbd> cycles Vol.01 → 05. A toast shows the name. |
| On YouTube | <kbd>⌥ Option</kbd> + <kbd>⇧ Shift</kbd> + <kbd>X</kbd> turns the skin off / back on. |
| Extension toolbar | Click the DOUGA icon and pick a volume. |

Shortcuts are ignored while you type in the search box or a comment field. Your choice is saved in the browser and comes back on every visit.

Light/dark: Shirokuro, Washi and Sakura follow YouTube's own appearance setting (your avatar ▸ **Appearance**). Neon Yoichi is always dark, 8-Bit Pocket always green.

---

## Updating

- **Userscripts / Violentmonkey:** use the manager's *Check for updates* — the script updates from this repo.
- **Extension:** download the new zip from `dist/`, replace the contents of your `douga-extension` folder, then press the **↻ reload** button on the extensions page.
- **Stylus:** reinstall the style from `dist/stylus/`.
- **Safari native:** `git pull && ./scripts/build-safari.sh`.

## Uninstalling

- **Extension:** extensions page ▸ DOUGA ▸ **Remove**.
- **Userscripts / Violentmonkey / Stylus:** delete the DOUGA entry in the manager.
- **Safari native:** Settings ▸ Extensions ▸ untick DOUGA, then delete the DOUGA app from `build/safari`.

YouTube is back to normal on the next reload — DOUGA never changes your YouTube account or settings.

---

## Troubleshooting

**Nothing changes.**
Reload the YouTube tab after installing. Check that the extension/userscript is enabled **for www.youtube.com** (Safari asks per site). Make sure the skin is not switched off — press <kbd>⌥</kbd> <kbd>⇧</kbd> <kbd>X</kbd>.

**The fonts look plain.**
The typefaces load from Google Fonts. Content blockers that block `fonts.googleapis.com` / `fonts.gstatic.com` make DOUGA fall back to your system fonts (on a Mac: Hiragino Maru Gothic). Allow those two domains to get the full look.

**The shortcut does nothing.**
Click somewhere on the page first so YouTube has focus, and make sure the cursor is not in the search box. On a Mac use the **Option** key, not Command.

**Part of the page looks unstyled.**
YouTube rolls out layout experiments to some accounts. [Open an issue](https://github.com/vurado0/douga-youtube-themes/issues) with a screenshot and the page URL.

**Arc says "Manifest file is missing".**
You selected the zip or a parent folder. Select the folder that directly contains `manifest.json`.
