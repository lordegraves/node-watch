import json

from nodewatch.service import get_node_data


def main():
    try:
        node_data = get_node_data()
        print(json.dumps(node_data, indent=2))
    except Exception as exc:
        print(
            json.dumps(
                {
                    "error": "nodewatch execution failed",
                    "detail": str(exc),
                },
                indent=2,
            )
        )


if __name__ == "__main__":
    main()