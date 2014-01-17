SIGHT_RANGE = 16

def compute (self):
    cast_light (self, self.player.x, self.player.y, 1, 1.0, 0.0, SIGHT_RANGE,
      1, 0, 0, 1, 0)

def cast_light (self, cx, cy, row, start, end, radius, xx, xy, yx, yy, id):
    if start < end:
        return
    radius_squared = radius * radius
    for j in range (row, radius + 1):
        dx, dy = -j - 1, -j
        blocked = False
        while dx <= 0:
            dx += 1
            # translate dx, dy into map coordinates
            X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy
            # l_slope and r_slope are the slopes for the extremities
            l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
            if start < r_slope:
                continue
            elif end > l_slope:
                break
            else:
                # our light beam is touching the square, light it
                if dx * dx + dy * dy < radius_squared:
                    self [Y, X] = True
                if blocked:
                    if self.sight_block_map [Y, X]:
                        new_start = r_slope
                        continue
                    else:
                        blocked = False
                        start = new_start
                else:
                    if self.sight_block_map [Y, X] and j < radius:
                        # this is a blocking square, start a child scan
                        blocked = True
                        cast_light (self, cx, cy, j + 1, start, l_slope, radius,
                                xx, xy, yx, yy, id + 1)
                        new_start = r_slope
        if blocked:
            break
