import pygame
import math
from collections import OrderedDict


class Tile:
    def __init__(self, color, pos, rect=None):
        self.color = color
        self.rect = rect
        self.pos = pos  # as in cell position, not pixel position
        self.neighbours = []
        self.edges = {'N': False, 'S': False, 'W': False, 'E': False}
        self.edge_id = {}

    def reset_edges(self):
        self.edges = {'N': False, 'S': False, 'W': False, 'E': False}
        self.edge_id = {}

    def edge_exists(self, edge):
        return self.edges[edge]

    def set_edge(self, edge, edge_exists):
        self.edges[edge] = edge_exists

    def set_edge_id(self, edge, edge_id):
        self.edge_id[edge] = edge_id


class Edge:
    def __init__(self, sx, sy, ex, ey):
        self.start_x = sx
        self.start_y = sy
        self.end_x = ex
        self.end_y = ey


class Light:
    def __init__(self, pos, radius):
        self.light_edges = None
        self.bottom_edge = None
        self.top_edge = None
        self.right_edge = None
        self.left_edge = None
        self.pos = pos
        self.radius = radius

    def update(self):
        self.left_edge = Edge(self.rect.left, self.rect.top, self.rect.left, self.rect.bottom)
        self.right_edge = Edge(self.rect.right, self.rect.top, self.rect.right, self.rect.bottom)
        self.top_edge = Edge(self.rect.left, self.rect.top, self.rect.right, self.rect.top)
        self.bottom_edge = Edge(self.rect.left, self.rect.bottom, self.rect.right, self.rect.bottom)

        self.light_edges = [self.left_edge, self.right_edge, self.top_edge, self.bottom_edge]

    @property
    def rect(self):
        return pygame.Rect(self.pos[0] - 64, self.pos[1] - 64, 128, 128)


def create_tile(pos):
    x_pos = pos[0] // tile_size
    y_pos = pos[1] // tile_size
    tile_grid[(x_pos, y_pos)] = Tile((0, 0, 255), (x_pos, y_pos))


def delete_tile(pos):
    x_pos = pos[0] // tile_size
    y_pos = pos[1] // tile_size
    del (tile_grid[(x_pos, y_pos)])


