def register_conductor_tools(mcp):
    @mcp.tool()
    def conductor_status() -> str:
        """Get the status of the Conductor module."""
        return "Conductor module is active and ready."
