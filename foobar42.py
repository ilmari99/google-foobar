"""
Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers!
Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were 
running through the station, so you have a chance to fight your way out. But the beam 
weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect 
off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause 
damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. 
And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 
integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, 
an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number 
of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both 
positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. 
Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite trainer were positioned in a room with
dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot 
in seven different directions to hit the elite trainer (given as vector bearings from your location):
[1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing
[1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left 
wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot 
at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).


ME
===

Unfortunately I couldn't solve this one in time, even though I knew how to do it. I had other things to prioritize during this challenge.
I did try to get it working, but there was too much debugging etc. to get it to work in time.

I figured the solution after reading about problems related to paths in Billiard tables.
The solution is to mirror the room and everyone in it in along each side of the room, and form a square of mirrored rooms
with sides (about) 2*distance. Then check which targets are reachable from the original room with a straight line.

Since the laser reflects in the same angle, the mirrored room is a continuation of the original room.

This was the third hardest problem in general, but hardest/second hardest to implement.

NOTE: This code is quite terrible in quality and readability, but implements the correct solution.
"""

import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle


def relative_pos(wrt,pos):
    return [pos[0]-wrt[0],pos[1]-wrt[1]]

def vector_length(vector):
    return math.sqrt(sum([v**2 for v in vector]))


class Tile:
    my_pos = ()
    enemy_pos = ()
    corner_pos = ()
    size = ()
    def __init__(self,my_pos,enemy_pos,corner_pos,size):
        self.my_pos = tuple(my_pos)
        self.enemy_pos = tuple(enemy_pos)
        self.corner_pos = tuple(corner_pos)
        self.size = tuple(size)
        
    def to_relative_pos(self,pos):
        """Converts absolute position to coordinates relative to the tiles corner"""
        pos = relative_pos(self.corner_pos,pos)
        return tuple(pos)
    
    def change_position_to_relative(self,new_origin):
        self.my_pos = tuple(relative_pos(new_origin,self.my_pos))
        self.enemy_pos = tuple(relative_pos(new_origin,self.enemy_pos))
        self.corner_pos = tuple(relative_pos(new_origin,self.corner_pos))
        
    def plot_tile(self,ax=None):
        if ax is None:
            ax = plt.subplots()[1]
        linewidth = 1 if self.my_pos != (0,0) else 3    # Thiccer if this is the starting tile
        ax.plot([self.corner_pos[0],
                 self.corner_pos[0],
                 self.corner_pos[0]+self.size[0],
                 self.corner_pos[0]+self.size[0],
                 self.corner_pos[0]],
                
                [self.corner_pos[1],
                 self.corner_pos[1]+self.size[1],
                 self.corner_pos[1]+self.size[1],
                 self.corner_pos[1],
                 self.corner_pos[1]],
                linewidth=linewidth
                )
        ax.scatter(self.my_pos[0],self.my_pos[1],color="green")
        ax.scatter(self.enemy_pos[0],self.enemy_pos[1],color="red")


def copy_tile(tile,direction):
    cpos = list(tile.corner_pos)                    # Absolute positions of the tile to be copied
    my_pos = list(tile.my_pos)
    enemy_pos = list(tile.enemy_pos)
    if abs(direction[1]) == 1:                      # If the tile is to be copied in the x-direction
        cpos[0] += direction[1]*tile.size[0]        # The new tiles absolute corner position is moved in the given x-direction by the width of the tile
        # The new absolute positions are calculated by adding the tile width to the original tiles absolute position,
        # then the point (my_pos and enemy_pos) is moved 2*the relative distance in the given direction,
        # finally the tile_size is added to the new absolute position
        my_pos[0] += direction[1]*tile.size[0] - 2*tile.to_relative_pos(my_pos)[0] + tile.size[0]
        enemy_pos[0] += direction[1]*tile.size[0] - 2*tile.to_relative_pos(enemy_pos)[0] + tile.size[0]
        
    elif abs(direction[0]) == 1:                    # If the tile is to be copied in the y-direction
        cpos[1] += direction[0]*tile.size[1]
        my_pos[1] += direction[0]*tile.size[1] - 2*tile.to_relative_pos(my_pos)[1] + tile.size[1]
        enemy_pos[1] += direction[0]*tile.size[1] - 2*tile.to_relative_pos(enemy_pos)[1] + tile.size[1]
    return Tile(my_pos,enemy_pos,cpos,tile.size)

def create_none_array(tile_size,distance,my_pos):
    tile_size = [float(t) for t in tile_size]
    xneq = math.ceil((distance - my_pos[0])/tile_size[0])
    xpos = math.ceil((distance + my_pos[0])/tile_size[0])
    ypos = math.ceil((distance + my_pos[1])/tile_size[1])
    yneq = math.ceil((distance - my_pos[1])/tile_size[1])
    inxdir = xpos + xneq
    inydir = ypos + yneq
    l = [[0 for i in range(-1,int(inxdir)+1)] for j in range(-1,int(inydir)+1)]     # create a list of lists
    return l
    
def insert_center_tile_inplace(tile_array,tile):
    """Inserts the given (original) tile into the tile_array
    The tile should have its coordinates relative to my_pos(=(0,0))
    """
    
    mp = tile.to_relative_pos(tile.my_pos)      # Get my_pos relative to the corner of the tile
    xt = len(tile_array[0])                     # Total number of tiles in the x direction
    yt = len(tile_array)                        # Total number of tiles in the y direction
    tile_size = [float(t) for t in tile.size]    
    # Calculate the index of the tile in the tile array
    row_ind = yt//2 if mp[1]>=tile_size[1]/2 else yt//2 - 1
    col_ind = xt//2 if mp[0]<=tile_size[0]/2 else xt//2 - 1
    tile_array[row_ind][col_ind] = tile
    return (row_ind,col_ind)

