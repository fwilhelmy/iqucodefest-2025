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
            txt = font.render(f"{gate} ({player.gates[gate]})", True, (0,0,0))
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
            else:
                gate, qubit = g[:2]
                y = base_y + qubit * 60
                pygame.draw.rect(screen, gate_colors.get(gate, (220, 220, 220)), (x - 20, y - 20, 40, 40))
                txt = font.render(gate, True, (0, 0, 0))
                screen.blit(txt, (x - 10, y - 10))
            gate_idx += 1
            layer += 1