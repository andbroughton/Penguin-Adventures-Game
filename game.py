#Andrew Broughton & Marissa Cash

# Our game was inspired by Donkey Kong, and is called The Adventures of Mr. Penguin. It ended up not being very similar to Donkey Kong, but that's ok!
# In level 1, the player (Mr. Penguin) will attempt to reach the top of the level to save Penguinette while avoiding being hit by snowballs being thrown by The Polar Bear, AKA Polar, and additional enemies (eskimos)
# In level 2, Mr. Penguin collects fish (collectibles) to bring back to Penguinette for dinner, all while avoiding being hit again!

# Basic Features:
#   User Input: The player will use the arrow keys to move left and right and the space bar to jump
#   Game Over: When the player is hit by a snowball or other enemy, they lose a "life." When they lose all three lives, they are shown a game over screen, from which they can try the level again
#   Graphics/Images: We will use local image files for Mr. Penguin, Polar, snowballs, the eskimos, fish, penguinette, the health bar, and the background

# Additional Features:
#   Health Bar: The player will have three lives, which will be represented in the top left corner of the screen as hearts, which will deplete by 1 after each hit
#   Collectibles: In level 2, fish must be collected to complete the level
#   Enemies: in addition to snowballs, eskimos will get in the way of the player
#   Sprite Animation: The player will be an animated gamebox using a sprite sheet; Polar, Penguinette, and the eskimos also have sprite animation
#   Restart from Game Over: When the player gets game over, they can hit "1" to restart the level they are on
#   Multiple Levels: 2 levels; must beat the first to proceed to the second

'''
Update Log:
4/24/2023: All code is new since the last checkpoint. User Input, Game Over, and Graphics/Images are all included.
The health bar, collectibles, and sprite animation are also included.
Game is now titled "The Adventures of Mr. Penguin"; "Restart from Game Over" Included
Still to add: Enemies, additional sprites, background (image), updated penguin movement, "winning", general fixes.
Removed: Ladders

5/2/2023: There have been massive additions to the game since last checkpoint. New features include the following:
background; enemies; penguinette character; second level; collectibles (in second level); waiting screen between levels; intro screen; thank you screen; + anything I'm forgetting
'''

### IMPORTANT NOTE: Our game can be quite tricky, but we have a couple things you can use for testing.
#Lines 67 & 68: You can turn 67 into a comment, and 68 from comment to code to start near the end of the first level
#Lines 124 & 125: You can turn 124 into a comment, and 125 from comment to code to not have to collect any fish

#There will be additional commenting throughout the file to help follow along (often above a function, explaining what it does)


#necessary modules are imported and global variables are set to defaults for later use
import uvage
import random

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 800
tick_counter = 0
frame = 0
enemy_frame = 0
bear_frame = 0
penguinette_frame = 5
game_on = False
lives = 3
game_over = False
level = 1
slide1 = False
slide2 = False
setup2_count = 0


