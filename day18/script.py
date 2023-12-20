import re
from typing import NamedTuple
from dataclasses import dataclass, field
from collections import deque
from PIL.Image import new
from PIL.ImageDraw import Draw

print(__file__)




@dataclass
class Point:
    x: int
    y: int

    def __hash__(self):
        return hash((self.x, self.y))

    def __iter__(self):
        return iter((self.x, self.y))


DigPlan = NamedTuple('DigPlan', [('direction', str), ('distance', str), ('color', str)])


with open('input.txt') as f:
    plans: list[DigPlan] = [
        DigPlan(*re.search(r'([LURD]) (\d+) \(#([a-f0-9]{6})\)', line).groups())
        for line in f.read().splitlines()
    ]

DIRECTIONS = {
    'U': Point(0, -1),
    'D': Point(0, 1),
    'L': Point(-1, 0),
    'R': Point(1, 0),
    '0': Point(1, 0),
    '1': Point(0, 1),
    '2': Point(-1, 0),
    '3': Point(0, -1),
}


@dataclass(slots=True)
class Node:
    x: int
    y: int
    next_dir: str = None

    next: 'Node' = None
    prev: 'Node' = None

    @property
    def position(self) -> tuple[int, int]:
        return self.x, self.y


def left_up_most_node(node: Node) -> Node:
    result = start = node
    while node.next is not start:
        node = node.next
        if node.y < result.y or (node.y == result.y and node.x < result.x):
            result = node
    return result


def linked_size(node: Node) -> int:
    result = 0
    start = node
    while node.next is not start:
        result += 1
        node = node.next
    return result


