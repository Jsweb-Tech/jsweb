import re
from typing import Dict, List, Tuple, Optional, Callable, any


class NotFound(Exception):
    """
    Raised when a route is not found.
    """
    pass


class MethodNotAllowed(Exception):
    """
    Raised when a method is not allowed for a route.
    """
    pass


class Route:
    # Class-level type converters to be shared across all Route instances
    TYPE_CONVERTERS = {
        'str': (str, r'[^/]+'),
        'int': (int, r'\d+'),
        'path': (str, r'.+?')
    }
    """
    Represents a single route with path, handler, and parameter conversion.
    """
    def __init__(self, path: str, handler: Callable, methods: List[str], endpoint: str):
        self.path = path
        self.handler = handler
        self.methods_set = set(methods) #set for faster method checking
        self.endpoint = endpoint
        self.converters = {}
        self.is_static = '<' not in path # Be this a Flag for static routes
        if not self.is_static:
            self.regex, self.param_names = self._compile_path()
        else:
            self.regex = None
            self.param_names = []
        

    def _compile_path(self):
        """
        Compiles the path into a regex and extracts parameter converters.
        """
        
        param_defs = re.findall(r"<(\w+):(\w+)>", self.path)
        regex_path = "^" + self.path + "$"
        param_names = []

        for type_name, param_name in param_defs:
            converter, regex_part = self.TYPE_CONVERTERS.get(type_name, self.TYPE_CONVERTERS['str'])
            regex_path = regex_path.replace(f"<{type_name}:{param_name}>", f"(?P<{param_name}>{regex_part})")
            self.converters[param_name] = converter
            param_names.append(param_name)

        return re.compile(regex_path), param_names

    def match(self, path):
        """
        Matches the given path against the route's regex and returns converted parameters.
        """

        #For static routes, string comparison is much faster than regex
        if self.is_static:
            return {} if path == self.path else None
        
        # For dynamic routes, use pre-compiled regex
        match = self.regex.match(path)
        if not match:
            return None

        params = match.groupdict()
        try:
            for name, value in params.items():
                params[name] = self.converters[name](value)
            return params
        except (ValueError, TypeError):
            return None


class Router:
    """
    Handles routing by mapping URL paths to view functions and endpoint names.
    """
    def __init__(self):
        self.static_routes: Dict[str, Route] = {}
        self.dynamic_routes: List[Route] = []
        self.endpoints: Dict[str, Route] = {}  # For reverse lookups (url_for)
        self.static_url_path = None
        self.static_dir = None


    def add_route(self, path: str, handler: Callable, methods: Optional[List[str]]=None, endpoint: Optional[str]=None):
        """
        Adds a new route to the router.
        """
        if methods is None:
            methods = ["GET"]
        
        if endpoint is None:
            endpoint = handler.__name__

        if endpoint in self.endpoints:
            raise ValueError(f"Endpoint \"{endpoint}\" is already registered.")

        route = Route(path, handler, methods, endpoint)

        if route.is_static:
            self.static_routes[path] = route
        else:
            self.dynamic_routes.append(route)

    def route(self, path: str, methods:Optional[List[str]]=None, endpoint:Optional[str]=None):
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
        """
        if path in self.static_routes:
            route = self.static_routes[path]
            if method in route.methods_set:
                return route.handler, {}
            raise MethodNotAllowed(f"Method {method} not allowed for path {path}.")
        #here we can check method before expensive regex matching, we iterate with pre-compiled patterns
        for route in self.dynamic_routes:
            if method not in route.methods_set: # Quick rejection, checking method first is cheap
                continue
            # Now we do the expensive regex matching
            params = route.match(path)
            if params is not None:
                    return route.handler, params
        raise NotFound(f"No route found for {path}")

    def url_for(self, endpoint, **params):
        """
        Generates a URL for a given endpoint and parameters.
        """
        if endpoint not in self.endpoints:
            raise ValueError(f"No route found for endpoint '{endpoint}'.")

        route = self.endpoints[endpoint]
        path = route.path

        if route.is_static:
            return path

        for param_name in route.param_names:
            if param_name not in params:
                raise ValueError(f"Missing parameter '{param_name}' for endpoint '{endpoint}'.")
            
            for type_name in Route.TYPE_CONVERTERS.keys():
                pattern = f"<{type_name}:{param_name}>"
                if pattern in path:
                    path = path.replace(pattern, str(params[param_name]))
                    break
        
        return path
