from server import mcp

# Import tools so they get registered via decorators
import tools.retrieve
import tools.metrics
import tools.plot

if __name__ == "__main__":
    mcp.run()
