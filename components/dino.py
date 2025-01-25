import sys

import pygame

class Dino:
    def __init__(self, x, y, normal_size=(80, 80), giant_size=(160, 160)):
        self.x = x
        self.y = y
        self.normal_size = normal_size
        self.giant_size = giant_size

        # 공룡 애니메이션 이미지 로드
        self.normal_frames = [
            pygame.transform.scale(pygame.image.load(f"assets/images/dino{i}.png"), normal_size)
            for i in range(1,7)
        ]
        self.giant_frames = [
            pygame.transform.scale(pygame.image.load(f"assets/images/dino{i}.png"), giant_size)
            for i in range(1,7)
        ]
        self.kick_frames = [
            pygame.transform.scale(pygame.image.load(f"assets/images/kick{i}.png"), giant_size)
            for i in range(1,4)
        ]

        # 상태 변수
        self.is_giant = False
        self.is_kicking = False
        self.kick_timer = 0  # 발차기 지속 시간 (프레임 단위)
        self.kick_duration = 15  # 발차기 애니메이션 지속 시간
        self.kick_frame_index = 0
        self.frame_index = 0
        self.animation_speed = 0.1  # 애니메이션 속도 (프레임 전환 속도)
        self.frame_counter = 0
        self.frame_delay = 0
        # 점프 상태
        self.is_jumping = False
        self.jump_step = 7

        # 초기 이미지
        self.current_image = self.normal_frames[0]
        self.rect = pygame.Rect(x, y - normal_size[1], normal_size[0], normal_size[1])
        self.giant_rect = pygame.Rect(x, y - giant_size[1], giant_size[0], giant_size[1])

    def toggle_giant_mode(self, is_giant):
        """거대화 모드 전환"""
        self.is_giant = is_giant
        self.is_kicking = False  # Giant 상태에서만 발차기 가능
        self.frame_index = 0  # 애니메이션 초기화

    def animate(self, speed):
        """애니메이션 처리"""
        self.frame_delay = max(1, int(10 / speed))  # speed가 높을수록 delay가 줄어듦

        if self.is_kicking:
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.kick_frame_index += 1
            if self.kick_frame_index >= len(self.kick_frames):
                self.kick_frame_index = 0
            self.current_image = self.kick_frames[self.kick_frame_index]
        else:
            # 걷기 애니메이션 처리
            frames = self.giant_frames if self.is_giant else self.normal_frames
            self.frame_counter += 1
            if self.frame_counter >= self.frame_delay:
                self.frame_counter = 0
                self.frame_index += 1
                if self.frame_index >= len(frames):
                    self.frame_index = 0
                self.current_image = frames[int(self.frame_index)]

    def jump(self):
        """점프 처리"""
        if self.is_jumping:
            if self.jump_step >= - 7:
                self.rect.y -= self.jump_step * abs(self.jump_step)
                self.jump_step -= 1
            else:
                self.is_jumping = False
                self.jump_step = 7

    def start_kick(self):
        """발차기 시작"""
        self.is_kicking = True
        self.kick_timer = self.kick_duration

    def update_kick(self):
        """발차기 지속 시간 업데이트"""
        if self.is_kicking:
            self.kick_timer -= 1
            if self.kick_timer <= 0:
                self.is_kicking = False

    def check_collision(self, hurdles):
        """장애물 충돌 검사"""
        if self.is_giant:
            for hurdle in hurdles:
                if self.giant_rect.colliderect(hurdle.rect):
                    self.start_kick()
                    hurdles.remove(hurdle)  # 충돌한 장애물 제거
        else:
            for hurdle in hurdles:
                if self.rect.colliderect(hurdle.rect):
                    sys.exit()

    def draw(self, screen):
        """공룡을 화면에 그리기"""
        rect = self.giant_rect if self.is_giant else self.rect
        screen.blit(self.current_image, rect)





