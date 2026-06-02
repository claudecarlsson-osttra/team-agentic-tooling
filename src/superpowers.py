def register_superpowers_tools(mcp):
    @mcp.tool()
    def superpowers_status() -> str:
        """Get the status of the Superpowers module."""
        return "Superpowers module is active and ready."
