import pygame
import sys
import math
from datetime import datetime

# 初始化pygame
pygame.init()

# 屏幕设置
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CrazyOS 1.0 - Python 操作系统模拟器")


# 颜色定义（Windows 11风格）
BACKGROUND = (245, 245, 250)
TASKBAR = (255, 255, 255, 180)
WINDOW_BG = (255, 255, 255)
WINDOW_TITLE_BAR = (230, 240, 255)
BUTTON_COLOR = (180, 220, 250)
BUTTON_HOVER = (160, 200, 230)
BUTTON_TEXT = (0, 0, 0)
TEXT_COLOR = (40, 40, 40)
ICON_COLOR = (120, 160, 200)
CLOSE_BUTTON = (255, 100, 100)
CLOSE_HOVER = (255, 120, 120)
MAXIMIZE_BUTTON = (100, 200, 100)
MAXIMIZE_HOVER = (120, 220, 120)
MINIMIZE_BUTTON = (220, 200, 100)
MINIMIZE_HOVER = (240, 220, 120)
SYSTEM_BLUE = (0, 120, 215)
DOCUMENT_BG = (250, 250, 255)
EDITOR_BG = (245, 245, 255)
SAVE_BUTTON = (100, 200, 255)
SAVE_HOVER = (120, 220, 255)
TEXT_HIGHLIGHT = (0, 120, 215, 100)


# 字体设置
try:
    font_small = pygame.font.SysFont("Microsoft YaHei", 14)
    font_medium = pygame.font.SysFont("Microsoft YaHei", 18)
    font_large = pygame.font.SysFont("Microsoft YaHei", 24, bold=True)
    font_title = pygame.font.SysFont("Microsoft YaHei", 28, bold=True)
    font_code = pygame.font.SysFont("Microsoft YaHei", 16)
except:
    font_small = pygame.font.SysFont(None, 14)
    font_medium = pygame.font.SysFont(None, 18)
    font_large = pygame.font.SysFont(None, 24, bold=True)
    font_title = pygame.font.SysFont(None, 28, bold=True)
    font_code = pygame.font.SysFont(None, 16)

# 文档存储
class DocumentStorage:
    def __init__(self):
        self.documents = {
            "welcome.txt": ["欢迎使用CrazyOS文档编辑器", "这是一个示例文档"],
            "notes.txt": ["我的笔记", "重要事项：", "- 修复图层问题", "- 添加文档存储"]
        }
    
    def save_document(self, filename, content):
        self.documents[filename] = content
    
    def get_documents(self):
        return list(self.documents.keys())

