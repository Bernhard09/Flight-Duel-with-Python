import pygame
import time
import os
import sys

pygame.init() # -> Inisialisasi pygame
pygame.font.init() # -> inisialisasi pygame.font

"""
GAME PROPERTIES

"""

"""Menampilan layar"""
WIDTH, HEIGHT = 900, 500 # Lebar dan Tinggi
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) #membuat layar
pygame.display.set_caption("Flight duel") # Judul Game
game_icon = pygame.image.load("Asset\game_icon.png") # load gambar game icon
pygame.display.set_icon(game_icon) # memberi gambar pada icon game

"""Shape"""
BORDER = pygame.Rect((WIDTH//2)-5, 0, 10, HEIGHT)

"""Mengimport Asset"""
# Lebar dan tinggi pesawat
AIRCRAFT_WIDTH, AIRCRAFT_HEIGHT = 100, 70 

"""Properties"""
FPS = 60
COLOR = {
    "Black": (0,0,0),
    "White": (255,255,255),
    "Yellow": (255,255,0),
    "Red": (255,0,0)
}




"""Font-Player Name"""
font_name = pygame.font.SysFont("bahnschrift", 30) #-> Load Font
player_one = font_name.render("Player One", True, COLOR["White"])
player_two = font_name.render("Player Two", True, COLOR["White"])

"""Font-Winner Condition"""
font_win = pygame.font.SysFont("bahnschrift", 40)
player_one_win = font_win.render("Player One Win!", True, COLOR["Yellow"])
player_two_win = font_win.render("Player Two Win!", True, COLOR["Yellow"])
draw_txt = font_win.render("Draw", True, COLOR["Yellow"])

"""Sound Effect"""
bullet_sound = pygame.mixer.Sound("Asset\Audio\shoot sound effect.wav")
hit_sound = pygame.mixer.Sound("Asset\Audio\hit sound effect.wav")
win_sound = pygame.mixer.Sound("Asset\Audio\win medival style.wav")

"""Import asset"""
# German Aircraft
PLANE_ONE_IMG = pygame.image.load("Asset\wwii_german_aircraft.png") # load asset pesawat jerman
PLANE_ONE = pygame.transform.rotate(pygame.transform.scale(
    surface=PLANE_ONE_IMG, size=(AIRCRAFT_WIDTH, AIRCRAFT_HEIGHT)), angle=-90)# mengubah arah sudut dan ukuran pesawat

# US Aircraft
PLANE_TWO_IMG = pygame.image.load("Asset\p-47.png") # load asset pesawat us
PLANE_TWO = pygame.transform.rotate(pygame.transform.scale(
    surface=PLANE_TWO_IMG, size=(AIRCRAFT_WIDTH,AIRCRAFT_HEIGHT)), angle=90) # mengubah arah sudut dan ukuran pesawat


# Game Background
BG_IMG = pygame.image.load(os.path.join('Asset', 'background.jpeg'))

# Health Symbol
HEALTH_SYMBOL = pygame.transform.scale(pygame.image.load("Asset\health_logo.png"), (20,20))


"""
Class Pesawat
"""

class Aircraft:
    VEL = 7 #- > Aircraft Velocty
    BULLET_VEL = 10 # -> Bullet Velocity
    
    # Menambahkan ke pygame event
    ONE_HIT = pygame.USEREVENT + 1
    TWO_HIT = pygame.USEREVENT + 2

    def __init__(self, pos_x, pos_y, WIDTH, HEIGHT, IMG):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.IMG = IMG
    
    """Draw Aircraft to the screen"""
    def draw(self):
        return SCREEN.blit(self.IMG, (self.pos_x, self.pos_y))
    
    """Get Aircraft Rectangle"""
    @property
    def ac_get_rect(self):
        return pygame.Rect(self.pos_x, self.pos_y, self.WIDTH, self.HEIGHT)

    """Handle Movement"""
    @classmethod
    def handle_move(cls, keys, one, two, isEnable):
        if isEnable == True:
            # AIRCRAFT ONE MOVEMENT HANDLER
            if keys[pygame.K_a] and one.pos_x > 0:
                    one.pos_x -= cls.VEL
            if keys[pygame.K_d] and one.pos_x < BORDER.x - (one.WIDTH-25):
                    one.pos_x += cls.VEL 
            if keys[pygame.K_w] and one.pos_y > 0:
                    one.pos_y -= cls.VEL
            if keys[pygame.K_s] and one.pos_y < HEIGHT-100:
                    one.pos_y += cls.VEL

            # AIRCRAFT TWO MOVEMENT HANDLER
            if keys[pygame.K_LEFT] and two.pos_x > BORDER.x + BORDER.width:
                    two.pos_x -= cls.VEL
            if keys[pygame.K_RIGHT] and two.pos_x < WIDTH-60:
                    two.pos_x += cls.VEL 
            if keys[pygame.K_UP] and two.pos_y > 0:
                    two.pos_y -= cls.VEL
            if keys[pygame.K_DOWN] and two.pos_y < HEIGHT-100:
                    two.pos_y += cls.VEL

    """Mengatur Sifat Dari Bullet"""
    @classmethod
    def handle_bullet(cls, one, two, bullet_one, bullet_two, isEnable):
        if isEnable == True:
            for bullets in bullet_one:
                bullets.x += cls.BULLET_VEL 
                if two.ac_get_rect.colliderect(bullets): # jika peluru Pesawat 1 mengenai pesawat 2
                    hit_sound.play() 
                    pygame.event.post(pygame.event.Event(cls.TWO_HIT)) #Maka -> menambahkan event baru TWO_HIT ke pygame.event
                    bullet_one.remove(bullets) # Maka -> peluru "dihilangkan" atau hancur
                
                elif bullets.x > WIDTH: # -> Jika peluru pesawat 1 melewati batas layar
                    bullet_one.remove(bullets) # -> maka peluru "dihilangkan"
        
            for bullets in bullet_two:
                bullets.x -= cls.BULLET_VEL
                if one.ac_get_rect.colliderect(bullets): # jika peluru Pesawat 2 mengenai pesawat 1
                    hit_sound.play()  
                    pygame.event.post(pygame.event.Event(cls.ONE_HIT)) # -> Maka menambahkan event baru ONE_HIT ke pygame.event
                    bullet_two.remove(bullets) # -> Maka peluru "dihilangkan" atau hancur

                elif bullets.x < 0: # Jika peluru pesawat melewati batas layar
                    bullet_two.remove(bullets) # -> Maka peluru "dihilangkan" atau hancur


class PostGame:
    continue_button = pygame.image.load("Asset\continue.png").convert_alpha()
    restart_button = pygame.image.load(os.path.join("Asset", "restart.png")).convert_alpha()
    square_box = pygame.image.load("Asset\PostGameSquare.png").convert_alpha()
    
    # rectangle of each button
    button_width, button_height = 60, 60
    continue_rect = pygame.Rect(square_box.get_rect().width + 80, 300, 60, 60)
    restart_rect = pygame.Rect(300, 300, 60, 60) 

    # add new user event to pygame.USEREVENT 
    isShow = pygame.USEREVENT + 3
    isRestart = pygame.USEREVENT + 4

    def __init__(self, status_txt) -> None:
        self.status_txt = status_txt

    def show(self):
        SCREEN.blit(PostGame.square_box, (220,100))
        SCREEN.blit(self.status_txt, (300, 120))
        SCREEN.blit(PostGame.restart_button, (300, 300))
        SCREEN.blit(PostGame.continue_button, (PostGame.continue_rect.x, PostGame.continue_rect.y))
        pygame.event.post(pygame.event.Event(PostGame.isShow))

    @classmethod
    def check_option(cls, mouse_pos, event):
        if cls.continue_rect.collidepoint(mouse_pos) and event.button == 1:
                print("continue button clicked")
                return True
        
        if cls.restart_rect.collidepoint(mouse_pos) and event.button == 1:
                print("restart button clicked")
                pygame.event.post(pygame.event.Event(cls.isRestart))
                return False

        

"""Menampilkan Objek pada layar"""
def draw_screen(one, two, bullet_one, bullet_two, health_one_bar,health_one_num, health_two_bar, health_two_num, 
    one_win_condition, two_win_condition, draw_condition, score_one_font, score_two_font, post_game):

    #memberi warna putih pada layar
    SCREEN.fill(COLOR["White"])
    
    #Menampilkan background
    SCREEN.blit(BG_IMG,(0,0))

    # menampilkan border ke layar
    pygame.draw.rect(surface=SCREEN, color=COLOR["White"], rect=BORDER)
    
    # menampilkan peluru
    for bullet in bullet_one:
        pygame.draw.rect(surface=SCREEN, color=COLOR["Yellow"], rect=bullet) # surface, colorm, rect

    for bullet in bullet_two:
        pygame.draw.rect(surface=SCREEN, color=COLOR["Yellow"], rect=bullet)

    # menampilkan pesawat
    one.draw()
    two.draw()
    
    # Player name
    SCREEN.blit(player_one, (10, 10))
    SCREEN.blit(player_two, (740, 10))
    
    # Health logo
    SCREEN.blit(HEALTH_SYMBOL, (10,50))
    SCREEN.blit(HEALTH_SYMBOL, (870, 50))
    
    # Health Number
    SCREEN.blit(health_one_num, (140, 45))
    SCREEN.blit(health_two_num, (742, 45))

    # Health Bar
    pygame.draw.rect(SCREEN, COLOR["Red"], health_one_bar)
    pygame.draw.rect(SCREEN, COLOR["Red"], health_two_bar)

    # Player Score
    SCREEN.blit(score_one_font, (WIDTH//2-100, 10))
    SCREEN.blit(score_two_font, (WIDTH//2+70, 10))

    # Show win status/text
    if one_win_condition == True:
        post_game.show()
        

    if two_win_condition == True:
        post_game.show()

    
    if draw_condition == True:
        post_game.show()

    pygame.display.update() # refresh gambar


# Fungsi Utama
def main():
    run = True

    match_range = 2

    while run:
        """screen reset condition"""
        reset_screen = False

        """kondisi musik menang"""
        win_sound_play = True # -> True akan dimainkan

        """object pesawat"""
        one = Aircraft(WIDTH-800, 200, AIRCRAFT_WIDTH, AIRCRAFT_HEIGHT, PLANE_ONE) #left-x, top-y, width, height, image
        two = Aircraft(WIDTH-200, 200, AIRCRAFT_WIDTH, AIRCRAFT_HEIGHT, PLANE_TWO) #left-x, top-y, width, height, image
        
        clock = pygame.time.Clock() # - > FPS
        
        """Tempat/Magazine Amunisi Pesawat"""

        bullet_one = []
        bullet_two = []

        """Player Health Properties"""  
        # Health Bar
        health_bar_width = 100
        health_two_bar_x = 765

        health_one_bar = pygame.Rect(35, 55, health_bar_width, 10)
        health_two_bar = pygame.Rect(health_two_bar_x,55, health_bar_width, 10)

        # Health Number Properties -> diletakkan di dalam fungsi main() karena agar mudah mengganti nilainya saat program dijalankan

        font_health = pygame.font.SysFont("bahnschrift", 20)
        health_one = 10
        health_two = 10

        """Score per-round"""
        font_score = pygame.font.SysFont("bahnschrift", 50)
        score_one = 0
        score_two = 0

        """INDIKASI FUNGSI(Handle Movement dan Bullet) AKTIF """
        isEnable = True

        """TEMPORARY WIN CONDITION"""
        aircraft_one_win = False # aircraft one condition
        aircraft_two_win = False # aircraft two condition
        draw = False # draw condition
        
        """kondisi musik menang"""
        win_sound_play = True # -> kondisi "True" -> akan dimainkan

        """POST GAME"""
        post_game = None

        """PENENTU-AKHIR GAME"""
        isContinue = False

        add_score = True
        

        sub_run = True

        while sub_run:

            mouse_pos = pygame.mouse.get_pos()
            clock.tick(FPS) # -> mengatur kecepatan di 60 frame per-second
            for event in pygame.event.get(): # mendapatkan event seperti tombol yang ditekan dll
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN: # mendeteksi adanya tombol yang ditekan
                    
                    if event.key == pygame.K_LCTRL and len(bullet_one) < 3: # Saat menekan tombol LCTRL maka akan membuat rect Bullet dan mengisi ke amunisi pesawat jika tidak lebih dari 3 amunisi 
                        bullet_sound.play()
                        
                        bullet = pygame.Rect(one.pos_x + (AIRCRAFT_WIDTH//2)-10, one.pos_y + 47, 22, 7) # membuat bullet 
                        bullet_one.append(bullet) # memasukkan bullet ke dalam amunisi (list) 
                        print("Bullet one", bullet_one)

                    if event.key == pygame.K_RCTRL and len(bullet_two) < 3:
                        print(event.key)
                        bullet_sound.play()
                        
                        bullet = pygame.Rect(two.pos_x + (AIRCRAFT_WIDTH//2)-10, two.pos_y + 47, 22, 7)
                        bullet_two.append(bullet)
                        print("Bullet two", bullet_two)
                

                
                """Jika event type -> ONE HIT/TWO_HIT atau Saat pesawat terkena peluru"""
                if event.type == Aircraft.ONE_HIT:
                    print("event type: ",event.type)
                    health_one_bar.width -= 10 # Mengurangi panjang bar darah pesawat 1
                    if health_one > 0: # jika health num lebih besar dari nol
                        health_one -= 1 # mengurangi jumlah nyawa pesawat 1

                if event.type == Aircraft.TWO_HIT:
                    health_two_bar.width -= 10 # Mengurangi panjang bar darah pesawat 2
                    health_two_bar.x += 10 # jika terkena peluru dan panjang bar terkurangi maka geser 10px ke kanan
                    if health_two > 0: # jika heal   
                        health_two -= 1 # mengurangi jumlah nyawa pesawat 2

                if event.type == PostGame.isShow:
                    isEnable = False

                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    isContinue = PostGame.check_option(mouse_pos, event)

                if event.type == PostGame.isRestart:
                    reset_screen = True

            # rendered health num (diletakkan dalam while loop agar health_one & two dapat terupdate di layar)
            # jika tidak diletakkan di while loop, health_one & two tidak akan terupdate di layar hanya terupdate nilai varnya saja
            health_one_num = font_health.render(str(health_one), True, COLOR["White"])
            health_two_num = font_health.render(str(health_two), True, COLOR["White"])

            #render score font
            score_one_font = font_score.render(str(score_one), True, COLOR["White"])
            score_two_font = font_score.render(str(score_two), True, COLOR["White"])

            # movement handling
            key_press = pygame.key.get_pressed()# -> Mendeteksi input dari keybouard seperti W, A, S, D dan semua input dari keyboard dari yang 'press' sampai 'hold'
            Aircraft.handle_move(key_press, one, two, isEnable) # -> Fungsi untuk menghandle movement
            Aircraft.handle_bullet(one, two, bullet_one, bullet_two, isEnable)
            
            """Handling win condition"""
            if health_one == 0:
                aircraft_two_win = True
                if add_score == True:
                    score_two += 1
                    add_score = False
                
                # untuk mengatasi agar musik dimainkan hanya sekali
                if win_sound_play == True:    
                    win_sound.play()
                    win_sound_play = False  #-> Kondisi musik diubah menjadi False sehingga tidak akan dimainkan di loop selanjutnya

                win_status_txt = player_two_win
                post_game = PostGame(win_status_txt)
                
            elif health_two == 0:
                aircraft_one_win = True
                if add_score == True:    
                    score_one+=1
                    add_score = False 
                
                # untuk mengatasi agar musik dimainkan hanya sekali
                if win_sound_play == True:
                    win_sound.play()
                    win_sound_play = False #-> Kondisi musik diubah menjadi False sehingga tidak akan dimainkan di loop selanjutnya

                win_status_txt = player_one_win
                post_game = PostGame(win_status_txt)
                
            elif (health_one and health_two) == 0:
                draw = True
                
            
            
            draw_screen(one, two, bullet_one, bullet_two, health_one_bar,health_one_num ,
                health_two_bar, health_two_num, aircraft_one_win, aircraft_two_win, draw,score_one_font, score_two_font, post_game) # -> Menampilkan objek ke layar dan me-refreshnya jika kondisi berubah seperti posisi objek

        
            #Jika end == true maka run == false sehingga while loop terhenti
            if isContinue == True:
                sub_run = False
                run = False
            
            elif isContinue == False and reset_screen == True:
                sub_run = False # sub_run diubah menjadi False sehingga kembali ke awal run dan merubah value variable seperti semula
                pygame.event.clear()
                
                bullet_one.clear()
                bullet_two.clear()

                win_sound.stop()



                

        # saat game selesai maka tunggu selama 5 detik lalu tutup game 
        time.sleep(1)
        pygame.mixer.stop()

"""
MAIN MENU
"""



"""Menu Properties"""
play_button = pygame.image.load("Asset\play button.png")
quit_button = pygame.image.load("Asset\quit button.png")

title_logo = pygame.image.load(os.path.join("Asset", "title logo.png"))

menu_bg = pygame.transform.scale(pygame.image.load("Asset\menu_bg.jpg"), (WIDTH,HEIGHT))

def draw_menu(play_rect, quit_rect, hm_rect):
    SCREEN.fill(COLOR["Black"])

    SCREEN.blit(menu_bg, (0,0))

    SCREEN.blit(title_logo, (312, 20))
    SCREEN.blit(play_button, (play_rect.x, play_rect.y))
    SCREEN.blit(quit_button, (quit_rect.x, quit_rect.y))
  


    pygame.display.update() 

""" 
def handle_button(mouse):
    # if mouse -> press play button
    if mouse and 
"""


        

def menu():
    play_rect = pygame.Rect(WIDTH//2-100, (HEIGHT//2)+30, 170, 30)
    hm_rect = pygame.Rect(play_rect.x, (play_rect.y + 50), 170, 30)
    quit_rect = pygame.Rect(play_rect.x, (play_rect.y + 50), 170, 30)

    run_menu = True


    while run_menu:
        pygame.init()
        mouse_pos = pygame.mouse.get_pos()

        """Mengatur seluruh event dalam pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
        
            if event.type == pygame.MOUSEBUTTONDOWN: # jika terdereksi ada tombol mouse yang di tekan
                if play_rect.collidepoint(mouse_pos) and event.button == 1: # maka jika tombol mouse kiri dan posisi cursor mouse bertabrakan dengan tombol play 
                    print("Play button clicked")
                    

                    run_menu = False # -> run menu false
                    return True #-> return true
                
                if quit_rect.collidepoint(mouse_pos) and event.button == 1:
                    print("Quit button clicked")
                    run_menu = False
        
        #handle_button(mouse_press)
        draw_menu(play_rect, quit_rect, hm_rect)
       
    
    return False

"""
PreGame
"""
class PreGame:
    pregame_box = pygame.image.load("Asset\PreGame.png")
    switch_button_r = pygame.image.load("Asset\Switch Button.png")
    switch_button_l = pygame.transform.rotate(switch_button_r, 180)
    round_request = 1
    much_round_font = pygame.font.SysFont("Bahnschrift", 20)
    isShow = pygame.USEREVENT + 5 


    @classmethod
    def show(cls):
        SCREEN.blit(cls.pregame_box, (70, 10))
        SCREEN.blit(cls.switch_button_r, (600, 250))
        SCREEN.blit(cls.switch_button_l, (220, 250))

def draw_pre_game():
    SCREEN.fill(COLOR["White"])

    SCREEN.blit(menu_bg, (0,0))

    pygame.display.update()

def pre_game():
    run = True
    while run:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                run = False
    

        draw_pre_game()
    pygame.quit()


if __name__ == "__main__":
    run_game = True

    while run_game == True:
        play = menu()
        if play == True:
            #pre_game()
            

            main()
        else:
            sys.exit()