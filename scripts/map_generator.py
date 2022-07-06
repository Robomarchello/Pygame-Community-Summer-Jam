from perlin_noise import PerlinNoise

def GenerateMap(NoiseSize, TileRect, threshold):
    noise = PerlinNoise(octaves=3, seed=1)
    noise = [[noise([i/NoiseSize[0], j/NoiseSize[1]]) for j in range(NoiseSize[0])] for i in range(NoiseSize[1])]

    position = [0, 0]
    for tile in noise[0]:
        if tile > threshold:
            ...
            #place a tile
        
map = GenerateMap((200, 150), (16, 16), 0.0)