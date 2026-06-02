import os
import sys
import importlib
import pkgutil
from fastmcp import FastMCP

# Initialize Unified Server
mcp = FastMCP("TriOptima Team Agentic Tools")

# --- Dynamic Plugin Architecture ---
# This allows developers to simply drop new modules into `src/skills`
# without ever needing to modify `main.py`. It promotes extreme modularity.
import src.skills as skills_package

def load_skills():
    """Iterate over the skills directory and load based on env flags."""
    for _, module_name, _ in pkgutil.iter_modules(skills_package.__path__):
        # Convention: If the module is named `conductor`, look for `ENABLE_CONDUCTOR`
        env_flag = f"ENABLE_{module_name.upper()}"
        
        # We default to "false" to ensure safe, opt-in behavior for each project workspace
        is_enabled = os.getenv(env_flag, "false").lower() == "true"
        
        if is_enabled:
            try:
                module = importlib.import_module(f"src.skills.{module_name}")
                if hasattr(module, "register"):
                    module.register(mcp)
                    print(f"✅ Loaded skill module: {module_name}", file=sys.stderr)
                else:
                    print(f"⚠️ Warning: Module {module_name} missing 'register(mcp)' function.", file=sys.stderr)
            except Exception as e:
                print(f"❌ Failed to load {module_name}: {e}", file=sys.stderr)

if __name__ == "__main__":
    load_skills()
    
    # Ensure it's running via stdio connection
    mcp.run()
