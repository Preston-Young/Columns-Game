import random

class ColumnsState:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.x_coor = 0
        self.y_coor = 0
        self.board = []
        self.landed = False
        self.is_matched = False
        self.faller_exists = False
        self.is_game_over = False
        self.color_list = ['R', 'Y', 'G', 'F' , 'L']
        

    def create_board(self):
        '''
        Creates the board and returns the nested list.
        '''
        for row_index in range(self.rows+2):
            self.board.append([])

            for col_index in range(self.cols+2):
                if col_index == 0 or col_index == self.cols+1:
                    self.board[row_index].append('|')
                        
                else:
                    self.board[row_index].append('   ')

        return self.board


    def drop(self):
        '''
        Changes the contents of the board when
        the user decides to drop the jewel.
        '''
        self.y_coor += 1
        self.has_landed()

        if not self.landed:    
            for i in range(3):
                self.board[self.y_coor+i][self.x_coor] = '[' + self.faller[i] + ']'
                self.board[self.y_coor-1][self.x_coor] = '   '
 
        else:
            self.y_coor -= 1
            self.landed = False
            self.landing()
            
        return self.board
    

    def move_left(self):
        '''
        Changes the contents of the board when
        the user decides to move the jewel to the left.
        '''

        # This allows the user to move left even when they're at the left-most edge of
        # the board without any consequences
        if self.board[self.y_coor+2][self.x_coor-1] != '   ' or self.x_coor <= 1:
            pass
        
        elif self.x_coor > 1:
            self.x_coor -= 1
            self.has_landed()
            
            if not self.landed:           
                for i in range(3):
                    self.board[self.y_coor+i][self.x_coor] = '[' + self.faller[i] + ']'
                    self.board[self.y_coor+i][self.x_coor+1] = '   '

            else:
                for i in range(3):
                    self.board[self.y_coor+i][self.x_coor] = '|' + self.faller[i] + '|'
                    self.board[self.y_coor+i][self.x_coor+1] = '   '
        
        return self.board
    

    def move_right(self):
        '''
        Changes the contents of the board when
        the user decides to move the jewel to the right.
        '''

        # This allows the user to move right even when they're at the right-most edge of
        # the board without any consequences
        if self.board[self.y_coor+2][self.x_coor+1] != '   ' or self.x_coor >= self.cols:
            pass
   
        elif self.x_coor < self.cols:
            self.x_coor += 1
            self.has_landed()

            if not self.landed:           
                for i in range(3):
                    self.board[self.y_coor+i][self.x_coor] = '[' + self.faller[i] + ']'
                    self.board[self.y_coor+i][self.x_coor-1] = '   '

            else:
                for i in range(3):
                    self.board[self.y_coor+i][self.x_coor] = '|' + self.faller[i] + '|'
                    self.board[self.y_coor+i][self.x_coor-1] = '   '

        
        return self.board
        

    def create_faller(self):
        '''
        Creates a faller in a random column with 3 random colors.
        If the column is full, this method simply returns the board.
        If the faller is created on top of a jewel,
        it changes the board because it's now considered as landed.
        '''

        self.x_coor = random.randint(1,self.cols)

        # Keep trying to create a faller until it's created in a column that isn't full
        while self.is_col_full():
            self.x_coor = random.randint(1,6)

        self.y_coor = 0
        self.faller = []
        self.faller_exists = True
        
        if self.faller_exists:
            for i in range(3):
                next_color = random.choice(self.color_list)

                self.faller.append(next_color)

        else:
            return self.board 

        self.has_landed()
        if not self.landed:
            for i in range(3):
                self.board[i][self.x_coor] = '[' + self.faller[i] + ']'

        else:
            for i in range(3):
                self.board[i][self.x_coor] = '|' + self.faller[i] + '|'

        return self.board


    def is_col_full(self):
        '''
        Checks to see if the column that
        the faller is dropped in is full or not.
        '''
        temp_list = []
        for row_index in range(2, self.rows+2):
            temp_list.append(self.board[row_index][self.x_coor])

        if '   ' not in temp_list:
            self.faller_exists = False

        
    def rotate_faller(self):
        '''
        Changes the contents of the board when
        the user decides to rotate the jewel.
        '''
        self.faller.insert(0,self.faller[-1])
        self.faller.pop(-1)
        self.has_landed()        

        if not self.landed:
            for i in range(3):
                self.board[self.y_coor+i][self.x_coor] = '[' + self.faller[i] + ']'

        else:
            for i in range(3):
                self.board[self.y_coor+i][self.x_coor] = '|' + self.faller[i] + '|'
                
        return self.board
    

    def has_landed(self):
        '''
        Checks to see if the jewel has landed.
        '''
        try:
            if self.board[self.y_coor+3][self.x_coor] != '   ':
                self.landed = True

            else:
                self.landed = False

        except IndexError:
            self.landed = True


    def landing(self):
        '''
        Changes the contents of the board when
        the jewel is landing. If the user waits, the jewel is
        now frozen and the frozen method is called to check for
        a match and change the state of the board.
        '''
        if '|' in self.board[self.y_coor][self.x_coor]:
            for i in range(3):
                self.board[self.y_coor+i][self.x_coor] = ' ' + self.faller[i] + ' '
            self.freeze()
                
        else:
            for i in range(3):
                self.board[self.y_coor+1+i][self.x_coor] = '|' + self.faller[i] + '|'

            self.board[self.y_coor][self.x_coor] = '   '
            self.y_coor += 1
        

    def matching(self):
        '''
        Checks for the matching of the jewels and
        puts asterisks around the jewels where there
        was a match.
        '''
        self.matches = []
        self.left_diagonal()
        self.right_diagonal()
        self.horizontal()
        self.vertical()
        self.remove_duplicates()

        if len(self.matches) >= 3:
            self.is_matched = True

            for match in self.matches:
                value = self.board[match[0]][match[1]][1]
                self.board[match[0]][match[1]] = '*' + value + '*'

        else:
            self.is_matched = False
            

    def left_diagonal(self):
        '''
        Checks for the matching of the jewels in
        the left diagonal direction (forward slash).
        '''
        for col_index in range(2, self.cols):
            for row_index in range(3, self.rows+1):
                previous_value = self.board[row_index-1][col_index+1][1]
                current_value = self.board[row_index][col_index][1]
                next_value = self.board[row_index+1][col_index-1][1]

                if current_value != ' ':
                    if previous_value == current_value and current_value == next_value:
                        self.matches.append([row_index-1, col_index+1])
                        self.matches.append([row_index, col_index])
                        self.matches.append([row_index+1, col_index-1])


    def right_diagonal(self):
        '''
        Checks for the matching of the jewels in
        the right diagonal direction (back slash).
        '''
        for col_index in range(2, self.cols):
            for row_index in range(3, self.rows+1):
                previous_value = self.board[row_index-1][col_index-1][1]
                current_value = self.board[row_index][col_index][1]
                next_value = self.board[row_index+1][col_index+1][1]

                if current_value != ' ':
                    if previous_value == current_value and current_value == next_value:
                        self.matches.append([row_index-1, col_index-1])
                        self.matches.append([row_index, col_index])
                        self.matches.append([row_index+1, col_index+1])


    def horizontal(self):
        '''
        Checks for the matching of the jewels in
        the horizontal direction.
        '''
        for row_index in range(2, self.rows+2):
            for col_index in range(2,self.cols):
                previous_value = self.board[row_index][col_index-1][1]
                current_value = self.board[row_index][col_index][1]
                next_value = self.board[row_index][col_index+1][1]

                if current_value != ' ':
                    if previous_value == current_value and current_value == next_value:
                        self.matches.append([row_index, col_index-1])
                        self.matches.append([row_index, col_index])
                        self.matches.append([row_index, col_index+1])


    def vertical(self):
        '''
        Checks for the matching of the jewels in
        the vertical direction.
        '''
        for col_index in range(1, self.cols+1):
            for row_index in range(3, self.rows+1):
                previous_value = self.board[row_index-1][col_index][1]
                current_value = self.board[row_index][col_index][1]
                next_value = self.board[row_index+1][col_index][1]

                if current_value != ' ':
                    if previous_value == current_value and current_value == next_value:
                        self.matches.append([row_index-1, col_index])
                        self.matches.append([row_index, col_index])
                        self.matches.append([row_index+1, col_index])


    def remove_duplicates(self):
        '''
        If there are matches in more than one
        direction, this method removes the duplicate
        matches that were counted.
        '''
        temp_list = []
        for match in self.matches:
            if match not in temp_list:
                temp_list.append(match)
        self.matches = temp_list


    def remove_matches(self):
        '''
        After the matches have been found, this
        method removes them from the board.
        '''
        for row_index in range(2, self.rows+2):     
            for col_index in range(1, self.cols+2):

                if '*' in self.board[row_index][col_index]:
                    self.board[row_index][col_index] = '   '
        

    def freeze(self):
        '''
        After the board is frozen, it calls the
        matching method to see if there are any matches.
        If there are, the matches are removed and board
        is updated. The freeze method checks again to
        see if there are any matches after the first match
        has completed and so forth. If there are no matches,
        the board returns normally with no brackets around each
        jewel.
        '''
        self.faller_exists = False
        
        if not self.is_matched:

            self.matching()
            if not self.is_matched:  
                self.game_over()

            return self.board

        else:
            self.remove_matches()
            self.gravity()
            self.matching()

            if not self.is_matched:
                self.game_over()
                
            return self.board


    def gravity(self):
        '''
        Implements gravity by making the pieces all
        fall to the bottom of the board.
        '''
        for row_index in range(self.rows+2):     
            for col_index in range(self.cols+2):
                current_item = self.board[row_index][col_index]
                
                if current_item != '   ' \
                and row_index < self.rows+1:
                    
                    if self.board[row_index+1][col_index] == '   ':
                        self.board[row_index+1][col_index] = current_item
                        self.board[row_index][col_index] = '   '
                        self.gravity()
            

    def game_over(self):
        '''
        Checks to see if there is a game over
        after the board is frozen.
        '''
        self.is_game_over = False

        for i in range(2):
            for col in self.board[i]:
                if col != '   ' and col != '|':
                    self.is_game_over = True

            

    
