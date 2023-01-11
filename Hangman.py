import random
import sqlite3

class Hangman:
    
    #---------------------------------------------------LIST DATA TO CREATE INITIAL DATABASE-----------------------------------------

    Celebs = ['Taylor Swift', 'Chester Bennington', 'Avicii', 'Johnny Depp', 'Arnold Schwarzenegger', 'Tom Hanks', 'Morgan Freeman',
              'Charlie Chaplin', 'Brad Pitt', 'Tom Cruise', 'Leonardo DiCaprio','Daniel Radcliffe','Emma Watson', 'Jim Carrey']
    
    Foods = ['Biryani','Gulab Jamun', 'Pad Thai', 'Fish and Sticks', 'Scrambled Eggs', 'Pork Chop', 'Rasgullah', 'Sushi', 'Pasta',
             'Steak', 'Ramen']
    
    Movies = ['The Godfather', 'The Shawshank Redemption', 'Raging Bull', 'Casablanca', 'Citizen Kane', 'Gone with the Wind',
              'The Wizard of Oz', 'Lawrence of Arabia', 'Up', 'Titanic', 'Harry Potter']
    
    Sports = ['Football', 'Tennis', 'Cricket', 'Basketball', 'Baseball', 'Squash', 'Badminton', 'Handball', 'Kho Kho',
              'Kabaddi', 'Rugby', 'Table Tennis', 'Ping Pong', 'Beach Volleyball', 'Volleyball', 'Hockey', 'Polo',
              'Ice Hockey', 'Swimming']
    
    #-------------------------------------------------END LIST DATA TO CREATE INITIAL DATABASE---------------------------------------
    
    connection = sqlite3.connect('Hangman.db')
    cursor = connection.cursor()
    topics_headings = ['Celebs', 'Foods', 'Movies','Sports']
    topics = [Celebs, Foods, Movies, Sports]

    #-----------------------------------------------------BEGIN METHOD TO CREATE DATABASE--------------------------------------------
    def create_db(self):
        for item in self.topics_headings:

            # SQL command to drop table
            self.cursor.execute(f'DROP TABLE IF EXISTS {item}')
            
            # SQL command to create tables in the database for each item in topics_headings
            self.cursor.execute(f'CREATE TABLE IF NOT EXISTS {item}(keyword CHAR(30))')

        for i in range(len(self.topics_headings)):
            for j in range(0,len(self.topics[i])):

                # SQL command to add values into the respective tables
                self.cursor.execute(f'INSERT INTO {self.topics_headings[i]} VALUES ("{self.topics[i][j]}")')
                test = self.cursor.execute(f'SELECT * FROM {self.topics_headings[i]}').fetchall()
                print(str(test))

        # Save updated changes
        self.connection.commit()
    #---------------------------------------------------END METHOD TO CREATE DATABASE------------------------------------------------

    #----------------------------------------------BEGIN METHOD TO UPADTE DATABASE---------------------------------------------------
    def update_db(self):
        print("\nAdd your favourite topic\n")
        new_topic = input()
        print("\nAdd words to the topic\n")
        new_topiclist = input().split()

        print(new_topiclist)

        if(len(new_topic) == 0 or len(new_topiclist) == 0):
            print("Invalid data entered\n\n")
            self.replay()
            
        # Update existing lists
        if(new_topic not in self.topics_headings):
            self.topics_headings.append(new_topic)
            self.topics.append(new_topiclist)
        else:
            existing_index = self.topics_headings.index(new_topic)
            new_values = list(set(self.topics[existing_index] + new_topiclist)) 
            self.topics[existing_index] = new_values


        # Create Database with new data
        self.create_db()

        print('Added successfully!\n\n')

    #----------------------------------------------END METHOD TO UPADTE DATABASE-----------------------------------------------------
        
    #-----------------------------------------------BEGIN METHOD TO DRAW HANGMAN CARICATURE------------------------------------------
    def draw_hangman(self, inp):
        if(inp==1):
            print(
"""
      _____
     |  
     |  
     |  
     |  
     |  
     |  
   __|__
   
""")
            
        if(inp==2):
            print(
"""
      _____
     |     |
     |     |
     |  
     |  
     |  
     |  
   __|__
   
""")
            
        if(inp==3):
            print(
"""
      _____
     |     |
     |     |
     |  
     |     O
     |  
     |  
   __|__
   
""")
            
        if(inp==4):
            print(
"""
      _____
     |     |
     |     |
     |  
     |     O
     |     |
     |  
   __|__
   
""")

            
        if(inp==5):
            print(
"""
      _____
     |     |
     |     |
     |  
     |     O
     |    /|\\
     |  
   __|__
   
""")

            
        if(inp==6):
            print(
"""
      _____
     |     |
     |     |
     |  
     |     O
     |    /|\\
     |    / \\
   __|__
   
""")
            
            
        if(inp==7):
            print(
"""
      _____
     |     |
     |     |
     |     |
     |     O
     |    /|\\
     |    / \\
   __|__
   
""")

    #--------------------------------------------END METHOD TO DRAW HANGMAN CARICATURE-----------------------------------------------
            
    #-----------------------------------------------------BEGIN-GAMEPLAY METHOD------------------------------------------------------
    def play(self):
        
        input_list = []
        guessed_word = ''
        draw_number = 0
        guess_number = 0
        
        print("""
Let's Play
 _    _          _   _  _____ __  __          _   _ 
| |  | |   /\   | \ | |/ ____|  \/  |   /\   | \ | |
| |__| |  /  \  |  \| | |  __| \  / |  /  \  |  \| |
|  __  | / /\ \ | . ` | | |_ | |\/| | / /\ \ | . ` |
| |  | |/ ____ \| |\  | |__| | |  | |/ ____ \| |\  |
|_|  |_/_/    \_\_| \_|\_____|_|  |_/_/    \_\_| \_|

""")
        
        print('Choose a topic to play:\n')

        # Print available topics
        index = 1
        for item in self.topics_headings:
            print (index,':', item)
            index = index+1
            
        print('\n')
        input_number = int(input())
        print('\nThe topic chosen is',self.topics_headings[input_number-1])

        try:
            # SQL command to select all values for the selected topic from the Database
            selected_list = self.cursor.execute(f'SELECT * from {self.topics_headings[input_number-1]}').fetchall()
        except:
            print("An error occured from our end")
            exit(0)

        # Select random word from the selected topic list
        random_number = random.randint(0,len(selected_list)-1)
        selected_word = str((selected_list)[random_number])
        selected_word = selected_word[2: len(selected_word)-3]

        # Hide letters of selected_word, which are yet to be guessed
        for elem in selected_word:
            if (elem != ' '):
                guessed_word = guessed_word + '-'
            else:
                guessed_word = guessed_word + ' '

        while draw_number < 7:
            
            guess_number= guess_number+1
            print('\n\n'+'Guess Number: ',guess_number)
            print('\nPrevious Inputs:' + str(input_list))
            print('\n\nThe',self.topics_headings[input_number-1][0:-1],'to guess is\n\n',guessed_word)
            print('\n\nYour Guess:')
            input_letter = input()

            # Check if input is present in the word
            if input_letter not in input_list:
                input_list.append(input_letter)
                index = ([i for i, letter in enumerate(selected_word.lower()) if letter == input_letter]) + ([i for i, letter in enumerate(selected_word.upper()) if letter == input_letter])
                for i in range(0,len(selected_word)):
                    if i in index:
                        guessed_word = guessed_word[:i] + selected_word[i] + guessed_word[i + 1:]
                print('\n',guessed_word)

                # Draw Hangman based on incorrect letters
                if((len(index)==0)):
                    draw_number = draw_number+1
                    self.draw_hangman(draw_number)
                    print('Hangman'[:draw_number])

                # Message for the winner
                elif(guessed_word == selected_word):
                    print(
"""
__     __          __          ___         _ _ _ 
\ \   / /          \ \        / (_)       | | | |
 \ \_/ /__  _   _   \ \  /\  / / _ _ __   | | | |
  \   / _ \| | | |   \ \/  \/ / | | '_ \  | | | |
   | | (_) | |_| |    \  /\  /  | | | | | |_|_|_|
   |_|\___/ \__,_|     \/  \/   |_|_| |_| (_|_|_)
   
You unlocked the skill to add a favourite topic & words to the game

""")
                    self.update_db()
                    self.replay()

            # Correctly guessed the letter
            else:
                print('\n',guessed_word)
        else:

            # Print the word when user loses
            print('\n\nThe',self.topics_headings[input_number-1][0:-1],'is:',selected_word,'\n')
            print('You Lose, Try again!\n\n')
            self.replay()
            
    #------------------------------------------------------END GAMEPLAY METHOD-------------------------------------------------------
            
    #----------------------------------------------BEGIN METHOD TO REPLAY GAMEPLAY---------------------------------------------------
    def replay(self):
        print('Press 1 to play again')
        if (1 == int(input())):
            self.play()
        else:
            exit(0)

    #-----------------------------------------------END METHOD TO REPLAY GAMEPLAY----------------------------------------------------

# Start game
Hangman().create_db()
Hangman().play()


