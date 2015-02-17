# Index for BodyTrack / Fluxtream / ESDR datastore tiles include
# level and offset

import math

class TileIndex:
    TILE_SIZE = 512
    
    def __init__(self, level, offset):
        self.level = level
        self.offset = offset
    
    # Tile duration in seconds
    @classmethod
    def duration_at_level(cls, level):
        return (2 ** level) * cls.TILE_SIZE
    
    @classmethod
    def tile_for_time_and_level(cls, time, level):
        return cls(level, int(time / cls.duration_at_level(level)))
    
    @classmethod
    def tile_for_time_and_sample_width(cls, time, sample_width):
        level = cls.level_for_sample_width(sample_width)
        return cls.tile_for_time_and_level(time, level)
    
    # Minimum level required to return samples with no bins no wider than
    # sample_width, in seconds
    @classmethod
    def level_for_sample_width(cls, sample_width):
        return int(math.floor(math.log(sample_width, 2)))

    def duration(self):
        return TileIndex.duration_at_level(self.level)
    
    def start_time(self):
        return self.duration() * self.offset
    
    def end_time(self):
        return self.start_time() + self.duration()
    
    def __eq__(self, rhs):
        return self.level == rhs.level and self.offset == rhs.offset
    
    def __repr__(self):
        return 'TileIndex(level=%d, offset=%d)' % (self.level, self.offset)      

def TestTileIndex():
    assert TileIndex.duration_at_level(16) == 65536 * 512
    assert TileIndex(16, 41).start_time() == 1375731712
    assert TileIndex(16, 42).start_time() == 1409286144 
    assert TileIndex.tile_for_time_and_level(1375731712, 16) == TileIndex(16, 41)
    assert TileIndex.tile_for_time_and_level(1409286143.9, 16) == TileIndex(16, 41)
    assert TileIndex.tile_for_time_and_level(1409286144, 16) == TileIndex(16, 42)
    assert TileIndex.level_for_sample_width(0.5) == -1
    assert TileIndex.level_for_sample_width(0.6) == -1
    assert TileIndex.level_for_sample_width(1) == 0
    assert TileIndex.level_for_sample_width(1.2) == 0
    assert TileIndex.level_for_sample_width(2) == 1
    assert TileIndex.tile_for_time_and_sample_width(1375731712, 65536) == TileIndex(16, 41)

TestTileIndex()
