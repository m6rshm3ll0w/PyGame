from MODULES.init import CONFIG
import PIL.Image as Image

WIDTH = HEIGHT = CONFIG['world_gen']['size']
TILES = CONFIG['world_gen']['tile_set']["tiles"]
SIZE = CONFIG['world_gen']['tile_set']["size"]


def crop_tiles(path_to_tileset):
    im = Image.open(path_to_tileset)
    tiles_img = {}


    for tile, data in TILES.items():
        top_y, top_x = data['coord']
        top_x, top_y = (top_x - 1) * SIZE, (top_y - 1) * SIZE
        down_x, down_y = top_x + SIZE, top_y + SIZE

        nt = im.crop((top_x, top_y, down_x+1, down_y+1))
        tiles_img[tile] = nt

    return tiles_img


def search(row, col, worldmap):
    for tile, data in TILES.items():
        if data["ej"] == worldmap[row][col]:
            return tile


def map_visualise(TILEMAP):
    tiles_imgs = crop_tiles(path_to_tileset="./DATA/reses/tileset/tileset.png")

    img = Image.new('RGB', (32*WIDTH, 32*HEIGHT), 'black')

    for row in range(HEIGHT):
        for col in range(WIDTH):
            tilename = search(row, col, TILEMAP)
            img.paste(tiles_imgs[tilename], (col*32, row*32))

    img.save("./DATA/world/map.png")
    img.show()

