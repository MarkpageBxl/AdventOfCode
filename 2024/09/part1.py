#!/usr/bin/env python
#
# Solution for Advent of Code 2024
# Day 9, part 1
#
# Challenge URL: https://adventofcode.com/2024/day/9
#
# Author: Markus Lindström <markus@markpage.be>
#

import heapq


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


def defragment_free_space(
    disk_map: tuple[dict[int, set[int]], list[int]]
) -> tuple[dict[int, set[int]], list[int]]:
    file_blocks, free_list = disk_map
    used_list = [-lba for blocks in file_blocks.values() for lba in blocks]
    heapq.heapify(used_list)
    block_to_file = {
        lba: file_id for file_id, blocks in file_blocks.items() for lba in blocks
    }
    # move rightmost file block to leftmost free block
    while True:
        leftmost_free_block = heapq.heappop(free_list)
        rightmost_used_block = -heapq.heappop(used_list)
        if leftmost_free_block >= rightmost_used_block:
            heapq.heappush(free_list, leftmost_free_block)
            heapq.heappush(used_list, -rightmost_used_block)
            break
        file_id = block_to_file[rightmost_used_block]
        # move block, update data structures
        file_blocks[file_id].remove(rightmost_used_block)
        file_blocks[file_id].add(leftmost_free_block)
        heapq.heappush(free_list, rightmost_used_block)
        heapq.heappush(used_list, -leftmost_free_block)
        del block_to_file[rightmost_used_block]
        block_to_file[leftmost_free_block] = file_id
        # print(disk_map_to_str((file_blocks, free_list)))
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
