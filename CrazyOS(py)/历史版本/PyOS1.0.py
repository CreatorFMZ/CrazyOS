import pygame
import sys
import os
import math
from datetime import datetime

# 初始化 Pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyOS - Python 操作系统模拟器")

# 颜色定义
BACKGROUND = (40, 44, 52)
TASKBAR = (30, 34, 45)
WINDOW_BG = (50, 54, 64)
WINDOW_TITLE_BAR = (70, 130, 180)
BUTTON_COLOR = (86, 182, 194)
BUTTON_HOVER = (106, 202, 214)
BUTTON_TEXT = (240, 240, 240)
TEXT_COLOR = (220, 220, 220)
ICON_COLOR = (100, 200, 200)
CLOSE_BUTTON = (220, 100, 100)
CLOSE_HOVER = (240, 120, 120)

# 字体
font_small = pygame.font.SysFont("Arial", 14)
font_medium = pygame.font.SysFont("Arial", 18)
font_large = pygame.font.SysFont("Arial", 24, bold=True)

# 图标类
class Icon:
    def __init__(self, x, y, label, app_type):
        self.x = x
        self.y = y
        self.label = label
        self.app_type = app_type
        self.width = 80
        self.height = 90
        self.selected = False
    
    def draw(self, surface):
        color = (150, 200, 220) if self.selected else ICON_COLOR
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height), border_radius=8)
        pygame.draw.rect(surface, (color[0]-20, color[1]-20, color[2]-20), 
                         (self.x, self.y, self.width, self.height), 2, border_radius=8)
        
        # 绘制图标图形
        if self.app_type == "explorer":
            pygame.draw.rect(surface, (70, 130, 180), (self.x+20, self.y+15, 40, 30), border_radius=4)
            pygame.draw.rect(surface, (100, 160, 210), (self.x+25, self.y+20, 30, 20), border_radius=3)
            pygame.draw.circle(surface, (240, 200, 80), (self.x+40, self.y+55), 15)
        elif self.app_type == "calculator":
            pygame.draw.rect(surface, (70, 160, 110), (self.x+20, self.y+15, 40, 40), border_radius=5)
            for i in range(3):
                pygame.draw.rect(surface, (220, 220, 220), (self.x+25, self.y+25+i*15, 30, 8), border_radius=3)
        elif self.app_type == "browser":
            pygame.draw.rect(surface, (100, 180, 100), (self.x+15, self.y+15, 50, 40), 0, border_radius=5)
            pygame.draw.arc(surface, (50, 120, 50), (self.x+20, self.y+20, 40, 30), 0, math.pi, 3)
            pygame.draw.line(surface, (50, 120, 50), (self.x+20, self.y+35), (self.x+60, self.y+35), 2)
        
        # 绘制标签
        text = font_small.render(self.label, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height - 15))
        surface.blit(text, text_rect)
    
    def is_hovered(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

# 窗口类
class Window:
    def __init__(self, title, x, y, width, height, app_type):
        self.title = title
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.app_type = app_type
        self.active = True
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.content = []
        self.buttons = []
        
        # 添加关闭按钮
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 35, self.y + 10, 25, 25),
            "action": "close"
        })
        
        # 根据应用类型初始化内容
        if app_type == "explorer":
            self.content = ["文档", "图片", "音乐", "视频", "下载", "桌面"]
        elif app_type == "calculator":
            self.content = ["7", "8", "9", "/", 
                            "4", "5", "6", "*", 
                            "1", "2", "3", "-", 
                            "0", ".", "=", "+"]
        elif app_type == "browser":
            self.content = ["欢迎使用 PyBrowser", "Python 是一个强大的编程语言", 
                            "Pygame 可以创建游戏和图形应用", "尝试开发你自己的应用吧!"]
    
    def draw(self, surface):
        # 绘制窗口阴影
        pygame.draw.rect(surface, (20, 20, 30, 180), 
                         (self.x+5, self.y+5, self.width, self.height), border_radius=8)
        
        # 绘制窗口背景
        pygame.draw.rect(surface, WINDOW_BG, (self.x, self.y, self.width, self.height), border_radius=8)
        
        # 绘制标题栏
        pygame.draw.rect(surface, WINDOW_TITLE_BAR, (self.x, self.y, self.width, 40), border_radius=8)
        pygame.draw.rect(surface, WINDOW_TITLE_BAR, (self.x, self.y, self.width, 40), border_radius=8)
        title_text = font_medium.render(self.title, True, TEXT_COLOR)
        surface.blit(title_text, (self.x + 15, self.y + 10))
        
        # 绘制关闭按钮
        button = self.buttons[0]["rect"]
        color = CLOSE_HOVER if button.collidepoint(pygame.mouse.get_pos()) else CLOSE_BUTTON
        pygame.draw.circle(surface, color, button.center, 12)
        pygame.draw.circle(surface, (240, 240, 240), button.center, 12, 2)
        pygame.draw.line(surface, (240, 240, 240), (button.centerx-6, button.centery-6), 
                         (button.centerx+6, button.centery+6), 2)
        pygame.draw.line(surface, (240, 240, 240), (button.centerx+6, button.centery-6), 
                         (button.centerx-6, button.centery+6), 2)
        
        # 绘制窗口内容
        if self.app_type == "explorer":
            for i, item in enumerate(self.content):
                y_pos = self.y + 60 + i * 40
                pygame.draw.rect(surface, (60, 64, 74), (self.x + 20, y_pos, self.width - 40, 30), border_radius=4)
                item_text = font_medium.render(item, True, TEXT_COLOR)
                surface.blit(item_text, (self.x + 40, y_pos + 5))
                
        elif self.app_type == "calculator":
            # 显示区域
            pygame.draw.rect(surface, (30, 34, 40), (self.x + 20, self.y + 60, self.width - 40, 50), border_radius=5)
            display_text = font_large.render("0", True, (100, 200, 150))
            surface.blit(display_text, (self.x + self.width - 40, self.y + 75))
            
            # 按钮
            button_size = 50
            for i in range(4):
                for j in range(4):
                    idx = i * 4 + j
                    if idx < len(self.content):
                        btn_x = self.x + 30 + j * (button_size + 10)
                        btn_y = self.y + 130 + i * (button_size + 10)
                        pygame.draw.rect(surface, BUTTON_COLOR, 
                                        (btn_x, btn_y, button_size, button_size), border_radius=5)
                        btn_text = font_medium.render(self.content[idx], True, TEXT_COLOR)
                        surface.blit(btn_text, (btn_x + button_size//2 - btn_text.get_width()//2, 
                                               btn_y + button_size//2 - btn_text.get_height()//2))
        
        elif self.app_type == "browser":
            # 地址栏
            pygame.draw.rect(surface, (30, 34, 40), (self.x + 20, self.y + 60, self.width - 100, 35), border_radius=5)
            url_text = font_medium.render("pyos://home", True, (150, 180, 220))
            surface.blit(url_text, (self.x + 30, self.y + 65))
            
            # 转到按钮
            pygame.draw.rect(surface, BUTTON_COLOR, (self.x + self.width - 70, self.y + 60, 50, 35), border_radius=5)
            go_text = font_medium.render("GO", True, TEXT_COLOR)
            surface.blit(go_text, (self.x + self.width - 45 - go_text.get_width()//2, self.y + 65))
            
            # 内容区域
            pygame.draw.rect(surface, (60, 64, 74), (self.x + 20, self.y + 110, self.width - 40, self.height - 140), border_radius=5)
            for i, line in enumerate(self.content):
                content_text = font_medium.render(line, True, TEXT_COLOR)
                surface.blit(content_text, (self.x + 40, self.y + 130 + i * 35))
    
    def is_title_bar_hit(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + 40
    
    def is_inside(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

# 任务栏类
class Taskbar:
    def __init__(self):
        self.height = 50
        self.app_buttons = []
        self.time_rect = pygame.Rect(WIDTH - 120, HEIGHT - self.height + 10, 100, 30)
    
    def draw(self, surface):
        # 绘制任务栏
        pygame.draw.rect(surface, TASKBAR, (0, HEIGHT - self.height, WIDTH, self.height))
        pygame.draw.line(surface, (60, 70, 90), (0, HEIGHT - self.height), (WIDTH, HEIGHT - self.height), 2)
        
        # 绘制开始按钮
        pygame.draw.rect(surface, BUTTON_COLOR, (10, HEIGHT - self.height + 5, 80, 40), border_radius=5)
        start_text = font_medium.render("开始", True, TEXT_COLOR)
        surface.blit(start_text, (50 - start_text.get_width()//2, HEIGHT - self.height + 20))
        
        # 绘制应用按钮
        for i, btn in enumerate(self.app_buttons):
            btn_rect = pygame.Rect(100 + i * 120, HEIGHT - self.height + 5, 110, 40)
            pygame.draw.rect(surface, BUTTON_HOVER if btn_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR, 
                           btn_rect, border_radius=5)
            app_text = font_medium.render(btn, True, TEXT_COLOR)
            surface.blit(app_text, (btn_rect.centerx - app_text.get_width()//2, btn_rect.centery - app_text.get_height()//2))
        
        # 绘制时间
        pygame.draw.rect(surface, (40, 50, 70), self.time_rect, border_radius=5)
        current_time = datetime.now().strftime("%H:%M:%S")
        time_text = font_medium.render(current_time, True, TEXT_COLOR)
        surface.blit(time_text, (self.time_rect.centerx - time_text.get_width()//2, 
                               self.time_rect.centery - time_text.get_height()//2))

# 创建桌面图标
desktop_icons = [
    Icon(100, 100, "文件管理器", "explorer"),
    Icon(220, 100, "计算器", "calculator"),
    Icon(340, 100, "浏览器", "browser"),
    Icon(100, 220, "文档", "explorer"),
    Icon(220, 220, "图片", "explorer")
]

# 创建任务栏
taskbar = Taskbar()

# 窗口管理
windows = []
active_window_index = -1

# 时钟
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    current_time = datetime.now()
    mouse_pos = pygame.mouse.get_pos()
    
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 检查是否点击了桌面图标
            for icon in desktop_icons:
                if icon.is_hovered(mouse_pos):
                    # 取消选择其他图标
                    for i in desktop_icons:
                        i.selected = False
                    icon.selected = True
                    
                    # 双击打开应用
                    if event.button == 1 and pygame.time.get_ticks() - getattr(icon, 'last_click', 0) < 300:
                        # 创建新窗口
                        window_title = icon.label
                        if icon.app_type == "explorer":
                            window_title = "文件管理器"
                        elif icon.app_type == "calculator":
                            window_title = "计算器"
                        elif icon.app_type == "browser":
                            window_title = "浏览器"
                        
                        new_window = Window(window_title, 150 + len(windows)*20, 100 + len(windows)*20, 
                                          400, 400, icon.app_type)
                        windows.append(new_window)
                        active_window_index = len(windows) - 1
                        
                        # 添加到任务栏
                        if window_title not in taskbar.app_buttons:
                            taskbar.app_buttons.append(window_title)
                    
                    icon.last_click = pygame.time.get_ticks()
            
            # 检查窗口操作
            for i, window in enumerate(windows[::-1]):
                idx = len(windows) - 1 - i
                if window.is_title_bar_hit(mouse_pos):
                    active_window_index = idx
                    
                    # 开始拖动
                    window.dragging = True
                    window.drag_offset_x = mouse_pos[0] - window.x
                    window.drag_offset_y = mouse_pos[1] - window.y
                    break
                
                # 检查关闭按钮
                for button in window.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["action"] == "close":
                            # 从任务栏移除
                            if window.title in taskbar.app_buttons:
                                taskbar.app_buttons.remove(window.title)
                            windows.pop(idx)
                            if active_window_index == idx:
                                active_window_index = -1
                        break
        
        elif event.type == pygame.MOUSEBUTTONUP:
            # 停止拖动
            for window in windows:
                window.dragging = False
    
    # 更新
    # 更新窗口位置（拖动）
    for i, window in enumerate(windows):
        if window.dragging and i == active_window_index:
            window.x = mouse_pos[0] - window.drag_offset_x
            window.y = mouse_pos[1] - window.drag_offset_y
            window.y = max(0, window.y)  # 限制在屏幕顶部内
            # 更新按钮位置
            window.buttons[0]["rect"] = pygame.Rect(window.x + window.width - 35, window.y + 10, 25, 25)
    
    # 绘制
    # 绘制桌面背景
    screen.fill(BACKGROUND)
    
    # 绘制桌面网格
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, (50, 54, 64), (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (50, 54, 64), (0, i), (WIDTH, i), 1)
    
    # 绘制桌面图标
    for icon in desktop_icons:
        icon.draw(screen)
    
    # 绘制窗口（从后向前）
    for window in windows:
        window.draw(screen)
    
    # 绘制任务栏
    taskbar.draw(screen)
    
    # 绘制系统信息
    os_text = font_large.render("PyOS v1.0", True, (100, 180, 220))
    screen.blit(os_text, (20, 20))
    
    date_text = font_medium.render(current_time.strftime("%Y-%m-%d %A"), True, (150, 180, 200))
    screen.blit(date_text, (WIDTH - 200, 20))
    
    # 绘制鼠标
    pygame.draw.circle(screen, (200, 220, 240), mouse_pos, 5)
    pygame.draw.circle(screen, (100, 150, 200), mouse_pos, 5, 1)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()