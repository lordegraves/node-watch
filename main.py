import json

from nodewatch.service import get_node_data


def main():
    node_data = get_node_data()
    print(json.dumps(node_data, indent=2))


if __name__ == "__main__":
    main()