"""
Parse Bank of America stmt.txt files.
"""
import re
import json
import argparse

import time
from time import mktime

from datetime import datetime
from collections import namedtuple

Entry = namedtuple("entry", "date description change balance")

def json_encoder(obj):
    if isinstance(obj) is datetime:
        return str(obj)


def print_change(e):
    print("[{}] - [{}] - {}".format(str(e.date), e.change, e.description))


def summarize_group(e, name):
    print("Summary: {} [{}]".format(name, len(e)))
    print("Total: {}".format(sum([x.change for x in e])))
    print("Largest: {}".format(max([x.change for x in e])))
    print("Smallest: {}".format(min([x.change for x in e])))


def filter_entry(x, args):
    if args.hide_transfers:
        if "Online Banking transfer" in x.description:
            return False
    return True


def withdrawls(entries, args):
    return [x for x in entries if x.change < 0 and filter_entry(x, args)]


def deposits(entries, args):
    return [x for x in entries if x.change > 0 and filter_entry(x, args)]


def transactions(raw):
    exp = re.compile("^(\d{2}/\d{2}/\d{4})\s+(.*)\s\s([-|.|,|\d]+)\s+([\d|,|.]+)")
    entries = []
    for line in raw.split("\n"):
        match = exp.match(line.strip())
        if match:
            e = Entry(
                datetime.fromtimestamp(mktime(
                    time.strptime(match.groups()[0], "%m/%d/%Y")
                )),
                match.groups()[1].strip(),
                float(match.groups()[2].replace(",", "")),
                float(match.groups()[3].replace(",", ""))
            )
            entries.append(e)
    return entries


def main():
    parser = argparse.ArgumentParser("boa_parser")
    parser.add_argument("--path", help="path to statement txt file", default="stmt.txt")
    parser.add_argument("--withdrawls", help="show withdrawls", action="store_true", default=False)
    parser.add_argument("--deposits", help="show deposits", action="store_true", default=False)
    parser.add_argument("--hide_transfers", action="store_true", default=False)
    parser.add_argument("--json", action="store_true", default=False)
    args = parser.parse_args()
    with open(args.path, "r") as fp:
        entries = transactions(fp.read())
    if args.deposits:
        summarize_group(deposits(entries, args), "Deposits")
        [print_change(x) for x in deposits(entries, args)]
    if args.withdrawls:
        summarize_group(withdrawls(entries, args), "Withdrawls")
        [print_change(x) for x in withdrawls(entries, args)]
    if args.json:
        print(json.dumps(entries, indent=4, default=json_encoder))


if __name__ == '__main__':
    main()