# 创建文档存储
document_storage = DocumentStorage()

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
        
        # 应用图标
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
        self.last_click = 0
        
        # 全屏状态
        self.is_maximized = False
        self.normal_rect = pygame.Rect(x, y, width, height)
        
        # 文档应用属性
        self.document_content = ["欢迎使用CrazyOS文档编辑器", "在这里输入您的文本...", "", "按Ctrl+S保存文档"]
        self.document_lines = self.document_content.copy()
        self.cursor_pos = [0, 0]
        self.cursor_visible = True
        self.cursor_timer = 0
        self.editing = False
        self.save_button = None
        self.save_status = ""
        self.save_timer = 0
        self.filename = "untitled.txt"  # 默认文件名
        self.show_save_dialog = False  # 显示保存对话框
        self.save_filename = "document.txt"  # 保存文件名
        
        # 设置应用属性
        self.selected_setting = -1  # 选中的设置项
        self.show_about = False  # 是否显示关于信息
        
        # 文件管理器属性
        self.current_folder = "root"
        self.folder_contents = {
            "root": ["文档", "图片", "音乐", "视频", "下载", "桌面"],
            "文档": document_storage.get_documents()  # 使用文档存储中的文档列表
        }
        
        # 窗口控制按钮
        self.add_window_buttons()
        
        # 应用特定初始化
        if app_type == "explorer":
            self.content = self.folder_contents[self.current_folder]
        elif app_type == "calculator":
            self.init_calculator()
        elif app_type == "browser":
            self.init_browser()
        elif app_type == "settings":
            self.init_settings()
        elif app_type == "documents":
            self.init_documents()
    
    def add_window_buttons(self):
        """添加窗口控制按钮"""
        self.buttons = []
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 35, self.y + 10, 25, 25),
            "action": "close"
        })
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 65, self.y + 10, 25, 25),
            "action": "maximize"
        })
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 95, self.y + 10, 25, 25),
            "action": "minimize"
        })
    
    def init_calculator(self):
        """初始化计算器"""
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
    
    def init_browser(self):
        """初始化浏览器"""
        self.content = ["欢迎使用 CrazyOS 浏览器", "CrazyOS 1.0 已发布", 
                        "- 优化UI界面", "- 修复设置部分问题"]
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 70, self.y + 60, 50, 35),
            "action": "go"
        })
    
    def init_settings(self):
        """初始化设置应用"""
        self.content = ["显示设置", "声音设置", "网络设置", "个性化", "系统更新", "关于"]
    
    def init_documents(self):
        """初始化文档应用"""
        self.save_button = {
            "rect": pygame.Rect(self.x + self.width - 100, self.y + self.height - 40, 80, 30),
            "action": "save_document"
        }
        self.buttons.append(self.save_button)
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 190, self.y + self.height - 40, 80, 30),
            "action": "save_as"
        })
    
    def toggle_maximize(self):
        """切换最大化状态"""
        if self.is_maximized:
            # 还原到正常状态
            self.x, self.y, self.width, self.height = self.normal_rect
            self.is_maximized = False
        else:
            # 保存当前状态
            self.normal_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            # 最大化（保留任务栏空间）
            self.x, self.y = 0, 0
            self.width, self.height = WIDTH, HEIGHT - taskbar.height
            self.is_maximized = True
        
        # 更新按钮位置
        self.update_button_positions()
    
    def minimize(self):
        """最小化窗口"""
        self.active = False
        if self.title not in taskbar.app_buttons:
            taskbar.app_buttons.append(self.title)
    
    def restore(self):
        """恢复窗口"""
        self.active = True
    
    def update_button_positions(self):
        """更新按钮位置"""
        # 重新创建窗口控制按钮
        self.add_window_buttons()
        
        # 更新应用特定按钮
        if self.app_type == "browser":
            self.buttons.append({
                "rect": pygame.Rect(self.x + self.width - 70, self.y + 60, 50, 35),
                "action": "go"
            })
        elif self.app_type == "documents":
            self.save_button = {
                "rect": pygame.Rect(self.x + self.width - 100, self.y + self.height - 40, 80, 30),
                "action": "save_document"
            }
            self.buttons.append(self.save_button)
            self.buttons.append({
                "rect": pygame.Rect(self.x + self.width - 190, self.y + self.height - 40, 80, 30),
                "action": "save_as"
            })
        
        # 更新计算器按钮位置
        if self.app_type == "calculator":
            self.calc_buttons = []
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
    
    def handle_keyboard_input(self, event):
        """处理键盘输入（文档应用）"""
        if self.app_type != "documents" or not self.editing:
            return
        
        # 处理特殊按键
        if event.key == pygame.K_RETURN:
            current_line = self.document_lines[self.cursor_pos[0]]
            before_cursor = current_line[:self.cursor_pos[1]]
            after_cursor = current_line[self.cursor_pos[1]:]
            
            self.document_lines[self.cursor_pos[0]] = before_cursor
            self.document_lines.insert(self.cursor_pos[0] + 1, after_cursor)
            self.cursor_pos[0] += 1
            self.cursor_pos[1] = 0
            self.cursor_visible = True
            self.cursor_timer = 0
            
        elif event.key == pygame.K_BACKSPACE:
            if self.cursor_pos[1] > 0:
                current_line = self.document_lines[self.cursor_pos[0]]
                self.document_lines[self.cursor_pos[0]] = current_line[:self.cursor_pos[1]-1] + current_line[self.cursor_pos[1]:]
                self.cursor_pos[1] -= 1
            elif self.cursor_pos[0] > 0:
                prev_line = self.document_lines[self.cursor_pos[0]-1]
                current_line = self.document_lines[self.cursor_pos[0]]
                self.document_lines[self.cursor_pos[0]-1] = prev_line + current_line
                self.document_lines.pop(self.cursor_pos[0])
                self.cursor_pos[0] -= 1
                self.cursor_pos[1] = len(prev_line)
            self.cursor_visible = True
            self.cursor_timer = 0
            
        elif event.key == pygame.K_DELETE:
            if self.cursor_pos[1] < len(self.document_lines[self.cursor_pos[0]]):
                current_line = self.document_lines[self.cursor_pos[0]]
                self.document_lines[self.cursor_pos[0]] = current_line[:self.cursor_pos[1]] + current_line[self.cursor_pos[1]+1:]
            self.cursor_visible = True
            self.cursor_timer = 0
            
        elif event.key == pygame.K_LEFT:
            if self.cursor_pos[1] > 0:
                self.cursor_pos[1] -= 1
            elif self.cursor_pos[0] > 0:
                self.cursor_pos[0] -= 1
                self.cursor_pos[1] = len(self.document_lines[self.cursor_pos[0]])
            self.cursor_visible = True
            self.cursor_timer = 0
            
        elif event.key == pygame.K_RIGHT:
            current_line = self.document_lines[self.cursor_pos[0]]
            if self.cursor_pos[1] < len(current_line):
                self.cursor_pos[1] += 1
            elif self.cursor_pos[0] < len(self.document_lines) - 1:
                self.cursor_pos[0] += 1
                self.cursor_pos[1] = 0
            self.cursor_visible = True
            self.cursor_timer = 0
            
        elif event.key == pygame.K_UP:
            if self.cursor_pos[0] > 0:
                self.cursor_pos[0] -= 1
                self.cursor_pos[1] = min(self.cursor_pos[1], len(self.document_lines[self.cursor_pos[0]]))
            self.cursor_visible = True
            self.cursor_timer = 0
            
        elif event.key == pygame.K_DOWN:
            if self.cursor_pos[0] < len(self.document_lines) - 1:
                self.cursor_pos[0] += 1
                self.cursor_pos[1] = min(self.cursor_pos[1], len(self.document_lines[self.cursor_pos[0]]))
            self.cursor_visible = True
            self.cursor_timer = 0
            
        elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.save_document()
            
        elif event.unicode.isprintable():
            current_line = self.document_lines[self.cursor_pos[0]]
            self.document_lines[self.cursor_pos[0]] = current_line[:self.cursor_pos[1]] + event.unicode + current_line[self.cursor_pos[1]:]
            self.cursor_pos[1] += len(event.unicode)
            self.cursor_visible = True
            self.cursor_timer = 0
    
    def save_document(self):
        """保存文档"""
        document_storage.save_document(self.filename, self.document_lines)
        self.save_status = f"文档已保存: {self.filename} - {datetime.now().strftime('%H:%M:%S')}"
        self.save_timer = 180
    
    def save_as(self):
        """另存为文档"""
        self.show_save_dialog = True
        self.save_filename = f"document_{datetime.now().strftime('%H%M%S')}.txt"
    
    def update_cursor(self):
        """更新光标状态"""
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
            
        if self.save_timer > 0:
            self.save_timer -= 1
    
    def draw(self, surface):
        # 窗口阴影（非最大化状态）
        if not self.is_maximized:
            pygame.draw.rect(surface, (200, 200, 200, 100), 
                             (self.x+5, self.y+5, self.width, self.height), border_radius=8)
        
        # 窗口主体
        pygame.draw.rect(surface, WINDOW_BG, (self.x, self.y, self.width, self.height), border_radius=8 if not self.is_maximized else 0)
        
        # 标题栏
        pygame.draw.rect(surface, WINDOW_TITLE_BAR, (self.x, self.y, self.width, 40), border_radius=8 if not self.is_maximized else 0)
        title_text = font_medium.render(self.title, True, TEXT_COLOR)
        surface.blit(title_text, (self.x + 15, self.y + 10))
        
        # 窗口控制按钮
        mouse_pos = pygame.mouse.get_pos()
        
        # 关闭按钮
        close_button = self.buttons[0]["rect"]
        color = CLOSE_HOVER if close_button.collidepoint(mouse_pos) else CLOSE_BUTTON
        pygame.draw.circle(surface, color, close_button.center, 12)
        pygame.draw.circle(surface, (240, 240, 240), close_button.center, 12, 2)
        pygame.draw.line(surface, (240, 240, 240), (close_button.centerx-6, close_button.centery-6), 
                         (close_button.centerx+6, close_button.centery+6), 2)
        pygame.draw.line(surface, (240, 240, 240), (close_button.centerx+6, close_button.centery-6), 
                         (close_button.centerx-6, close_button.centery+6), 2)
        
        # 最大化/还原按钮
        maximize_button = self.buttons[1]["rect"]
        color = MAXIMIZE_HOVER if maximize_button.collidepoint(mouse_pos) else MAXIMIZE_BUTTON
        pygame.draw.circle(surface, color, maximize_button.center, 12)
        pygame.draw.circle(surface, (240, 240, 240), maximize_button.center, 12, 2)
        
        if self.is_maximized:
            pygame.draw.rect(surface, (240, 240, 240), (maximize_button.centerx-7, maximize_button.centery-4, 5, 5), 1)
            pygame.draw.rect(surface, (240, 240, 240), (maximize_button.centerx-3, maximize_button.centery, 5, 5), 1)
            pygame.draw.line(surface, (240, 240, 240), (maximize_button.centerx-7, maximize_button.centery-4), 
                            (maximize_button.centerx-2, maximize_button.centery-4), 1)
            pygame.draw.line(surface, (240, 240, 240), (maximize_button.centerx-7, maximize_button.centery-4), 
                            (maximize_button.centerx-7, maximize_button.centery+1), 1)
        else:
            pygame.draw.rect(surface, (240, 240, 240), (maximize_button.centerx-7, maximize_button.centery-4, 9, 9), 1)
        
        # 最小化按钮
        minimize_button = self.buttons[2]["rect"]
        color = MINIMIZE_HOVER if minimize_button.collidepoint(mouse_pos) else MINIMIZE_BUTTON
        pygame.draw.circle(surface, color, minimize_button.center, 12)
        pygame.draw.circle(surface, (240, 240, 240), minimize_button.center, 12, 2)
        pygame.draw.line(surface, (240, 240, 240), (minimize_button.centerx-6, minimize_button.centery), 
                         (minimize_button.centerx+6, minimize_button.centery), 2)
        
        # 应用特定内容
        if self.app_type == "explorer":
            self.draw_explorer(surface)
        elif self.app_type == "calculator":
            self.draw_calculator(surface)
        elif self.app_type == "browser":
            self.draw_browser(surface)
        elif self.app_type == "settings":
            self.draw_settings(surface)
        elif self.app_type == "documents":
            self.draw_documents(surface)
    
    def draw_explorer(self, surface):
        """绘制文件管理器"""
        # 文件列表
        for i, item in enumerate(self.folder_contents[self.current_folder]):
            y_pos = self.y + 60 + i * 40
            pygame.draw.rect(surface, (60, 64, 74), (self.x + 20, y_pos, self.width - 40, 30), border_radius=4)
            item_text = font_medium.render(item, True, TEXT_COLOR)
            surface.blit(item_text, (self.x + 40, y_pos + 5))
            
            # 文件图标
            if item.endswith(".txt"):
                pygame.draw.rect(surface, (180, 180, 220), (self.x + self.width - 50, y_pos + 5, 20, 20), border_radius=2)
    
    def draw_calculator(self, surface):
        """绘制计算器"""
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
    
    def draw_browser(self, surface):
        """绘制浏览器"""
        # URL栏
        pygame.draw.rect(surface, (30, 34, 40), (self.x + 20, self.y + 60, self.width - 100, 35), border_radius=5)
        url_text = font_medium.render("pyos://home", True, (150, 180, 220))
        surface.blit(url_text, (self.x + 30, self.y + 65))
        
        # GO按钮
        if len(self.buttons) > 3:
            go_button = self.buttons[3]["rect"]
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
    
    def draw_settings(self, surface):
        """绘制设置应用"""
        # 设置项
        for i, item in enumerate(self.content):
            y_pos = self.y + 60 + i * 50
            color = (70, 80, 100) if i == self.selected_setting else (60, 64, 74)
            pygame.draw.rect(surface, color, (self.x + 20, y_pos, self.width - 40, 40), border_radius=4)
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
        
        # 关于信息
        if self.show_about:
            about_rect = pygame.Rect(self.x + 50, self.y + 100, self.width - 100, self.height - 150)
            pygame.draw.rect(surface, (40, 45, 55), about_rect, border_radius=10)
            pygame.draw.rect(surface, (70, 130, 180), about_rect, 2, border_radius=10)
            
            about_texts = [
                "CrazyOS 1.0",
                "Python 操作系统模拟器",
                "©Fanatic Star梦幻星",
                "2025, All rights reserved"
                
            ]
            
            for i, text in enumerate(about_texts):
                text_surface = font_medium.render(text, True, (180, 200, 220))
                surface.blit(text_surface, (about_rect.x + 30, about_rect.y + 30 + i * 35))
    
    def draw_documents(self, surface):
        """绘制文档应用"""
        # 文档编辑区域
        editor_rect = pygame.Rect(self.x + 20, self.y + 60, self.width - 40, self.height - 110)
        pygame.draw.rect(surface, EDITOR_BG, editor_rect, border_radius=5)
        
        # 绘制文本行
        line_height = 25
        visible_lines = min(len(self.document_lines), (editor_rect.height - 20) // line_height)
        
        for i in range(visible_lines):
            line = self.document_lines[i]
            line_text = font_code.render(line, True, TEXT_COLOR)
            surface.blit(line_text, (self.x + 30, self.y + 70 + i * line_height))
        
        # 绘制光标
        if self.editing and self.cursor_visible and self.cursor_pos[0] < visible_lines:
            cursor_x = self.x + 30 + font_code.size(self.document_lines[self.cursor_pos[0]][:self.cursor_pos[1]])[0]
            cursor_y = self.y + 70 + self.cursor_pos[0] * line_height
            pygame.draw.line(surface, TEXT_COLOR, (cursor_x, cursor_y), 
                            (cursor_x, cursor_y + line_height - 5), 2)
        
        # 绘制按钮
        for button in self.buttons:
            if button["action"] in ["save_document", "save_as"]:
                mouse_pos = pygame.mouse.get_pos()
                color = SAVE_HOVER if button["rect"].collidepoint(mouse_pos) else SAVE_BUTTON
                pygame.draw.rect(surface, color, button["rect"], border_radius=5)
                btn_text = font_medium.render("保存" if button["action"] == "save_document" else "另存为", True, TEXT_COLOR)
                surface.blit(btn_text, (button["rect"].centerx - btn_text.get_width()//2, 
                                       button["rect"].centery - btn_text.get_height()//2))
        
        # 绘制保存状态
        if self.save_timer > 0:
            status_text = font_small.render(self.save_status, True, (100, 200, 100))
            surface.blit(status_text, (self.x + 30, self.y + self.height - 35))
        
        # 提示信息
        hint_text = font_small.render(f"当前文件: {self.filename} | 按Ctrl+S保存文档 | 双击开始编辑", True, (150, 180, 220))
        surface.blit(hint_text, (self.x + 30, self.y + self.height - 60))
    
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
active_input_window = None
clock = pygame.time.Clock()

# 主循环
running = True
while running:
    current_time = datetime.now()
    mouse_pos = pygame.mouse.get_pos()
    
    # 更新光标状态
    for window in windows:
        if window.app_type == "documents":
            window.update_cursor()
    
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
                        if current_ticks - icon.last_click < 300:
                            window_title = icon.label
                            if icon.app_type == "explorer":
                                window_title = "文件管理器"
                            elif icon.app_type == "calculator":
                                window_title = "计算器"
                            elif icon.app_type == "browser":
                                window_title = "浏览器"
                            elif icon.app_type == "documents":
                                window_title = "文档编辑器"
                            elif icon.app_type == "settings":
                                window_title = "系统设置"
                            
                            new_window = Window(window_title, 150 + len(windows)*20, 100 + len(windows)*20, 
                                              500 if icon.app_type == "documents" else 400, 
                                              500 if icon.app_type == "documents" else 400, 
                                              icon.app_type)
                            windows.append(new_window)
                            active_window_index = len(windows) - 1
                            
                            if window_title not in taskbar.app_buttons:
                                taskbar.app_buttons.append(window_title)
                        
                        icon.last_click = current_ticks
                        break
            
            # 任务栏应用按钮点击
            for i, btn in enumerate(taskbar.app_buttons):
                btn_rect = pygame.Rect(100 + i * 120, HEIGHT - taskbar.height + 5, 110, 40)
                if btn_rect.collidepoint(mouse_pos):
                    for window in windows:
                        if window.title == btn:
                            window.restore()
                            active_window_index = windows.index(window)
                            break
            
            # 窗口交互
            handled = False
            for i in range(len(windows)-1, -1, -1):
                window = windows[i]
                if not window.active:
                    continue
                
                # 按钮点击
                for button in window.buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["action"] == "close":
                            if window.title in taskbar.app_buttons:
                                taskbar.app_buttons.remove(window.title)
                            windows.pop(i)
                            if active_window_index == i:
                                active_window_index = -1
                                active_input_window = None
                            elif active_window_index > i:
                                active_window_index -= 1
                            handled = True
                            break
                        elif button["action"] == "go":
                            if window.app_type == "browser":
                                window.content = [
                                    "CrazyOS 1.0 浏览器",
                                    "正在加载 pyos://home...",
                                    "CrazyOS 1.3.3.1 更新日志：",
                                    "- 优化代码",
                                    "- 修复设置部分问题",
                                    "- 优化UI界面"
                                ]
                            handled = True
                            break
                        elif button["action"] == "save_document":
                            window.save_document()
                            handled = True
                            break
                        elif button["action"] == "save_as":
                            window.save_as()
                            handled = True
                            break
                        elif button["action"] == "maximize":
                            window.toggle_maximize()
                            handled = True
                            break
                        elif button["action"] == "minimize":
                            window.minimize()
                            handled = True
                            break
                
                if handled:
                    break
                
                # 标题栏点击
                if window.is_title_bar_hit(mouse_pos) and not window.is_maximized:
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
                    # 文档编辑器
                    if window.app_type == "documents" and event.button == 1:
                        if window.editing:
                            line_height = 25
                            editor_top = window.y + 70
                            
                            click_line = max(0, min(len(window.document_lines) - 1, 
                                           (mouse_pos[1] - editor_top) // line_height))
                            
                            line_text = window.document_lines[click_line]
                            click_x = mouse_pos[0] - (window.x + 30)
                            char_index = 0
                            current_width = 0
                            for i, char in enumerate(line_text):
                                char_width = font_code.size(char)[0]
                                if current_width + char_width / 2 > click_x:
                                    break
                                current_width += char_width
                                char_index = i + 1
                            
                            window.cursor_pos = [click_line, char_index]
                            window.cursor_visible = True
                            window.cursor_timer = 0
                        else:
                            if pygame.time.get_ticks() - window.last_click < 300:
                                window.editing = True
                                window.cursor_visible = True
                                window.cursor_timer = 0
                                active_input_window = window
                            window.last_click = pygame.time.get_ticks()
                        handled = True
                    
                    # 计算器
                    elif window.app_type == "calculator":
                        for btn in window.calc_buttons:
                            if btn["rect"].collidepoint(mouse_pos):
                                window.handle_calculator_click(btn["text"])
                                handled = True
                                break
                    
                    # 文件管理器
                    elif window.app_type == "explorer":
                        for i, item in enumerate(window.folder_contents[window.current_folder]):
                            y_pos = window.y + 60 + i * 40
                            item_rect = pygame.Rect(window.x + 20, y_pos, window.width - 40, 30)
                            if item_rect.collidepoint(mouse_pos):
                                if item == "文档":
                                    window.current_folder = "文档"
                                    window.content = window.folder_contents["文档"]
                                elif item.endswith(".txt"):
                                    # 打开文档
                                    doc_content = document_storage.documents.get(item, ["文档内容为空"])
                                    new_window = Window(f"文档: {item}", 200, 150, 500, 500, "documents")
                                    new_window.document_lines = doc_content.copy()
                                    new_window.filename = item
                                    windows.append(new_window)
                                    if new_window.title not in taskbar.app_buttons:
                                        taskbar.app_buttons.append(new_window.title)
                                handled = True
                                break
                    
                    # 系统设置
                    elif window.app_type == "settings":
                        for i, item in enumerate(window.content):
                            y_pos = window.y + 60 + i * 50
                            item_rect = pygame.Rect(window.x + 20, y_pos, window.width - 40, 40)
                            if item_rect.collidepoint(mouse_pos):
                                window.selected_setting = i
                                if item == "关于":
                                    window.show_about = not window.show_about
                                handled = True
                                if item == "系统更新":
                                    window.show_about = not window.show_about
                                handled = True
                                break
                    
                    if handled:
                        break
                else:
                    # 点击文档窗口外部时取消编辑状态
                    if window.app_type == "documents" and window.editing:
                        window.editing = False
                        active_input_window = None
            
            # 取消选择图标
            if not handled and not icon_clicked:
                for icon in desktop_icons:
                    icon.selected = False
                
                # 点击空白处取消文档编辑状态
                if active_input_window:
                    active_input_window.editing = False
                    active_input_window = None
                
                # 关闭设置中的关于面板
                for window in windows:
                    if window.app_type == "settings" and window.show_about:
                        window.show_about = False
        
        elif event.type == pygame.MOUSEBUTTONUP:
            for window in windows:
                window.dragging = False
        
        elif event.type == pygame.KEYDOWN:
            if active_input_window:
                active_input_window.handle_keyboard_input(event)
            
            # F11全屏切换
            if event.key == pygame.K_F11 and active_window_index >= 0:
                windows[active_window_index].toggle_maximize()
    
    # 窗口拖动
    if active_window_index >= 0 and active_window_index < len(windows):
        window = windows[active_window_index]
        if window.dragging and not window.is_maximized and window.active:
            window.x = mouse_pos[0] - window.drag_offset_x
            window.y = mouse_pos[1] - window.drag_offset_y
            window.y = max(0, window.y)
            
            # 更新按钮位置
            window.update_button_positions()
    
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
        if window.active:
            window.draw(screen)
    
    # 绘制任务栏
    taskbar.draw(screen)
    
    # 绘制系统信息
    date_text = font_medium.render(current_time.strftime("%Y-%m-%d %A"), True, (150, 180, 200))
    screen.blit(date_text, (WIDTH - date_text.get_width() - 125, 730))
    
    # 绘制鼠标指针
    pygame.draw.circle(screen, (200, 220, 240), mouse_pos, 5)
    pygame.draw.circle(screen, (100, 150, 200), mouse_pos, 5, 1)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()