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

Unfortunately I couldn't solve this one in time, even though I know how to do it. I had other things to prioritize during this challenge.
I did try to get it working, but there was too much debugging etc. to get it to work in time.

I figured the solution after reading about problems related to paths in Billiard tables.
The solution is to mirror the room and everyone in it in along each side of the room, and form a square of mirrored rooms
with sides (not exactly) 2*distance. Then check which targets are reachable from the original room with a straight line.

Since the laser reflects in the same angle, the mirrored room is a continuation of the original room.

This was the third hardest problem in general, but hardest/second hardest to implement.

"""