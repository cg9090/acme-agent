import requests

class MCPClient:

    def __init__(self, base_url: str):
        self.base_url = base_url
        self._tools_cache = None

    def list_tools(self):
        if self._tools_cache is not None:
            return self._tools_cache
        
        self._tools_cache = requests.get(f"{self.base_url}/tools").json()
        return self._tools_cache

    def execute_tool(self, tool_name, args):
        return requests.post(
            f"{self.base_url}/tools/execute",
            json={
                "tool": tool_name,
                "args": args
            }
        ).json()