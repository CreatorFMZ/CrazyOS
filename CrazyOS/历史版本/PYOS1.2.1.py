import pygame
import sys
import math
from datetime import datetime

# 初始化pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PYOS v1.2.1 - Python 操作系统模拟器")

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
SYSTEM_BLUE = (64, 156, 255)

# 字体设置 - 使用支持中文的字体
try:
    # 尝试加载微软雅黑字体
    font_small = pygame.font.SysFont("Microsoft YaHei", 14)
    font_medium = pygame.font.SysFont("Microsoft YaHei", 18)
    font_large = pygame.font.SysFont("Microsoft YaHei", 24, bold=True)
    font_title = pygame.font.SysFont("Microsoft YaHei", 28, bold=True)
except:
    # 回退到系统默认字体
    font_small = pygame.font.SysFont(None, 14)
    font_medium = pygame.font.SysFont(None, 18)
    font_large = pygame.font.SysFont(None, 24, bold=True)
    font_title = pygame.font.SysFont(None, 28, bold=True)

class Icon:
    def __init__(self, x, y, label, app_type):
        self.x = x
        self.y = y
        self.label = label
        self.app_type = app_type
        self.width = 80
        self.height = 90
        self.selected = False
        self.last_click = 0
    
    def draw(self, surface):
        color = (150, 200, 220) if self.selected else ICON_COLOR
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height), border_radius=8)
        pygame.draw.rect(surface, (color[0]-20, color[1]-20, color[2]-20), 
                         (self.x, self.y, self.width, self.height), 2, border_radius=8)
        
        # 应用图标绘制
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
        elif self.app_type == "documents":
            pygame.draw.rect(surface, (180, 180, 220), (self.x+20, self.y+15, 40, 50), border_radius=3)
            pygame.draw.line(surface, (140, 140, 180), (self.x+25, self.y+25), (self.x+55, self.y+25), 2)
            pygame.draw.line(surface, (140, 140, 180), (self.x+25, self.y+35), (self.x+55, self.y+35), 2)
            pygame.draw.line(surface, (140, 140, 180), (self.x+25, self.y+45), (self.x+45, self.y+45), 2)
        elif self.app_type == "images":
            pygame.draw.rect(surface, (220, 180, 220), (self.x+20, self.y+15, 40, 40), border_radius=3)
            pygame.draw.polygon(surface, (180, 140, 180), 
                               [(self.x+30, self.y+25), (self.x+50, self.y+30), (self.x+40, self.y+45)])
            pygame.draw.circle(surface, (180, 140, 180), (self.x+35, self.y+35), 5)
        elif self.app_type == "settings":
            pygame.draw.circle(surface, (180, 180, 220), (self.x+40, self.y+35), 20)
            pygame.draw.circle(surface, (140, 140, 180), (self.x+40, self.y+35), 20, 2)
            for i in range(6):
                angle = i * math.pi / 3
                x1 = self.x + 40 + 15 * math.cos(angle)
                y1 = self.y + 35 + 15 * math.sin(angle)
                x2 = self.x + 40 + 8 * math.cos(angle)
                y2 = self.y + 35 + 8 * math.sin(angle)
                pygame.draw.line(surface, (140, 140, 180), (x1, y1), (x2, y2), 2)
        
        # 图标标签
        text = font_small.render(self.label, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height - 15))
        surface.blit(text, text_rect)
    
    def is_hovered(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

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
        self.calc_buttons = []
        self.calc_display = "0"
        self.calc_value = 0
        self.calc_operator = None
        self.calc_waiting_operand = False
        
        # 关闭按钮
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 35, self.y + 10, 25, 25),
            "action": "close"
        })
        
        # 应用特定初始化
        if app_type == "explorer":
            self.content = ["文档", "图片", "音乐", "视频", "下载", "桌面"]
        elif app_type == "calculator":
            self.content = ["7", "8", "9", "/", 
                            "4", "5", "6", "*", 
                            "1", "2", "3", "-", 
                            "C", "0", "=", "+"]
            button_size = 50
            for i in range(4):
                for j in range(4):
                    idx = i * 4 + j
                    if idx < len(self.content):
                        btn_x = self.x + 30 + j * (button_size + 10)
                        btn_y = self.y + 130 + i * (button_size + 10)
                        self.calc_buttons.append({
                            "rect": pygame.Rect(btn_x, btn_y, button_size, button_size),
                            "text": self.content[idx]
                        })
        elif app_type == "browser":
            self.content = ["欢迎使用 PYOS 浏览器", "PYOS v1.2.1 已发布", 
                            "新增功能：文件管理器、计算器、浏览器", "体验更流畅的操作系统模拟环境"]
            self.buttons.append({
                "rect": pygame.Rect(self.x + self.width - 70, self.y + 60, 50, 35),
                "action": "go"
            })
        elif app_type == "settings":
            self.content = ["显示设置", "声音设置", "网络设置", "个性化", "系统更新", "关于"]
    
    def handle_calculator_click(self, button_text):
        """处理计算器按钮点击"""
        if button_text in "0123456789":
            if self.calc_display == "0" or self.calc_waiting_operand:
                self.calc_display = button_text
                self.calc_waiting_operand = False
            else:
                self.calc_display += button_text
        elif button_text == '.' and '.' not in self.calc_display:
            self.calc_display += button_text
        elif button_text in ['+', '-', '*', '/']:
            if self.calc_operator and not self.calc_waiting_operand:
                self.calculate()
            self.calc_value = float(self.calc_display)
            self.calc_operator = button_text
            self.calc_waiting_operand = True
        elif button_text == '=':
            self.calculate()
            self.calc_operator = None
        elif button_text == 'C':
            self.calc_display = "0"
            self.calc_value = 0
            self.calc_operator = None
            self.calc_waiting_operand = False
    
    def calculate(self):
        """执行计算"""
        if self.calc_operator and not self.calc_waiting_operand:
            current_value = float(self.calc_display)
            try:
                if self.calc_operator == '+':
                    result = self.calc_value + current_value
                elif self.calc_operator == '-':
                    result = self.calc_value - current_value
                elif self.calc_operator == '*':
                    result = self.calc_value * current_value
                elif self.calc_operator == '/':
                    if current_value != 0:
                        result = self.calc_value / current_value
                    else:
                        result = 0
                self.calc_display = str(int(result)) if result.is_integer() else str(round(result, 6))
                self.calc_value = result
                self.calc_waiting_operand = True
            except:
                self.calc_display = "Error"
    
    def draw(self, surface):
        # 窗口阴影
        pygame.draw.rect(surface, (20, 20, 30, 180), 
                         (self.x+5, self.y+5, self.width, self.height), border_radius=8)
        
        # 窗口主体
        pygame.draw.rect(surface, WINDOW_BG, (self.x, self.y, self.width, self.height), border_radius=8)
        
        # 标题栏
        pygame.draw.rect(surface, WINDOW_TITLE_BAR, (self.x, self.y, self.width, 40), border_radius=8)
        title_text = font_medium.render(self.title, True, TEXT_COLOR)
        surface.blit(title_text, (self.x + 15, self.y + 10))
        
        # 关闭按钮
        close_button = self.buttons[0]["rect"]
        mouse_pos = pygame.mouse.get_pos()
        color = CLOSE_HOVER if close_button.collidepoint(mouse_pos) else CLOSE_BUTTON
        pygame.draw.circle(surface, color, close_button.center, 12)
        pygame.draw.circle(surface, (240, 240, 240), close_button.center, 12, 2)
        pygame.draw.line(surface, (240, 240, 240), (close_button.centerx-6, close_button.centery-6), 
                         (close_button.centerx+6, close_button.centery+6), 2)
        pygame.draw.line(surface, (240, 240, 240), (close_button.centerx+6, close_button.centery-6), 
                         (close_button.centerx-6, close_button.centery+6), 2)
        
        # 应用特定内容
        if self.app_type == "explorer":
            for i, item in enumerate(self.content):
                y_pos = self.y + 60 + i * 40
                pygame.draw.rect(surface, (60, 64, 74), (self.x + 20, y_pos, self.width - 40, 30), border_radius=4)
                item_text = font_medium.render(item, True, TEXT_COLOR)
                surface.blit(item_text, (self.x + 40, y_pos + 5))
                
        elif self.app_type == "calculator":
            # 显示区域
            pygame.draw.rect(surface, (30, 34, 40), (self.x + 20, self.y + 60, self.width - 40, 50), border_radius=5)
            display_text = font_large.render(self.calc_display, True, (100, 200, 150))
            text_x = self.x + self.width - 40 - display_text.get_width()
            surface.blit(display_text, (text_x, self.y + 75))
            
            # 按钮
            for btn in self.calc_buttons:
                mouse_pos = pygame.mouse.get_pos()
                color = BUTTON_HOVER if btn["rect"].collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(surface, color, btn["rect"], border_radius=5)
                btn_text = font_medium.render(btn["text"], True, TEXT_COLOR)
                surface.blit(btn_text, (btn["rect"].centerx - btn_text.get_width()//2, 
                                       btn["rect"].centery - btn_text.get_height()//2))
        
        elif self.app_type == "browser":
            # URL栏
            pygame.draw.rect(surface, (30, 34, 40), (self.x + 20, self.y + 60, self.width - 100, 35), border_radius=5)
            url_text = font_medium.render("pyos://home", True, (150, 180, 220))
            surface.blit(url_text, (self.x + 30, self.y + 65))
            
            # GO按钮
            if len(self.buttons) > 1:
                go_button = self.buttons[1]["rect"]
                mouse_pos = pygame.mouse.get_pos()
                color = BUTTON_HOVER if go_button.collidepoint(mouse_pos) else BUTTON_COLOR
                pygame.draw.rect(surface, color, go_button, border_radius=5)
                go_text = font_medium.render("GO", True, TEXT_COLOR)
                surface.blit(go_text, (go_button.centerx - go_text.get_width()//2, go_button.centery - go_text.get_height()//2))
            
            # 内容区域
            pygame.draw.rect(surface, (60, 64, 74), (self.x + 20, self.y + 110, self.width - 40, self.height - 140), border_radius=5)
            for i, line in enumerate(self.content):
                content_text = font_medium.render(line, True, TEXT_COLOR)
                surface.blit(content_text, (self.x + 40, self.y + 130 + i * 35))
        
        elif self.app_type == "settings":
            # 设置项
            for i, item in enumerate(self.content):
                y_pos = self.y + 60 + i * 50
                pygame.draw.rect(surface, (60, 64, 74), (self.x + 20, y_pos, self.width - 40, 40), border_radius=4)
                item_text = font_medium.render(item, True, TEXT_COLOR)
                surface.blit(item_text, (self.x + 40, y_pos + 10))
                
                # 设置图标
                if i == 0:  # 显示设置
                    pygame.draw.rect(surface, (100, 180, 220), (self.x + self.width - 60, y_pos + 5, 30, 30), border_radius=3)
                elif i == 1:  # 声音设置
                    pygame.draw.circle(surface, (180, 180, 220), (self.x + self.width - 45, y_pos + 20), 12)
                    pygame.draw.line(surface, (180, 180, 220), (self.x + self.width - 45, y_pos + 8), 
                                    (self.x + self.width - 45, y_pos + 32), 2)
                elif i == 5:  # 关于
                    pygame.draw.circle(surface, (100, 200, 150), (self.x + self.width - 45, y_pos + 20), 12)
                    info_text = font_small.render("i", True, TEXT_COLOR)
                    surface.blit(info_text, (self.x + self.width - 50, y_pos + 12))
    
    def is_title_bar_hit(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + 40
    
    def is_inside(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

class Taskbar:
    def __init__(self):
        self.height = 50
        self.app_buttons = []
        self.time_rect = pygame.Rect(WIDTH - 120, HEIGHT - self.height + 10, 100, 30)
    
    def draw(self, surface):
        pygame.draw.rect(surface, TASKBAR, (0, HEIGHT - self.height, WIDTH, self.height))
        pygame.draw.line(surface, (60, 70, 90), (0, HEIGHT - self.height), (WIDTH, HEIGHT - self.height), 2)
        
        # 开始按钮
        pygame.draw.rect(surface, BUTTON_COLOR, (10, HEIGHT - self.height + 5, 80, 40), border_radius=5)
        start_text = font_medium.render("开始", True, TEXT_COLOR)
        surface.blit(start_text, (50 - start_text.get_width()//2, HEIGHT - self.height + 20))
        
        # 应用按钮
        for i, btn in enumerate(self.app_buttons):
            btn_rect = pygame.Rect(100 + i * 120, HEIGHT - self.height + 5, 110, 40)
            mouse_pos = pygame.mouse.get_pos()
            color = BUTTON_HOVER if btn_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(surface, color, btn_rect, border_radius=5)
            app_text = font_medium.render(btn, True, TEXT_COLOR)
            surface.blit(app_text, (btn_rect.centerx - app_text.get_width()//2, btn_rect.centery - app_text.get_height()//2))
        
        # 时间显示
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
    Icon(100, 220, "文档", "documents"),
    Icon(220, 220, "图片", "images"),
    Icon(340, 220, "系统设置", "settings")
]

# 创建任务栏
taskbar = Taskbar()
windows = []
active_window_index = -1

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
            # 桌面图标点击
            icon_clicked = False
            for icon in desktop_icons:
                if icon.is_hovered(mouse_pos):
                    for i in desktop_icons:
                        i.selected = False
                    icon.selected = True
                    icon_clicked = True
                    
                    if event.button == 1:
                        current_ticks = pygame.time.get_ticks()
                        if current_ticks - icon.last_click < 300:  # 双击检测
                            window_title = icon.label
                            if icon.app_type == "explorer":
                                window_title = "文件管理器"
                            elif icon.app_type == "calculator":
                                window_title = "计算器"
                            elif icon.app_type == "browser":
                                window_title = "浏览器"
                            elif icon.app_type == "settings":
                                window_title = "系统设置"
                            
                            new_window = Window(window_title, 150 + len(windows)*20, 100 + len(windows)*20, 
                                              400, 400, icon.app_type)
                            windows.append(new_window)
                            active_window_index = len(windows) - 1
                            
                            if window_title not in taskbar.app_buttons:
                                taskbar.app_buttons.append(window_title)
                        
                        icon.last_click = current_ticks
            
            # 窗口交互
            handled = False
            for i in range(len(windows)-1, -1, -1):
                window = windows[i]
                
                # 按钮点击
                for button in window.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["action"] == "close":
                            if window.title in taskbar.app_buttons:
                                taskbar.app_buttons.remove(window.title)
                            windows.pop(i)
                            if active_window_index == i:
                                active_window_index = -1
                            elif active_window_index > i:
                                active_window_index -= 1
                            handled = True
                            break
                        elif button["action"] == "go":
                            if window.app_type == "browser":
                                window.content = [
                                    "PYOS v1.2.1 浏览器",
                                    "正在加载 pyos://home...",
                                    "PYOS 1.2.1 更新日志：",
                                    "- 修复文字显示问题",
                                    "- 优化计算器功能",
                                    "- 添加系统设置应用"
                                ]
                            handled = True
                            break
                
                if handled:
                    break
                
                # 标题栏点击
                if window.is_title_bar_hit(mouse_pos):
                    active_window_index = i
                    windows.append(windows.pop(i))
                    active_window_index = len(windows) - 1
                    window = windows[-1]
                    
                    window.dragging = True
                    window.drag_offset_x = mouse_pos[0] - window.x
                    window.drag_offset_y = mouse_pos[1] - window.y
                    handled = True
                    break
                
                # 窗口内容交互
                if window.is_inside(mouse_pos) and not window.is_title_bar_hit(mouse_pos):
                    if window.app_type == "calculator":
                        for btn in window.calc_buttons:
                            if btn["rect"].collidepoint(mouse_pos):
                                window.handle_calculator_click(btn["text"])
                                handled = True
                                break
                    
                    elif window.app_type == "explorer" or window.app_type == "settings":
                        for i, item in enumerate(window.content):
                            y_pos = window.y + 60 + i * (40 if window.app_type == "explorer" else 50)
                            item_rect = pygame.Rect(window.x + 20, y_pos, window.width - 40, 
                                                   30 if window.app_type == "explorer" else 40)
                            if item_rect.collidepoint(mouse_pos):
                                if window.app_type == "explorer":
                                    print(f"打开: {item}")
                                elif window.app_type == "settings":
                                    if i == 5:  # 关于
                                        window.content = [
                                            "PYOS v1.2.1",
                                            "Python 操作系统模拟器",
                                            "© 2023 PYOS 开发团队",
                                            "所有权利保留"
                                        ]
                                handled = True
                                break
                    
                    if handled:
                        break
            
            # 取消选择图标
            if not handled and not icon_clicked:
                for icon in desktop_icons:
                    icon.selected = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            for window in windows:
                window.dragging = False
    
    # 窗口拖动
    if active_window_index >= 0 and active_window_index < len(windows):
        window = windows[active_window_index]
        if window.dragging:
            window.x = mouse_pos[0] - window.drag_offset_x
            window.y = mouse_pos[1] - window.drag_offset_y
            window.y = max(0, window.y)
            
            # 更新按钮位置
            for button in window.buttons:
                if button["action"] == "close":
                    button["rect"] = pygame.Rect(window.x + window.width - 35, window.y + 10, 25, 25)
                elif button["action"] == "go":
                    button["rect"] = pygame.Rect(window.x + window.width - 70, window.y + 60, 50, 35)
            
            # 更新计算器按钮位置
            if window.app_type == "calculator":
                button_size = 50
                window.calc_buttons = []
                for i in range(4):
                    for j in range(4):
                        idx = i * 4 + j
                        if idx < len(window.content):
                            btn_x = window.x + 30 + j * (button_size + 10)
                            btn_y = window.y + 130 + i * (button_size + 10)
                            window.calc_buttons.append({
                                "rect": pygame.Rect(btn_x, btn_y, button_size, button_size),
                                "text": window.content[idx]
                            })
    
    # 绘制界面
    screen.fill(BACKGROUND)
    
    # 绘制网格背景
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, (50, 54, 64), (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (50, 54, 64), (0, i), (WIDTH, i), 1)
    
    # 绘制桌面图标
    for icon in desktop_icons:
        icon.draw(screen)
    
    # 绘制窗口
    for window in windows:
        window.draw(screen)
    
    # 绘制任务栏
    taskbar.draw(screen)
    
    # 绘制系统信息
    os_text = font_title.render("PYOS v1.2.1", True, SYSTEM_BLUE)
    screen.blit(os_text, (20, 20))
    
    date_text = font_medium.render(current_time.strftime("%Y-%m-%d %A"), True, (150, 180, 200))
    screen.blit(date_text, (WIDTH - date_text.get_width() - 20, 20))
    
    # 绘制鼠标指针
    pygame.draw.circle(screen, (200, 220, 240), mouse_pos, 5)
    pygame.draw.circle(screen, (100, 150, 200), mouse_pos, 5, 1)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()