def convert_map_to_poly(sx, sy, width, height, block_size, pitch):
    vecEdges.clear()

    for tile in tile_grid:
        tile_grid[tile].reset_edges()

    for y in range(0, height):
        for x in range(0, width):
            if (x, y) in tile_grid:
                tile = tile_grid[(x, y)]

                i = tile.pos
                n = tile.pos[1] - 1
                s = tile.pos[1] + 1
                w = tile.pos[0] - 1
                e = tile.pos[0] + 1

                # check for western neighbour
                # if there is no western neighbour it needs an edge
                if (w, i[1]) not in tile_grid:
                    # check if northern neighbour exists
                    if (i[0], n) in tile_grid:
                        northern_neighbour = tile_grid[(i[0], n)]
                        if northern_neighbour.edge_exists('W'):
                            vecEdges[northern_neighbour.edge_id['W']].end_y += block_size
                            tile.set_edge_id('W', northern_neighbour.edge_id['W'])
                            tile.set_edge('W', True)
                            tile_grid[(x, y)] = tile
                        else:
                            new_edge = Edge((sx + x) * block_size, (sy + y) * block_size,
                                            (sx + x) * block_size, ((sy + y) * block_size) + block_size)
                            edge_id = len(vecEdges)
                            vecEdges[edge_id] = new_edge
                            tile.set_edge_id('W', edge_id)
                            tile.set_edge('W', True)
                            tile_grid[(x, y)] = tile

                    else:
                        new_edge = Edge((sx + x) * block_size, (sy + y) * block_size,
                                        (sx + x) * block_size, ((sy + y) * block_size) + block_size)
                        edge_id = len(vecEdges)
                        vecEdges[edge_id] = new_edge
                        tile.set_edge_id('W', edge_id)
                        tile.set_edge('W', True)
                        tile_grid[(x, y)] = tile

                # check for eastern neighbour
                # if there is no eastern neighbour it needs an edge
                if (e, i[1]) not in tile_grid:
                    # check if northern neighbour exists
                    if (i[0], n) in tile_grid:
                        northern_neighbour = tile_grid[(i[0], n)]
                        if northern_neighbour.edge_exists('E'):
                            vecEdges[northern_neighbour.edge_id['E']].end_y += block_size
                            tile.set_edge_id('E', northern_neighbour.edge_id['E'])
                            tile.set_edge('E', True)
                            tile_grid[(x, y)] = tile
                        else:
                            new_edge = Edge((sx + x + 1) * block_size, (sy + y) * block_size,
                                            (sx + x + 1) * block_size, ((sy + y) * block_size) + block_size)
                            edge_id = len(vecEdges)
                            vecEdges[edge_id] = new_edge
                            tile.set_edge_id('E', edge_id)
                            tile.set_edge('E', True)
                            tile_grid[(x, y)] = tile
                    else:
                        new_edge = Edge((sx + x + 1) * block_size, (sy + y) * block_size,
                                        (sx + x + 1) * block_size, ((sy + y) * block_size) + block_size)
                        edge_id = len(vecEdges)
                        vecEdges[edge_id] = new_edge
                        tile.set_edge_id('E', edge_id)
                        tile.set_edge('E', True)
                        tile_grid[(x, y)] = tile

                # check for northern neighbour
                # if there is no northern neighbour it needs an edge
                if (i[0], n) not in tile_grid:
                    # check if western neighbour exists
                    if (w, i[1]) in tile_grid:
                        western_neighbour = tile_grid[(w, i[1])]
                        if western_neighbour.edge_exists('N'):
                            vecEdges[western_neighbour.edge_id['N']].end_x += block_size
                            tile.set_edge_id('N', western_neighbour.edge_id['N'])
                            tile.set_edge('N', True)
                            tile_grid[(x, y)] = tile
                        else:
                            new_edge = Edge((sx + x) * block_size, (sy + y) * block_size,
                                            ((sx + x) * block_size) + block_size, (sy + y) * block_size)
                            edge_id = len(vecEdges)
                            vecEdges[edge_id] = new_edge
                            tile.set_edge_id('N', edge_id)
                            tile.set_edge('N', True)
                            tile_grid[(x, y)] = tile
                    else:
                        new_edge = Edge((sx + x) * block_size, (sy + y) * block_size,
                                        ((sx + x) * block_size) + block_size, (sy + y) * block_size)
                        edge_id = len(vecEdges)
                        vecEdges[edge_id] = new_edge
                        tile.set_edge_id('N', edge_id)
                        tile.set_edge('N', True)
                        tile_grid[(x, y)] = tile

                # check for southern neighbour
                # if there is no southern neighbour it needs an edge
                if (i[0], s) not in tile_grid:
                    # check if western neighbour exists
                    if (w, i[1]) in tile_grid:
                        western_neighbour = tile_grid[(w, i[1])]
                        if western_neighbour.edge_exists('S'):
                            vecEdges[western_neighbour.edge_id['S']].end_x += block_size
                            tile.set_edge_id('S', western_neighbour.edge_id['S'])
                            tile.set_edge('S', True)
                            tile_grid[(x, y)] = tile
                        else:
                            new_edge = Edge((sx + x) * block_size, (sy + y + 1) * block_size,
                                            ((sx + x) * block_size) + block_size, (sy + y + 1) * block_size)
                            edge_id = len(vecEdges)
                            vecEdges[edge_id] = new_edge
                            tile.set_edge_id('S', edge_id)
                            tile.set_edge('S', True)
                            tile_grid[(x, y)] = tile
                    else:
                        new_edge = Edge((sx + x) * block_size, (sy + y + 1) * block_size,
                                        ((sx + x) * block_size) + block_size, (sy + y + 1) * block_size)
                        edge_id = len(vecEdges)
                        vecEdges[edge_id] = new_edge
                        tile.set_edge_id('S', edge_id)
                        tile.set_edge('S', True)
                        tile_grid[(x, y)] = tile