#the setup function is responsible for things like setting up the environment, setting up the player and other characters,
#and setting up collectibles (although they aren't used until the second level). Many of the variables are set to global for future use
#this function is only called once, but works for both levels
def setup():
    global player, icon, camera, bear1, bear_images, walls, player_images, health_bar_images, health_bar, snowball_list, enemy, enemy_images, enemy_walls, enemy_list, enemy1, background, platforms, bear_list, penguinette_images, penguinette, fish_list, fish1, fish2, fish3, fish4, fish5, fish6, fish7, fish8, fish9
    camera = uvage.Camera(SCREEN_WIDTH, SCREEN_HEIGHT)

    player_images = uvage.load_sprite_sheet("penguin-gray.png", 4, 3)
    player = uvage.from_image(50, 560, player_images[-1])
    # player = uvage.from_image(500, 60, player_images[-1]) # used for testing
    player.scale_by(1.25)

    penguinette_images = uvage.load_sprite_sheet("obviouslyfemalepenguin.png", 3, 8)
    penguinette = uvage.from_image(20, 77, penguinette_images[-1])
    penguinette.scale_by(1.25)

    background = uvage.from_image(300, 400, "PRE_ORIG_SIZE.png")
    background.scale_by(2.5)

    bear_images = uvage.load_sprite_sheet("bear-polar.png", 1, 8)
    bear1 = uvage.from_image(90, 70, bear_images[-1])
    bear1.scale_by(2)
    bear_list = [bear1]

    platforms = [
        uvage.from_color(200, 500, "white", 1050, 10),
        uvage.from_color(600, 400, "white", 1050, 10),

        uvage.from_color(200, 300, "white", 1050, 10),
        uvage.from_color(600, 200, "white", 1050, 10),

        uvage.from_color(200, 100, "white", 1050, 10),
    ]


    walls = [
           uvage.from_color(0, SCREEN_HEIGHT / 2, "black", 5, SCREEN_HEIGHT),
           uvage.from_color(SCREEN_WIDTH, SCREEN_HEIGHT / 2, "black", 5, SCREEN_HEIGHT)
       ]

    snowball_list = []

    enemy_images = uvage.load_sprite_sheet("Eskimo_32 x 32.png", 4, 8)
    enemy1 = uvage.from_image(400, 555, enemy_images[29])
    enemy1.scale_by(2)
    enemy1.speedx = 3
    enemy1.flip()
    enemy2 = enemy1.copy_at(400, 465)
    enemy2.speedx = -3
    enemy3 = enemy1.copy_at(400, 365)
    enemy3.speedx = 3
    enemy3.flip()
    enemy_list = [enemy1, enemy2, enemy3]

    fish1 = uvage.from_image(400, 569, "fish.png")
    fish1.scale_by(0.08)
    fish2 = fish1.copy_at(400, 379)
    fish3 = fish1.copy_at(400, 179)
    fish4 = fish1.copy_at(15, 279)
    fish5 = fish1.copy_at(785, 279)
    fish6 = fish1.copy_at(15, 479)
    fish7 = fish1.copy_at(785, 479)
    fish8 = fish1.copy_at(15, 79)
    fish9 = fish1.copy_at(785, 79)

    fish_list = [fish1, fish2, fish3, fish4, fish5, fish6, fish7, fish8, fish9]
    # fish_list = [] # used for testing
    for f in fish_list:
        f.speedy = 1


    enemy_walls = [
        uvage.from_color(100, 300, "red", 10, 600),
        uvage.from_color(700, 300, "red", 10, 600)
    ]

    icon = uvage.from_image(50, 560, player_images[-1])
    icon.scale_by(1.25)


#just draws the platforms, which were defined in setup, (also draws the bottom floor)
def handle_platforms():
    global floors, bottom_floor, platforms
    bottom_floor = uvage.from_color(SCREEN_WIDTH / 2, SCREEN_HEIGHT, "white", SCREEN_WIDTH + 10, 30)
    camera.draw(bottom_floor)

    for p in platforms:
        camera.draw(p)


# handles the player's x movement. This is also where the player sprite animation is set up.
# Makes sure the player can't move through walls or platforms
def handle_xmovement():
    global frame
    is_moving = False
    if uvage.is_pressing("right arrow"):
        player.x += 8
        is_moving = True
        frame += .3
        if frame >= 3:
            frame = 0
        player.image = player_images[int(frame)+3]
    if uvage.is_pressing("left arrow"):
        player.x -= 8
        is_moving = True
        frame += .3
        if frame >= 3:
            frame = 0
        player.image = player_images[int(frame) + 9]
    for w in walls:
        player.move_to_stop_overlapping(w)
    for p in platforms:
        if player.left_touches(p) or player.right_touches(p):
            player.move_to_stop_overlapping(p)
    if not is_moving:
        player.image = player_images[8]
    player.move_speed()
    camera.draw(player)


#same idea as xmovement, but ymovement
def handle_ymovement():
    condition = False
    for p in platforms:
        if player.bottom_touches(bottom_floor):
            player.yspeed = 0
            condition = True
            player.move_to_stop_overlapping(bottom_floor)
            if uvage.is_pressing("space"):
                player.yspeed = -10
        elif player.bottom_touches(p):
            player.move_to_stop_overlapping(p)
            player.yspeed = 0
            condition = True
            if uvage.is_pressing("space"):
                player.yspeed = -10
        elif player.top_touches(p):
            player.move_to_stop_overlapping(p)
    if condition == False:
        player.yspeed += 1
    player.move_speed()
    camera.draw(player)


