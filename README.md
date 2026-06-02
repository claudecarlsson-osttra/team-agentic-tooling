# team-agentic-tooling

This is the production-grade, full architectural specification for our unified AI tooling ecosystem.

By integrating **GitHub** (for source control and CI/CD), **Artifactory** (as your private container registry), and a local **Shell Wrapper**, you create a zero-friction loop where developers simply type `gemini` and instantly chat with an agent empowered by up-to-date corporate tooling.

## 🏗️ 1. Complete Architecture & Data Flow

### The Lifecycle Components:

1. **The Build (GitHub):** Developers commit new skills or agentic extensions to `team-agentic-tooling`. GitHub Actions compiles the Python environment and builds a secure Docker image.
2. **The Registry (Artifactory):** The compiled image is pushed to `artifactory.trioptima.net`. This acts as the single source of truth for the team's AI capabilities.
3. **The Execution (Developer Local):** Typing `gemini` triggers an instantaneous manifest handshake with Artifactory. If a newer image version exists, it streams down the diffs. Gemini CLI drops the user into an interactive loop, while the container serves tools in the background via `stdio`.

## 💾 2. Source Repo Specification

This repository manages, builds, and publishes the unified image.

- `.github/workflows/publish.yml`: CI/CD Automations
- `src/main.py`: MCP Server Entrypoint (FastMCP)
- `src/conductor.py`: Conductor Skill Module
- `src/superpowers.py`: Superpowers Skill Module
- `Dockerfile`: Light-weight production runtime
- `requirements.txt`: Engine dependencies

## 💻 3. Client Repo Specification (Developer Machine)

To make it seamless for developers, any project repository they work on daily just needs a small configuration configuration file and a global terminal hook.

### Local Project Config (`.mcp-config.json`)

Drop this file in the root directory of your active application projects.

```json
{
  "mcpServers": {
    "trioptima-unified-agent": {
      "command": "docker",
      "args": [
        "run",
        "-i",
        "--rm",
        "--pull", "always",
        "-v", "${PWD}:/workspace",
        "-e", "ENABLE_CONDUCTOR",
        "-e", "ENABLE_SUPERPOWERS",
        "-e", "ARTIFACTORY_API_KEY",
        "-e", "GITHUB_TOKEN",
        "artifactory.trioptima.net/docker-local/team-agentic-tooling:latest"
      ]
    }
  }
}
```

### The Terminal Shortcut Hook

Add this wrapper function to your team's global dotfile setups.

#### For **Fish Shell** (`~/.config/fish/functions/gemini.fish`):

```fish
function gemini
    if test -f .env
        export (cat .env | grep -v '^#' | xargs) 2>/dev/null
    end

    echo "🤖 Initializing Agent Work environment..."
    echo "🔄 Checking artifactory.trioptima.net for updated AI Skills..."

    npx @google/gemini-cli --config .mcp-config.json
end
```

#### For **Zsh / Bash** (`~/.zshrc`):

```bash
gemini() {
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs) 2>/dev/null
    fi
    echo "🤖 Initializing Agent Work environment..."
    echo "🔄 Checking artifactory.trioptima.net for updated AI Skills..."
    
    npx @google/gemini-cli --config .mcp-config.json
}
```

## 🔒 4. Authentication Matrix

1. **The Standard Approach:** Developers run `docker login artifactory.trioptima.net` once.
2. **The Zero-Onboarding Wrapper Approach:** Check for auth automatically:
```bash
if ! docker system info | grep -q "artifactory.trioptima.net"; then
    echo "🔒 Logging into TriOptima Artifactory..."
    echo "$ARTIFACTORY_TOKEN" | docker login artifactory.trioptima.net --username "$ARTIFACTORY_USER" --password-stdin
fi
```
