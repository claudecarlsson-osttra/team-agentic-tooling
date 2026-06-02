def register(mcp):
    @mcp.tool()
    def superpowers_status() -> str:
        """Get the status of the Superpowers module."""
        return "Superpowers module is dynamically active and ready."
