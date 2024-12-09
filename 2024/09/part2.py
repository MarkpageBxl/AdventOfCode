#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 9, part 2
#
# Challenge URL: https://adventofcode.com/2024/day/9#part2
#
# Author: Markus Lindström <markus@markpage.be>
#

import heapq
from collections import defaultdict


def build_disk_map(layout: str) -> tuple[dict[int, set[int]], list[int]]:
    file_blocks: dict[int, set[int]] = {}
    free_list: list[int] = []
    file_id = 0
    block_number = 0
    for i, k in enumerate(layout):
        length = int(k)
        blocks = range(block_number, block_number + length)
        if i % 2 == 0:
            # file
            file_blocks[file_id] = set(blocks)
            file_id += 1
        else:
            # free space
            free_list.extend(blocks)
        block_number += length
    heapq.heapify(free_list)
    return file_blocks, free_list


def disk_map_to_str(disk_map: tuple[dict[int, set[int]], list[int]]) -> str:
    fs_size = 0
    file_blocks, free_list = disk_map
    buffer: list[str] = []
    for blocks in file_blocks.values():
        fs_size += len(blocks)
    fs_size += len(free_list)
    block_to_file = {
        lba: file_id for file_id, blocks in file_blocks.items() for lba in blocks
    }
    for i in range(fs_size):
        if i in block_to_file:
            buffer.append(str(block_to_file[i]))
        else:
            assert i in free_list
            buffer.append(".")
    return "".join(buffer)


def compute_free_ranges(free_list: list[int]) -> dict[int, list[int]]:
    # return a dict where keys are range size and values are respective start indices
    free_blocks = free_list[:]
    result = defaultdict(list)
    range_size = 0
    start_block = heapq.heappop(free_blocks)
    prev_block = start_block - 1
    current_block = start_block
    while True:
        if current_block != prev_block + 1:
            result[range_size].append(start_block)
            start_block = current_block
            range_size = 1
        else:
            range_size += 1
        prev_block = current_block
        if not free_blocks:
            break
        current_block = heapq.heappop(free_blocks)
    result[range_size].append(start_block)
    for k in result:
        heapq.heapify(result[k])
    return result


def defragment_free_space(
    disk_map: tuple[dict[int, set[int]], list[int]]
) -> tuple[dict[int, set[int]], list[int]]:
    file_blocks, free_list = disk_map
    free_ranges = compute_free_ranges(free_list)
    # debugging
    # print(disk_map_to_str((file_blocks, free_list)))
    free_block_set = set(free_list)
    for file_id in reversed(file_blocks):
        blocks = file_blocks[file_id]
        file_size = len(blocks)
        # search for big enough range
        range_size = file_size
        best_start_block = None
        for k in sorted(free_ranges):
            if k < file_size:
                continue
            if best_start_block is None or best_start_block > free_ranges[k][0]:
                range_size = k
                best_start_block = free_ranges[k][0]
        if best_start_block is not None:
            start_block = free_ranges[range_size][0]
            if start_block < min(file_blocks[file_id]):
                heapq.heappop(free_ranges[range_size])
                remaining_range_size = range_size - file_size
                if remaining_range_size > 0:
                    heapq.heappush(
                        free_ranges[remaining_range_size], start_block + file_size
                    )
                if len(free_ranges[range_size]) == 0:
                    del free_ranges[range_size]
                file_blocks_to_move = sorted(file_blocks[file_id])
                for i in range(file_size):
                    src = file_blocks_to_move.pop()
                    dst = start_block + i
                    file_blocks[file_id].add(dst)
                    file_blocks[file_id].remove(src)
                    free_block_set.remove(dst)
                    free_block_set.add(src)
                    # debugging
                    # free_list = list(free_block_set)
                    # print(disk_map_to_str((file_blocks, free_list)))
    free_list = list(sorted(free_block_set))
    return file_blocks, free_list


def compute_checksum(file_blocks: dict[int, set[int]]) -> int:
    checksum = 0
    for file_id, blocks in file_blocks.items():
        file_checksum = sum([file_id * block_number for block_number in blocks])
        checksum += file_checksum
    return checksum


def main():
    input_file = "input"
    with open(input_file) as fp:
        layout = fp.read().rstrip()
    disk_map = build_disk_map(layout)
    # debugging
    # print(disk_map_to_str(disk_map))
    disk_map = defragment_free_space(disk_map)
    checksum = compute_checksum(disk_map[0])
    # debugging
    # print(disk_map_to_str(disk_map))
    print(checksum)


if __name__ == "__main__":
    main()