def tile_to_left_lower_corner(tar,tile,ind):
    """Tiles the tile array to the left lower corner.
    First goes to left side of the array, and then to the bottom of the array."""
    while True:
        if ind[1] > 0:
            d = (0,-1)
        elif ind[0] > 0:
            d = (-1,0)
        else:
            break
        ind = [ind[0]+d[0],ind[1]+d[1]]
        try:
            if not isinstance(tar[ind[0]][ind[1]],Tile):
                tar[ind[0]][ind[1]] = copy_tile(tile,d)
            tile = tar[ind[0]][ind[1]]
        except IndexError:
            raise IndexError("IndexError: tile array index out of bounds")
    return tar,tile,ind

def gen_next_tile(tar,tile,ind):
    # First tile to the left upper corner
    tar,tile,ind = tile_to_left_lower_corner(tar, tile, ind)
    size = (len(tar[0]),len(tar))
    coldir = 1
    directions = [(0,1) for _ in range(size[0]-1)] + [(1,0)]
    yield tile
    while True:
        if not directions:
            coldir = -1*coldir
            directions = [(0,coldir) for _ in range(size[0]-1)] + [(1,0)]
        d = directions.pop(0)
        ind = [ind[0]+d[0],ind[1]+d[1]]
        try:
            if not isinstance(tar[ind[0]][ind[1]],Tile):
                tar[ind[0]][ind[1]] = copy_tile(tile,d)
            tile = tar[ind[0]][ind[1]]
        except IndexError:
            break
        yield tile
    
def generate_directions(bounds,my_pos,enemy_pos,distance):
    ogtile = Tile(my_pos,enemy_pos,(0,0),bounds)
    ogtile.change_position_to_relative(my_pos)
    assert ogtile.my_pos == (0,0)
    tile_arr = create_none_array(bounds, distance, my_pos)
    rind,cind = insert_center_tile_inplace(tile_arr,ogtile)
    next_tile_gen = gen_next_tile(tile_arr,ogtile,(rind,cind))
    for i,t in enumerate(next_tile_gen):
        yield t

def heading_dist_corners(corner,tile_size):
    """ Return a list of (heading, dist) tuples. These mark the directions and distances to a tiles corners from the beam.
    Order: left lower corner, left upper corner, right upper corner, right lower corner
    """
    corners = []
    ccorner = list(corner)
    for i in range(4):
        if i==0:
            ccorner = (corner[0],corner[1])
        if i==1:
            ccorner = (corner[0],corner[1] + tile_size[1])
        if i==2:
            ccorner = (ccorner[0] + tile_size[0],ccorner[1])
        if i==3:
            ccorner = (ccorner[0],ccorner[1]-tile_size[1])
        corners.append((math.atan2(ccorner[1],ccorner[0]),vector_length(ccorner)))
    return corners


def solution(bounds,my_pos,enemy_pos,distance,plot=False):
    """Count the total number of directions where we can shoot a laser to hit the point at 'enemy_pos' from 'my_pos' in
    a room with dimensions = bounds with the laser traveling a distance of 'distance'

    Args:
        bounds (tuple of 2 ints): Dimensions of the 2D room, (width, height)
        my_pos (tuple of 2 ints): The position (in the room) from where the laser is shot
        enemy_pos (tuple of 2 ints): the position to which we want to hit
        distance (int): The distance that the laser is able to travel
        plot (bool, optional): Whether we want to plot the mirrored rooms and the succesful directions. Defaults to False.

    Returns:
        int : total number of directions that hit the target
    """
    if plot:
        # Initialize plot
        fig,ax = plt.subplots()
        ax.axes.set_visible(True)
        c = Circle((0,0),distance,color='b',fill=False)
        ax.add_patch(c)
        fig.set_size_inches(10,10)
    # Store the closest hit (heading,dist -pair) in a direction (heading) to either the target, self, or a corner
    # If the beam at heading hits self, or a corner (in which cases the beam never hits the target) the distance is stored as a negative value to filter later
    # If the beam hits the target
    hits = {}
    for t in generate_directions(bounds,my_pos,enemy_pos,distance):
        if plot:
            t.plot_tile(ax=ax)
        heading_dist_pairs = [(math.atan2(t.enemy_pos[1],t.enemy_pos[0]),vector_length(t.enemy_pos))]   # Store the heading : dist pair to the enemy at Tile t
        heading_dist_pairs += heading_dist_corners(t.corner_pos,bounds)                                  # Corner heading : dist pairs
        heading_dist_pairs.append((math.atan2(t.my_pos[1],t.my_pos[0]),vector_length(t.my_pos)))        # heading : dist pair to my_pos in mirrored Tile t
        for i,hd in enumerate(heading_dist_pairs):
            h = hd[0]
            d = hd[1]
            if d == float(0):   # Because this is equivalent to not shooting at all, and might overwrite hitting an enemy because d == 0
                continue
            store_value = -1*d
            if i == 0:
                # If the beam will hit me, store a positive value
                store_value *= -1
            hits[h] = store_value if d < abs(hits.get(h,float("inf"))) else hits[h]
    hits = {h:d for h,d in hits.items() if d>0 and d <= distance}
    if plot:
        for h,d in hits.items():
            ax.plot([0,d*math.cos(h)], [0,d*math.sin(h)])
    return len(hits)