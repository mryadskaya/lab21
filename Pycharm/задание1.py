#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os.path
import sys


def add_flight(flights, destination, departure_date, aircraft_type):

    flights.append(
        {
            "name": name,
            "знак зодиака": post,
            "year": year,
        }
    )

    return flights


def display_flights(flights):

    if flights:
        line = "+-{}-+-{}-+-{}-+-{}-+".format(
            "-" * 4, "-" * 30, "-" * 20, "-" * 8
        )
        print(line)
        print(
            "| {:^4} | {:^30} | {:^20} | {:^8} |".format(
                "No", "Name", "знак зодиака ", "year"
            )
        )
        print(line)
        for idx, flight in enumerate(flights, 1):
            print(
                "| {:>4} | {:<30} | {:<20} | {:>8} |".format(
                    idx,
                    flight.get("name", ""),
                    flight.get("знак зодиака", ""),
                    flight.get("year", ""),
                )
            )
            print(line)
    else:
        print("List of flights is empty.")


def select_flights(flights, date):

    result = []
    for flight in flights:
        if flight.get("year") == date:
            result.append(flight)
    return result


def save_flights(file_name, flights):

    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(flights, fout, ensure_ascii=False, indent=4)


def load_flights(file_name):

    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


def main(command_line=None):
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "-f",
        "--data",
        action="store",
        required=False,
        help="The data file name",
    )

    parser = argparse.ArgumentParser("flights")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")

    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new flight"
    )
    add.add_argument(
        "-d",
        "--name",
        action="store",
        required=True,
        help="name of the flight",
    )
    add.add_argument(
        "-dd",
        "--знак зодиака",
        action="store",
        required=True,
        help="знак зодиака date of the flight",
    )
    add.add_argument(
        "-at",
        "--year",
        action="store",
        required=True,
        help="year type of the flight",
    )

    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all flights"
    )

    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select flights by departure date",
    )
    select.add_argument(
        "-D",
        "--date",
        action="store",
        required=True,
        help="Departure date to select flights (YYYY-MM-DD)",
    )

    args = parser.parse_args(command_line)
    filename = args.data
    if not filename:
        filename = os.environ.get("maripython")
    if not filename:
        print("The data file name is absent", file=sys.stderr)
        sys.exit(1)

    is_dirty = False
    if os.path.exists(filename):
        flights = load_flights(filename)
    else:
        flights = []

    if args.command == "add":
        flights = add_flight(
            flights,
            args.name,
            args.post,
            args.year,
        )
        is_dirty = True

    elif args.command == "display":
        display_flights(flights)

    elif args.command == "select":
        selected = select_flights(flights, args.date)
        display_flights(selected)

    if is_dirty:
        save_flights(filename, flights)


if __name__ == "__main__":
    main()