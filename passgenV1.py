#!/usr/bin/env python3

from math import log2
import secrets
import argparse
import string
import subprocess

##Define global defaults if, for example, -l has no args
DEFAULT_COUNT = 1
DEFAULT_LEN = 16
MINIMUM_LEN = 8
SIMILAR_CHARS = "0Ool1I"
DEFAULT_MIN_NUM = 1
DEFAULT_MIN_SYM = 1


def argument_parser():
    ## Define terminal/user arguments, all defaults to true if none given except for -l, defaults to 16
    parser = argparse.ArgumentParser(
        prog="PyPassgen", description="generate a password"
    )
    parser.add_argument(
        "-l",
        default=DEFAULT_LEN,
        type=int,
        metavar="int",
        help=f"Specify a password length, defaults to {DEFAULT_LEN}",
    )
    parser.add_argument("-u", action="store_true", help="Use lowercase letters")
    parser.add_argument("-p", action="store_true", help="Use uppercase letters")
    parser.add_argument("-i", action="store_true", help="Use numbers")
    parser.add_argument("-s", action="store_true", help="Use symbols")
    ##If user wants the output to be piped somewhere
    parser.add_argument("--quiet", action="store_true", help="Output password only")
    ##If user wants multiple counts of passwords
    parser.add_argument(
        "--count",
        default=DEFAULT_COUNT,
        type=int,
        metavar="int",
        help="Specify how many passwords should be generated",
    )
    parser.add_argument(
        "--no_similar", action="store_true", help="Don't use ambiguous characters"
    )
    parser.add_argument(
        "--min_numbers",
        type=int,
        default=DEFAULT_MIN_NUM,
        metavar="int",
        help="Specify an amount of numbers needed for the password",
    )
    parser.add_argument(
        "--min_symbols",
        type=int,
        default=DEFAULT_MIN_SYM,
        metavar="int",
        help="Specify an amount of symbols needed for the password",
    )
    parser.add_argument("--copy", action="store_true", help="Copy output to clipboard")
    args = parser.parse_args()
    return args


def validate_args(args):

    flags = [args.u, args.p, args.i, args.s]

    if args.l < MINIMUM_LEN:
        print("Length must be more than 8 for a secure password")
        raise SystemExit(1)
    if not any(flags):
        args.u = args.p = args.i = args.s = True
    if args.min_numbers + args.min_symbols > args.l:
        print("Minimum numbers and symbols cannot be greater than length")
        raise SystemExit(1)
    return args


def charset_gen(args):
    pairs = [
        (args.u, string.ascii_uppercase),
        (args.p, string.ascii_lowercase),
        (args.i, string.digits),
        (args.s, string.punctuation),
    ]
    stringpool = ""
    for flag, chars in pairs:
        if flag:
            stringpool += chars
    if args.no_similar:
        return "".join(char for char in stringpool if char not in SIMILAR_CHARS)
    return stringpool


def password_gen(
    stringpool, length, digits_charset, symbols_charset, min_numbers, min_symbols
):
    remaining = length - (min_symbols + min_numbers)
    password_list = []
    for _ in range(min_numbers):
        password_list.append(secrets.choice(digits_charset))
    for _ in range(min_symbols):
        password_list.append(secrets.choice(symbols_charset))
    for _ in range(remaining):
        password_list.append(secrets.choice(stringpool))
    secrets.SystemRandom().shuffle(password_list)
    return "".join(password_list)


def entropy_calculator(stringpool, length):
    entropy = length * log2(len(stringpool))
    return entropy


def main():
    args = argument_parser()
    validated = validate_args(args)
    charpool = charset_gen(validated)
    entropy = entropy_calculator(charpool, validated.l)
    password = password_gen(
        charpool,
        args.l,
        string.digits,
        string.punctuation,
        args.min_numbers,
        args.min_symbols,
    )

    if args.quiet:
        for _ in range(args.count):
            print(
                password_gen(
                    charpool,
                    validated.l,
                    string.digits,
                    string.punctuation,
                    args.min_numbers,
                    args.min_symbol,
                )
            )
    else:
        for _ in range(args.count):
            print(
                password_gen(
                    charpool,
                    validated.l,
                    string.digits,
                    string.punctuation,
                    args.min_numbers,
                    args.min_symbols,
                )
            )
        print(f"Entropy: {entropy:.4f} bits")

        if args.copy:
            subprocess.run(["wl-copy"], input=password.encode())
            if not args.quiet:
                print("Password copied successfully")


if __name__ == "__main__":
    main()
