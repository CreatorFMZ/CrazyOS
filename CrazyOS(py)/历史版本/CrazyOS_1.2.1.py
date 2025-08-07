import pygame
import sys
import math
from datetime import datetime
import random

pygame.init()

WIDTH, HEIGHT = pygame.display.list_modes()[0]  # 获取全屏分辨率
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("CrazyOS 1.2.1 - Python 操作系统模拟器")

BACKGROUND = (98, 142, 203)
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

class DocumentStorage:
    def __init__(self):
        self.documents = {
            "welcome.txt": ["欢迎使用CrazyOS文档编辑器", "这是一个示例文档"],
        }

    def save_document(self, filename, content):
        self.documents[filename] = content

    def get_documents(self):
        return list(self.documents.keys())

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
        elif self.app_type == "deeplost":
            pygame.draw.rect(surface, (100, 100, 180), (self.x+15, self.y+15, 50, 40), 0, border_radius=5)
            pygame.draw.circle(surface, (200, 200, 240), (self.x+40, self.y+35), 15)
            pygame.draw.circle(surface, (160, 160, 220), (self.x+40, self.y+35), 12, 2)

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

        self.is_maximized = False
        self.normal_rect = pygame.Rect(x, y, width, height)

        self.document_content = ["欢迎使用CrazyOS文档编辑器", "在这里输入您的文本...", "", "按Ctrl+S保存文档"]
        self.document_lines = self.document_content.copy()
        self.cursor_pos = [0, 0]
        self.cursor_visible = True
        self.cursor_timer = 0
        self.editing = False
        self.save_button = None
        self.save_status = ""
        self.save_timer = 0
        self.filename = "untitled.txt"
        self.show_save_dialog = False
        self.save_filename = "document.txt"

        self.selected_setting = -1
        self.show_update = False
        self.show_about = False

        self.current_folder = "root"
        self.folder_contents = {
            "root": ["文档", "图片", "音乐", "视频", "下载", "桌面"],
            "文档": document_storage.get_documents()
        }

        self.input_box = None  # Initialize for deeplost
        self.generate_button = None
        self.output_text = ""
        self.input_text = ""
        self.common_chars = [
            "的", "一", "是", "在", "不", "了", "有", "和", "人", "这", "中", "大", "为", "上", "个", "国", "我", "以", "要", "他",
            "时", "来", "用", "们", "生", "到", "作", "地", "于", "出", "就", "分", "对", "成", "会", "可", "主", "发", "年", "动",
            "同", "工", "也", "能", "下", "过", "子", "说", "产", "种", "面", "而", "方", "后", "多", "定", "行", "学", "法", "所",
            "民", "得", "经", "十", "三", "之", "进", "着", "等", "部", "度", "家", "电", "力", "里", "如", "水", "化", "高", "自",
            "二", "理", "起", "小", "物", "现", "实", "加", "量", "都", "两", "体", "制", "机", "当", "使", "点", "从", "业", "本",
            "去", "把", "性", "好", "应", "开", "它", "合", "还", "因", "由", "其", "些", "然", "前", "外", "天", "政", "四", "日",
            "那", "社", "义", "事", "平", "形", "相", "全", "表", "间", "样", "与", "关", "各", "重", "新", "线", "内", "数", "正",
            "心", "反", "你", "明", "看", "原", "又", "么", "利", "比", "或", "但", "质", "气", "第", "向", "道", "命", "此", "变",
            "条", "只", "没", "结", "解", "问", "意", "建", "月", "公", "无", "系", "军", "很", "情", "者", "最", "立", "代", "想",
            "已", "通", "并", "提", "直", "题", "党", "程", "展", "五", "果", "料", "象", "员", "次", "位", "常", "文", "总", "次",
            "品", "式", "活", "设", "及", "管", "特", "件", "长", "求", "老", "头", "基", "资", "边", "流", "路", "级", "少", "图",
            "山", "统", "接", "知", "较", "将", "组", "见", "计", "别", "她", "手", "角", "期", "根", "论", "运", "农", "指", "几",
            "九", "区", "强", "放", "决", "西", "被", "干", "做", "必", "战", "先", "回", "则", "任", "取", "据", "处", "队", "南",
            "给", "色", "光", "门", "即", "保", "治", "北", "造", "百", "规", "热", "领", "七", "海", "口", "东", "导", "器", "压",
            "志", "世", "金", "增", "争", "济", "阶", "油", "思", "术", "极", "交", "受", "联", "什", "认", "六", "共", "权", "收",
            "证", "改", "清", "美", "再", "采", "转", "更", "单", "风", "切", "打", "白", "教", "速", "花", "带", "安", "场", "身",
            "车", "例", "真", "务", "具", "万", "每", "目", "至", "达", "走", "积", "示", "议", "声", "报", "斗", "完", "类", "八",
            "离", "华", "名", "确", "才", "科", "张", "信", "马", "节", "话", "米", "整", "空", "元", "况", "今", "集", "温", "传",
            "土", "许", "步", "群", "广", "石", "记", "需", "段", "研", "界", "拉", "林", "律", "叫", "且", "究", "观", "越", "织",
            "装", "影", "算", "低", "持", "音", "众", "书", "布", "复", "容", "儿", "须", "际", "商", "非", "验", "连", "断", "深",
            "难", "近", "矿", "千", "周", "委", "素", "技", "备", "半", "办", "青", "省", "列", "习", "响", "约", "支", "般", "史",
            "感", "劳", "便", "团", "往", "酸", "历", "市", "克", "何", "除", "消", "构", "府", "称", "太", "准", "精", "值", "号",
            "率", "族", "维", "划", "选", "标", "写", "存", "候", "毛", "亲", "快", "效", "斯", "院", "查", "江", "型", "眼", "王"
        ]

        self.add_window_buttons()

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
        elif app_type == "deeplost":
            self.init_deeplost()

    def add_window_buttons(self):
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
        self.content = ["7", "8", "9", "÷",
                        "4", "5", "6", "×",
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
        self.content = ["欢迎使用 CrazyOS 浏览器", "CrazyOS 1.2.1 现已发布",
                        "- 优化UI界面", "- 修复DeepLost-X1输入问题", "- 修复全屏内容位置问题"]
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 70, self.y + 60, 50, 35),
            "action": "go"
        })

    def init_settings(self):
        self.content = ["显示设置", "声音设置", "网络设置", "个性化", "系统更新", "关于"]

    def init_documents(self):
        self.save_button = {
            "rect": pygame.Rect(self.x + self.width - 100, self.y + self.height - 40, 80, 30),
            "action": "save_document"
        }
        self.buttons.append(self.save_button)
        self.buttons.append({
            "rect": pygame.Rect(self.x + self.width - 190, self.y + self.height - 40, 80, 30),
            "action": "save_as"
        })

    def init_deeplost(self):
        self.input_box = pygame.Rect(self.x + 20, self.y + 60, self.width - 40, 30)
        self.generate_button = {
            "rect": pygame.Rect(self.x + self.width - 100, self.y + 100, 80, 30),
            "action": "generate_text"
        }
        self.buttons.append(self.generate_button)
        self.output_text = ""
        self.input_text = ""

    def generate_text(self):
        if self.input_text.strip():
            length = random.randint(15, 200)
            result = ''.join(random.choices(self.common_chars, k=length))
            self.output_text = result
        else:
            self.output_text = "请输入请求"

    def toggle_maximize(self):
        if self.is_maximized:
            self.x, self.y, self.width, self.height = self.normal_rect
            self.is_maximized = False
        else:
            self.normal_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            self.x, self.y = 0, 0
            self.width, self.height = WIDTH, HEIGHT - taskbar.height
            self.is_maximized = True
        self.update_button_positions()

    def minimize(self):
        self.active = False
        if self.title not in taskbar.app_buttons:
            taskbar.app_buttons.append(self.title)

    def restore(self):
        self.active = True

    def update_button_positions(self):
        self.add_window_buttons()
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
        elif self.app_type == "deeplost":
            self.input_box = pygame.Rect(self.x + 20, self.y + 60, self.width - 40, 30)
            self.generate_button = {
                "rect": pygame.Rect(self.x + self.width - 100, self.y + 100, 80, 30),
                "action": "generate_text"
            }
            self.buttons.append(self.generate_button)
        elif self.app_type == "calculator":
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
        if button_text in "0123456789":
            if self.calc_display == "0" or self.calc_waiting_operand:
                self.calc_display = button_text
                self.calc_waiting_operand = False
            else:
                self.calc_display += button_text
        elif button_text == '.' and '.' not in self.calc_display:
            self.calc_display += button_text
        elif button_text in ['+', '-', '×', '÷']:
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
        if self.calc_operator and not self.calc_waiting_operand:
            current_value = float(self.calc_display)
            try:
                if self.calc_operator == '+':
                    result = self.calc_value + current_value
                elif self.calc_operator == '-':
                    result = self.calc_value - current_value
                elif self.calc_operator == '×':
                    result = self.calc_value * current_value
                elif self.calc_operator == '÷':
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
        if self.app_type == "deeplost" and self.editing:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN:
                self.generate_text()
            elif event.unicode.isprintable():
                self.input_text += event.unicode
        elif self.app_type == "documents" and self.editing:
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
                elif self.cursor_pos[0] < len(self.document_lines) - 1:
                    self.document_lines[self.cursor_pos[0]] += self.document_lines[self.cursor_pos[0] + 1]
                    self.document_lines.pop(self.cursor_pos[0] + 1)
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
        document_storage.save_document(self.filename, self.document_lines)
        self.save_status = f"文档已保存: {self.filename} - {datetime.now().strftime('%H:%M:%S')}"
        self.save_timer = 180

    def save_as(self):
        self.show_save_dialog = True
        self.save_filename = f"document_{datetime.now().strftime('%H%M%S')}.txt"

    def update_cursor(self):
        self.cursor_timer += 1
        if self.cursor_timer >= 30:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0
        if self.save_timer > 0:
            self.save_timer -= 1

    def draw(self, surface):
        if not self.is_maximized:
            pygame.draw.rect(surface, (200, 200, 200, 100),
                             (self.x+5, self.y+5, self.width, self.height), border_radius=8)
        pygame.draw.rect(surface, WINDOW_BG, (self.x, self.y, self.width, self.height), border_radius=8 if not self.is_maximized else 0)
        pygame.draw.rect(surface, WINDOW_TITLE_BAR, (self.x, self.y, self.width, 40), border_radius=8 if not self.is_maximized else 0)
        title_text = font_medium.render(self.title, True, TEXT_COLOR)
        surface.blit(title_text, (self.x + 15, self.y + 10))

        mouse_pos = pygame.mouse.get_pos()
        close_button = self.buttons[0]["rect"]
        color = CLOSE_HOVER if close_button.collidepoint(mouse_pos) else CLOSE_BUTTON
        pygame.draw.circle(surface, color, close_button.center, 12)
        pygame.draw.circle(surface, (240, 240, 240), close_button.center, 12, 2)
        pygame.draw.line(surface, (240, 240, 240), (close_button.centerx-6, close_button.centery-6),
                         (close_button.centerx+6, close_button.centery+6), 2)
        pygame.draw.line(surface, (240, 240, 240), (close_button.centerx+6, close_button.centery-6),
                         (close_button.centerx-6, close_button.centery+6), 2)

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

        minimize_button = self.buttons[2]["rect"]
        color = MINIMIZE_HOVER if minimize_button.collidepoint(mouse_pos) else MINIMIZE_BUTTON
        pygame.draw.circle(surface, color, minimize_button.center, 12)
        pygame.draw.circle(surface, (240, 240, 240), minimize_button.center, 12, 2)
        pygame.draw.line(surface, (240, 240, 240), (minimize_button.centerx-6, minimize_button.centery),
                         (minimize_button.centerx+6, minimize_button.centery), 2)

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
        elif self.app_type == "deeplost":
            self.draw_deeplost(surface)

    def draw_explorer(self, surface):
        for i, item in enumerate(self.folder_contents[self.current_folder]):
            y_pos = self.y + 60 + i * 40
            pygame.draw.rect(surface, (240, 245, 255), (self.x + 20, y_pos, self.width - 40, 30), border_radius=4)
            item_text = font_medium.render(item, True, TEXT_COLOR)
            surface.blit(item_text, (self.x + 40, y_pos + 5))
            if item.endswith(".txt"):
                pygame.draw.rect(surface, (180, 180, 220), (self.x + self.width - 50, y_pos + 5, 20, 20), border_radius=2)

    def draw_calculator(self, surface):
        pygame.draw.rect(surface, (230, 240, 250), (self.x + 20, self.y + 60, self.width - 40, 50), border_radius=5)
        display_text = font_large.render(self.calc_display, True, TEXT_COLOR)
        text_x = self.x + self.width - 40 - display_text.get_width()
        surface.blit(display_text, (text_x, self.y + 70))
        for btn in self.calc_buttons:
            mouse_pos = pygame.mouse.get_pos()
            color = BUTTON_HOVER if btn["rect"].collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(surface, color, btn["rect"], border_radius=5)
            btn_text = font_medium.render(btn["text"], True, TEXT_COLOR)
            surface.blit(btn_text, (btn["rect"].centerx - btn_text.get_width()//2,
                                   btn["rect"].centery - btn_text.get_height()//2))

    def draw_browser(self, surface):
        pygame.draw.rect(surface, (230, 240, 250), (self.x + 20, self.y + 60, self.width - 100, 35), border_radius=5)
        url_text = font_medium.render("pyos://home", True, TEXT_COLOR)
        surface.blit(url_text, (self.x + 30, self.y + 65))
        if len(self.buttons) > 3:
            go_button = self.buttons[3]["rect"]
            mouse_pos = pygame.mouse.get_pos()
            color = BUTTON_HOVER if go_button.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(surface, color, go_button, border_radius=5)
            go_text = font_medium.render("GO", True, TEXT_COLOR)
            surface.blit(go_text, (go_button.centerx - go_text.get_width()//2, go_button.centery - go_text.get_height()//2))
        pygame.draw.rect(surface, DOCUMENT_BG, (self.x + 20, self.y + 110, self.width - 40, self.height - 140), border_radius=5)
        for i, line in enumerate(self.content):
            content_text = font_medium.render(line, True, TEXT_COLOR)
            surface.blit(content_text, (self.x + 40, self.y + 130 + i * 35))

    def draw_settings(self, surface):
        for i, item in enumerate(self.content):
            y_pos = self.y + 60 + i * 50
            color = (230, 235, 245) if i == self.selected_setting else (240, 245, 255)
            pygame.draw.rect(surface, color, (self.x + 20, y_pos, self.width - 40, 40), border_radius=4)
            item_text = font_medium.render(item, True, TEXT_COLOR)
            surface.blit(item_text, (self.x + 40, y_pos + 10))
            if i == 0:
                pygame.draw.rect(surface, (100, 180, 220), (self.x + self.width - 60, y_pos + 5, 30, 30), border_radius=3)
            elif i == 1:
                pygame.draw.circle(surface, (180, 180, 220), (self.x + self.width - 45, y_pos + 20), 12)
                pygame.draw.line(surface, (180, 180, 220), (self.x + self.width - 45, y_pos + 8),
                                (self.x + self.width - 45, y_pos + 32), 2)
            elif i == 5:
                pygame.draw.circle(surface, (100, 200, 150), (self.x + self.width - 45, y_pos + 20), 12)
                info_text = font_small.render("i", True, TEXT_COLOR)
                surface.blit(info_text, (self.x + self.width - 50, y_pos + 12))
        if self.show_update:
            update_rect = pygame.Rect(self.x + 50, self.y + 100, self.width - 100, self.height - 150)
            pygame.draw.rect(surface, WINDOW_TITLE_BAR, update_rect, border_radius=10)
            pygame.draw.rect(surface, SYSTEM_BLUE, update_rect, 2, border_radius=10)
            update_text = [
                "当前版本: 1.2.1",
                "转到https://github.com",
                "/CreatorFMZ/CrazyOS/",
                "tree/main/CrazyOS",
                "以获取最新版本"
            ]
            for i, text in enumerate(update_text):
                text_surface = font_medium.render(text, True, TEXT_COLOR)
                surface.blit(text_surface, (update_rect.x + 30, update_rect.y + 30 + i * 35))
        elif self.show_about:
            about_rect = pygame.Rect(self.x + 50, self.y + 100, self.width - 100, self.height - 150)
            pygame.draw.rect(surface, WINDOW_TITLE_BAR, about_rect, border_radius=10)
            pygame.draw.rect(surface, SYSTEM_BLUE, about_rect, 2, border_radius=10)
            about_texts = [
                "CrazyOS 1.2.1",
                "Python 操作系统模拟器",
                "©Fanatic Star梦幻星",
                "2025, All rights reserved"
            ]
            for i, text in enumerate(about_texts):
                text_surface = font_medium.render(text, True, TEXT_COLOR)
                surface.blit(text_surface, (about_rect.x + 30, about_rect.y + 30 + i * 35))

    def draw_deeplost(self, surface):
        pygame.draw.rect(surface, (230, 240, 250), self.input_box, border_radius=5)
        input_text_surface = font_medium.render(self.input_text, True, TEXT_COLOR)
        surface.blit(input_text_surface, (self.input_box.x + 5, self.input_box.y + 5))
        generate_button = self.buttons[3]
        color = BUTTON_HOVER if generate_button["rect"].collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(surface, color, generate_button["rect"], border_radius=5)
        generate_text = font_medium.render("生成", True, TEXT_COLOR)
        surface.blit(generate_text, (generate_button["rect"].centerx - generate_text.get_width()//2,
                                     generate_button["rect"].centery - generate_text.get_height()//2))
        output_rect = pygame.Rect(self.x + 20, self.y + 140, self.width - 40, self.height - 160)
        pygame.draw.rect(surface, DOCUMENT_BG, output_rect, border_radius=5)
        output_lines = self.output_text.split('\n')
        for i, line in enumerate(output_lines):
            output_text_surface = font_medium.render(line, True, TEXT_COLOR)
            surface.blit(output_text_surface, (output_rect.x + 10, output_rect.y + 10 + i * 25))

    def draw_documents(self, surface):
        editor_rect = pygame.Rect(self.x + 20, self.y + 60, self.width - 40, self.height - 110)
        pygame.draw.rect(surface, EDITOR_BG, editor_rect, border_radius=5)
        line_height = 25
        visible_lines = min(len(self.document_lines), (editor_rect.height - 20) // line_height)
        for i in range(visible_lines):
            line = self.document_lines[i]
            line_text = font_code.render(line, True, TEXT_COLOR)
            surface.blit(line_text, (self.x + 30, self.y + 70 + i * line_height))
        if self.editing and self.cursor_visible and self.cursor_pos[0] < visible_lines:
            cursor_x = self.x + 30 + font_code.size(self.document_lines[self.cursor_pos[0]][:self.cursor_pos[1]])[0]
            cursor_y = self.y + 70 + self.cursor_pos[0] * line_height
            pygame.draw.line(surface, TEXT_COLOR, (cursor_x, cursor_y),
                            (cursor_x, cursor_y + line_height - 5), 2)
        for button in self.buttons:
            if button["action"] in ["save_document", "save_as"]:
                mouse_pos = pygame.mouse.get_pos()
                color = SAVE_HOVER if button["rect"].collidepoint(mouse_pos) else SAVE_BUTTON
                pygame.draw.rect(surface, color, button["rect"], border_radius=5)
                btn_text = font_medium.render("保存" if button["action"] == "save_document" else "另存为", True, TEXT_COLOR)
                surface.blit(btn_text, (button["rect"].centerx - btn_text.get_width()//2,
                                       button["rect"].centery - btn_text.get_height()//2))
        if self.save_timer > 0:
            status_text = font_small.render(self.save_status, True, (100, 200, 100))
            surface.blit(status_text, (self.x + 30, self.y + self.height - 35))
        hint_text = font_small.render(f"当前文件: {self.filename} | 按Ctrl+S保存文档 | 双击开始编辑", True, TEXT_COLOR)
        surface.blit(hint_text, (self.x + 30, self.y + self.height - 60))

    def is_title_bar_hit(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + 40

    def is_inside(self, pos):
        return self.x <= pos[0] <= self.x + self.width and self.y <= pos[1] <= self.y + self.height

class Taskbar:
    def __init__(self):
        self.height = 50
        self.app_buttons = []
        self.time_rect = pygame.Rect(WIDTH - 150, HEIGHT - self.height + 10, 130, 30)

    def draw(self, surface):
        s = pygame.Surface((WIDTH, self.height))
        s.set_alpha(180)
        s.fill(TASKBAR)
        surface.blit(s, (0, HEIGHT - self.height))
        pygame.draw.line(surface, (200, 210, 230), (0, HEIGHT - self.height), (WIDTH, HEIGHT - self.height), 1)
        start_rect = pygame.Rect(10, HEIGHT - self.height + 5, 80, 40)
        color = BUTTON_HOVER if start_rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLOR
        pygame.draw.rect(surface, color, start_rect, border_radius=5)
        start_text = font_medium.render("开始", True, TEXT_COLOR)
        surface.blit(start_text, (start_rect.centerx - start_text.get_width()//2, start_rect.centery - start_text.get_height()//2))
        for i, btn in enumerate(self.app_buttons):
            btn_rect = pygame.Rect(100 + i * 120, HEIGHT - self.height + 5, 110, 40)
            mouse_pos = pygame.mouse.get_pos()
            color = BUTTON_HOVER if btn_rect.collidepoint(mouse_pos) else BUTTON_COLOR
            pygame.draw.rect(surface, color, btn_rect, border_radius=5)
            app_text = font_medium.render(btn, True, TEXT_COLOR)
            surface.blit(app_text, (btn_rect.centerx - app_text.get_width()//2, btn_rect.centery - app_text.get_height()//2))
        current_time = datetime.now()
        day_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][current_time.weekday()]
        time_text = font_medium.render(f"{day_of_week} {current_time.strftime('%H:%M:%S')}", True, TEXT_COLOR)
        surface.blit(time_text, (self.time_rect.centerx - time_text.get_width()//2,
                               self.time_rect.centery - time_text.get_height()//2))

icon_positions = [(100 + (i % 3) * 120, 100 + (i // 3) * 120) for i in range(7)]
desktop_icons = [
    Icon(*icon_positions[0], "文件管理器", "explorer"),
    Icon(*icon_positions[1], "计算器", "calculator"),
    Icon(*icon_positions[2], "浏览器", "browser"),
    Icon(*icon_positions[3], "DeepLost-X1", "deeplost"),
    Icon(*icon_positions[4], "文档", "documents"),
    Icon(*icon_positions[5], "图片", "images"),
    Icon(*icon_positions[6], "系统设置", "settings")
]

taskbar = Taskbar()
windows = []
active_window_index = -1
active_input_window = None
clock = pygame.time.Clock()

running = True
while running:
    current_time = datetime.now()
    mouse_pos = pygame.mouse.get_pos()

    for window in windows:
        if window.app_type == "documents":
            window.update_cursor()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            icon_clicked = False
            # Check if any active window is in front of the mouse position
            window_in_front = False
            for i in range(len(windows)-1, -1, -1):
                window = windows[i]
                if window.active and window.is_inside(mouse_pos):
                    window_in_front = True
                    break
            if not window_in_front:
                for icon in desktop_icons:
                    if icon.is_hovered(mouse_pos):
                        for i in desktop_icons:
                            i.selected = False
                        icon.selected = True
                        icon_clicked = True
                        if event.button == 1:
                            current_ticks = pygame.time.get_ticks()
                            if current_ticks - icon.last_click < 300:
                                app_type = icon.app_type
                                is_open = False
                                for w in windows:
                                    if w.title == icon.label:
                                        is_open = True
                                        w.restore()
                                        windows.append(windows.pop(windows.index(w)))
                                        active_window_index = len(windows) - 1
                                        break
                                if is_open:
                                    break
                                window_title = ""
                                if app_type == "explorer":
                                    window_title = "文件管理器"
                                elif app_type == "calculator":
                                    window_title = "计算器"
                                elif app_type == "browser":
                                    window_title = "浏览器"
                                elif app_type == "documents":
                                    window_title = "文档编辑器"
                                elif app_type == "settings":
                                    window_title = "系统设置"
                                elif app_type == "deeplost":
                                    window_title = "DeepLost-X1"
                                else:
                                    window_title = icon.label
                                win_width = 500 if app_type == "documents" else 400
                                win_height = 500 if app_type == "documents" else 400
                                new_window = Window(window_title, 150 + len(windows)*20, 100 + len(windows)*20, win_width, win_height, app_type)
                                windows.append(new_window)
                                active_window_index = len(windows) - 1
                                if window_title not in taskbar.app_buttons:
                                    taskbar.app_buttons.append(window_title)
                            icon.last_click = current_ticks
                            break

            if not icon_clicked:
                for i, btn_title in enumerate(taskbar.app_buttons):
                    btn_rect = pygame.Rect(100 + i * 120, HEIGHT - taskbar.height + 5, 110, 40)
                    if btn_rect.collidepoint(mouse_pos):
                        for j, window in enumerate(windows):
                            if window.title == btn_title:
                                window.restore()
                                windows.append(windows.pop(j))
                                active_window_index = len(windows) - 1
                                break

            handled = False
            for i in range(len(windows)-1, -1, -1):
                window = windows[i]
                if not window.active:
                    continue
                if window.is_inside(mouse_pos):
                    active_window_index = i
                    windows.append(windows.pop(i))
                    active_window_index = len(windows) - 1
                    window = windows[-1]
                    handled = True
                    for button in window.buttons:
                        if button["rect"].collidepoint(mouse_pos):
                            if button["action"] == "close":
                                if window.title in taskbar.app_buttons:
                                    taskbar.app_buttons.remove(window.title)
                                windows.pop(i)
                                active_window_index = -1 if not windows else len(windows)-1
                                active_input_window = None
                                break
                            elif button["action"] == "go":
                                if window.app_type == "browser":
                                    window.content = [
                                        "CrazyOS 1.2.1 浏览器",
                                        "正在加载 pyos://home...",
                                        "CrazyOS 1.2.1 更新日志：",
                                        "- 优化代码",
                                        "- 修复DeepLost-X1输入问题",
                                        "- 修复全屏内容位置问题"
                                    ]
                                break
                            elif button["action"] == "save_document":
                                window.save_document()
                                break
                            elif button["action"] == "save_as":
                                window.save_as()
                                break
                            elif button["action"] == "generate_text":
                                if window.app_type == "deeplost":
                                    window.generate_text()
                                break
                            elif button["action"] == "maximize":
                                window.toggle_maximize()
                                break
                            elif button["action"] == "minimize":
                                window.minimize()
                                break
                    if window.is_title_bar_hit(mouse_pos) and not window.is_maximized:
                        window.dragging = True
                        window.drag_offset_x = mouse_pos[0] - window.x
                        window.drag_offset_y = mouse_pos[1] - window.y
                    elif not window.is_title_bar_hit(mouse_pos):
                        if window.app_type == "deeplost" and window.input_box.collidepoint(mouse_pos):
                            window.editing = True
                            active_input_window = window
                        elif window.app_type == "documents" and event.button == 1:
                            if window.editing:
                                line_height = 25
                                editor_top = window.y + 70
                                click_line = max(0, min(len(window.document_lines) - 1, (mouse_pos[1] - editor_top) // line_height))
                                line_text = window.document_lines[click_line]
                                click_x = mouse_pos[0] - (window.x + 30)
                                char_index = 0
                                current_width = 0
                                for char_i, char in enumerate(line_text):
                                    char_width = font_code.size(char)[0]
                                    if current_width + char_width / 2 > click_x:
                                        break
                                    current_width += char_width
                                    char_index = char_i + 1
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
                        elif window.app_type == "calculator":
                            for btn in window.calc_buttons:
                                if btn["rect"].collidepoint(mouse_pos):
                                    window.handle_calculator_click(btn["text"])
                                    break
                        elif window.app_type == "explorer":
                            for item_i, item in enumerate(window.folder_contents[window.current_folder]):
                                y_pos = window.y + 60 + item_i * 40
                                item_rect = pygame.Rect(window.x + 20, y_pos, window.width - 40, 30)
                                if item_rect.collidepoint(mouse_pos):
                                    if item == "文档":
                                        window.current_folder = "文档"
                                        window.content = window.folder_contents["文档"]
                                    elif item.endswith(".txt"):
                                        doc_content = document_storage.documents.get(item, ["文档内容为空"])
                                        new_window = Window(f"文档: {item}", 200, 150, 500, 500, "documents")
                                        new_window.document_lines = doc_content.copy()
                                        new_window.filename = item
                                        windows.append(new_window)
                                        if new_window.title not in taskbar.app_buttons:
                                            taskbar.app_buttons.append(new_window.title)
                                    break
                        elif window.app_type == "settings":
                            for item_i, item in enumerate(window.content):
                                y_pos = window.y + 60 + item_i * 50
                                item_rect = pygame.Rect(window.x + 20, y_pos, window.width - 40, 40)
                                if item_rect.collidepoint(mouse_pos):
                                    window.selected_setting = item_i
                                    if item == "关于":
                                        window.show_about = not window.show_about
                                        window.show_update = False
                                    elif item == "系统更新":
                                        window.show_update = not window.show_update
                                        window.show_about = False
                                    break
                else:
                    if window.app_type == "deeplost" and window.editing:
                        window.editing = False
                        if active_input_window == window:
                            active_input_window = None
                if handled:
                    break
            if not handled and not icon_clicked:
                for icon in desktop_icons:
                    icon.selected = False
                if active_input_window and not active_input_window.is_inside(mouse_pos):
                    active_input_window.editing = False
                    active_input_window = None
                for window in windows:
                    if window.app_type == "settings" and (window.show_about or window.show_update) and not window.is_inside(mouse_pos):
                        window.show_about = False
                        window.show_update = False

        elif event.type == pygame.MOUSEBUTTONUP:
            for window in windows:
                window.dragging = False

        elif event.type == pygame.KEYDOWN:
            if active_input_window:
                active_input_window.handle_keyboard_input(event)
            if event.key == pygame.K_F11 and active_window_index >= 0:
                windows[active_window_index].toggle_maximize()

    if active_window_index >= 0 and active_window_index < len(windows):
        window = windows[active_window_index]
        if window.dragging and not window.is_maximized and window.active:
            window.x = mouse_pos[0] - window.drag_offset_x
            window.y = mouse_pos[1] - window.drag_offset_y
            window.y = max(0, window.y)
            window.update_button_positions()

    screen.fill(BACKGROUND)
    for i in range(0, WIDTH, 40):
        pygame.draw.line(screen, (108, 152, 213), (i, 0), (i, HEIGHT), 1)
    for i in range(0, HEIGHT, 40):
        pygame.draw.line(screen, (108, 152, 213), (0, i), (WIDTH, i), 1)
    for icon in desktop_icons:
        icon.draw(screen)
    for window in windows:
        if window.active:
            window.draw(screen)
    taskbar.draw(screen)
    current_time = datetime.now()
    date_text = font_medium.render(current_time.strftime("%Y-%m-%d"), True, TEXT_COLOR)
    screen.blit(date_text, (WIDTH - date_text.get_width() - 150, HEIGHT - 37))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()