#bear's movement is set up (sprite animation); it just moves in place, doesn't change position;
# I create a bear list since there will be multiple bears in level 2
def handle_bear():
    global bear_frame
    bear_frame += .3
    if bear_frame >= 5:
        bear_frame = 0
    for bear in bear_list:
        bear.image = bear_images[int(bear_frame)+3]
        camera.draw(bear)


#sets up penguinette's movement; similar to the bear, she doesn't change position, just moves in place
def handle_penguinette():
    global penguinette_frame
    penguinette_frame += 0.3
    if penguinette_frame >= 8:
        penguinette_frame = 5
    penguinette.image = penguinette_images[int(penguinette_frame)+3]
    camera.draw(penguinette)


#sets up the snowballs which are thrown by the bear(s).
# Set up such that they flip direction when they hit a wall, and they roll on platforms
def handle_snowballs():
    global snowball, snowball_list, random_x
    random_x = random.randint(77, 87)
    snowball = uvage.from_image(random_x, 70, "snowball.png")
    snowball.scale_by(0.5)
    snowball.speedx = 5
    for s in snowball_list:
        if s.bottom_touches(bottom_floor):
            snowball_list.remove(s)
        s.yspeed += 1
        for p in platforms:
            if s.touches(p):
                s.yspeed = 0
                s.move_to_stop_overlapping(p)
        for w in walls:
                if s.touches(w):
                    s.xspeed *= -1
        s.move_speed()
    if level == 1:
        if tick_counter % 90 == 0:
            snowball_list.append(snowball)
    for s in snowball_list:
        camera.draw(s)
    if level == 2:
        random_x2 = random.randint(750, 760)
        snowball2 = uvage.from_image(random_x2, 70, "snowball.png")
        snowball2.scale_by(0.5)
        snowball2.speedx = -5
        if tick_counter % 180 == 0:
            snowball_list.append(snowball2)
        if tick_counter % 180 == 0:
            snowball_list.append(snowball)


#ends level 1 when you reach penguinette. Level is set equal to 2, which allows level 2 to start (this is set up in tick).
def level1win():
    global level, snowball_list, lives
    if player.touches(penguinette):
        player.x = penguinette.x = 20
        for s in snowball_list:
            s.xspeed = 0
        if uvage.is_pressing('space'):
            player.speedy = 0
        level = 2
        lives = 3


#sets up the health_bar; the player has three lives; the player is reset to the starting position everytime they are hit;
#if all lives are lost, game_over = True, which allows the player to try again
def health_bar():
    global lives, game_over
    heart1 = uvage.from_image(780, 20, "healthsymbol.png")
    heart1.scale_by(0.75)
    heart2 = uvage.from_image(755, 20, "healthsymbol.png")
    heart2.scale_by(0.75)
    heart3 = uvage.from_image(730, 20, "healthsymbol.png")
    heart3.scale_by(0.75)
    for s in snowball_list:
        if player.touches(s, -5):
            lives -= 1
            player.x = 80
            player.y = 560
    for enemy in enemy_list:
        if player.touches(enemy, -40):
            lives -= 1
            player.x = 80
            player.y = 560
    for b in bear_list:
        if player.touches(b,-15):
            lives -= 1
            player.x = 80
            player.y = 560
    if lives == 3:
        camera.draw(heart1)
        camera.draw(heart2)
        camera.draw(heart3)
    if lives == 2:
        camera.draw(heart1)
        camera.draw(heart2)
    if lives == 1:
        camera.draw(heart1)
    if lives == 0:
        game_over = True


#handles the eskimo movement, and sets up their sprite animation,
# makes them turn around when they hit certain invisible walls that are set up in each level
def enemies():
    global enemy_frame, enemy_facing_right, enemy, enemy_images
    enemy_frame += .3
    if enemy_frame >= 4:
        enemy_frame = 0
    for enemy in enemy_list:
        enemy.image = enemy_images[int(enemy_frame) + 26]
        for i in enemy_walls:
            if enemy.touches(i):
                enemy.xspeed *= -1
                enemy.flip()
        for w in walls:
            if enemy.touches(w, -10):
                enemy.xspeed *= -1
                enemy.flip()
        enemy.move_speed()
        camera.draw(enemy)


