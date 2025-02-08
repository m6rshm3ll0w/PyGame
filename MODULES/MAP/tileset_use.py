from MODULES.init import CONFIG


class MAP2TILEMAP:
    def __init__(self):
        self.ELEMENTS = CONFIG['world_gen']['elements']
        self.WIDTH = self.HEIGHT = CONFIG['world_gen']['size']
        self.TILES = CONFIG['world_gen']['tile_set']["tiles"]
        self.tile_map = [[self.ELEMENTS["empty"]["ej"]] * self.WIDTH for _ in range(self.HEIGHT)]
        self.MAP = None

    def get_tile(self, row, col):
        if 0 <= row < self.HEIGHT and 0 <= col < self.WIDTH:
            if not self.MAP[row][col] in [self.ELEMENTS["start_point"]["ej"], self.ELEMENTS["end_point"]["ej"]]:
                return self.MAP[row][col]
        else:
            return self.ELEMENTS["floor"]["ej"]


    def find_tile(self, row, col):
        current_tile = self.MAP[row][col]

        RightBlock = self.get_tile(row, col + 1)
        LeftBlock = self.get_tile(row, col - 1)
        UpBlock = self.get_tile(row + 1, col)
        DownBlock = self.get_tile(row - 1, col)


        if current_tile == self.ELEMENTS["floor"]["ej"]:
            return self.TILES["floor"]["ej"]

        if current_tile == self.ELEMENTS["start_point"]["ej"]:
            return self.TILES["floor"]["ej"]

        if current_tile == self.ELEMENTS["end_point"]["ej"]:
            return self.TILES["floor"]["ej"]

        elif current_tile == self.ELEMENTS["wall"]["ej"]:
            if UpBlock == self.ELEMENTS["floor"]["ej"]:
                if DownBlock == self.ELEMENTS["floor"]["ej"]:
                    if LeftBlock == self.ELEMENTS["floor"]["ej"]:
                        if RightBlock == self.ELEMENTS["floor"]["ej"]:
                            return self.TILES["O-wall"]["ej"]  # no wall

                        elif RightBlock == self.ELEMENTS["wall"]["ej"]:
                            return self.TILES["horizontal-left-end"]["ej"]  # only right wall

                    elif LeftBlock == self.ELEMENTS["wall"]["ej"]:
                        if RightBlock == self.ELEMENTS["floor"]["ej"]:
                            return self.TILES["horizontal-right-end"]["ej"]  # only left wall

                        elif RightBlock == self.ELEMENTS["wall"]["ej"]:
                            return self.TILES["horizontal-wall"]["ej"]  # right-left wall

                if DownBlock == self.ELEMENTS["wall"]["ej"]:
                    if LeftBlock == self.ELEMENTS["floor"]["ej"]:
                        if RightBlock == self.ELEMENTS["floor"]["ej"]:
                            return self.TILES["vertical-down-end"]["ej"]  # only down wall

                        elif RightBlock == self.ELEMENTS["wall"]["ej"]:
                            return self.TILES["down-left-corner"]["ej"]  # down-right wall

                    elif LeftBlock == self.ELEMENTS["wall"]["ej"]:
                        if RightBlock == self.ELEMENTS["floor"]["ej"]:
                            return self.TILES["down-right-corner"]["ej"]  # down-left wall

                        elif RightBlock == self.ELEMENTS["wall"]["ej"]:
                            return self.TILES["T-up"]["ej"]  # down-left-right wall


            if UpBlock == self.ELEMENTS["wall"]["ej"]:
                if DownBlock == self.ELEMENTS["floor"]["ej"]:
                    if LeftBlock == self.ELEMENTS["floor"]["ej"]:
                        if RightBlock == self.ELEMENTS["floor"]["ej"]:
                            return self.TILES["vertical-up-end"]["ej"]  # only up wall

                        elif RightBlock == self.ELEMENTS["wall"]["ej"]:
                            return self.TILES["up-left-corner"]["ej"]  # up-right wall

                    elif LeftBlock == self.ELEMENTS["wall"]["ej"]:
                        if RightBlock == self.ELEMENTS["floor"]["ej"]:
                            return self.TILES["up-right-corner"]["ej"]  # up-left wall

                        elif RightBlock == self.ELEMENTS["wall"]["ej"]:
                            return self.TILES["T-down"]["ej"]  # up-left-right wall

                if DownBlock == self.ELEMENTS["wall"]["ej"]:
                    if LeftBlock == self.ELEMENTS["floor"]["ej"]:
                        if RightBlock == self.ELEMENTS["floor"]["ej"]:
                            return self.TILES["vertical-wall"]["ej"]  # up-down wall

                        elif RightBlock == self.ELEMENTS["wall"]["ej"]:
                            return self.TILES["T-right"]["ej"]  # up-down-right wall

                    elif LeftBlock == self.ELEMENTS["wall"]["ej"]:
                        if RightBlock == self.ELEMENTS["floor"]["ej"]:
                            return self.TILES["T-left"]["ej"]  # up-down-left wall

                        elif RightBlock == self.ELEMENTS["wall"]["ej"]:
                            return self.TILES["4-corners"]["ej"]  # up-down-left-right wall

        return self.TILES["O-wall"]["ej"]

    def reformat(self, MAP):
        self.MAP = MAP
        for row in range(self.HEIGHT):
            for col in range(self.WIDTH):
                self.tile_map[row][col] = self.find_tile(row, col)

    def get_tilemap(self):
        return self.tile_map