'''Utility functions for tests'''


def get_mock_response(filename: str) -> str:
    with open(f'tests/mock_responses/{filename}', 'r') as response:
        response_json = response.read()
    return response_json
