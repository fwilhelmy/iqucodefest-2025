"""
Tiny scene framework – one active scene at a time.
"""

class Scene:
    def __init__(self, manager):
        self.manager = manager           # back-reference if the scene needs to switch

    # The three standard callbacks every scene must implement
    def handle_event(self, event): pass
    def update(self, dt):             pass
    def draw(self, surface):          pass


class SceneManager:
    """
    A 3-line façade around the current scene.
    Call manager.go_to(AnotherScene(...)) whenever you want to switch.
    """
    def __init__(self, start_scene):
        self.scene = start_scene

    def go_to(self, scene):
        self.scene = scene
        print(f">>> switched to {scene.__class__.__name__}")

    # Thin proxies used by the main loop
    def handle_event(self, event): self.scene.handle_event(event)
    def update(self, dt):          self.scene.update(dt)
    def draw(self, surface):       self.scene.draw(surface)