def calculate_polygon(ox, oy, radius):
    vecVisibilityPolygonPoints.clear()
    for edge in vecEdges.values():
        for i in range(0, 2):
            rdx = (edge.start_x if i == 0 else edge.end_x) - ox
            rdy = (edge.start_y if i == 0 else edge.end_y) - oy

            base_ang = math.atan2(rdy, rdx)
            ang = 0.0
            for j in range(0, 3):
                if j == 0:
                    ang = base_ang - 0.0001
                if j == 1:
                    ang = base_ang
                if j == 2:
                    ang = base_ang + 0.0001

                rdx = radius * math.cos(ang)
                rdy = radius * math.sin(ang)

                min_t1 = math.inf
                min_px, min_py, min_ang = 0, 0, 0.0
                is_valid = False

                for edge2 in vecEdges.values():
                    sdx = edge2.end_x - edge2.start_x
                    sdy = edge2.end_y - edge2.start_y

                    if abs(sdx - rdx) > 0.0 and abs(sdy - rdy) > 0.0:
                        t2 = (rdx * (edge2.start_y - oy) + (rdy * (ox - edge2.start_x))) / (sdx * rdy - sdy * rdx)
                        t1 = (edge2.start_x + sdx * t2 - ox) / rdx

                        if t1 > 0 and 0 <= t2 <= 1.0:
                            if t1 < min_t1:
                                min_t1 = t1
                                min_px = ox + rdx * t1
                                min_py = oy + rdy * t1
                                min_ang = math.atan2(min_py - oy, min_px - ox)
                                is_valid = True

                if is_valid:
                    vecVisibilityPolygonPoints.append((min_ang, min_px, min_py))
    vecVisibilityPolygonPoints.sort(key=lambda y: y[0])


pygame.init()  # Start Pygame

screen = pygame.display.set_mode((1280, 720))  # Start the screen
clock = pygame.time.Clock()
clock.tick(60)

tile_size = 32
map_width = 1280 // tile_size
map_height = 720 // tile_size
tile_grid = {}
mouse_pos = None
vecEdges = OrderedDict()
vecVisibilityPolygonPoints = []
light = Light((512, 256), 128)
process1 = multiprocessing.Process(target=calculate_polygon, args=(light.pos[0], light.pos[1], 1000.0))

for i in range(2, 16):
    create_tile((i * tile_size, 64))
    create_tile((i * tile_size, 512))

for i in range(2, 16):
    create_tile((64, i * tile_size))
    create_tile((496, i * tile_size))

tile_grid_old = len(tile_grid)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # The user closed the window!
            running = False  # Stop running
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                create_tile(mouse_pos)
            if event.button == 3:
                mouse_pos = pygame.mouse.get_pos()
                try:
                    delete_tile(mouse_pos)
                except Exception as e:
                    print(e)

    if len(tile_grid) != tile_grid_old:
        convert_map_to_poly(0, 0, map_width, map_height, tile_size, map_width)
        tile_grid_old = len(tile_grid)

    amount_of_rays = len(vecVisibilityPolygonPoints)
    vecVisibilityPolygonPoints = list(dict.fromkeys(vecVisibilityPolygonPoints))
    new_amount = len(vecVisibilityPolygonPoints)
    print((amount_of_rays, new_amount))
    calculate_polygon(light.pos[0], light.pos[1], 1000.0)

    mouse_pos = pygame.mouse.get_pos()
    light.pos = mouse_pos
    light.update()

    screen.fill((0, 0, 0))
    # pygame.draw.circle(screen, (255, 255, 255), light.pos, light.radius)
    if len(vecVisibilityPolygonPoints) > 1:
        for index, point in enumerate(vecVisibilityPolygonPoints):
            try:
                next_point = vecVisibilityPolygonPoints[index + 1]
            except IndexError:
                next_point = vecVisibilityPolygonPoints[0]
            pygame.draw.polygon(screen, (255, 255, 255),
                                [(light.pos[0], light.pos[1]),
                                 (point[1] // 1, point[2] // 1),
                                 (next_point[1] // 1, next_point[2] // 1)], 0)

    for tile in tile_grid:
        tile = tile_grid[tile]
        pygame.draw.rect(screen, tile.color,
                         pygame.Rect(tile.pos[0] * tile_size, tile.pos[1] * tile_size, tile_size, tile_size))
    for edge in vecEdges.values():
        pygame.draw.line(screen, (255, 0, 0), (edge.start_x, edge.start_y), (edge.end_x, edge.end_y))

    '''pygame.draw.rect(screen, (255, 0, 0), light.rect, 1)'''

    pygame.draw.circle(screen, (255, 0, 0), light.pos, 8)
    pygame.display.update()

pygame.quit()  # Close the window
