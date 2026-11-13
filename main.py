# main.py
import heapq
import sys
from collections import deque

import pygame

ROWS, COLS, CELL = 25, 50, 20          # en az 20x50 şartı sağlanıyor
MIN_WALLS = 8
W, H = COLS * CELL, ROWS * CELL + 40   # altta bilgi çubuğu

WHITE, BLACK, GRAY = (255, 255, 255), (30, 30, 30), (210, 210, 210)
GREEN, RED = (46, 160, 67), (220, 53, 69)
BFS_C, ASTAR_C, PATH_C = (173, 216, 230), (255, 165, 0), (255, 220, 0)


def neighbors(cell, walls):
    r, c = cell
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and (nr, nc) not in walls:
            yield (nr, nc)


def hybrid_search(start, goal, walls):
    """Generator: her adımda (aşama, hücre) üretir. Animasyon bunu tüketir."""
    # Aşama 1: BFS ile ulaşılabilirlik kontrolü
    queue, seen, found = deque([start]), {start}, False
    while queue:
        cur = queue.popleft()
        if cur == goal:
            found = True
            break
        for n in neighbors(cur, walls):
            if n not in seen:
                seen.add(n)
                queue.append(n)
        yield ("bfs", cur)
    if not found:
        yield ("fail", None)
        return

    yield ("phase2", None)

    # Aşama 2: A* ile en kısa yol
    h = lambda a: abs(a[0] - goal[0]) + abs(a[1] - goal[1])
    heap = [(h(start), 0, start)]
    g, parent, closed = {start: 0}, {}, set()
    while heap:
        _, gc, cur = heapq.heappop(heap)
        if cur in closed:
            continue
        closed.add(cur)
        if cur == goal:
            break
        for n in neighbors(cur, walls):
            ng = gc + 1
            if ng < g.get(n, float("inf")):
                g[n] = ng
                parent[n] = cur
                heapq.heappush(heap, (ng + h(n), ng, n))
        yield ("astar", cur)

    path, cur = [], goal
    while cur != start:
        path.append(cur)
        cur = parent[cur]
    path.append(start)
    for p in reversed(path):
        yield ("path", p)
    yield ("done", len(path) - 1)


def draw(screen, font, walls, start, goal, marks, msg):
    screen.fill(WHITE)
    for cell, color in marks.items():
        pygame.draw.rect(screen, color, (cell[1] * CELL, cell[0] * CELL, CELL, CELL))
    for r, c in walls:
        pygame.draw.rect(screen, BLACK, (c * CELL, r * CELL, CELL, CELL))
    for cell, color in ((start, GREEN), (goal, RED)):
        pygame.draw.rect(screen, color, (cell[1] * CELL, cell[0] * CELL, CELL, CELL))
    for r in range(ROWS + 1):
        pygame.draw.line(screen, GRAY, (0, r * CELL), (W, r * CELL))
    for c in range(COLS + 1):
        pygame.draw.line(screen, GRAY, (c * CELL, 0), (c * CELL, ROWS * CELL))
    screen.blit(font.render(msg, True, BLACK), (8, ROWS * CELL + 10))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Labirent Ajanı - BFS + A* Hibrit")
    font = pygame.font.SysFont("arial", 16)
    clock = pygame.time.Clock()

    walls, marks = set(), {}
    start, goal = (ROWS // 2, 2), (ROWS // 2, COLS - 3)
    gen, bfs_count, astar_count = None, 0, 0
    msg = "Sol tık: duvar | Sağ tık: sil | S+tık: başlangıç | G+tık: hedef | SPACE: başlat | C: temizle"

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    walls.clear(); marks.clear(); gen = None
                    msg = "Temizlendi."
                if e.key == pygame.K_SPACE and gen is None:
                    if len(walls) < MIN_WALLS:
                        msg = f"En az {MIN_WALLS} duvar ekle (şu an {len(walls)})."
                    else:
                        marks.clear()
                        bfs_count = astar_count = 0
                        gen = hybrid_search(start, goal, walls)
                        msg = "Aşama 1: BFS ile ulaşılabilirlik..."

        # Fare ile çizim (arama sırasında kapalı)
        if gen is None:
            buttons = pygame.mouse.get_pressed()
            keys = pygame.key.get_pressed()
            x, y = pygame.mouse.get_pos()
            cell = (y // CELL, x // CELL)
            if 0 <= cell[0] < ROWS and 0 <= cell[1] < COLS:
                if buttons[0] and keys[pygame.K_s] and cell not in walls and cell != goal:
                    start = cell
                elif buttons[0] and keys[pygame.K_g] and cell not in walls and cell != start:
                    goal = cell
                elif buttons[0] and cell not in (start, goal):
                    walls.add(cell)
                elif buttons[2]:
                    walls.discard(cell)

        # Animasyon: her karede birkaç adım ilerlet
        if gen is not None:
            for _ in range(3):
                try:
                    kind, val = next(gen)
                except StopIteration:
                    gen = None
                    break
                if kind == "bfs":
                    marks[val] = BFS_C; bfs_count += 1
                elif kind == "phase2":
                    marks.clear()
                    msg = "Aşama 2: A* ile en kısa yol aranıyor..."
                elif kind == "astar":
                    marks[val] = ASTAR_C; astar_count += 1
                elif kind == "path":
                    marks[val] = PATH_C
                elif kind == "fail":
                    msg = "Hedefe ulaşılamıyor!"; gen = None; break
                elif kind == "done":
                    msg = (f"Bitti. En kısa yol: {val} adım | BFS gezilen: {bfs_count} "
                           f"| A* gezilen: {astar_count}")
                    gen = None; break

        draw(screen, font, walls, start, goal, marks, msg)
        clock.tick(60)


if __name__ == "__main__":
    main()