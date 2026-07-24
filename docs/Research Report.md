# Installing Claude Code on Android (Termux) — 2026 Guide

Running Anthropic's Claude Code CLI (`@anthropic-ai/claude-code`) on Android Termux **is possible but requires a workaround**, because Anthropic ships no Android build and the current default native installer is a glibc binary that Android's Bionic libc cannot load.

## TL;DR
- **Yes, it works, but not by the official route.** Anthropic ships no `android-arm64` build (its prebuilt binaries cover only darwin-arm64/x64, linux-x64/arm64, their musl variants, and win32-x64/arm64), and the now-default native installer (`curl … claude.ai/install.sh`) delivers a glibc-linked ELF that Android's Bionic kernel rejects with `unexpected e_type: 2`. The two reliable methods are (A) running Claude Code natively in Termux via the Termux **glibc-runner** shim that patches the official `linux-arm64` binary, or (B) installing it inside a **proot-distro Ubuntu** sandbox where everything "just works."
- **The single biggest gotcha** is the v2.1.113 regression (upstream landed **April 17–18, 2026**): Claude Code dropped its bundled JavaScript `cli.js` entry point and switched to a native binary, breaking every plain-`npm` Termux install with `Error: claude native binary not installed`. [GitHub](https://github.com/ferrumclaudepilgrim/claude-code-android/releases) The last JS version that works unpatched is `2.1.112`; everything newer needs the glibc-runner patch (Path A) or a real Linux userland (Path B). It is tracked upstream at `anthropics/claude-code#50270`.
- **Recommendation:** New users should use **Path B (proot-distro Ubuntu)** — fewest moving parts, stays current with `claude` updates. Power users wanting a lightweight, auto-updating native setup should use the community **glibc-runner** installer (Path A). Avoid the bare `npm install -g @anthropic-ai/claude-code` shown in older guides; on current versions it installs but will not run.

## Key Findings
- **Requirements:** A 64-bit ARM (aarch64) Android device — confirm with `uname -m`. The maintained community repo's test suite was verified end-to-end across **Android 8, 10, 13, and 17 Beta** (verified May 16, 2026), so the practical floor is broad, though Android 14+ has the most coverage. Termux **must** come from F-Droid or the Termux GitHub releases — **not** Google Play. The Play Store build is functionally frozen (Termux's own maintainers note the Play release "remains deprecated" and v0.120 is "functionally equivalent to v0.108"), [GitHub](https://github.com/termux/termux-app/discussions/4000) stuck since 2020 by Google Play's Android 10 `targetSdkVersion` requirement and its W^X `exec()` restriction. You need a paid Anthropic account (Claude Pro, Max, Team, Enterprise, or a Console/API account); the free Claude.ai plan does not include Claude Code. An internet connection is mandatory (all model compute is server-side).
- **The core incompatibility (issue #50270):** Since v2.1.113, `install.cjs` reads `process.platform`, gets `android` (not `linux`), and — per the issue verbatim — "returns android → not in PLATFORMS map → skips binary install." [GitHub](https://github.com/anthropics/claude-code/issues/50270) Force-installing `@anthropic-ai/claude-code-linux-arm64` doesn't help either: the binary is a glibc-linked ELF (`ELF 64-bit LSB executable, ARM aarch64 … interpreter /lib/ld-linux-aarch64.so.1, for GNU/Linux`, per issue #20778) and Android's kernel rejects it (`"bin/claude.exe" has unexpected e_type: 2`); patching with the glibc loader directly fails with `Could not find a PHDR: broken executable?`. [GitHub](https://github.com/anthropics/claude-code/issues/50270)
- **Path A (native Termux, glibc-runner):** The maintained community installer (`ferrumclaudepilgrim/claude-code-android`) installs Termux's `glibc-runner` + `patchelf-glibc`, downloads the latest official `linux-arm64` `claude` binary (the README states "the binary alone is ~233 MB, plus ~200 MB if you accept recommended packages," [GitHub](https://github.com/ferrumclaudepilgrim/claude-code-android) install time "About 5-10 minutes"), verifies its SHA-256 against Anthropic's signed manifest, rewrites the ELF interpreter to point at Termux's glibc loader, and installs an auto-updating wrapper at `$PREFIX/bin/claude`. The patched-binary technique was originally described by **gtbuchanan** in a comment on `anthropics/claude-code#50270`. It is a shim, not native support.
- **Path B (proot-distro Ubuntu):** Install proot-distro, install Ubuntu, `apt update && apt upgrade`, then run Anthropic's official `curl … install.sh`. Inside Ubuntu `process.platform === 'linux'`, so the official native binary runs unmodified and updates normally. No `/tmp` workaround, no ripgrep fix. Heavier — the maintainer's README puts the full Ubuntu path at **~2 GB on disk**. [GitHub](https://github.com/ferrumclaudepilgrim/claude-code-android) Auth requires manually copy-pasting the OAuth URL into your phone browser.
- **Path C (AVF Linux VM):** On Pixel-class hardware on Android 16+ with the built-in Linux Terminal (Developer options → Linux development environment), you get a real Debian VM via the Android Virtualization Framework, where the official installer works directly. [GitHub](https://github.com/ferrumclaudepilgrim/claude-code-android) Experimental and hardware-limited.
- **Node.js trap:** Node.js v24 hangs on startup under Termux on ARM64 — a 60+ second stall (issue #23634 logs show `configureGlobalAgents complete` then a "60+ second gap here"; the reporter notes "Node.js v24 is the only version available on Termux (no way to downgrade)" [GitHub](https://github.com/anthropics/claude-code/issues/23634) and resorted to proxying through another machine). Use Node v25+ (Termux now ships it). Relevant only to the npm path; the glibc-runner binary embeds its own runtime.
- **ripgrep trap:** Claude Code bundles ripgrep but has no `arm64-android` build, so Grep/Glob fail with (verbatim, issue #8760) `Error: spawn /data/data/com.termux/files/home/.claude/local/node_modules/@anthropic-ai/claude-code/vendor/ripgrep/arm64-android/rg ENOENT [GitHub](https://github.com/anthropics/claude-code/issues/8760) `. Fix: `pkg install ripgrep [npmx](https://npmx.dev/package/claude-code-termux) ` and symlink the system `rg` into the vendor path (or set `USE_BUILTIN_RIPGREP=0`).

## Details

### Why the official methods fail
Anthropic's recommended install is now the native installer (`curl -fsSL https://claude.ai/install.sh | bash`) or Homebrew/WinGet; npm is marked deprecated. [GitHub](https://github.com/anthropics/claude-code) All deliver the same platform-native binary (npm pulls it via a per-platform optional dependency such as `@anthropic-ai/claude-code-linux-arm64` plus a postinstall link step). None target `android-arm64`, and the `linux-arm64` binary is glibc-linked against `/lib/ld-linux-aarch64.so.1`, which Android/Bionic cannot load. This is documented in upstream issues #50270 (the v2.1.113 regression) and #20778/#10644 (the broader "native installer can never work on Bionic" problem). The latest published version on npm is in the 2.1.x series and releases roughly weekly, so the gap from the last working JS version (2.1.112) keeps widening.

### Path A — Native Termux via glibc-runner (recommended for power users)
The cleanest way is the maintained installer, which encapsulates the patching, checksum verification, and auto-update logic:

```bash
# In Termux (from F-Droid)
curl -fsSL https://raw.githubusercontent.com/ferrumclaudepilgrim/claude-code-android/main/install.sh -o install.sh
# read it first if you like, then:
bash install.sh
```

What it does, step by step:
1. Enables the Termux glibc package source and installs the runtime/patch tools:
   ```bash
   pkg install glibc-repo
   pkg update
   pkg install glibc-runner patchelf-glibc
   ```
2. Resolves the latest version from `registry.npmjs.org`, downloads `linux-arm64/claude` (~233 MB) from `downloads.claude.ai`, and verifies its SHA-256 against the published `manifest.json`.
3. Repatches the ELF interpreter to Termux's glibc loader:
   ```bash
   patchelf --set-interpreter "$PREFIX/glibc/lib/ld-linux-aarch64.so.1" <binary>
   ```
4. Writes `~/.claude/settings.json` with `"autoUpdates": false` plus an `env` block setting `LD_PRELOAD` to Termux's `libtermux-exec` shim (so subprocesses Claude spawns behave), and installs a wrapper at `$PREFIX/bin/claude` that `unset`s `LD_PRELOAD` before exec-ing the glibc binary, self-heals the interpreter on each launch, and checks for a newer release once per day.

**Note on repo state:** As of this writing the repo's *scripts* (`install.sh`/`migrate.sh`) implement this current glibc-runner approach, while the rendered `README.md`/`INSTALL.md` still describe an older npm-or-pin method. Trust the scripts.

**Manual / legacy alternative (only for pinned 2.1.112):** Older guides install with plain npm and run through proot. This is now viable only if you deliberately pin the last JS version, and you must defend the pin against the in-process auto-updater:
```bash
pkg install nodejs git curl proot ripgrep -y
export TMPDIR=$PREFIX/tmp
npm install -g @anthropic-ai/claude-code@2.1.112
# the binary hardcodes /tmp, which Android lacks — bind-mount it:
proot -b $PREFIX/tmp:/tmp claude
```
The maintainer warns that "a user who manually downgrades to 2.1.112 sees the pin silently re-overwritten with 2.1.114 within minutes," [GitHub](https://github.com/ferrumclaudepilgrim/claude-code-android/releases) so "the pin must be defended with `DISABLE_AUTOUPDATER=1` plus a load-bearing `chmod -R a-w` on the install directory" [GitHub](https://github.com/ferrumclaudepilgrim/claude-code-android/releases) — and notes "the chmod is the load-bearing one — the env reduces but does not stop the attempt." Because of this fragility, prefer the glibc-runner installer over manual pinning.

### Path B — proot-distro Ubuntu (recommended for new users)
```bash
pkg upgrade -y                       # updates SSL/curl — required or the installer returns 403
pkg install proot-distro -y
proot-distro install ubuntu          # downloads the Ubuntu rootfs
proot-distro login ubuntu
# now inside Ubuntu:
apt update && apt upgrade -y         # required, or the native installer returns 403
curl -fsSL https://claude.ai/install.sh | bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
claude --version
claude
```
Trade-offs: ~10–15 minute setup and **~2 GB on disk** vs. Path A's ~2-minute setup, but no `/tmp` workaround, no ripgrep symlink fix, no Node version juggling, and updates "just work" like on desktop Linux. On first launch you must copy the OAuth URL from the terminal into your Android browser (no browser auto-opens inside proot). Samsung One UI 8 users have a known performance regression when Termux is backgrounded (proot-distro issue #567) — keep Termux in the foreground or split-screen.

### Path C — Android Virtualization Framework (experimental)
On supported devices (Pixel-class hardware on Android 16+), enable Developer options → Linux development environment, open the Terminal app, accept the Debian image download, then run the standard `curl -fsSL https://claude.ai/install.sh | bash`. Because it's a real Linux VM, the official binary runs unmodified. Hardware support is limited and the feature is still maturing.

### Authentication
On first run, `claude` prints an OAuth URL. In native Termux the browser may auto-open; in proot it will not — long-press to copy the URL and open it in your phone browser, log in with your paid Anthropic account, and return to the terminal. For headless/CI-style use you can set `ANTHROPIC_API_KEY` instead. You can also point Claude Code at alternative backends (e.g. OpenRouter) via `ANTHROPIC_BASE_URL`/`ANTHROPIC_AUTH_TOKEN`, [GitHub](https://github.com/AbuZar-Ansarii/ClaudeCodeOnPhone) or via the community Claude Code Router, to use other models from the same CLI.

### Known issues and constraints on Android/ARM
- **No glibc, no native Android build** — the root cause of everything (#50270, #20778).
- **Node v24 hang on ARM64** (#23634, #23665) — use v25+.
- **ripgrep `arm64-android` missing** (#8760) — `pkg install ripgrep` + symlink, or `USE_BUILTIN_RIPGREP=0`.
- **`/tmp` doesn't exist / isn't writable** — Claude Code hardcodes it for sockets/IPC; fix with `proot -b $PREFIX/tmp:/tmp` or `CLAUDE_CODE_TMPDIR`.
- **OAuth quirks** — manual URL copy/paste is the norm on Termux; some wrappers recommend API-key auth as more reliable.
- **Bun installs silently break** (#50203) — Bun blocks the postinstall that fetches the native binary; use npm, not Bun.
- **Runtime limits on a phone:** no root (no `sudo`, no ports < 1024), no systemd, ~512 MB Node heap, ~1024 file descriptors, Android's phantom-process killer culls background processes (keep to a few), and `/tmp` under proot is volatile. Expect significant battery drain during heavy sessions.
- **Auto-updater fights manual pins** — the in-process updater re-fetches "latest" on a timer, which can re-break a pinned 2.1.112 install within minutes unless disabled and the directory is made read-only.

### Alternatives to running it on-device
If on-device fragility isn't worth it: run Claude Code on an always-on desktop/VPS and connect from Termux over **SSH + Tailscale** (your phone is a thin client; compute and the binary live on a real Linux box), or use Anthropic's official Claude mobile app / Remote Control for review-style workflows. These avoid the Bionic/glibc problem entirely.

## Recommendations
1. **Start with Path B (proot-distro Ubuntu)** unless you specifically need a minimal footprint. It's the most robust, uses the official installer, and survives Claude Code's frequent releases without per-update fixes. Budget ~2 GB of storage.
2. **Choose Path A (glibc-runner installer)** if you want a fast, lightweight, auto-updating native command and are comfortable with a community shim. Use the maintained `install.sh`; don't hand-roll the patching.
3. **Do not** use the bare `npm install -g @anthropic-ai/claude-code` from older blog posts on current versions — it installs but exits with `claude native binary not installed`. If you must use npm, either pin `@2.1.112` (and lock it down) or, better, switch to Path A/B.
4. **Always install Termux from F-Droid or GitHub**, run `pkg upgrade` first, and verify Node is **v25+** before any npm-based step.
5. **Benchmarks that change the recommendation:** If Anthropic ships an official `android-arm64` target or a static musl build (discussed but not delivered as of this writing, tracked in #50270), switch to the official installer and drop the shim. If `claude doctor` reports ripgrep or `/tmp` failures, apply the symlink and bind-mount fixes before troubleshooting anything else. If you hit the Node v24 hang, upgrade Node rather than debugging network timeouts.

## Caveats
- **Fast-moving target.** Claude Code releases roughly weekly and recently changed its packaging mid-stream (the 2.1.113 regression). Exact version numbers and the community repo's recommended commands will drift; treat specific versions here as point-in-time.
- **Community repo is internally inconsistent.** As of writing, the `ferrumclaudepilgrim/claude-code-android` scripts (`install.sh`/`migrate.sh`) implement the current glibc-runner approach, while the rendered `README.md`/`INSTALL.md` still describe the older npm-or-pin method. Trust the scripts; read them before running.
- **Unofficial and unsupported.** None of these paths are supported by Anthropic; the glibc-runner approach in particular is a third-party shim around a glibc binary. Anthropic has *said it may* add Android support, but that is forward-looking and not shipped.
- **Security:** Always read `install.sh` before piping to bash, and prefer the checksum-verifying installer. Don't run npm as `sudo`.