"""Original terminal artwork, framed to a consistent 35 by 20 character grid."""

import random
import secrets


# Each subject is a separate composition, not a different face on the ghost.
ARTWORKS = {
    "robot": ("Relay robot", r"""
              o
              |
       .------+------.
       |  .-------.  |
       |  | O   O |  |
       |  '-------'  |
       |    [===]    |
       '------+------'
          ____|____
     .---|         |---.
     |   |  [:::]  |   |
    [ ]  |  POWER  |  [ ]
     |   |   /\/   |   |
    /_\  '----+----'  /_\
           |     |
          [ ]   [ ]
         _| |_ _| |_
        |_____|_____|
"""),
    "skull": ("Digital skull", r"""
          .-======-.
       .-'          '-.
      /   .--------.   \
     /   /          \   \
    |   |  .--. .--. |   |
    |   |  |##| |##| |   |
    |   |  '--' '--' |   |
     \  |     /\     |  /
      \ '----/  \----' /
       |    /____\    |
       |   .------.   |
       |   | | | ||   |
       '---+-+-+-+- --'
           | | | |
           '-+-+-'
       //           \\
     ==               ==
"""),
    "cat": ("Terminal cat", r"""
       /\             /\
      /  \___________/  \
     /  /             \  \
    |  /   /\     /\   \  |
    | |    \/     \/    | |
    | |        Y        | |
 ---+-+--    \_|_/    --+-+-
    |  \               /  |
     \  '-------------'  /
      '----.       .----'
           |       |     __
           |  / \  |    /  \
           | |   | |   | /\|
           | |   | |   | |
          /  |   |  \_/ /
         (___|___|___)__/
"""),
    "satellite": ("Orbital satellite", r"""
                         .
      +           .
                  /)
                 //
     .------.   //   .------.
    /__|__|_/\ //   /__|__|_/\
   /__|__|_/ /==O==/__|__|_/ /
   \__|__|_\/  /|  \__|__|_\/
              / |\
             /__|_\
               / \
              '   '
    .                      +
           .-~~~~~~~~-.
        .-'  .--.      '-.
      .'    /    '--.     '.
     /     /        |      \
    /~~~~~~\________/~~~~~~~\
"""),
    "moth": ("Circuit moth", r"""
       \             /
        \     .     /
    .----\---(o)---/----.
   / .--. \   |   / .--. \
  / / /\ \ \  |  / / /\ \ \
 / / /  \ \ \ | / / /  \ \ \
| | | () | | \|/ | | () | | |
 \ \ \__/ / --+-- \ \__/ / /
  \ '----'  / | \  '----' /
   '------./  |  \.------'
     .---./   |   \.---.
    / .-. \   |   / .-. \
   | ( o ) \  |  / ( o ) |
    \ '-'   \ | /   '-' /
     '---.   \|/   .---'
          '-- V --'
              |
"""),
    "portal": ("Signal portal", r"""
           .-=======-.
        .-' .-----. '-.
      .'  .' .---. '.  '.
     /   /  /     \  \   \
    |   |  |   .   |  |   |
    |   |  |  /|\  |  |   |
    |   |  | / | \ |  |   |
    |   |  |/  |  \|  |   |
    |   |  /---+---\  |   |
    |   | /    |    \ |   |
    |   |/_____|_____\|   |
    |   /      |      \   |
    |  /-------+-------\  |
    | /        |        \ |
    |/_________|_________\|
   /           |           \
  /------------+------------\
"""),
}


def frame_art(drawing):
    lines = drawing.strip("\n").splitlines()
    art_width = max(len(line) for line in lines)
    left = (35 - art_width) // 2
    rows = [(" " * left + line).ljust(35) for line in lines]
    top = (20 - len(rows)) // 2
    return "\n".join([" " * 35] * top + rows + [" " * 35] * (20 - top - len(rows)))


def generate_gallery():
    ghost, render_id = generate_ghost()
    gallery = [{"id": "ghost", "name": "Hooded digital ghost", "art": ghost,
                "render_id": render_id}]
    gallery.extend({"id": key, "name": name, "art": frame_art(drawing),
                    "render_id": secrets.token_hex(4).upper()}
                   for key, (name, drawing) in ARTWORKS.items())
    return gallery


def generate_ghost():
    seed = secrets.randbits(64)
    rng = random.Random(seed)
    width, height = 35, 20
    center = width // 2
    canvas = [[" "] * width for _ in range(height)]
    # Random silhouette, mirrored texture, and facial features keep each ghost
    # different while retaining a readable character at small screen sizes.
    crown = rng.choice([2, 3, 4])
    spread = rng.choice([0, 1, 2])
    silhouette = [crown, 6, 9, 11, 12, 13, 13, 14, 14, 14,
                  14, 14, 13, 13, 14, 15, 16, 16, 14, 13]
    palette = rng.choice(["▓▓▒", "██▓", "▒▒▓", "▓▒░"])
    for y, half_width in enumerate(silhouette):
        half_width = min(16, half_width + spread)
        for distance in range(half_width + 1):
            char = "░" if distance == half_width else rng.choice(palette)
            # A scalloped hem instead of a solid rectangular base.
            if y >= 18 and (distance + rng.choice([0, 1])) % 7 < 2:
                char = " "
            canvas[y][center - distance] = char
            canvas[y][center + distance] = char

    face_width = rng.choice([8, 9, 10])
    for y in range(5, 15):
        inset = abs(y - 9) // 2
        for x in range(center - face_width + inset, center + face_width - inset + 1):
            canvas[y][x] = " "

    eyes = rng.choice([
        ("▄▄▄", "███", "▀▀▀"),
        ("╭─╮", "│●│", "╰─╯"),
        ("   ", "[×]", "   "),
        ("╲ ╱", " ╳ ", "╱ ╲"),
        ("▄▄▄", " ▀ ", "   "),
    ])
    eye_gap = rng.choice([3, 4, 5])
    for row, text in enumerate(eyes, start=7):
        for x in (center - eye_gap - 1, center + eye_gap - 1):
            canvas[row][x:x + 3] = text
    canvas[11][center] = rng.choice(["▴", "^", "·", "×"])
    mouth = rng.choice(["─────", "╰───╯", "═╤═╤═", " ▀▀▀ ", "└─┬─┘"])
    canvas[13][center - 2:center + 3] = mouth
    return "\n".join("".join(row) for row in canvas), f"{seed:016X}"[:8]
