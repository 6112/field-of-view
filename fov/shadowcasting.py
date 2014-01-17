import fov.map

def compute (world_map, sight_map):
    """Compute shadowcasting on a given map."""
    player = sight_map.player
    radius = sight_map.radius
    for octant_index in range (8):
        cast_light (world_map, sight_map, player, 1, 1.0, 0.0, 
          radius, fov.map.Octant (octant_index, (player.y, player.x)))

def cast_light (world_map, sight_map, player, starting_row, start_slope, \
        end_slope, radius, octant):
    """Cast a ray of light onto the map.
    
    Args:
        world_map: WorldMap to cast the ray onto.
        sight_map: FieldOfViewMap to cast the ray onto.
        player: player whose position is the origin of the rays.
        starting_row: row at which to start iterating.
        start_slope: maximum slope of the tiles to check.
        end_slope: minimum slope of the tiles to check.
        radius: sight radius.
        octant: Octant to use for coordinate transformations.
    """
    if start_slope < end_slope:
        return
    for row in range (starting_row, radius + 1):
        dy = - row
        dx = - row - 1
        blocked = False
        while dx <= 0:
            dx += 1
            # translate dx, dy into map coordinates
            y, x = octant.transformed_point ((dy, dx))
            if y < 0 or x < 0 or y >= world_map.height or x >= world_map.width:
                continue
            # left_slope and right_slope are the slopes for the extremities
            left_slope = (dx - 0.5) / (dy + 0.5)
            right_slope = (dx + 0.5) / (dy - 0.5)
            if start_slope < right_slope:
                continue
            elif end_slope > left_slope:
                break
            else:
                # our light beam is touching the square, light it
                if dx * dx + dy * dy < radius * radius:
                    sight_map [y, x] = True
                if blocked:
                    if world_map [y, x].blocks_sight:
                        new_start_slope = right_slope
                        continue
                    else:
                        blocked = False
                        start_slope = new_start_slope
                else:
                    if world_map [y, x].blocks_sight and row < radius:
                        # this is a blocking square, start a child scan
                        blocked = True
                        cast_light (world_map, sight_map, player, row + 1, 
                          start_slope, left_slope, radius, octant)
                        new_start_slope = right_slope
        if blocked:
            break
