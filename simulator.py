#!/usr/bin/env python3
import sys
import math
import random
import pygame

# Configuration
WIDTH, HEIGHT = 800, 800
CX, CY = WIDTH // 2, HEIGHT // 2
TOTAL_PARTICLES = 10**9
PLANET_DATA = [
    ('Mercury', 0.055, 50, 3),
    ('Venus',   0.815, 80, 5),
    ('Earth',   1.000,100, 5),
    ('Mars',    0.107,120, 4),
    ('Jupiter',318.000,160,11),
    ('Saturn', 95.000,190, 9),
    ('Uranus', 14.500,220, 7),
    ('Neptune',17.100,260, 7),
]

# initialize planets
total_mass = sum(p[1] for p in PLANET_DATA)
planets = []
for name, mass, dist, size in PLANET_DATA:
    particles = int(mass / total_mass * TOTAL_PARTICLES)
    orbit_period = 10 * (dist / 100)**1.5  # seconds
    planets.append({
        'name': name,
        'mass': mass,
        'particles': particles,
        'orig_dist': float(dist),
        'dist': float(dist),
        'orig_size': float(size),
        'size': float(size),
        'angle': random.random() * 2 * math.pi,
        'orbit_speed': 2 * math.pi / orbit_period,
        'affected': False,
        'transition': 0.0,
    })

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dead Zone Simulator')
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

button_rect = pygame.Rect(10, 10, 120, 30)
shock_active = False
shock_radius = 0.0
shock_speed = 100.0  # px per second
DRAG_FACTOR = 0.3

running = True
while running:
    dt = clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_rect.collidepoint(event.pos) and not shock_active:
                shock_active = True

    screen.fill((0, 0, 0))
    # draw sun
    pygame.draw.circle(screen, (255, 255, 0), (CX, CY), 20)
    # update and draw planets
    for p in planets:
        p['angle'] += p['orbit_speed'] * (dt / 1000.0)
        if shock_active and not p['affected'] and shock_radius >= p['orig_dist']:
            p['affected'] = True
            p['target_dist'] = p['orig_dist'] * (1 - DRAG_FACTOR)
            p['target_size'] = p['orig_size'] * (1 + DRAG_FACTOR)
        if p['affected']:
            # transition over 1 second
            p['transition'] = min(p['transition'] + dt / 1000.0, 1.0)
            p['dist'] = p['orig_dist'] + (p['target_dist'] - p['orig_dist']) * p['transition']
            p['size'] = p['orig_size'] + (p['target_size'] - p['orig_size']) * p['transition']
        x = CX + math.cos(p['angle']) * p['dist']
        y = CY + math.sin(p['angle']) * p['dist']
        pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), int(p['size']))

    # supernova
    if shock_active:
        shock_radius += shock_speed * (dt / 1000.0)
        # dead zone
        pygame.draw.circle(screen, (255, 0, 0), (CX, CY), int(shock_radius), 0)
        # shock front
        pygame.draw.circle(screen, (255, 255, 255), (CX, CY), int(shock_radius), 2)

    # draw button
    pygame.draw.rect(screen, (100, 100, 100), button_rect)
    pygame.draw.rect(screen, (200, 200, 200), button_rect, 2)
    label = font.render('Supernova', True, (255, 255, 255))
    screen.blit(label, (button_rect.x + 10, button_rect.y + 5))

    # display particles
    y_off = 50
    for p in planets:
        text = f'{p['name']}: {p['particles']}'
        screen.blit(font.render(text, True, (255, 255, 255)), (10, y_off))
        y_off += 20

    pygame.display.flip()

pygame.quit()
sys.exit()