#shows the player a screen, that allows them to press "1" to try the level they are on again
def loss():
    camera.clear("dark blue")
    player.x = snowball.x
    camera.draw(uvage.from_text(400, 150, "game over...", 50, "white", italic=False))
    camera.draw(uvage.from_text(400, 300, "You got pummeled!", 50, "white", italic=False))
    camera.draw(uvage.from_text(400, 450, "Mr. Penguin Died.", 50, "white", italic=False))
    camera.draw(uvage.from_text(400, 500, "Press 1 to restart.", 30, "white", italic=False))
    camera.display()


#setup is called before the additional functions for level 2 are written
setup()





#Level 2 Code; two addition functions are written: setup2 and fish

#setup2 does thing like resetting the snowballs and player position, and setting up the new positions of enemies,
#platforms, Penguinette, bears, and invisible enemy walls
def setup2():
    global game_on, enemy_list, enemy_walls, platforms
    game_on = False
    snowball_list.clear()

    player.x = 80
    player.y = 565

    penguinette.x = 20
    penguinette.y = 567

    enemy_list.clear()
    L2enemy1 = uvage.from_image(400, 555, enemy_images[29])
    L2enemy1.scale_by(2)
    L2enemy1.speedx = 3
    L2enemy1.flip()
    L2enemy2 = L2enemy1.copy_at(100, 465)
    L2enemy2.speedx = -3
    L2enemy3 = L2enemy1.copy_at(700, 465)
    L2enemy3.speedx = 3
    L2enemy3.flip()
    L2enemy4 = L2enemy1.copy_at(400, 365)
    L2enemy4.speedx = 3
    L2enemy4.flip()
    L2enemy5 = L2enemy1.copy_at(400, 165)
    L2enemy5.speedx = -3
    L2enemy6 = L2enemy1.copy_at(100, 265)
    L2enemy6.speedx = -3
    L2enemy7 = L2enemy1.copy_at(700, 265)
    L2enemy7.speedx = 3
    L2enemy7.flip()
    enemy_list = [L2enemy1,L2enemy2,L2enemy3,L2enemy4,L2enemy5,L2enemy6,L2enemy7]

    bear2 = bear1.copy_at(710,70)
    bear2.flip()
    bear_list.append(bear2)

    enemy_walls = [
        uvage.from_color(255, 300, "red", 10, 600),
        uvage.from_color(535, 300, "red", 10, 600)
    ]

    platforms.clear()
    platforms = [
        uvage.from_color(100, 100, "white", 300, 10),
        uvage.from_color(700, 100, "white", 300, 10),
        uvage.from_color(400, 200, "white", 200, 10),

        uvage.from_color(100, 300, "white", 300, 10),
        uvage.from_color(700, 300, "white", 300, 10),
        uvage.from_color(400, 400, "white", 200, 10),

        uvage.from_color(700, 500, "white", 300, 10),
        uvage.from_color(100, 500, "white", 300, 10),
    ]


#fish sets up the mechanics of the collectibles; they hover up and down over the platforms and disappear after collected;
# they must all be collected before the level can be completed; they are reset if the player gets game over and tries again
def fish():
    global fish_list
    for f in fish_list:
        if tick_counter % 10 == 0:
            f.speedy *= -1
        f.move_speed()
        camera.draw(f)
        if player.touches(f):
            fish_list.remove(f)

    if len(fish_list) == 0 and player.touches(penguinette):
        camera.clear('blue')
        camera.draw(
            uvage.from_text(400, 200, "Yay! Mr. Penguin and Penguinette live happily ever after,", 40, "white",italic=False))
        new_icon = icon.copy_at(350, 400)
        new_icon.flip()
        camera.draw(new_icon)
        fish_icon = uvage.from_image(400, 403, "fish.png")
        fish_icon.scale_by(0.08)
        camera.draw(fish_icon)
        penguinette_icon = uvage.from_image(450, 405, penguinette_images[0])
        penguinette_icon.scale_by(1.25)
        penguinette_icon.flip()
        camera.draw(penguinette_icon)
        camera.draw(uvage.from_text(400, 300, "with their freshly-cooked dinner.", 40, "white", italic=False))
        camera.draw(uvage.from_text(400, 500, "Thanks for Playing!", 40, "white", italic=False))
        camera.display()
        player.x = penguinette.x = 20
        for s in snowball_list:
            s.xspeed = 0
        if uvage.is_pressing('space'):
            player.speedy = 0
    if level ==2 and uvage.is_pressing('1'):
        fish_list = [fish1, fish2, fish3, fish4, fish5, fish6,fish7, fish8, fish9]


