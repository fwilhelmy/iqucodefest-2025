import pygame

class GameUI:
    
    @staticmethod
    def draw_measure_button(screen, font, width, height):
        btn_rect = pygame.Rect(width - 180, height - 80, 150, 50)
        pygame.draw.rect(screen, (100, 200, 100), btn_rect)
        txt = font.render("Measurement", True, (0, 0, 0))
        screen.blit(txt, (btn_rect.x + 10, btn_rect.y + 10))
        return btn_rect

    @staticmethod
    def draw_skip_button(screen, font, width, height):
        btn_rect = pygame.Rect(width - 350, height - 80, 120, 50)
        pygame.draw.rect(screen, (200, 100, 100), btn_rect)
        txt = font.render("Skip", True, (0, 0, 0))
        screen.blit(txt, (btn_rect.x + 30, btn_rect.y + 10))
        return btn_rect

    @staticmethod
    def draw_player_info(screen, font, players, current_player):
        txt = font.render(f"Current Player: {players[current_player].name}", True, (0, 0, 0))
        screen.blit(txt, (30, 10))

    def draw_gates(screen, font, player, players, current_player, gate_rects, GATE_LIST, GATE_COLORS):
        for i, gate in enumerate(GATE_LIST):
            rect = gate_rects[gate]
            # Highlight in green if current player
            if players[current_player] == player:
                pygame.draw.rect(screen, (0, 255, 0), rect, 4)
            pygame.draw.rect(screen, GATE_COLORS[gate], rect)
            txt = font.render(f"{gate} ({player.gates.get(gate, 0)})", True, (0,0,0))
            screen.blit(txt, (rect.x+5, rect.y+5))

    @staticmethod
    def draw_circuit(screen, font, gate_history, gate_colors, max_gates):
        base_x = 200
        base_y = 150
        num_layers = 1  # layer 0 for both H
        num_layers += max(0, len(gate_history) - 2)
        place_x = base_x + (num_layers + 1) * 60

        for q in range(2):
            y = base_y + q * 60
            ket0_txt = font.render("|0>", True, (0, 0, 0))
            screen.blit(ket0_txt, (base_x - 50, y - 12))
            pygame.draw.line(screen, (0, 0, 0), (base_x, y), (base_x + (max_gates + 5) * 60, y), 2)
            pygame.draw.rect(screen, (0, 255, 0), (place_x - 20, y - 20, 40, 40), 3)

        layer_x = base_x + 60
        for q in range(2):
            y = base_y + q * 60
            pygame.draw.rect(screen, gate_colors["H"], (layer_x - 20, y - 20, 40, 40))
            txt = font.render("H", True, (0, 0, 0))
            screen.blit(txt, (layer_x - 10, y - 10))

        gate_idx = 2
        layer = 1
        while gate_idx < len(gate_history):
            g = gate_history[gate_idx]
            x = base_x + (layer + 1) * 60
            if g[0] == "CNOT":
                _, control, target = g[:3]
                y1 = base_y + control * 60
                y2 = base_y + target * 60
                pygame.draw.circle(screen, (0, 0, 0), (x, y1), 8)
                pygame.draw.line(screen, (0, 0, 0), (x, y1), (x, y2), 2)
                pygame.draw.circle(screen, (0, 0, 0), (x, y2), 12, 2)
                pygame.draw.line(screen, (0, 0, 0), (x - 10, y2), (x + 10, y2), 2)
                pygame.draw.line(screen, (0, 0, 0), (x, y2 - 10), (x, y2 + 10), 2)
            elif g[0] == "SWAP":
                _, q1, q2 = g[:3]
                y1 = base_y + q1 * 60
                y2 = base_y + q2 * 60
                pygame.draw.line(screen, (0, 0, 0), (x - 10, y1 - 10), (x + 10, y1 + 10), 2)
                pygame.draw.line(screen, (0, 0, 0), (x - 10, y1 + 10), (x + 10, y1 - 10), 2)
                pygame.draw.line(screen, (0, 0, 0), (x - 10, y2 - 10), (x + 10, y2 + 10), 2)
                pygame.draw.line(screen, (0, 0, 0), (x - 10, y2 + 10), (x + 10, y2 - 10), 2)
                pygame.draw.line(screen, (0, 0, 0), (x, y1), (x, y2), 2)
            elif g[0] == "DECOH":
                # Draw decoherence gate as a gray box with "D"
                for q in range(2):
                    y = base_y + q * 60
                    pygame.draw.rect(screen, (120,120,120), (x - 20, y - 20, 40, 40))
                    txt = font.render("D", True, (255,255,255))
                    screen.blit(txt, (x - 8, y - 10))
            else:
                gate, qubit = g[:2]
                y = base_y + qubit * 60
                pygame.draw.rect(screen, gate_colors.get(gate, (220, 220, 220)), (x - 20, y - 20, 40, 40))
                txt = font.render(gate, True, (0, 0, 0))
                screen.blit(txt, (x - 10, y - 10))
            gate_idx += 1
            layer += 1

    @staticmethod
    def draw_probability_table(screen, font, probs, width, height):
        # Dessine un graphique à barres comme dans IBM composer
        bar_width = 50
        bar_gap = 30
        base_x = width // 2 - (2 * (bar_width + bar_gap))
        base_y = height - 250
        max_height = 120
        # Axes
        pygame.draw.line(screen, (200,200,200), (base_x-20, base_y), (base_x+4*(bar_width+bar_gap), base_y), 2)
        pygame.draw.line(screen, (200,200,200), (base_x-20, base_y), (base_x-20, base_y-max_height-10), 2)
        # Barres
        for i, state in enumerate(["00", "01", "10", "11"]):
            prob = probs.get(state, 0)
            bar_h = int(prob * max_height)
            x = base_x + i * (bar_width + bar_gap)
            y = base_y - bar_h
            pygame.draw.rect(screen, (100,180,255), (x, y, bar_width, bar_h))
            # Pourcentage
            pct_txt = font.render(f"{int(prob*100)}%", True, (0,0,0))
            screen.blit(pct_txt, (x+5, y-25))
            # Label état
            label_txt = font.render(state, True, (0,0,0))
            screen.blit(label_txt, (x+10, base_y+10))