import re

class Router:
    """
    Handles routing by mapping URL paths to view functions and endpoint names.
    """
    def __init__(self):
        self.routes = []
        self.endpoints = {}  # For reverse lookups (url_for)

    def add_route(self, path, handler, methods=None, endpoint=None):
        """
        Adds a new route to the router.
        """
        if methods is None:
            methods = ["GET"]
        
        if endpoint is None:
            endpoint = handler.__name__

        if endpoint in self.endpoints:
            raise ValueError(f"Endpoint \"{endpoint}\" is already registered.")

        self.routes.append((path, handler, methods))
        self.endpoints[endpoint] = path

    def route(self, path, methods=None, endpoint=None):
        """
        A decorator to register a view function for a given URL path.
        """
        def decorator(handler):
            self.add_route(path, handler, methods, endpoint)
            return handler
        return decorator

    def resolve(self, path, method):
        """
        Finds the appropriate handler for a given path and HTTP method.
        Also handles typed URL parameters like <int:id>.
        """
        for route_path, handler, allowed_methods in self.routes:
            if method not in allowed_methods:
                continue

            # Define converters for URL parameter types
            type_converters = {
                'str': (str, r'[^/]+'),
                'int': (int, r'\d+'),
                'path': (str, r'.+?')
            }

            param_defs = re.findall(r"<(\w+):(\w+)>", route_path)
            regex_path = "^" + route_path + "$"

            # Build the final regex for matching the URL
            for type_name, param_name in param_defs:
                converter, regex_part = type_converters.get(type_name, type_converters['str'])
                regex_path = regex_path.replace(f"<{type_name}:{param_name}>", f"(?P<{param_name}>{regex_part})")

            match = re.match(regex_path, path)
            if match:
                params = match.groupdict()
                # Convert captured parameters to their specified types
                try:
                    for type_name, param_name in param_defs:
                        converter, _ = type_converters.get(type_name, type_converters['str'])
                        if param_name in params:
                            params[param_name] = converter(params[param_name])
                    return handler, params
                except ValueError:
                    # If type conversion fails, this route does not match.
                    continue

        return None, None
