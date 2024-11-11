import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set window size
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Number Conversion Quiz")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load fonts
font_title = pygame.font.SysFont('Comic Sans MS', 70)  # Font for the title
font_instructions = pygame.font.SysFont('Verdana', 24)  # Font for instructions
font_quiz = pygame.font.SysFont('Comic Sans MS', 35)  # Font for quiz questions
font_feedback = pygame.font.SysFont('Comic Sans MS', 40)  # Font for feedback messages
font_small = pygame.font.SysFont('Comic Sans MS', 24)  # Font for small texts (e.g., score)

# Load background images
try:
    intro_image = pygame.image.load('intro_image.png')  # Add your intro image file here
    intro_image = pygame.transform.scale(intro_image, (WIDTH, HEIGHT))  # Scale the image to fit the screen
except pygame.error:
    print("Image file not found. Make sure 'intro_image.png' is in the correct path.")
    intro_image = None

quiz_bg = pygame.image.load('quiz_bg.png')  # Image for quiz background
quiz_bg = pygame.transform.scale(quiz_bg, (WIDTH, HEIGHT))  # Scale to fit the screen

# Load correct and wrong backgrounds
correct_bg = pygame.image.load('correct_bg.png')
wrong_bg = pygame.image.load('wrong_bg.png')

# Load sounds
correct_sound = pygame.mixer.Sound('correct_sound.mp3')
wrong_sound = pygame.mixer.Sound('wrong_sound.mp3')
question_sound = pygame.mixer.Sound('background_music.mp3')

# Start background music
pygame.mixer.music.load('background_music.mp3')  # Load your background music file
pygame.mixer.music.play(-1)  # Play it indefinitely

# Define game variables
score = 0
current_num = 0
conversion_from = ""
conversion_to = ""
correct_answer = ""
timer = 45  # Timer for each question
clock = pygame.time.Clock()  # Create a clock object to manage frame rate

def decimal_to_any_base(number, base):
    """Convert decimal to any base (2, 8, 16)"""
    if base == 2:
        return bin(number)[2:]
    elif base == 8:
        return oct(number)[2:]
    elif base == 16:
        return hex(number)[2:].upper()

def any_base_to_decimal(number_str, base):
    """Convert any base (2, 8, 16) to decimal"""
    try:
        return str(int(number_str, base))
    except ValueError:
        return "ERROR"

def generate_question():
    global current_num, conversion_from, conversion_to, correct_answer
    
    # Include Octal in conversion types
    conversion_types = ['Binary', 'Decimal', 'Hexadecimal', 'Octal']
    conversion_from, conversion_to = random.sample(conversion_types, 2)
    
    # Generate a random number based on the 'from' type
    if conversion_from == 'Decimal':
        current_num = random.randint(1, 255)  # Increased range
        if conversion_to == 'Binary':
            correct_answer = decimal_to_any_base(current_num, 2)
        elif conversion_to == 'Hexadecimal':
            correct_answer = decimal_to_any_base(current_num, 16)
        elif conversion_to == 'Octal':
            correct_answer = decimal_to_any_base(current_num, 8)
    
    elif conversion_from == 'Binary':
        decimal_num = random.randint(1, 255)
        current_num = decimal_to_any_base(decimal_num, 2)
        if conversion_to == 'Decimal':
            correct_answer = str(decimal_num)
        elif conversion_to == 'Hexadecimal':
            correct_answer = decimal_to_any_base(decimal_num, 16)
        elif conversion_to == 'Octal':
            correct_answer = decimal_to_any_base(decimal_num, 8)

    elif conversion_from == 'Hexadecimal':
        decimal_num = random.randint(1, 255)
        current_num = decimal_to_any_base(decimal_num, 16)
        if conversion_to == 'Decimal':
            correct_answer = str(decimal_num)
        elif conversion_to == 'Binary':
            correct_answer = decimal_to_any_base(decimal_num, 2)
        elif conversion_to == 'Octal':
            correct_answer = decimal_to_any_base(decimal_num, 8)

    elif conversion_from == 'Octal':
        decimal_num = random.randint(1, 255)
        current_num = decimal_to_any_base(decimal_num, 8)
        if conversion_to == 'Decimal':
            correct_answer = str(decimal_num)
        elif conversion_to == 'Binary':
            correct_answer = decimal_to_any_base(decimal_num, 2)
        elif conversion_to == 'Hexadecimal':
            correct_answer = decimal_to_any_base(decimal_num, 16)

