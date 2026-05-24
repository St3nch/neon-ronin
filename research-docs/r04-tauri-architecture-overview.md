# 1. Tauri Architecture Overview

Tauri is an open-source framework for building cross‑platform desktop apps with a web front end (HTML/JS/React) and a small Rust-based core. Unlike Electron, it uses the OS’s native webview (no bundled Chrome), so apps are much smaller and more secure【21†L318-L320】. Tauri can bundle multiple “sidecar” processes (e.g. a Python/FastAPI backend) as executables. The frontend communicates with these via IPC or REST. Tauri’s security model follows a unidirectional messaging pattern (events/commands) and optional sandboxing.  

| Topic                           | Finding                                                                                                                                                                                                                                                                               | Source                       | Confidence | Practical Implication                                                                                                                                         |
|---------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------|------------|------------------------------------------------------------------------------------------------------------------------------------------|
| **What is Tauri?**              | A toolkit for building desktop apps with web front ends and Rust core. Smaller footprint than Electron; uses OS webview.                                                                                                                                                             | [21] L318-320                | High       | Reduces app size & memory vs Electron. Good for cross-platform desktop UI with web tech.                                                  |
| **Solves vs Electron?**         | Tauri avoids bundling a full browser engine (relying on system WebView) so executables are much smaller and use less RAM. It also emphasizes security (strict API exposure).                                                                                                            | [21] L318-320, Common knowledge | High    | More lightweight & secure than Electron, but Rust core means steeper learning curve.                                                    |
| **Strengths/Weaknesses**        | **Strengths:** Small size, security (native webview sandbox), Rust speed. **Weaknesses:** Newer/ecosystem smaller; complex native integration (Rust) versus Electron’s JS ecosystem. Packaging sidecars is possible but requires setup (e.g. PyInstaller for Python)【23†L234-L239】. | [23] L228-236, [21] L318-320  | High       | Good for our use case (desktop, local DB, local backend). Dev velocity slower (Rust), but benefits may outweigh for production stability. |
| **Frontend↔Backend comms**      | Tauri exposes APIs/events for invoking commands. You can spawn a Python process as a “sidecar” (standalone executable) and communicate via stdout/events or via HTTP on localhost【23†L234-L239】【21†L318-L320】.                                                                   | [23] L234-239                | High       | Supports a local API approach (FastAPI) or CLI tools. Frontend can use `@tauri-apps/api` to call Rust commands or listen to events.       |
| **Filesystem access**           | Tauri provides Rust APIs (and plugins) to read/write the local filesystem. It also supports a JS API for file dialogs and operations. The app can access local files (sandbox restricted by default, but configurable).                                                                   | Common knowledge             | Medium     | We can save assets/images to user directories. Must ensure proper permissions and sanitization.                                         |
| **Local commands/processes**    | Tauri can spawn and manage subprocesses via its sidecar mechanism (e.g. launch a Python binary)【23†L234-L239】. It also allows spawning OS commands using Rust’s `Command`.                                                                                                         | [23] L234-239                | High       | We can launch long-running LangGraph workflows or Invoke CLIs from Rust. We must manage lifecycle (see #7).                            |
| **Security model**              | Tauri runs the webview in a very restricted environment. All powerful APIs (filesystem, networking) must be explicitly enabled or accessed via Rust bridges. It uses a permission/whitelist model. The default is very locked down.                                                   | Tauri docs (v2)              | High       | By default, frontend cannot do file I/O or spawn processes without going through Rust. This helps security (e.g. avoid XSS attacks).     |
| **Production gotchas**          | Tauri v2 (in Rust) has matured, but cross-compiling for Windows/macOS requires setup (Rust toolchains). Developers must manage signing and notarization for distribution. Auto-updates need configuration.                                                                              | Community experience         | Medium     | We must plan build pipelines for each OS (using Rust + Node build). Auto-update can be integrated (e.g. GitHub releases).                 |

# 2. Tauri + Python Backend Options

We consider several architectures for tying Tauri (UI) to the Python LangGraph backend:

| Option                       | Pros                                                                                                                                                              | Cons                                                                                                                                                                      | Packaging Difficulty           | Dev Experience                  | Production Reliability        | Fit for Project                 |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|--------------------------------|-------------------------------|-------------------------------|
| **A. Python Sidecar Service** | - Dedicated Python process (FastAPI/LangGraph) can run long workflows<br>- Clear separation; can use HTTP or event I/O【23†L234-L239】<br>- Well-understood pattern (examples exist【21†L318-L320】). | - Need to build Python into native executable (PyInstaller etc)【23†L234-L239】<br>- More moving parts (service process) to manage<br>- Inter-process comms overhead             | Moderate (need PyInstaller)    | Good (isolated backend dev)     | High (if monitored properly)   | **Strong candidate**         |
| **B. Invoke Python on Demand** | - Simplest: call Python scripts via Tauri's `Command::sidecar` per action【23†L234-L239】<br>- No persistent server needed                                              | - Each request spawns new process (slower)<br>- Harder to maintain persistent state across calls (no long-running session)<br>- Likely more complex for user prompts      | Low (just keep .py files)     | Moderate (need sync calls)      | Medium (reliant on child calls)| Possible for simple tasks      |
| **C. Docker Compose**        | - Fully isolates services; can use standard Docker for Python+Postgres<br>- Dev/test parity with Prod containers.                                                   | - Unusual for desktop app (requires Docker installed locally)<br>- Heavyweight; not user-friendly for non-technical users                                                         | High (need Docker env)         | Lower (Docker needed)           | Low (users must run Docker)    | **Not recommended**           |
| **D. Remote Backend**        | - Simplest client-only Tauri app; backend on server<br>- Offloads scale and persistence.                                                                            | - Not offline; defeats “desktop-first” goal<br>- Adds latency; requires internet and auth<br>- Against project’s “desktop app with local control” intent.                      | Low (just API calls)          | Simple UI dev; backend dev remote | High (cloud infra)             | **Unwanted for core workflows** |
| **E. Rewrite in TypeScript** | - Eliminates Python; use LangGraph.js/TS and LangChain.js<br>- Single technology stack (Node/JS).                                                                    | - Major rewrite of LangGraph logic and flows in TS<br>- LangGraph.py features may differ<br>- Less community usage; fewer examples than Python                                    | Very High (rewrite needed)     | Slow (learning LangGraph.js)    | Unknown (LangGraph.js is newer)| **Low priority**              |

**Insights:** Option A (Python sidecar FastAPI) is the most promising: Tauri can spawn a bundled Python executable and communicate via REST or stdout【23†L234-L239】. This allows a continuous LangGraph process (necessary for long-running workflows). PyInstaller or Nuitka can package Python into a binary【23†L234-L239】. Option B might be used for quick tasks but is poor for long sessions. Docker (C) is too heavy for end users. A remote backend (D) contradicts the “desktop-first” requirement. Rewriting in TS (E) avoids Python but is a large cost for uncertain gain. 

Additional factors:
- **Packaging Python:** Tauri supports bundling sidecars by placing binaries in `src-tauri`. Python code must be compiled to an executable (PyInstaller, `python-app`, or Goaw).  Cross-platform packaging of Python can be painful (PyInstaller on each OS)【23†L234-L239】. 
- **Communication:** Use HTTP (FastAPI) on `localhost` or IPC events. Localhost HTTP is simpler (use FastAPI as a REST API that Tauri JS can call). 
- **Security:** Sidecar model encapsulates Python; since it's local, fewer secrets leakage issues, but must guard any open endpoints (e.g. no open CORS). 
- **Resilience:** Running Python as a sidecar means if it crashes, app should detect and restart or alert user.

# 3. LangGraph Inside Desktop Architecture

LangGraph can run inside a local Python service (sidecar). Workflows will run in that process and maintain state via the checkpointer.

| Question                                       | Finding                                                                                                                                                                                                                           | Source                  | Confidence | Practical Implication                                                                                           |
|-----------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------|------------|----------------------------------------------------------------------------------------------------------------|
| LangGraph in local Python?                     | Fully supported: LangGraph is a Python library. Workflows can run as part of a standalone Python service (e.g. FastAPI app) on the user’s machine.                                                                                  | [12] L296-301           | High       | The LangGraph “backend” is just Python code; can embed in our sidecar service.                                    |
| Long-running workflows?                        | Yes – LangGraph is designed for long-running, stateful graphs【12†L296-L301】. It supports durable execution (can span minutes/hours/days) with automatic checkpointing【12†L296-L301】.                                            | [12] L296-301           | High       | Workflows (e.g. multi-step product creation) can persist even if user takes long breaks.                        |
| Local vs remote Postgres checkpointer?         | LangGraph has a Postgres checkpointer (`langgraph-checkpoint-postgres`) for persistence【18†L820-L823】. We can run Postgres locally (sidecar or bundled) or use SQLite as alternative for local use【18†L816-L824】.                 | [18] L816-L823          | High       | For local app, SQLite saver may be easier. Postgres saver ideal for production (LangSmith). SQLite is lighter.     |
| Interrupts → UI integration?                  | LangGraph supports interrupts (human-in-loop) via checkpoints【16†L139-L146】. A paused workflow yields a saved state. Our UI must poll or subscribe to LangGraph state to present approval screens.                                 | [16] L139-L146          | High       | We must implement a mechanism (WebSocket or polling) for Tauri UI to detect “pending approval” states in LangGraph. |
| Need LangGraph Server?                        | Not strictly: LangGraph can run without the LangGraph Agent Server. The open-source API with a checkpointer suffices. Agent Server automates persistence but is not mandatory.                                                    | [16] L127-129           | High       | Can use LangGraph as a library; we lose managed services (thread management UI) but remain in control.            |
| Loss without LangSmith/Platform?              | Without LangSmith, we miss built-in tracing UI and hosted orchestration features【16†L127-L134】. All workflow control and storage must be done by us (LangSmith Engine not used).                                                    | [16] L127-134          | Medium     | No commercial subscription; rely on our own audit logs/state introspection.                                     |
| Resume after app restart?                     | Yes, if persistence is used. A new Python run with the same thread_id (or loading last checkpoint) can continue. The checkpointer allows resuming where left off【16†L139-L146】.                                                  | [16] L139-L146          | High       | Design: keep consistent thread_id or store thread info so workflow can resume after UI restart.                   |
| If killed while waiting approval?             | The checkpoint system means workflow state is saved at interruption【16†L139-L146】. If process crashes, on restart we can reload latest checkpoint. However, unsubmitted actions may need retry logic.                            | [16] L139-L146          | Medium     | We must implement cleanup (e.g. mark workflows that were mid-pause) and allow resuming or manual recovery.        |

Overall, LangGraph fits our human-in-loop model well: it has durable checkpoints and explicit interrupt points【16†L139-L146】. We must build the UI-side “approval gate” logic – e.g., poll LangGraph state or subscribe to interrupts (e.g. via LangSmith-style events). Since we may not use LangSmith, we’ll likely implement our own status API (e.g. FastAPI endpoints that query `graph.get_state()`). Interrupted workflows can wait indefinitely for user input – LangGraph does not enforce timeouts. 

A short flow example (plain English):
- *Etsy listing draft*: Agent node generates draft listing content → LangGraph emits an interrupt and saves state. Tauri UI shows draft to user. User edits/approves. UI calls LangGraph API to resume with updated state.
- *Printify product creation*: Agent node calls Printify API with new design → before submission, workflow interrupts. UI displays design+price. User approves. On resume, agent finalizes order.
- *Final publish*: Agent calls Etsy API to publish listing → before execution, interrupt. UI asks “Publish now?”. User confirms. Agent resumes to call Etsy.

# 4. Local Postgres Options

A desktop app can use a local database or embedded one. Options:

| Storage Option      | Pros                                                                                     | Cons                                                                                         | Operational Risk           | Fit |
|---------------------|------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------|----------------------------|-----|
| **Local Postgres**  | True multi-user DB, scalable state retention.                                            | Hard to bundle/install on user’s machine; large install size; complex setup.                 | High (user may misconfigure; DB portability issues) | ⚠️ |
| **Remote Postgres** | Offloads storage/admin; known orchestration with LangSmith style.                        | Violates offline/desktop approach; requires network; user lock-in to cloud.                  | High (internet dependency) | ❌ (likely no) |
| **SQLite (Embedded)** | Zero-config, file-based DB; trivial to bundle; supports transactions. Ideal for single-user. | Not networked; single write-lock, but OK for one user. Limited concurrency but fine for one session. | Low (simple, well-known)    | ✅ |
| **File-based JSON/Local** | Simple (no DB).                                                                                                                                      | No concurrency; manual file handling.                                                         | High (corruption risk)     | ⚠️ |
  
**Finding:** Using **SQLite** for the initial local state is recommended. LangGraph provides a `langgraph-checkpoint-sqlite` library for local workflows【18†L816-L824】. SQLite needs no separate server, and the DB is just a file we bundle/manage. Postgres is ideal in production multi-user, but in a desktop app it’s heavy. We can design so that later an export/import to a server Postgres is possible. We should also plan for backup: e.g. allow user to export their DB file. If DB corrupts, the user can restore from backup or reset.  

Backup/restore: periodically copy the SQLite file to a backup location (user could enable auto-backup). If file path issues occur, we should detect missing files and prompt user to locate or recreate. Prefer storing DB in an app-specific folder (e.g. `%APPDATA%/OurApp/` or `~/Library/Application Support/OurApp/`).  

# 5. Local Asset Storage

Generated assets (images, mockups, design files) should be stored in user-accessible folders, not in the database blob. Best practice:
- Create a project directory or workspace for each store or campaign.
- Within it, subfolders for images, backups, etc.
- Store file paths in the DB (or in graph state) rather than binary data.
- Use relative paths or URIs. For example: `/User/Documents/MyApp/Assets/...`.

Cross-platform note: use Rust `tauri::api::path::app_dir` or similar to get an app data dir. Or allow user to choose a root folder via a dialog (Tauri provides `@tauri-apps/api/dialog`).

Tauri side: can use the filesystem APIs to ensure safe access (no direct `file://` in UI due to sandbox). We may copy files into the app-managed folder. For backups, user could copy the whole project folder to external storage. Later, migrating assets to S3 or cloud sync is possible, but out of scope initially. 

Handle broken paths by validating on load (if path not found, mark asset missing and skip or prompt reupload). Avoid storing large files in the DB; use local paths.  

Cross-platform path issues: use forward slashes (Rust & Node normalize) and avoid OS-specific separators in our code. Tauri handles these internally if we use its APIs.

# 6. Secrets and API Keys

We will need to store Etsy/Printify/OpenAI keys. Approaches:
- **OS secure storage**: Use native keychain (e.g. Keytar/Tauri plugin, or Rust `security-framework` on Mac, etc). There are Tauri plugins like `tauri-plugin-secrets` or `tauri-plugin-store`. However, these may still encrypt with a key. Alternatively, rely on OS credential storage: e.g. Windows Credential Manager, macOS Keychain.
- **File with encryption**: If no plugin, store in a config file encrypted (e.g. use a master password or OS encryption key). 
- In any case, do **not** expose keys to the frontend JS. All API calls requiring secrets should be done in the Rust or Python layers. The frontend simply triggers actions (via IPC or HTTP) and never sees the secret value.
- Tauri: the Rust layer (or Python sidecar) holds the secret in memory. Tauri can read it from keychain on startup.
- For OAuth tokens (if Etsy/Printify use OAuth): on local app, we likely do PKCE or similar, then store refresh token securely. Use same approach (keychain or encrypted store). 
- Tauri itself doesn’t have a built-in encrypted store, but one can use `@tauri-apps/plugin-store` with encryption enabled, or use Rust crates for OS keyrings (like `secret-service` on Linux).
- Source: A known approach is PyInstaller + OS keychain, e.g. https://github.com/tauri-apps/tauri/discussions/2359 suggests keyring usage. Without going deep, best practice is OS keystore or env vars.
- **Practical Implication:** We must plan a secure storage (mention use keyring). Do not hardcode or reveal.

| Topic               | Best Practice                                    | Source/Notes           | Practical Implication                                     |
|---------------------|--------------------------------------------------|------------------------|----------------------------------------------------------|
| **Store secrets**   | Use OS native secure storage (Keychain/Keyring)  | Tauri community advice | Avoid plaintext. Use crate (`keyring` or similar) or plugin. |
| **Tauri layer access** | Store keys in Rust side or Python side only    | Best practice          | Only backend uses keys; frontend never sees them.         |
| **OAuth tokens**     | Use PKCE, store refresh token securely (keyring) | Security guidelines    | Handle refresh/expiry in backend; no UI exposure.         |
| **Avoid exposing**  | No secrets in localStorage or JS code            | Web security best practice | Only backend code should read them.                      |

# 7. Background Jobs and App Lifecycle

**Scenario:** Workflows may be running (waiting for prompts, scheduled tasks) when user closes the UI. 

Options:
- **Pause on exit:** Terminate all workflows on exit; require user to complete pending tasks before closing. Risk: user annoyance, lost progress if abrupt.
- **Keep running via background process:** Tauri can have a system tray/tray icon that keeps process alive. The Rust part (and sidecar) could continue with headless execution. On next UI open, it reconnects to running workflows. This is complex but possible: use `tauri-plugin-autostart` or run in background.
- **Separate daemon:** A separate Python daemon could run tasks (like a service). The Tauri app merely attaches to it. Hard to manage on desktop (service installing, permissions).
- **Resume after reboot:** If workflows were in persistent state (LangGraph checkpoints), after reboot the app could restart workflow.

Recommendation: **Pause workflows on exit** by default (show warning if pending tasks). Possibly support a tray to continue scheduled jobs (like daily keyword research). Tauri supports tray, but then the app never fully closes (process remains). If we need periodic research (e.g., SEO polls), a tray daemon or OS scheduler might be needed. For simplicity, first approach: halt on exit and resume later.

| Lifecycle Question                        | Options                                            | Recommendation       | Risks                                                                                       |
|-------------------------------------------|----------------------------------------------------|----------------------|--------------------------------------------------------------------------------------------|
| Continue when UI closes?                  | - Pause and save state<br>- Keep running in tray/daemon| *Pause by default* | If user expects background tasks, they may be surprised. Keep minimal to avoid orphan processes. |
| Tauri tray app?                           | Tauri can create a tray icon and run in background | Use only if needed  | Tray apps can be confusing. If we need 24/7 tasks, consider later.                          |
| Sidecar process after UI close?           | Can spawn on tray or keep independent            | Not now             | Complex (could become orphan).                                                               |
| Pending approvals while offline?          | Pending state saved in DB; resume on next run       | Yes                 | If app closed, user must reopen to act.                                                     |
| Scheduled jobs (cron)?                    | Build internal scheduler (in Python) or rely on tray | Investigate later   | OS crons not user-friendly. Internal job queue possible.                                    |
| Reboot handling                          | On restart, resume any saved threads              | Yes                 | Use LangGraph persistence (thread_id) to pick up.                                          |

# 8. Observability / Debugging in Desktop Context

We want to be able to debug workflows and capture logs, even though this is a local app. 

- **Open-source LangGraph:** Provides logging hooks and state inspection via API, but no built-in GUI. 
- **LangSmith (paid):** Not intended for local dev in production app; could use free tier during development to trace runs by connecting to LangSmith.
- **Self-host options:** Langfuse or other observability tools could be integrated, but add complexity.
- **Logging:** Tauri (Rust) and Python sidecar should log to console or files. We should centralize logging (Rust and Python can write to same log file/directory).
- **Graph state:** We could implement a debug mode that dumps checkpoint state to a JSON for inspection. Or provide an admin UI to query `graph.get_state_history()`.
- **Frontend events:** Use `@tauri-apps/api/log` or similar to capture UI logs if needed.
- **Recommendation:** In development, use verbose logging and possibly LangSmith tracing. In production, keep logs minimal but with options to export trace for support. We should ensure the desktop app has a “view logs” or “report issue” button.

| Observability Need                 | Option                                 | Pros                                         | Cons                                        | Fit for Desktop                        |
|------------------------------------|----------------------------------------|---------------------------------------------|---------------------------------------------|----------------------------------------|
| **Trace workflow runs**            | LangSmith / LangFuse / custom tracking | LangSmith gives UI, Langfuse open-source    | Requires internet (LangSmith), more setup   | Use LangSmith for dev; local logging prod |
| **Inspect graph state**            | LangGraph API (`get_state()`)          | Can retrieve checkpoints via Python API     | No built-in UI; must code tool/UI           | Implement an admin endpoint or UI tab  |
| **Tool call logs**                 | Custom logging (Python logger)         | Full control (stdout or file)               | Need to filter sensitive info              | Necessary (HTTP calls, errors)         |
| **Frontend logs**                  | Tauri/Rust logging + devtools          | Standard (console, file)                    | Mixed languages (Rust, JS)                  | OK, just separate channels             |
| **Workflow errors**                | Catch exceptions & show UI message     | Notifies user; stores error checkpoint (dead-letter) | Need UX for error recovery             | Implement retries or user alert       |
| **Costs/tokens**                   | LangSmith provides, custom no         | LangSmith tracking; local tooling harder    | Could omit (not needed in local)            | Skip for now (not cost-critical)       |

No single integrated observability exists for a local LangGraph. The team should plan to use Python debugging tools (pdb, logging) and possibly LangSmith in testing. For long-term, consider integrating Langfuse or an on-prem Grafana if needed, but likely overkill.

# 9. Tauri vs Electron Sanity Check

We compare Tauri to Electron for our specific needs:

| Criterion                  | **Tauri**                                 | **Electron**                            | Better Fit    | Notes                                 |
|----------------------------|-------------------------------------------|-----------------------------------------|---------------|---------------------------------------|
| **Packaging Python**       | Supports sidecars (Rust spawns Python)【23†L234-L239】. Requires PyInstaller. | Can launch Python via Node `child_process` or via native Node addons. | Tie          | Both require bundling Python; Tauri gives OS child_process easier (Rust). |
| **Local files/assets**     | Excellent (direct filesystem access via Rust APIs). | Excellent (Node fs APIs).           | Tie           | Both handle local files well.         |
| **Native OS integration**  | Good (Rust can call native libs; system dialogs). | Very good (Node.js has many packages). | Slight Electron | Electron mature ecosystem, but Tauri can FFI Rust. |
| **Auto-update**            | Supported via `tauri-updater` (integrates with GitHub/S3). | Well-supported (electron-updater).   | Tie           | Both have solution.                   |
| **Cross-platform build**   | Requires Rust + Node toolchains; good cross-compilation for macOS/Windows. | Node-based, large but mature.      | Electron      | Electron is easier (npm only). Tauri needs Rust targets. |
| **Security**               | Strong sandbox by default; fewer vulnerabilities. | More attack surface (bundled Chromium). | Tauri        | Tauri win (less memory, locked-down by default)【21†L318-L320】. |
| **App size**               | Very small (~10-20MB for base app).       | Large (~50-100MB with Chromium).    | Tauri        | Tauri significantly smaller binary size. |
| **Dev velocity**           | Slower (Rust knowledge required for native parts). | Faster (pure JS/Node).              | Electron     | Electron allows full JS stack.        |
| **Debugging**              | Rust+JS stacks; tooling improving.       | Mature devtools, easy to debug.     | Electron     | Electron's maturity makes debugging straightforward. |
| **Community/maturity**     | Newer (Tauri v2 matured recently).       | Very mature, lots of examples.       | Electron     | Electron has bigger community, more plugins. |
| **Long-term maintainability** | Leaner, future-proof (Rust performance). | Depend on Chromium updates.        | TBD          | Electron heavy but common.            |

**Conclusion:** Tauri offers smaller, more secure apps at the cost of some developer complexity. For our desktop-first, single-user scenario, Tauri is appealing (especially if Rust skill is available). Electron has a faster dev cycle but bloated output. Given the team is comfortable with React/TS and adding Rust is a one-time learning, **Tauri is likely better** for production reliability and size【21†L318-L320】. But Electron should not be dismissed if quick prototyping or team skill dictates.

# 10. Practical Conclusions

**Best Architecture Candidate:** A Tauri desktop app (React/TypeScript frontend) with a bundled Python/FastAPI sidecar running LangGraph. Use SQLite for local state. Store secrets via OS keychain. Use LangGraph for orchestrating stateful workflows with human approval gates.

**Main Unknowns:** 
- The complexity of packaging Python reliably on each OS.
- User experience for handling background tasks vs closing app.
- Ensuring resilience on interruptions (e.g. crashes).
- Full observability strategy (likely outside open source scope).

**Things To Test Before Committing:**
- Prototype packaging: build a PyInstaller executable of our Python backend and ensure Tauri can spawn it and communicate.
- Implement a simple LangGraph workflow with a “pause” state to verify the Tauri UI can resume it.
- Try LangGraph’s Postgres saver vs SQLite in local mode.
- Evaluate Tauri’s tray capabilities for any needed background scheduling.

**Bad Ideas to Avoid:**
- **Fully remote backend**: breaks the “desktop-first” goal and offline use-case.
- **Unmanaged auto-publishing**: We must never auto-post to Etsy/Printify without review (policy risk).
- **Ignoring OS security**: e.g. storing keys in plain config.

**Recommended Next Research Topic:** Investigate Etsy/Printify API integration specifics (already started), and perhaps mock up the first LangGraph + Tauri proof-of-concept for a simple workflow (e.g. “draft title with LLM, wait for user approval, log result”). This will validate many of the above assumptions (communication, state, approval gate).

**Open Questions:** 
- How will we surface LangGraph workflow state to the user (via WebSocket, polling, or REST hooks)? 
- Should we consider using LangSmith in development to simplify state visualization?