def draw_map(node: Node):
    image = new("RGB", (1024, 1024), 0)
    canvas = Draw(image)
    offset = 300
    start = node
    curr = node
    while start != curr.next:
        next = curr.next
        canvas.line((
            (curr.x + offset // 2) * 2,
            (curr.y + offset) * 2,
            (next.x + offset // 2) * 2,
            (next.y + offset) * 2
        ), width=1)
        curr = next
    image.show()


def compute_area(node: Node) -> int:
    left_top = left_up_most_node(node)
    left_bottom = left_top.prev
    right_top = left_top.next
    right_bottom = right_top.next

    draw_map(node)
    input()
    if right_bottom.next is left_bottom:
        width = right_top.x - left_top.x + 1
        height = left_bottom.y - left_top.y + 1
        print("base case", width * height)
        return width * height

    total_area = 0

    # assert that left and right are parallel
    assert left_top.x == left_bottom.x and right_top.x == right_bottom.x \
           and left_top.y == right_top.y  # assert that both start at the same y

    rectangle_width = right_top.x - left_top.x + 1
    rectangle_height = min(
        left_bottom.y - left_top.y,
        right_bottom.y - right_top.y
    ) + 1

    new_left_bottom_position = (left_top.x, left_top.y + rectangle_height - 1)
    new_right_bottom_position = (right_top.x, right_top.y + rectangle_height - 1)

    next_node = None
    if not (left_top.next_dir == right_bottom.next_dir == left_bottom.prev.next_dir):
        total_area += rectangle_width * rectangle_height
        """
            There are 3 cases:
            1.F----7   
              L-7xx|     left side turns right
                |  L---        

            2.F----7   
              |xxF-J     right side turns left
            --J  |     

            3.F-----7   
              L-7xF-J     both sides turn
                | |                      
        """
        if left_bottom.position == new_left_bottom_position \
                and right_bottom.position == new_right_bottom_position:  # case 3

            if left_bottom.prev.next_dir != right_bottom.next_dir:  # case 3.1
                """
                #######
                #.....#
                ###...#
                ..#...#
                ..#...#
                ###.### <- this edge case is not handled
                #...#..
                ##..### <- as well as this one
                .#....#
                .######
                
                we need to find which side turns into the other side
                    - in 1st case it's right side (turn is direction of left side)
                      so we need to set next node of left_bottom to right_bottom.next
                    - in 2nd case it's left side (turn is direction of right side)
                      so we need to set next node of left_bottom.prev to right_bottom
                and properly remove the duplicated 'path'
                """
                if left_bottom.prev.next_dir == left_top.next_dir:  # right side turns into left side
                    left_bottom.prev.next = right_bottom.next
                    right_bottom.next.prev = left_bottom.prev
                    next_node = left_bottom.prev
                    width = right_bottom.next.x - left_bottom.x + 1
                else:  # left side turns into right side
                    left_bottom.prev.next = right_bottom.next
                    right_bottom.next.prev = left_bottom.prev
                    left_bottom.prev.next_dir = left_top.next_dir
                    next_node = left_bottom.prev
                    width = right_bottom.x - left_bottom.prev.x + 1
            else:
                left_bottom.prev.next_dir = left_top.next_dir
                left_bottom.prev.next = right_bottom.next
                right_bottom.next.prev = left_bottom.prev
                next_node = left_bottom.prev

                # remove the duplicated 'path'
                width = right_bottom.x - left_bottom.x + 1
            total_area -= width
            print("top: case 3")
        elif left_bottom.position == new_left_bottom_position:  # case 1
            new_right_bottom = Node(*new_right_bottom_position,
                                    next_dir=right_top.next_dir,
                                    prev=left_bottom.prev,
                                    next=right_bottom
                                    )
            right_bottom.prev = new_right_bottom
            left_bottom.prev.next = new_right_bottom
            left_bottom.prev.next_dir = left_top.next_dir
            next_node = new_right_bottom

            # remove the duplicated 'path'
            width = new_right_bottom.x - new_right_bottom.prev.x + 1
            total_area -= width
            print("top: case 1")
        elif right_bottom.position == new_right_bottom_position:  # case 2
            new_left_bottom = Node(*new_left_bottom_position,
                                   next_dir=left_top.next_dir,
                                   prev=left_bottom,
                                   next=right_bottom.next
                                   )
            left_bottom.next = new_left_bottom
            right_bottom.next.prev = new_left_bottom
            next_node = new_left_bottom

            # remove the duplicated 'path'
            width = new_left_bottom.next.x - new_left_bottom.x + 1
            total_area -= width
            print("top: case 2")
        else:
            raise RuntimeError('should not happen')
        # pass  # more work to do
    else:  # if rectangle has no duplicated 'paths'
        total_area += rectangle_width * rectangle_height - rectangle_width
        """
            There are 3 cases:
            1.F----7   
            --Jxxxx|     right side is longer
                   L---        
            
            2.F----7   
              |xxxxL---  left side is longer
            --J        
            
            3.F----7   
            --JxxxxL---  both sides are equal
                    
        """
        if left_bottom.position == new_left_bottom_position \
                and right_bottom.position == new_right_bottom_position:  # case 3
            left_bottom.next = right_bottom.next
            right_bottom.next.prev = left_bottom.prev
            next_node = left_bottom.next
            print("bottom: case 3")
        elif left_bottom.position == new_left_bottom_position:  # case 1
            new_right_bottom = Node(*new_right_bottom_position,
                                    next_dir=right_top.next_dir,
                                    prev=left_bottom.prev,
                                    next=right_bottom
                                    )
            right_bottom.prev = new_right_bottom
            left_bottom.prev.next = new_right_bottom
            next_node = new_right_bottom
            print("bottom: case 1")
        elif right_bottom.position == new_right_bottom_position:  # case 2
            new_left_bottom = Node(*new_left_bottom_position,
                                   next_dir=left_top.next_dir,
                                   prev=left_bottom,
                                   next=right_bottom.next
                                   )
            left_bottom.next = new_left_bottom
            right_bottom.next.prev = new_left_bottom
            next_node = new_left_bottom
            print("bottom: case 2")
        else:
            raise RuntimeError('should not happen')

    assert next_node is not None
    print("going in", total_area)
    additional_area = compute_area(next_node)
    print("going out: ", additional_area)
    return total_area + additional_area


def parse_part1(_plans: list[DigPlan]) -> Node:
    start = Node(0, 0)
    node = start
    for plan in _plans:
        dx, dy = DIRECTIONS[plan.direction]
        node.next_dir = plan.direction
        distance = int(plan.distance)
        node.next = Node(
            node.x + dx * distance,
            node.y + dy * distance,
            prev=node
        )
        node = node.next
    start.prev, node.prev.next = node.prev, start
    return start


def parse_part2(_plans: list[DigPlan]) -> Node:
    start = Node(0, 0)
    node = start
    for plan in _plans:
        *distance_hex, direction = plan.color
        distance = int(''.join(distance_hex), 16)
        dx, dy = DIRECTIONS[direction]
        node.next_dir = direction
        node.next = Node(
            node.x + dx * distance,
            node.y + dy * distance,
            prev=node
        )
        node = node.next
    start.prev, node.prev.next = node.prev, start
    return start


nodes = parse_part1(plans)

print('Part1:', compute_area(nodes))
print(compute_area(parse_part2(plans)))
