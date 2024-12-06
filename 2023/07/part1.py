#!/usr/bin/env python
#
# Solution for Advent of Code 2023
# Day 7, part 1
#
# Challenge URL: https://adventofcode.com/2023/day/7
#
# Author: Markus Lindström <markus@markpage.be>
#

from collections import defaultdict

CARD_ORDER = "AKQJT98765432"[::-1]


def card_strength(card: str) -> int:
    pos = CARD_ORDER.find(card)
    assert pos != -1
    return pos


def hand_type_strength(hand: str) -> int:
    card_counter = defaultdict(int)
    for card in hand:
        card_counter[card] += 1
    # reverse lookup
    reverse_lookup = defaultdict(set)
    for card, count in card_counter.items():
        reverse_lookup[count].add(card)
    # five of a kind
    if 5 in reverse_lookup:
        return 7
    # four of a kind
    if 4 in reverse_lookup:
        return 6
    # full house
    if 3 in reverse_lookup and 2 in reverse_lookup:
        return 5
    # three of a kind
    if 3 in reverse_lookup:
        return 4
    # two pair
    if 2 in reverse_lookup and len(reverse_lookup[2]) == 2:
        return 3
    # one pair
    if 2 in reverse_lookup:
        return 2
    # high card
    return 1


def hand_sort_key(hand: str):
    key = [hand_type_strength(hand)]
    key += [card_strength(card) for card in hand]
    return tuple(key)


hands = []
with open("input") as fp:
    for line in fp:
        line = line.strip()
        split = line.split()
        hand, bid = split[0], int(split[1])
        hands.append((hand, bid))

hands.sort(key=lambda h: hand_sort_key(h[0]))

winnings = 0
for i, (hand, bid) in enumerate(hands):
    rank = i + 1
    winnings += rank * bid

print(winnings)
