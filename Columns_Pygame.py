import pygame
import Columns_game_logic as Logic

class ColumnsGame:
    def __init__(self):
        self.running = True
        self.num_rows = 13
        self.num_cols = 8
        self.width = 500
        self.height = 500
        self.game = Logic.ColumnsState(self.num_rows, self.num_cols)
        self.red = (255,0,0)
        self.coral = (213,81,50)
        self.yellow = (219,225,28)
        self.green = (136,248,75)
        self.teal = (30, 158, 194)
        self.frost = (155,250,242)
        self.lavender = (201,68,243)
        self.colors = {'R':self.red,'C':self.coral,'Y':self.yellow,'G':self.green,'T':self.teal,'F':self.frost,'L':self.lavender}
        

    def run(self) -> None:
        '''
        Runs the game
        '''

        pygame.init()

        self.surface = pygame.display.set_mode((self.width, self.height))

        pygame.display.set_caption("Columns")
        
        self.game_board = self.game.create_board()

        clock = pygame.time.Clock()

        WAIT = pygame.USEREVENT
        pygame.time.set_timer(WAIT, 500)
        
        while self.running:
            clock.tick(60)
            
            if not self.game.faller_exists and not self.game.is_matched:
                self.game_board = self.game.create_faller()
                self.print_board()

            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    self.end_game()

                elif event.type == pygame.KEYDOWN and not self.game.is_matched:
                    self.handle_event()

                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.size
                    self._resize_surface(event.size)

                elif event.type == WAIT:
                    if self.game.faller_exists:
                        self.game_board = self.game.drop()
                        self.print_board()

                    else:
                        self.game_board = self.game.freeze()
                        self.print_board()

        pygame.quit()


    def handle_event(self) -> None:
        action = pygame.key.get_pressed()
            
        if action[pygame.K_LEFT] and self.game.faller_exists:
            self.game_board = self.game.move_left()
            self.print_board()

        elif action[pygame.K_RIGHT] and self.game.faller_exists:
            self.game_board = self.game.move_right()
            self.print_board()

        elif action[pygame.K_SPACE] and self.game.faller_exists:
            self.game_board = self.game.rotate_faller()
            self.print_board()

        elif action[pygame.K_DOWN] and self.game.faller_exists:
            self.game_board = self.game.drop()
            self.print_board()

        elif action[pygame.K_DOWN] and not self.game.has_landed():
            self.game_board = self.game.freeze()
            self.print_board()

        elif action[pygame.K_q]:
            self.running = False     

        if self.game.is_game_over:
            print('GAME OVER')
            self.running = False


    def _resize_surface(self, size: (int, int)) -> None:
        pygame.display.set_mode(size, pygame.RESIZABLE)


    def end_game(self) -> None:
        '''
        Sets the self.running variable to False.
        '''
        self.running = False
                
            
    def print_board(self):
        '''
        Takes the current board and prints it.
        '''
        self.surface.fill(pygame.Color(0,0,0))   

        x_counter = 0
        y_counter = 0
        height = self.height // self.num_rows
        width = self.width // (self.num_cols + 14)
        
        for row_index in range(2, self.num_rows + 2):
            y_coor = height * y_counter
            y_counter += 1
            x_counter = 0
            
            for col_index in range(1,self.num_cols+1):
                x_coor = width * (x_counter+7)
                x_counter += 1
                element = self.game_board[row_index][col_index]

                # Normal grid square (hollow white square with thickness of 1 pixel)
                if element == '   ':
                    pygame.draw.rect(self.surface, (255, 255, 255), (x_coor , y_coor, width, height), 1)

                # Matching animation
                elif '*' in element:
                    color = self.colors[element[1]]
                    pygame.draw.rect(self.surface, color, (x_coor , y_coor, width, height), 5)

                # Landing animation
                elif '|' in element:
                    color = self.colors[element[1]]
                    pygame.draw.rect(self.surface, color, (x_coor , y_coor, 5, height))
                    pygame.draw.rect(self.surface, color, (x_coor+width-5 , y_coor, 5, height))
                    
                else:
                    color = self.colors[element[1]]
                    pygame.draw.rect(self.surface, color, (x_coor , y_coor, width, height))

        pygame.display.update()


if __name__ == '__main__':
    ColumnsGame().run()

    