# Function to display the intro screen
def intro_screen():
    screen.blit(intro_image, (0, 0))  # Ensure the intro image fills the screen
    
    title_text1 = font_title.render("Welcome to", True, WHITE)
    title_text2 = font_title.render("Number Quiz", True, WHITE)
    
    title_text1_rect = title_text1.get_rect(center=(WIDTH // 2, HEIGHT // 3 - 50))
    title_text2_rect = title_text2.get_rect(center=(WIDTH // 2, HEIGHT // 3 + 20))
    
    screen.blit(title_text1, title_text1_rect)
    screen.blit(title_text2, title_text2_rect)

    instructions = [
        "Convert numbers between different bases:",
        "- Binary (base 2)",
        "- Octal (base 8)",
        "- Decimal (base 10)",
        "- Hexadecimal (base 16)"
    ]
    
    y_pos = HEIGHT // 2 + 30
    for line in instructions:
        instruction_text = font_instructions.render(line, True, BLACK)
        screen.blit(instruction_text, (50, y_pos))
        y_pos += 25  # Reduced spacing between instructions

    start_text = font_small.render("Press SPACE to Start", True, WHITE)
    start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(start_text, start_text_rect)

# Function to display the quiz question
def display_question():
    screen.blit(quiz_bg, (0, 0))  # Set the quiz background image
    question_text = f"Convert {current_num} from {conversion_from} to {conversion_to}"
    question_render = font_quiz.render(question_text, True, BLACK)
    
    margin = 30
    question_box = pygame.Rect(margin, margin + 50, WIDTH - 2 * margin, HEIGHT // 3)
    pygame.draw.rect(screen, WHITE, question_box)  # Draw a white background for the box
    pygame.draw.rect(screen, BLACK, question_box, 3)  # Draw black border around the box
    
    question_rect = question_render.get_rect(center=question_box.center)  # Centered question inside the box
    screen.blit(question_render, question_rect)

    timer_text = font_small.render(f"Time left: {int(timer)} seconds", True, BLACK)
    screen.blit(timer_text, (650, 50))

    score_text = font_small.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (50, 50))  # Position score on the left side

# Function to display the correct answer screen (green for correct)
def display_correct_answer_right():
    pygame.mixer.music.stop()  # Stop background music
    screen.blit(correct_bg, (0, 0))  # Set the correct background
    correct_text = font_feedback.render(f"Good Job! The answer was: {correct_answer}", True, BLACK)
    correct_text_rect = correct_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
    screen.blit(correct_text, correct_text_rect)
    
    next_question_text = font_small.render("Press SPACE for next question", True, BLACK)
    next_question_text_rect = next_question_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(next_question_text, next_question_text_rect)

    correct_sound.play()
    pygame.display.update()  # Update the display to show the message
    pygame.time.delay(2000)  # Delay to show the message for 2 seconds

# Function to display the wrong answer screen (red for incorrect)
def display_correct_answer_wrong():
    pygame.mixer.music.stop()  # Stop background music
    screen.blit(wrong_bg, (0, 0))  # Set the wrong background
    wrong_text = font_feedback.render(f"Try Again! The correct answer was: {correct_answer}", True, BLACK)
    wrong_text_rect = wrong_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen .blit(wrong_text, wrong_text_rect)

    next_question_text = font_small.render("Press SPACE for next question", True, BLACK)
    next_question_text_rect = next_question_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
    screen.blit(next_question_text, next_question_text_rect)

    wrong_sound.play()
    pygame.display.update()  # Update the display to show the message
    pygame.time.delay(2000)  # Delay to show the message for 2 seconds

# Main game loop
def game_loop():
    global score, timer
    user_answer = ""
    in_intro = True
    wrong_answer = False

    generate_question()

    running = True
    while running:
        screen.fill(WHITE)
        
        if in_intro:
            intro_screen()
        else:
            if wrong_answer:
                display_correct_answer_wrong()
            else:
                display_question()
                user_text_render = font_feedback.render(f"Your answer: {user_answer}", True, BLACK)
                user_text_rect = user_text_render.get_rect(center=(WIDTH // 2, HEIGHT - 100))
                pygame.draw.rect(screen, WHITE, user_text_rect.inflate(20, 20))  # Create a box for the answer
                pygame.draw.rect(screen, BLACK, user_text_rect.inflate(20, 20), 3)  # Border for the answer box
                screen.blit(user_text_render, user_text_rect)

                # Update timer
                timer -= 1 / 60  # Decrease timer based on frame rate
                if timer <= 0:
                    wrong_answer = True  # Time's up, mark as wrong
                    timer = 45  # Reset timer for the next question

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if in_intro:
                    if event.key == pygame.K_SPACE:
                        in_intro = False
                else:
                    if event.key == pygame.K_BACKSPACE:
                        user_answer = user_answer[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_answer.upper() == correct_answer:
                            score += 1
                            display_correct_answer_right()
                            user_answer = ""
                            wrong_answer = False
                            generate_question()  # Generate a new question after displaying the correct answer
                            timer = 45  # Reset timer for the new question
                            pygame.mixer.music.play(-1)  # Restart background music
                        else:
                            wrong_answer = True
                    elif event.key == pygame.K_SPACE and wrong_answer:
                        generate_question()
                        user_answer = ""
                        wrong_answer = False
                        timer = 45  # Reset timer for the new question
                        pygame.mixer.music.play(-1)  # Restart background music
                    else:
                        valid_char = True
                        if conversion_to == 'Binary' and event.unicode not in '01':
                            valid_char = False
                        elif conversion_to == 'Octal' and event.unicode not in '01234567':
                            valid_char = False
                        elif conversion_to == 'Decimal' and not event.unicode.isdigit():
                            valid_char = False
                        elif conversion_to == 'Hexadecimal' and event.unicode.upper() not in '0123456789ABCDEF':
                            valid_char = False
                        
                        if valid_char:
                            user_answer += event.unicode

# Start the game
if __name__ == "__main__":
    game_loop()