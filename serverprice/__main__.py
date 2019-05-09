import argparse
from .platform.aliyun import Aliyun
from prettytable import PrettyTable

def print_table(r, allow_keys=None):
    x = PrettyTable()
    # collect all possible keys
    keys = []
    for row in r:
        keys += row.keys()
    keys = sorted(list(set(keys)))
    if allow_keys is not None:
        keys = allow_keys
    x.field_names = keys
    for data in r:
        row = []
        for k in keys:
            row.append(data.get(k,''))
        x.add_row(row)
    x.align = "r"
    print(x)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("action")
    parser.add_argument("platform")
    parser.add_argument("-c", "--cpu", type=int,
                    help="cpu cores count")
    parser.add_argument("-m", "--memory", type=int,
                    help="memory MB")
    parser.add_argument("-r", "--region", type=str,
                    help="region id")
    args = parser.parse_args()

    result = None
    allow_keys = None
    if args.platform == 'aliyun':
        if args.action == 'list_region':
            result = Aliyun.list_region()
            allow_keys = None
        elif args.action == 'list_vm':
            result = Aliyun.list_vm()
            allow_keys = ['cpu', 'memory', 'value', 'text', 'family']
        elif args.action == 'get':
            result = Aliyun.get_price_by_spec(args.region, args.cpu, args.memory)
    if result is not None:
        print_table(result, allow_keys=allow_keys)

if __name__ == '__main__':
    main()