#Our tick function is extremely long because we were having a lot of trouble with setting up multiple levels,
#and our solution ending up involving a very long tick function.
#In hindsight, we should have used additional helper functions for our tick (or made it more concise),
#but are worried that changing it up now could mess with the level changing mechanics so we are leaving it as is.
def tick():
    global tick_counter, game_on, lives, snowball_list, game_over, slide2, slide1, setup2_count, fish_list
    #this is where the level number comes into effect; starts with code for level 1
    if level == 1:
        #the following lines set up the multiple intro screen and allows the player to start the game using the space bar
        if slide1 == False and slide2 == False:
            camera.clear("dark blue")
            camera.draw(uvage.from_text(400, 150, "Press Right Arrow Key to Continue...", 50, "white", italic=False))
            camera.draw(uvage.from_text(400, 300, "THE ADVENTURES OF MR. PENGUIN", 50, "white", italic=False))
            camera.display()
        if uvage.is_pressing("right arrow"):
            slide1 = True
        if slide1 == True and slide2 == False:
            camera.clear("dark blue")
            camera.draw(
                uvage.from_text(400, 120, "You are Mr. Penguin. Handsome and sweet.", 40, "white", italic=False))
            camera.draw(icon)
            icon.x = 400
            icon.y = 150
            camera.draw(uvage.from_text(400, 200, "You must save your mistress, Penguinette,", 40, "white", italic=False))
            camera.draw(uvage.from_text(400, 250, "from the evil Polar", 40, "white", italic=False))
            camera.draw(uvage.from_text(400, 300, "and get dinner afterwards.", 40, "white", italic=False))
            camera.draw(uvage.from_text(400, 370, "Use arrow keys to move", 40, "red", italic=True))
            camera.draw(uvage.from_text(400, 410, "& space bar to jump.", 40, "red", italic=True))
            camera.draw(uvage.from_text(400, 500, "Surpass the Evil Eskimos and the snowballs to save her!", 40, "white",italic=False))
            camera.draw(uvage.from_text(400, 550, "Press space to start Level 1.", 40, "white", italic=False))
            camera.display()
        if slide1 == True and uvage.is_pressing("space"):
            slide2 = True
        if slide1 == True and slide2 == True:
            # game is actually started
            camera.draw(background)
            handle_platforms()
            handle_xmovement()
            handle_ymovement()
            handle_snowballs()
            handle_penguinette()
            enemies()
            handle_bear()
            health_bar()
            level1win()
            #when the player dies, game_over is made true, and loss is called; pressing 1 allows restart
            if game_over == True:
                loss()
                if uvage.is_pressing("1"):
                    game_over = False
                    lives = 3
                    player.x = 80
                    player.y = 560
                    snowball_list = []
            camera.display()
            tick_counter += 1
    #here, the level 2 code starts
    if level == 2:
    #here, setup2 is called only once (only the first tick)
        if setup2_count == 0:
            setup2()
            setup2_count += 1
    #this is a screen between the two levels, where the player can press space to start level 2
        if game_on == False:
            camera.clear("dark blue")
            camera.draw(uvage.from_text(400, 150, "Now that have saved penguinette", 50, "white", italic=False))
            camera.draw(uvage.from_text(400, 200, "you want to make dinner!", 50, "white", italic=False))
            camera.draw(uvage.from_text(400, 300, "Pick up all the fish, and return to penguinette.", 50, "white",
                                        italic=False))
            camera.draw(uvage.from_text(400, 400, "Press space to start Level 2!", 50, "white", italic=False))
            camera.display()
        if uvage.is_pressing("space"):
            game_on = True
        #level two is actually run here
        if game_on == True:
            camera.draw(background)
            handle_platforms()
            handle_xmovement()
            handle_ymovement()
            handle_snowballs()
            enemies()
            handle_bear()
            health_bar()
            handle_penguinette()
            fish()
            #same loss mechanic as level 1
            if game_over == True:
                loss()
                if uvage.is_pressing("1"):
                    game_over = False
                    lives = 3
                    player.x = 80
                    player.y = 560
                    snowball_list = []
            camera.display()
            #this tick counter (and the one above for level 1) were crucial for things like sprite animation and snowball launching
            tick_counter += 1

#finally, we tell uvage to call the tick method 30 times per second
uvage.timer_loop(30, tick)