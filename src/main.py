import os
import sys
from fastmcp import FastMCP

# Initialize Unified Server
mcp = FastMCP("TriOptima Team Agentic Tools")

# --- Dynamic Feature Loading ---

# Load Conductor Module if toggled
if os.getenv("ENABLE_CONDUCTOR") == "true":
    from src.conductor import register_conductor_tools
    register_conductor_tools(mcp)

# Load Superpowers Module if toggled
if os.getenv("ENABLE_SUPERPOWERS") == "true":
    from src.superpowers import register_superpowers_tools
    register_superpowers_tools(mcp)

if __name__ == "__main__":
    # Ensure it's running via stdio connection
    mcp.run()
