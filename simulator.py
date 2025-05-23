#!/usr/bin/env python3
import sys, math, random
import pygame

# --- Configuration ---
WIDTH, HEIGHT = 800, 800
CX, CY = WIDTH // 2, HEIGHT // 2

# --- Simulation parameters ---
TOTAL_PARTICLES = 10**9     # total virtual particles
PLANET_DATA = [
    ('Mercury', 0.055,  50,  3),
    ('Venus',   0.815,  80,  5),
    ('Earth',   1.000, 100,  5),
    ('Mars',    0.107, 120,  4),
    ('Jupiter',318.000,160, 11),
    ('Saturn',  95.000,190, 9),
    ('Uranus', 14.500,220, 7),
    ('Neptune',17.100,260, 7),
]

# simulation control
ORBIT_SCALE = 10.0            # base period scale (seconds for 100px orbit)
DRAG_FACTOR = 0.3             # fraction of orbital radius reduction and size increase
SHOCK_SPEED = 100.0           # speed of shock wave (px per second)
EXPLOSION_ALPHA = 60          # alpha transparency for the dead zone (0-255)
SHOCK_THICKNESS = 10          # thickness of the shock ring (px)
SURVIVAL_RADIUS = 200.0       # planets with orig_dist > SURVIVAL_RADIUS are unaffected

# initialize planets
total_mass = sum(m for _, m, *_ in PLANET_DATA)
planets = []
for name, mass, dist, size in PLANET_DATA:
    particles = int(mass / total_mass * TOTAL_PARTICLES)
    period = ORBIT_SCALE * (dist / 100)**1.5
    planets.append({
        'name': name,
        'mass': mass,
        'particles': particles,
        'orig_dist': float(dist),
        'dist': float(dist),
        'orig_size': float(size),
        'size': float(size),
        'angle': random.random() * 2 * math.pi,
        'orbit_speed': 2 * math.pi / period,
        'affected': False,
        'destroyed': False,
        'transition': 0.0,
    })

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dead Zone Simulator')
font = pygame.font.SysFont(None, 24)
clock = pygame.time.Clock()

button = pygame.Rect(10, 10, 120, 30)
shock_active = False
shock_radius = 0.0

running = True
while running:
    dt = clock.tick(60) / 1000.0

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
            running = False
        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1 and button.collidepoint(ev.pos):
            if not shock_active:
                shock_active = True
                shock_radius = 0.0

    screen.fill((0, 0, 0))
    # draw sun
    pygame.draw.circle(screen, (255, 255, 0), (CX, CY), 20)

    # update & draw planets
    for p in planets:
        p['angle'] += p['orbit_speed'] * dt

        if shock_active:
            inner_r = max(0.0, shock_radius - SHOCK_THICKNESS)
            # destruction inside inner void
            if not p['destroyed'] and p['orig_dist'] < inner_r and p['orig_dist'] <= SURVIVAL_RADIUS:
                p['destroyed'] = True
            # drag in shell
            elif not p['affected'] and p['orig_dist'] >= inner_r and p['orig_dist'] <= shock_radius and p['orig_dist'] <= SURVIVAL_RADIUS:
                p['affected'] = True
                p['target_dist'] = p['orig_dist'] * (1 - DRAG_FACTOR)
                p['target_size'] = p['orig_size'] * (1 + DRAG_FACTOR)

        if p['destroyed']:
            continue

        if p['affected'] and p['transition'] < 1.0:
            p['transition'] = min(p['transition'] + dt, 1.0)
            t = p['transition']
            p['dist'] = p['orig_dist'] + (p['target_dist'] - p['orig_dist']) * t
            p['size'] = p['orig_size'] + (p['target_size'] - p['orig_size']) * t

        x = CX + math.cos(p['angle']) * p['dist']
        y = CY + math.sin(p['angle']) * p['dist']
        pygame.draw.circle(screen, (0, 0, 255), (int(x), int(y)), int(p['size']))

    # supernova (donut shell)
    if shock_active:
        shock_radius += SHOCK_SPEED * dt
        inner_r = max(0.0, shock_radius - SHOCK_THICKNESS)
        # draw transparent donut
        explosion_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.circle(explosion_surf, (255, 0, 0, EXPLOSION_ALPHA), (CX, CY), int(shock_radius))
        pygame.draw.circle(explosion_surf, (0, 0, 0, 0), (CX, CY), int(inner_r))
        screen.blit(explosion_surf, (0, 0))
        # ring edges
        pygame.draw.circle(screen, (255, 255, 255), (CX, CY), int(shock_radius), 2)
        pygame.draw.circle(screen, (255, 255, 255), (CX, CY), int(inner_r), 2)

    # draw button
    pygame.draw.rect(screen, (100, 100, 100), button)
    pygame.draw.rect(screen, (200, 200, 200), button, 2)
    label = font.render('Supernova', True, (255, 255, 255))
    screen.blit(label, (button.x + 10, button.y + 5))

    # display particles
    y_off = 60
    for p in planets:
        txt = f"{p['name']}: {p['particles']:,d}"
        screen.blit(font.render(txt, True, (255, 255, 255)), (10, y_off))
        y_off += 18

    pygame.display.flip()

pygame.quit()
sys.exit()
