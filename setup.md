# Setup

This guide consolidates the setup instructions for the **Build** and **Break** phases of the workshop. Complete these steps before starting either phase.

You'll need a terminal (PowerShell on Windows). The workshop repo will be shared later,clone it locally once the link is shared by the instructors.

---

## 1. Install uv

**uv** is the Python package manager used to run the MCP servers in this repo.
**Reference:** [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/)

### macOS

- **Standalone (recommended):**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **Homebrew:** `brew install uv`
- **MacPorts:** `sudo port install uv`

### Windows

- **PowerShell (recommended):**
  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```
- **WinGet:** `winget install --id=astral-sh.uv -e`
- **Scoop:** `scoop install main/uv`

### Linux

- **Standalone (recommended):**
  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
- **PyPI (if you have pip):** `pipx install uv` or `pip install uv`
- **Cargo (if you have Rust):** `cargo install --locked uv`

---

## 2. Install Node.js and npx

**Node.js** and **npm** are required so you can run **MCPJam Inspector** via `npx` (no global install needed). **npx** is included with npm.

### Check if you have them already installed

```bash
node -v 
npm -v
npx -v
```
If you see a version number for all three, you can skip this step and proceed to step 3.

### macOS

- **Official installer:** Download the LTS version from [nodejs.org](https://nodejs.org/) and run the installer.
- **Homebrew:**
  ```bash
  brew update && brew install node
  ```
  If `npx` is not available after installing Node, close and reopen your terminal, then run `npx -v`.
- **Version manager (avoids permission issues):** [nvm](https://github.com/nvm-sh/nvm) or [fnm](https://github.com/Schniz/fnm).

### Windows

- **Official installer:** Download the LTS version from [nodejs.org](https://nodejs.org/) and run the installer. npm and npx are included.
- **WinGet:** `winget install OpenJS.NodeJS.LTS`
- **Version manager:** [nvm-windows](https://github.com/coreybutler/nvm-windows).

### Linux

- **NodeSource (recommended):** See [Installing Node.js via package manager](https://nodejs.org/en/download/package-manager) for your distro (e.g. Ubuntu/Debian, Fedora, etc.).
- **Package manager examples:**
  - **Debian/Ubuntu:** `sudo apt update && sudo apt install nodejs npm`
  - **Fedora/RHEL:** `sudo dnf install nodejs npm`
  - **Arch:** `sudo pacman -S nodejs npm`
- **Version manager:** [nvm](https://github.com/nvm-sh/nvm), [n](https://github.com/tj/n), or [fnm](https://github.com/Schniz/fnm).

After installing, run `node -v` (and optionally `npm -v`, `npx -v`) again to confirm. Node v18 or newer is recommended.

---

## 3. Run MCPJam Inspector

MCPJam Inspector is the client you’ll use to connect to and test MCP servers (Build and Break).

1. Start the inspector in your terminal:

   ```bash
   npx @mcpjam/inspector@latest
   ```

2. MCPJam Inspector will open in your browser.
3. Sign in to use freely available models.

**Reference:** [MCPJam Inspector](https://github.com/MCPJam/inspector)

---

## 4. Join the Slack workspace

**[Join Build Break Defend MCP on Slack](https://join.slack.com/t/buildbreakdefend-mcp/shared_invite/zt-3r2jeltsn-djKDIBTNxpnorDww9Hbn_Q)**

Use this workspace to ask facilitators for support, hints, and discussions during the workshop. Post your questions/threads in #wicys-workshop channel

---

# Next Steps

Once your setup is complete, you're all set! Join the Slack workspace and follow the channel for updates. The main repo will be shared closer to the workshop.