from prance import ResolvingParser

def parse_swagger_spec(url_to_spec_file: str) -> dict:
    """Parses and validates an OpenAPI spec from a URL."""
    try:
        parser = ResolvingParser(url_to_spec_file)
        return parser.specification # This is the fully resolved spec as a dict
    except Exception as e:
        print(f"Error parsing specification: {e}")
        return None
    

res = parse_swagger_spec("https://petstore.swagger.io/v2/swagger.json")
print(res)