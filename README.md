# team-agentic-tooling

This is the production-grade, full architectural specification for our unified AI tooling ecosystem.

By integrating **GitHub** (for source control and CI/CD), **Artifactory** (as your private container registry), and a local **Shell Wrapper**, you create a zero-friction loop where developers simply type `gemini` and instantly chat with an agent empowered by up-to-date corporate tooling.

## 🏗️ 1. Complete Architecture & Data Flow

### The Lifecycle Components:

1. **The Build (GitHub):** Developers commit new skills or agentic extensions to `team-agentic-tooling`. GitHub Actions lints, compiles the Python environment, and builds a secure Docker image using a non-root user.
2. **The Registry (Artifactory):** The compiled image is pushed to `artifactory.trioptima.net`. This acts as the single source of truth for the team's AI capabilities.
3. **The Execution (Developer Local):** Typing `gemini` triggers an instantaneous manifest handshake with Artifactory. If a newer image version exists, it streams down the diffs. Gemini CLI drops the user into an interactive loop, while the container serves tools in the background via `stdio`.

## 💾 2. Source Repo Specification

This repository manages, builds, and publishes the unified image. The Python backend uses a **Dynamic Plugin Architecture** to ensure high modularity. 

- `.github/workflows/publish.yml`: CI/CD Automations with Linting & Validation
- `src/main.py`: MCP Server Entrypoint (FastMCP) with dynamic module loading.
- `src/skills/`: Drop new Python files here (e.g. `conductor.py`, `superpowers.py`) with a `register(mcp)` function. No need to touch `main.py`!
- `Dockerfile`: Production runtime (runs as non-root `appuser`)
- `requirements.txt`: Engine dependencies

## 💻 3. Client Repo Specification (Zero-Config Developer Workflow)

To make it completely frictionless for developers, they only need to add this global wrapper function to their shell profile. It auto-generates the necessary MCP config on the fly and maps volume ownership directly to the developer's user ID.

### The Terminal Shortcut Hook

#### For **Zsh / Bash** (`~/.zshrc` or `~/.bashrc`):

```bash
gemini() {
    # 1. Load local env vars if present
    if [ -f .env ]; then
        export $(cat .env | grep -v '^#' | xargs) 2>/dev/null
    fi
    
    echo "🤖 Initializing Agent Work environment..."
    echo "🔄 Checking artifactory.trioptima.net for updated AI Skills..."
    
    # 2. Zero-Friction Config Injection
    local CONFIG_FILE=".mcp-config.json"
    
    if [ ! -f "$CONFIG_FILE" ]; then
        CONFIG_FILE=$(mktemp)
        cat <<EOF > "$CONFIG_FILE"
{
  "mcpServers": {
    "trioptima-unified-agent": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm", "--pull", "always",
        "--user", "$(id -u):$(id -g)",
        "-v", "${PWD}:/workspace",
        "-e", "ENABLE_CONDUCTOR=true",
        "-e", "ENABLE_SUPERPOWERS=true",
        "-e", "ARTIFACTORY_API_KEY",
        "-e", "GITHUB_TOKEN",
        "artifactory.trioptima.net/docker-local/team-agentic-tooling:latest"
      ]
    }
  }
}
EOF
    fi

    # 3. Launch the agent
    npx @google/gemini-cli --config "$CONFIG_FILE"
}
```

## 🔒 4. Authentication Matrix

1. **The Standard Approach:** Developers run `docker login artifactory.trioptima.net` once.
2. **The Zero-Onboarding Wrapper Approach:** Check for auth automatically inside the wrapper:
```bash
if ! docker system info | grep -q "artifactory.trioptima.net"; then
    echo "🔒 Logging into TriOptima Artifactory..."
    echo "$ARTIFACTORY_TOKEN" | docker login artifactory.trioptima.net --username "$ARTIFACTORY_USER" --password-stdin
fi
```
