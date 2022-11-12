#!/usr/bin/env python3

import argparse
import scrython


def main():
    args = parse_args()

    if args.set:
        card = scrython.cards.Named(set=args.set, fuzzy=args.card)
    else:
        card = scrython.cards.Named(fuzzy=args.card)

    print_card(card)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("card", nargs="*", help="Card name to search Scryfall for")
    parser.add_argument("-s", "--set", default=False,
                        help="3 letter set code for card search")

    args = parser.parse_args()
    args.card = " ".join(args.card)

    return args


def print_card(card, indent=2):
    print("Name:")
    print("%s%s" % (" " * indent, card.name()))

    if card.mana_cost():
        print("Mana Cost:")
        print("%s%s" % (" " * indent, card.mana_cost()))

    if card.type_line():
        print("Type Line:")
        print("%s%s" % (" " * indent, card.type_line()))

    if card.oracle_text():
        print("Oracle Text:")
        for line in oracle_text_lines(card.oracle_text()):
            print("%s%s" % (" " * indent, line))

    if "power" in card.scryfallJson.keys():
        print("Power & Toughness:")
        print("%s%s/%s" % (" " * indent, card.power(), card.toughness()))


def oracle_text_lines(text, length=45):
    lines = []
    for remaining_text in text.split("\n"):
        while len(remaining_text) > 0:
            if len(remaining_text) <= length:
                end = len(remaining_text)
            else:
                end = length

            # Find break between words
            while len(remaining_text) > length and remaining_text[end] != " ":
                end -= 1

            lines.append(remaining_text[:end])
            remaining_text = remaining_text[end + 1:]

    return lines


if __name__ == "__main__":
    main()
