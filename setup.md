# Setup

This guide consolidates the setup instructions for the **Build** and **Break** phases of the workshop. Complete these steps before starting either phase.

---

## 1. Install uv

**uv** is the Python package manager used to run the MCP servers in this repo.

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

**Reference:** [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/)

---

## 2. Install Node.js and npx

**Node.js** and **npm** are required so you can run **MCPJam Inspector** via `npx` (no global install needed). **npx** is included with npm.

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

### Verify (all platforms)

```bash
node -v   # expect v18 or newer
npm -v
npx -v
```

---

## 3. Run MCPJam Inspector

MCPJam Inspector is the client you’ll use to connect to and test MCP servers (Build and Break).

1. Start the inspector:

   ```bash
   npx @mcpjam/inspector@latest
   ```

2. MCPJam Inspector will open in your browser.
3. Sign in to use freely available models.

For Build and Break, add servers in MCPJam with **Connection type: STDIO** and the command given in each phase’s README (`1-build/README.md` or `2-break/README.md`).

---

## 4. Join the Slack workspace

Join the workshop Slack workspace for support, hints, and discussion:

**[Join Build Break Defend MCP on Slack](https://join.slack.com/t/buildbreakdefend-mcp/shared_invite/zt-3r2jeltsn-djKDIBTNxpnorDww9Hbn_Q)**

Use this workspace to ask facilitators for help, share progress, and get updates during the workshop.

---

## Next steps

- **Build phase:** See [1-build/README.md](1-build/README.md) for dependencies, API keys, and running the Local Discovery server.
- **Break phase:** See [2-break/README.md](2-break/README.md) for running the CTF challenge servers.
