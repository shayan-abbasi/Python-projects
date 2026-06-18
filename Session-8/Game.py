
import pygame
import math
import random
import sys

pygame.init()
WIDTH, HEIGHT = 1100, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Angry Stone - Shayan Edition")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Segoe UI", 28, bold=True)

SKY_COLOR = (173, 216, 230)
GROUND_COLOR = (76, 153, 0)
WOOD_COLOR = (193, 154, 107)
STONE_GRAY = (112, 128, 144)
BALL_COLOR = (100, 100, 100) 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


blocks = []
GROUND_Y = 530 

for r in range(7): 
    for c in range(4): 
        y_pos = GROUND_Y - (r * 60) - 50
        blocks.append({
            'rect': pygame.Rect(750 + c*60, y_pos, 20, 50),
            'vel': [0, 0],
            'color': WOOD_COLOR,
            'active': True
        })
        if c < 3:
            blocks.append({
                'rect': pygame.Rect(750 + c*60, y_pos - 5, 80, 15),
                'vel': [0, 0],
                'color': STONE_GRAY,
                'active': True
            })

clouds = [[random.randint(0, WIDTH), random.randint(50, 200)] for i in range(5)]


sling_pos = (220, 480)
bird_pos = list(sling_pos)
is_dragging = False
is_fired = False
bird_vel = [0, 0]
gravity = 0.45
score = 0

def draw_trajectory(start_pos, m_pos):
    temp_pos = list(start_pos)
    temp_vel = [(start_pos[0] - m_pos[0]) * 0.18, (start_pos[1] - m_pos[1]) * 0.18]
    for i in range(15):
        temp_pos[0] += temp_vel[0]
        temp_pos[1] += temp_vel[1]
        temp_vel[1] += gravity
        pygame.draw.circle(screen, (255, 255, 255), (int(temp_pos[0]), int(temp_pos[1])), 2)

running = True
while running:
    screen.fill(SKY_COLOR)

    for cloud in clouds:
        pygame.draw.circle(screen, (255, 255, 255), (int(cloud[0]), int(cloud[1])), 30)
        pygame.draw.circle(screen, (255, 255, 255), (int(cloud[0]+20), int(cloud[1]+5)), 25)
        cloud[0] += 0.5
        if cloud[0] > WIDTH: cloud[0] = -50

    pygame.draw.rect(screen, GROUND_COLOR, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
    pygame.draw.rect(screen, (50, 100, 0), (0, GROUND_Y, WIDTH, 5))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        m_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if math.hypot(m_pos[0]-bird_pos[0], m_pos[1]-bird_pos[1]) < 40 and not is_fired:
                is_dragging = True

        if event.type == pygame.MOUSEBUTTONUP and is_dragging:
            is_dragging = False
            is_fired = True
            bird_vel = [(sling_pos[0] - m_pos[0]) * 0.18, (sling_pos[1] - m_pos[1]) * 0.18]

    if is_dragging:
        m_pos = pygame.mouse.get_pos()
        draw_trajectory(sling_pos, m_pos)
        dist = min(math.hypot(m_pos[0]-sling_pos[0], m_pos[1]-sling_pos[1]), 100)

        angle = math.atan2(m_pos[1]-sling_pos[1], m_pos[0]-sling_pos[0])
        bird_pos = [sling_pos[0] + dist*math.cos(angle), sling_pos[1] + dist*math.sin(angle)]
        pygame.draw.line(screen, (50, 20, 0), sling_pos, bird_pos, 4)

    elif is_fired:
        bird_pos[0] += bird_vel[0]
        bird_pos[1] += bird_vel[1]
        bird_vel[1] += gravity

        if bird_pos[1] > GROUND_Y or bird_pos[0] > WIDTH:
            is_fired = False
            bird_pos = list(sling_pos)

        bird_rect = pygame.Rect(bird_pos[0]-15, bird_pos[1]-15, 30, 30)
        for b in blocks:
            if b['active'] and bird_rect.colliderect(b['rect']):
                b['vel'] = [bird_vel[0]*0.8, bird_vel[1]*0.5]
                score += 5

    for b in blocks:
        if b['vel'] != [0, 0]:
            b['rect'].x += b['vel'][0]
            b['rect'].y += b['vel'][1]
            b['vel'][1] += gravity
            for other in blocks:
                if other != b and other['active'] and b['rect'].colliderect(other['rect']):
                    other['vel'] = [b['vel'][0]*0.5, b['vel'][1]*0.5]
            if b['rect'].bottom > GROUND_Y:
                b['rect'].bottom = GROUND_Y
                b['vel'] = [0, 0]

        pygame.draw.rect(screen, b['color'], b['rect'])
        pygame.draw.rect(screen, BLACK, b['rect'], 2)

    pygame.draw.line(screen, (80, 40, 0), (sling_pos[0], GROUND_Y), (sling_pos[0], 480), 12)

    pygame.draw.circle(screen, BALL_COLOR, (int(bird_pos[0]), int(bird_pos[1])), 18)

    txt = font.render(f"CASTLE SCORE: {score}", True, (50, 50, 50))
    screen.blit(txt, (20, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()