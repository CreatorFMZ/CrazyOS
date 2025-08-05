#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <SFML/Window.hpp>
#include <iostream>
#include <vector>
#include <ctime>
#include <cmath>
#include <sstream>
#include <iomanip>
#include <map>
#include <algorithm>

using namespace sf;
using namespace std;

// 颜色定义
const Color BACKGROUND(40, 44, 52);
const Color TASKBAR(30, 34, 45);
const Color WINDOW_BG(50, 54, 64);
const Color WINDOW_TITLE_BAR(70, 130, 180);
const Color BUTTON_COLOR(86, 182, 194);
const Color BUTTON_HOVER(106, 202, 214);
const Color TEXT_COLOR(220, 220, 220);
const Color ICON_COLOR(100, 200, 200);
const Color CLOSE_BUTTON(220, 100, 100);
const Color CLOSE_HOVER(240, 120, 120);
const Color MAXIMIZE_BUTTON(100, 180, 100);
const Color MAXIMIZE_HOVER(120, 200, 120);
const Color MINIMIZE_BUTTON(220, 180, 80);
const Color MINIMIZE_HOVER(240, 200, 100);
const Color SYSTEM_BLUE(64, 156, 255);
const Color DOCUMENT_BG(60, 64, 74);
const Color EDITOR_BG(45, 50, 60);
const Color SAVE_BUTTON(70, 160, 110);
const Color SAVE_HOVER(90, 180, 130);
const Color TEXT_HIGHLIGHT(100, 180, 255, 100);
const Color ACCENT_COLOR(0, 120, 215); // Windows 11 强调色
const Color DARK_MODE_BG(32, 32, 32); // Windows 11 深色模式背景
const Color LIGHT_BLUE(173, 216, 230); // Windows 11 风格浅蓝色
const Color TRANSPARENT(0, 0, 0, 0); // 透明色

// 字体设置
Font globalFont;

// 文档存储类
class DocumentStorage {
public:
    map<string, vector<string>> documents;
    
    DocumentStorage() {
        documents["welcome.txt"] = {"欢迎使用CrazyOS文档编辑器", "这是一个示例文档"};
        documents["notes.txt"] = {"我的笔记", "重要事项：", "- 修复图层问题", "- 添加文档存储"};
    }
    
    void save_document(const string& filename, const vector<string>& content) {
        documents[filename] = content;
    }
    
    vector<string> get_documents() {
        vector<string> keys;
        for (const auto& doc : documents) {
            keys.push_back(doc.first);
        }
        return keys;
    }
};

// 创建文档存储
DocumentStorage document_storage;

// 图标类
class Icon {
public:
    float x, y;
    string label;
    string app_type;
    float width = 80;
    float height = 90;
    bool selected = false;
    Clock last_click_clock;
    
    Icon(float x, float y, const string& label, const string& app_type)
        : x(x), y(y), label(label), app_type(app_type) {}
    
    void draw(RenderWindow& window) {
        RectangleShape rect(Vector2f(width, height));
        rect.setPosition(x, y);
        rect.setFillColor(selected ? Color(150, 200, 220) : ICON_COLOR);
        rect.setOutlineColor(Color(rect.getFillColor().r - 20, rect.getFillColor().g - 20, rect.getFillColor().b - 20));
        rect.setOutlineThickness(2);
        rect.setRadius(8);
        window.draw(rect);
        
        // 应用图标
        if (app_type == "explorer") {
            RectangleShape folder(Vector2f(40, 30));
            folder.setPosition(x + 20, y + 15);
            folder.setFillColor(Color(70, 130, 180));
            folder.setRadius(4);
            window.draw(folder);
            
            RectangleShape folder_inner(Vector2f(30, 20));
            folder_inner.setPosition(x + 25, y + 20);
            folder_inner.setFillColor(Color(100, 160, 210));
            folder_inner.setRadius(3);
            window.draw(folder_inner);
            
            CircleShape circle(15);
            circle.setPosition(x + 25, y + 40);
            circle.setFillColor(Color(240, 200, 80));
            window.draw(circle);
        }
        else if (app_type == "calculator") {
            RectangleShape calc(Vector2f(40, 40));
            calc.setPosition(x + 20, y + 15);
            calc.setFillColor(Color(70, 160, 110));
            calc.setRadius(5);
            window.draw(calc);
            
            for (int i = 0; i < 3; i++) {
                RectangleShape line(Vector2f(30, 8));
                line.setPosition(x + 25, y + 25 + i * 15);
                line.setFillColor(Color(220, 220, 220));
                line.setRadius(3);
                window.draw(line);
            }
        }
        else if (app_type == "browser") {
            RectangleShape browser(Vector2f(50, 40));
            browser.setPosition(x + 15, y + 15);
            browser.setFillColor(Color(100, 180, 100));
            browser.setRadius(5);
            window.draw(browser);
            
            // 简化的浏览器图标
            CircleShape arc(20, 30);
            arc.setPosition(x + 20, y + 20);
            arc.setFillColor(Color(50, 120, 50));
            window.draw(arc);
        }
        else if (app_type == "documents") {
            RectangleShape doc(Vector2f(40, 50));
            doc.setPosition(x + 20, y + 15);
            doc.setFillColor(Color(180, 180, 220));
            doc.setRadius(3);
            window.draw(doc);
            
            for (int i = 0; i < 3; i++) {
                RectangleShape line(Vector2f(30, 2));
                line.setPosition(x + 25, y + 25 + i * 10);
                line.setFillColor(Color(140, 140, 180));
                window.draw(line);
            }
        }
        else if (app_type == "images") {
            RectangleShape img(Vector2f(40, 40));
            img.setPosition(x + 20, y + 15);
            img.setFillColor(Color(220, 180, 220));
            img.setRadius(3);
            window.draw(img);
            
            // 简化的图片图标
            CircleShape circle(5);
            circle.setPosition(x + 35, y + 35);
            circle.setFillColor(Color(180, 140, 180));
            window.draw(circle);
        }
        else if (app_type == "settings") {
            CircleShape gear(20);
            gear.setPosition(x + 20, y + 15);
            gear.setFillColor(Color(180, 180, 220));
            gear.setOutlineColor(Color(140, 140, 180));
            gear.setOutlineThickness(2);
            window.draw(gear);
            
            // 齿轮齿
            for (int i = 0; i < 6; i++) {
                float angle = i * 3.14159f / 3;
                float x1 = x + 40 + 15 * cos(angle);
                float y1 = y + 35 + 15 * sin(angle);
                float x2 = x + 40 + 8 * cos(angle);
                float y2 = y + 35 + 8 * sin(angle);
                
                Vertex line[] = {
                    Vertex(Vector2f(x1, y1), Color(140, 140, 180)),
                    Vertex(Vector2f(x2, y2), Color(140, 140, 180))
                };
                window.draw(line, 2, Lines);
            }
        }
        
        // 图标标签
        Text text(label, globalFont, 14);
        text.setFillColor(TEXT_COLOR);
        text.setPosition(x + width/2 - text.getLocalBounds().width/2, y + height - 25);
        window.draw(text);
    }
    
    bool is_hovered(Vector2f pos) {
        return pos.x >= x && pos.x <= x + width && pos.y >= y && pos.y <= y + height;
    }
};

// 窗口类
class Window {
public:
    string title;
    float x, y;
    float width, height;
    string app_type;
    bool active = true;
    bool dragging = false;
    float drag_offset_x = 0;
    float drag_offset_y = 0;
    vector<string> content;
    vector<RectangleShape> buttons;
    vector<string> button_actions;
    vector<string> calc_buttons;
    string calc_display = "0";
    double calc_value = 0;
    string calc_operator;
    bool calc_waiting_operand = false;
    Clock last_click_clock;
    
    // 全屏状态
    bool is_maximized = false;
    FloatRect normal_rect;
    
    // 文档应用属性
    vector<string> document_lines = {"欢迎使用CrazyOS文档编辑器", "在这里输入您的文本...", "", "按Ctrl+S保存文档"};
    Vector2u cursor_pos = {0, 0};
    bool cursor_visible = true;
    Clock cursor_timer;
    bool editing = false;
    string save_status = "";
    Clock save_timer;
    string filename = "untitled.txt";
    bool show_save_dialog = false;
    string save_filename = "document.txt";
    
    // 设置应用属性
    int selected_setting = -1;
    bool show_about = false;
    
    // 文件管理器属性
    string current_folder = "root";
    map<string, vector<string>> folder_contents = {
        {"root", {"文档", "图片", "音乐", "视频", "下载", "桌面"}},
        {"文档", document_storage.get_documents()}
    };
    
    // Windows 11 特有属性
    bool mica_enabled = true; // Windows 11 Mica材质效果
    float corner_radius = 10.0f; // Windows 11 圆角半径
    
    Window(const string& title, float x, float y, float width, float height, const string& app_type)
        : title(title), x(x), y(y), width(width), height(height), app_type(app_type) {
        normal_rect = FloatRect(x, y, width, height);
        add_window_buttons();
        
        if (app_type == "explorer") {
            content = folder_contents[current_folder];
        }
        else if (app_type == "calculator") {
            init_calculator();
        }
        else if (app_type == "browser") {
            init_browser();
        }
        else if (app_type == "settings") {
            init_settings();
        }
        else if (app_type == "documents") {
            init_documents();
        }
    }
    
    void add_window_buttons() {
        buttons.clear();
        button_actions.clear();
        
        // 关闭按钮
        RectangleShape close_button(Vector2f(25, 25));
        close_button.setPosition(x + width - 35, y + 10);
        buttons.push_back(close_button);
        button_actions.push_back("close");
        
        // 最大化按钮
        RectangleShape maximize_button(Vector2f(25, 25));
        maximize_button.setPosition(x + width - 65, y + 10);
        buttons.push_back(maximize_button);
        button_actions.push_back("maximize");
        
        // 最小化按钮
        RectangleShape minimize_button(Vector2f(25, 25));
        minimize_button.setPosition(x + width - 95, y + 10);
        buttons.push_back(minimize_button);
        button_actions.push_back("minimize");
    }
    
    void init_calculator() {
        content = {"7", "8", "9", "/", "4", "5", "6", "*", "1", "2", "3", "-", "C", "0", "=", "+"};
    }
    
    void init_browser() {
        content = {"欢迎使用 CrazyOS 浏览器", "CrazyOS v1.0 已发布", 
                   "新增功能：Windows 11风格界面", "修复了多个已知问题"};
        
        RectangleShape go_button(Vector2f(50, 35));
        go_button.setPosition(x + width - 70, y + 60);
        buttons.push_back(go_button);
        button_actions.push_back("go");
    }
    
    void init_settings() {
        content = {"显示设置", "声音设置", "网络设置", "个性化", "系统更新", "关于"};
    }
    
    void init_documents() {
        RectangleShape save_button(Vector2f(80, 30));
        save_button.setPosition(x + width - 100, y + height - 40);
        buttons.push_back(save_button);
        button_actions.push_back("save_document");
        
        RectangleShape save_as_button(Vector2f(80, 30));
        save_as_button.setPosition(x + width - 190, y + height - 40);
        buttons.push_back(save_as_button);
        button_actions.push_back("save_as");
    }
    
    void toggle_maximize() {
        if (is_maximized) {
            x = normal_rect.left;
            y = normal_rect.top;
            width = normal_rect.width;
            height = normal_rect.height;
            is_maximized = false;
        } else {
            normal_rect = FloatRect(x, y, width, height);
            x = 0;
            y = 0;
            width = VideoMode::getDesktopMode().width;
            height = VideoMode::getDesktopMode().height - 50; // 任务栏高度
            is_maximized = true;
        }
        
        update_button_positions();
    }
    
    void minimize() {
        active = false;
    }
    
    void restore() {
        active = true;
    }
    
    void update_button_positions() {
        add_window_buttons();
        
        if (app_type == "browser") {
            RectangleShape go_button(Vector2f(50, 35));
            go_button.setPosition(x + width - 70, y + 60);
            buttons.push_back(go_button);
            button_actions.push_back("go");
        }
        else if (app_type == "documents") {
            RectangleShape save_button(Vector2f(80, 30));
            save_button.setPosition(x + width - 100, y + height - 40);
            buttons.push_back(save_button);
            button_actions.push_back("save_document");
            
            RectangleShape save_as_button(Vector2f(80, 30));
            save_as_button.setPosition(x + width - 190, y + height - 40);
            buttons.push_back(save_as_button);
            button_actions.push_back("save_as");
        }
    }
    
    void handle_calculator_click(const string& button_text) {
        if (button_text.find_first_of("0123456789") != string::npos) {
            if (calc_display == "0" || calc_waiting_operand) {
                calc_display = button_text;
                calc_waiting_operand = false;
            } else {
                calc_display += button_text;
            }
        }
        else if (button_text == "." && calc_display.find('.') == string::npos) {
            calc_display += button_text;
        }
        else if (button_text == "+" || button_text == "-" || button_text == "*" || button_text == "/") {
            if (!calc_operator.empty() && !calc_waiting_operand) {
                calculate();
            }
            calc_value = stod(calc_display);
            calc_operator = button_text;
            calc_waiting_operand = true;
        }
        else if (button_text == "=") {
            calculate();
            calc_operator = "";
        }
        else if (button_text == "C") {
            calc_display = "0";
            calc_value = 0;
            calc_operator = "";
            calc_waiting_operand = false;
        }
    }
    
    void calculate() {
        if (!calc_operator.empty() && !calc_waiting_operand) {
            double current_value = stod(calc_display);
            double result = 0;
            
            if (calc_operator == "+") {
                result = calc_value + current_value;
            } else if (calc_operator == "-") {
                result = calc_value - current_value;
            } else if (calc_operator == "*") {
                result = calc_value * current_value;
            } else if (calc_operator == "/") {
                if (current_value != 0) {
                    result = calc_value / current_value;
                } else {
                    result = 0;
                }
            }
            
            calc_display = to_string(result);
            if (calc_display.find('.') != string::npos) {
                // 去除多余的零
                calc_display.erase(calc_display.find_last_not_of('0') + 1, string::npos);
                if (calc_display.back() == '.') {
                    calc_display.pop_back();
                }
            }
            
            calc_value = result;
            calc_waiting_operand = true;
        }
    }
    
    void save_document() {
        document_storage.save_document(filename, document_lines);
        time_t now = time(0);
        tm* ltm = localtime(&now);
        ostringstream oss;
        oss << "文档已保存: " << filename << " - " 
            << setw(2) << setfill('0') << ltm->tm_hour << ":"
            << setw(2) << setfill('0') << ltm->tm_min << ":"
            << setw(2) << setfill('0') << ltm->tm_sec;
        save_status = oss.str();
        save_timer.restart();
    }
    
    void save_as() {
        show_save_dialog = true;
        time_t now = time(0);
        tm* ltm = localtime(&now);
        ostringstream oss;
        oss << "document_" 
            << setw(2) << setfill('0') << ltm->tm_hour
            << setw(2) << setfill('0') << ltm->tm_min
            << setw(2) << setfill('0') << ltm->tm_sec << ".txt";
        save_filename = oss.str();
    }
    
    void update_cursor() {
        if (cursor_timer.getElapsedTime().asMilliseconds() >= 500) {
            cursor_visible = !cursor_visible;
            cursor_timer.restart();
        }
    }
    
    void draw(RenderWindow& window) {
        // Windows 11 Mica效果背景
        if (mica_enabled) {
            RectangleShape mica_bg(Vector2f(width, height));
            mica_bg.setPosition(x, y);
            mica_bg.setFillColor(Color(30, 30, 30, 200)); // 半透明效果
            window.draw(mica_bg);
        }
        
        // 窗口主体
        RectangleShape window_bg(Vector2f(width, height));
        window_bg.setPosition(x, y);
        window_bg.setFillColor(WINDOW_BG);
        window_bg.setOutlineThickness(1);
        window_bg.setOutlineColor(Color(60, 60, 60));
        window_bg.setRadius(corner_radius);
        window.draw(window_bg);
        
        // 标题栏 (Windows 11风格)
        RectangleShape title_bar(Vector2f(width, 40));
        title_bar.setPosition(x, y);
        title_bar.setFillColor(WINDOW_TITLE_BAR);
        title_bar.setOutlineThickness(1);
        title_bar.setOutlineColor(Color(40, 40, 40));
        title_bar.setRadius(corner_radius);
        window.draw(title_bar);
        
        // 窗口标题
        Text title_text(title, globalFont, 18);
        title_text.setFillColor(TEXT_COLOR);
        title_text.setPosition(x + 15, y + 10);
        window.draw(title_text);
        
        // 窗口控制按钮
        Vector2f mouse_pos = Vector2f(Mouse::getPosition(window));
        
        // 关闭按钮
        buttons[0].setFillColor(buttons[0].getGlobalBounds().contains(mouse_pos) ? CLOSE_HOVER : CLOSE_BUTTON);
        window.draw(buttons[0]);
        
        // 最大化按钮
        buttons[1].setFillColor(buttons[1].getGlobalBounds().contains(mouse_pos) ? MAXIMIZE_HOVER : MAXIMIZE_BUTTON);
        window.draw(buttons[1]);
        
        // 最小化按钮
        buttons[2].setFillColor(buttons[2].getGlobalBounds().contains(mouse_pos) ? MINIMIZE_HOVER : MINIMIZE_BUTTON);
        window.draw(buttons[2]);
        
        // 应用特定内容
        if (app_type == "explorer") {
            draw_explorer(window);
        }
        else if (app_type == "calculator") {
            draw_calculator(window);
        }
        else if (app_type == "browser") {
            draw_browser(window);
        }
        else if (app_type == "settings") {
            draw_settings(window);
        }
        else if (app_type == "documents") {
            draw_documents(window);
        }
    }
    
    void draw_explorer(RenderWindow& window) {
        // 文件列表
        for (int i = 0; i < folder_contents[current_folder].size(); i++) {
            const string& item = folder_contents[current_folder][i];
            float y_pos = y + 60 + i * 40;
            
            RectangleShape item_bg(Vector2f(width - 40, 30));
            item_bg.setPosition(x + 20, y_pos);
            item_bg.setFillColor(DOCUMENT_BG);
            item_bg.setRadius(4);
            window.draw(item_bg);
            
            Text item_text(item, globalFont, 18);
            item_text.setFillColor(TEXT_COLOR);
            item_text.setPosition(x + 40, y_pos + 5);
            window.draw(item_text);
            
            // 文件图标
            if (item.find(".txt") != string::npos) {
                RectangleShape file_icon(Vector2f(20, 20));
                file_icon.setPosition(x + width - 50, y_pos + 5);
                file_icon.setFillColor(Color(180, 180, 220));
                file_icon.setRadius(2);
                window.draw(file_icon);
            }
        }
    }
    
    void draw_calculator(RenderWindow& window) {
        // 显示区域
        RectangleShape display(Vector2f(width - 40, 50));
        display.setPosition(x + 20, y + 60);
        display.setFillColor(Color(30, 34, 40));
        display.setRadius(5);
        window.draw(display);
        
        Text display_text(calc_display, globalFont, 24);
        display_text.setFillColor(Color(100, 200, 150));
        display_text.setPosition(x + width - 40 - display_text.getLocalBounds().width, y + 75);
        window.draw(display_text);
        
        // 按钮
        float button_size = 50;
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j < 4; j++) {
                int idx = i * 4 + j;
                if (idx < content.size()) {
                    float btn_x = x + 30 + j * (button_size + 10);
                    float btn_y = y + 130 + i * (button_size + 10);
                    
                    RectangleShape btn(Vector2f(button_size, button_size));
                    btn.setPosition(btn_x, btn_y);
                    btn.setFillColor(btn.getGlobalBounds().contains(Vector2f(Mouse::getPosition(window))) ? 
                                     BUTTON_HOVER : BUTTON_COLOR);
                    btn.setRadius(5);
                    window.draw(btn);
                    
                    Text btn_text(content[idx], globalFont, 18);
                    btn_text.setFillColor(TEXT_COLOR);
                    btn_text.setPosition(btn_x + button_size/2 - btn_text.getLocalBounds().width/2, 
                                        btn_y + button_size/2 - btn_text.getLocalBounds().height/2);
                    window.draw(btn_text);
                }
            }
        }
    }
    
    void draw_browser(RenderWindow& window) {
        // URL栏
        RectangleShape url_bar(Vector2f(width - 100, 35));
        url_bar.setPosition(x + 20, y + 60);
        url_bar.setFillColor(Color(30, 34, 40));
        url_bar.setRadius(5);
        window.draw(url_bar);
        
        Text url_text("crazyos://home", globalFont, 18);
        url_text.setFillColor(Color(150, 180, 220));
        url_text.setPosition(x + 30, y + 65);
        window.draw(url_text);
        
        // GO按钮
        if (buttons.size() > 3) {
            buttons[3].setFillColor(buttons[3].getGlobalBounds().contains(Vector2f(Mouse::getPosition(window))) ? 
                                   BUTTON_HOVER : BUTTON_COLOR);
            window.draw(buttons[3]);
            
            Text go_text("GO", globalFont, 18);
            go_text.setFillColor(TEXT_COLOR);
            go_text.setPosition(buttons[3].getPosition().x + buttons[3].getSize().x/2 - go_text.getLocalBounds().width/2,
                               buttons[3].getPosition().y + buttons[3].getSize().y/2 - go_text.getLocalBounds().height/2);
            window.draw(go_text);
        }
        
        // 内容区域
        RectangleShape content_bg(Vector2f(width - 40, height - 140));
        content_bg.setPosition(x + 20, y + 110);
        content_bg.setFillColor(DOCUMENT_BG);
        content_bg.setRadius(5);
        window.draw(content_bg);
        
        for (int i = 0; i < content.size(); i++) {
            Text content_text(content[i], globalFont, 18);
            content_text.setFillColor(TEXT_COLOR);
            content_text.setPosition(x + 40, y + 130 + i * 35);
            window.draw(content_text);
        }
    }
    
    void draw_settings(RenderWindow& window) {
        // 设置项
        for (int i = 0; i < content.size(); i++) {
            float y_pos = y + 60 + i * 50;
            
            RectangleShape setting(Vector2f(width - 40, 40));
            setting.setPosition(x + 20, y_pos);
            setting.setFillColor(i == selected_setting ? Color(70, 80, 100) : DOCUMENT_BG);
            setting.setRadius(4);
            window.draw(setting);
            
            Text setting_text(content[i], globalFont, 18);
            setting_text.setFillColor(TEXT_COLOR);
            setting_text.setPosition(x + 40, y_pos + 10);
            window.draw(setting_text);
            
            // 设置图标
            if (i == 0) { // 显示设置
                RectangleShape display_icon(Vector2f(30, 30));
                display_icon.setPosition(x + width - 60, y_pos + 5);
                display_icon.setFillColor(Color(100, 180, 220));
                display_icon.setRadius(3);
                window.draw(display_icon);
            }
            else if (i == 5) { // 关于
                CircleShape about_icon(12);
                about_icon.setPosition(x + width - 57, y_pos + 8);
                about_icon.setFillColor(Color(100, 200, 150));
                window.draw(about_icon);
                
                Text info_text("i", globalFont, 16);
                info_text.setFillColor(TEXT_COLOR);
                info_text.setPosition(x + width - 50, y_pos + 12);
                window.draw(info_text);
            }
        }
        
        // 关于信息
        if (show_about) {
            RectangleShape about_bg(Vector2f(width - 100, height - 150));
            about_bg.setPosition(x + 50, y + 100);
            about_bg.setFillColor(Color(40, 45, 55));
            about_bg.setOutlineThickness(2);
            about_bg.setOutlineColor(Color(70, 130, 180));
            about_bg.setRadius(10);
            window.draw(about_bg);
            
            vector<string> about_texts = {
                "CrazyOS v1.0",
                "Windows 11风格操作系统模拟器",
                "©Fanatic Star梦幻星",
                "保留PYOS v1.3.3版权信息",
                "2025, All rights reserved"
            };
            
            for (int i = 0; i < about_texts.size(); i++) {
                Text text(about_texts[i], globalFont, 18);
                text.setFillColor(Color(180, 200, 220));
                text.setPosition(x + 80, y + 130 + i * 35);
                window.draw(text);
            }
        }
    }
    
    void draw_documents(RenderWindow& window) {
        // 文档编辑区域
        RectangleShape editor_bg(Vector2f(width - 40, height - 110));
        editor_bg.setPosition(x + 20, y + 60);
        editor_bg.setFillColor(EDITOR_BG);
        editor_bg.setRadius(5);
        window.draw(editor_bg);
        
        // 绘制文本行
        float line_height = 25;
        int visible_lines = min(static_cast<int>(document_lines.size()), 
                               static_cast<int>((editor_bg.getSize().y - 20) / line_height));
        
        for (int i = 0; i < visible_lines; i++) {
            Text line_text(document_lines[i], globalFont, 16);
            line_text.setFillColor(TEXT_COLOR);
            line_text.setPosition(x + 30, y + 70 + i * line_height);
            window.draw(line_text);
        }
        
        // 绘制光标
        if (editing && cursor_visible && cursor_pos.y < visible_lines) {
            float cursor_x = x + 30;
            if (cursor_pos.x > 0) {
                Text before_cursor(document_lines[cursor_pos.y].substr(0, cursor_pos.x), globalFont, 16);
                cursor_x += before_cursor.getLocalBounds().width;
            }
            
            float cursor_y = y + 70 + cursor_pos.y * line_height;
            
            RectangleShape cursor(Vector2f(2, line_height - 5));
            cursor.setPosition(cursor_x, cursor_y);
            cursor.setFillColor(TEXT_COLOR);
            window.draw(cursor);
        }
        
        // 绘制按钮
        for (int i = 0; i < buttons.size(); i++) {
            if (button_actions[i] == "save_document" || button_actions[i] == "save_as") {
                buttons[i].setFillColor(buttons[i].getGlobalBounds().contains(Vector2f(Mouse::getPosition(window))) ? 
                                      SAVE_HOVER : SAVE_BUTTON);
                window.draw(buttons[i]);
                
                string btn_label = (button_actions[i] == "save_document") ? "保存" : "另存为";
                Text btn_text(btn_label, globalFont, 18);
                btn_text.setFillColor(TEXT_COLOR);
                btn_text.setPosition(buttons[i].getPosition().x + buttons[i].getSize().x/2 - btn_text.getLocalBounds().width/2,
                                   buttons[i].getPosition().y + buttons[i].getSize().y/2 - btn_text.getLocalBounds().height/2);
                window.draw(btn_text);
            }
        }
        
        // 绘制保存状态
        if (save_timer.getElapsedTime().asSeconds() < 3) {
            Text status_text(save_status, globalFont, 14);
            status_text.setFillColor(Color(100, 200, 100));
            status_text.setPosition(x + 30, y + height - 35);
            window.draw(status_text);
        }
        
        // 提示信息
        Text hint_text("当前文件: " + filename + " | 按Ctrl+S保存文档 | 双击开始编辑", globalFont, 14);
        hint_text.setFillColor(Color(150, 180, 220));
        hint_text.setPosition(x + 30, y + height - 60);
        window.draw(hint_text);
    }
    
    bool is_title_bar_hit(Vector2f pos) {
        return pos.x >= x && pos.x <= x + width && pos.y >= y && pos.y <= y + 40;
    }
    
    bool is_inside(Vector2f pos) {
        return pos.x >= x && pos.x <= x + width && pos.y >= y && pos.y <= y + height;
    }
};

// 任务栏类
class Taskbar {
public:
    float height = 50;
    vector<string> app_buttons;
    RectangleShape time_display;
    
    Taskbar() {
        time_display.setSize(Vector2f(100, 30));
        time_display.setPosition(VideoMode::getDesktopMode().width - 120, VideoMode::getDesktopMode().height - height + 10);
        time_display.setFillColor(Color(40, 50, 70));
        time_display.setRadius(5);
    }
    
    void draw(RenderWindow& window) {
        RectangleShape bar(Vector2f(window.getSize().x, height));
        bar.setPosition(0, window.getSize().y - height);
        bar.setFillColor(TASKBAR);
        bar.setOutlineThickness(1);
        bar.setOutlineColor(Color(60, 70, 90));
        window.draw(bar);
        
        // 开始按钮 (Windows 11风格)
        RectangleShape start_button(Vector2f(80, 40));
        start_button.setPosition(10, window.getSize().y - height + 5);
        start_button.setFillColor(BUTTON_COLOR);
        start_button.setRadius(5);
        window.draw(start_button);
        
        Text start_text("开始", globalFont, 18);
        start_text.setFillColor(TEXT_COLOR);
        start_text.setPosition(50 - start_text.getLocalBounds().width/2, window.getSize().y - height + 20);
        window.draw(start_text);
        
        // 应用按钮
        Vector2f mouse_pos = Vector2f(Mouse::getPosition(window));
        for (int i = 0; i < app_buttons.size(); i++) {
            RectangleShape app_button(Vector2f(110, 40));
            app_button.setPosition(100 + i * 120, window.getSize().y - height + 5);
            app_button.setFillColor(app_button.getGlobalBounds().contains(mouse_pos) ? BUTTON_HOVER : BUTTON_COLOR);
            app_button.setRadius(5);
            window.draw(app_button);
            
            Text app_text(app_buttons[i], globalFont, 16);
            app_text.setFillColor(TEXT_COLOR);
            app_text.setPosition(app_button.getPosition().x + app_button.getSize().x/2 - app_text.getLocalBounds().width/2,
                               app_button.getPosition().y + app_button.getSize().y/2 - app_text.getLocalBounds().height/2);
            window.draw(app_text);
        }
        
        // 时间显示
        time_t now = time(0);
        tm* ltm = localtime(&now);
        ostringstream oss;
        oss << setw(2) << setfill('0') << ltm->tm_hour << ":"
            << setw(2) << setfill('0') << ltm->tm_min << ":"
            << setw(2) << setfill('0') << ltm->tm_sec;
        
        window.draw(time_display);
        
        Text time_text(oss.str(), globalFont, 18);
        time_text.setFillColor(TEXT_COLOR);
        time_text.setPosition(time_display.getPosition().x + time_display.getSize().x/2 - time_text.getLocalBounds().width/2,
                             time_display.getPosition().y + time_display.getSize().y/2 - time_text.getLocalBounds().height/2);
        window.draw(time_text);
    }
};

// 绘制Windows 11风格的桌面背景
void draw_windows11_background(RenderWindow& window) {
    // 渐变背景
    RectangleShape background(Vector2f(window.getSize().x, window.getSize().y));
    background.setFillColor(Color(32, 32, 40)); // Windows 11深色模式背景色
    window.draw(background);
    
    // 添加一些装饰性元素
    for (int i = 0; i < 20; i++) {
        float size = 50 + rand() % 100;
        float x = rand() % window.getSize().x;
        float y = rand() % window.getSize().y;
        float alpha = 10 + rand() % 20;
        
        CircleShape circle(size);
        circle.setPosition(x, y);
        circle.setFillColor(Color(60, 70, 100, alpha));
        window.draw(circle);
    }
    
    // 添加一些光点
    for (int i = 0; i < 50; i++) {
        float size = 1 + rand() % 3;
        float x = rand() % window.getSize().x;
        float y = rand() % window.getSize().y;
        
        CircleShape star(size);
        star.setPosition(x, y);
        star.setFillColor(Color(200, 220, 255, 150));
        window.draw(star);
    }
}

int main() {
    // 创建窗口
    RenderWindow window(VideoMode::getDesktopMode(), "CrazyOS v1.0 - Windows 11风格操作系统模拟器", Style::Fullscreen);
    window.setFramerateLimit(60);
    
    // 加载字体
    if (!globalFont.loadFromFile("arial.ttf")) {
        // 如果加载失败，使用默认字体
        cout << "无法加载字体，使用默认字体" << endl;
    }
    
    // 创建桌面图标
    vector<Icon> desktop_icons = {
        Icon(100, 100, "文件管理器", "explorer"),
        Icon(220, 100, "计算器", "calculator"),
        Icon(340, 100, "浏览器", "browser"),
        Icon(100, 220, "文档", "documents"),
        Icon(220, 220, "图片", "images"),
        Icon(340, 220, "系统设置", "settings")
    };
    
    // 创建任务栏
    Taskbar taskbar;
    
    // 窗口列表
    vector<Window> windows;
    int active_window_index = -1;
    Window* active_input_window = nullptr;
    
    // 主循环
    Clock clock;
    while (window.isOpen()) {
        // 事件处理
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
            }
            
            // 键盘事件
            if (event.type == Event::KeyPressed) {
                if (event.key.code == Keyboard::Escape) {
                    window.close();
                }
                else if (event.key.code == Keyboard::F11 && active_window_index >= 0 && 
                         active_window_index < windows.size()) {
                    windows[active_window_index].toggle_maximize();
                }
                
                // 文档输入处理
                if (active_input_window && active_input_window->editing) {
                    // 这里简化处理，实际需要处理各种按键
                    if (event.key.code == Keyboard::Enter) {
                        // 换行
                    }
                    else if (event.key.code == Keyboard::BackSpace) {
                        // 退格
                    }
                    else if (event.key.code == Keyboard::S && event.key.control) {
                        active_input_window->save_document();
                    }
                }
            }
            
            // 鼠标事件
            if (event.type == Event::MouseButtonPressed) {
                Vector2f mouse_pos = Vector2f(Mouse::getPosition(window));
                
                // 桌面图标点击
                bool icon_clicked = false;
                for (Icon& icon : desktop_icons) {
                    if (icon.is_hovered(mouse_pos)) {
                        for (Icon& i : desktop_icons) {
                            i.selected = false;
                        }
                        icon.selected = true;
                        icon_clicked = true;
                        
                        if (event.mouseButton.button == Mouse::Left) {
                            if (icon.last_click_clock.getElapsedTime().asMilliseconds() < 300) {
                                string title;
                                if (icon.app_type == "explorer") title = "文件管理器";
                                else if (icon.app_type == "calculator") title = "计算器";
                                else if (icon.app_type == "browser") title = "浏览器";
                                else if (icon.app_type == "documents") title = "文档编辑器";
                                else if (icon.app_type == "settings") title = "系统设置";
                                else title = icon.label;
                                
                                Window new_window(title, 150 + windows.size() * 20, 
                                                100 + windows.size() * 20,
                                                (icon.app_type == "documents") ? 500 : 400,
                                                (icon.app_type == "documents") ? 500 : 400,
                                                icon.app_type);
                                windows.push_back(new_window);
                                active_window_index = windows.size() - 1;
                                
                                if (find(taskbar.app_buttons.begin(), taskbar.app_buttons.end(), title) == 
                                    taskbar.app_buttons.end()) {
                                    taskbar.app_buttons.push_back(title);
                                }
                            }
                            icon.last_click_clock.restart();
                        }
                        break;
                    }
                }
                
                // 任务栏应用按钮点击
                for (int i = 0; i < taskbar.app_buttons.size(); i++) {
                    RectangleShape btn(Vector2f(110, 40));
                    btn.setPosition(100 + i * 120, window.getSize().y - taskbar.height + 5);
                    if (btn.getGlobalBounds().contains(mouse_pos)) {
                        for (int j = 0; j < windows.size(); j++) {
                            if (windows[j].title == taskbar.app_buttons[i]) {
                                windows[j].restore();
                                active_window_index = j;
                                break;
                            }
                        }
                    }
                }
                
                // 窗口交互
                bool handled = false;
                for (int i = windows.size() - 1; i >= 0; i--) {
                    Window& window_obj = windows[i];
                    if (!window_obj.active) continue;
                    
                    // 按钮点击
                    for (int j = 0; j < window_obj.buttons.size(); j++) {
                        if (window_obj.buttons[j].getGlobalBounds().contains(mouse_pos)) {
                            if (window_obj.button_actions[j] == "close") {
                                auto it = find(taskbar.app_buttons.begin(), taskbar.app_buttons.end(), window_obj.title);
                                if (it != taskbar.app_buttons.end()) {
                                    taskbar.app_buttons.erase(it);
                                }
                                windows.erase(windows.begin() + i);
                                if (active_window_index == i) {
                                    active_window_index = -1;
                                    active_input_window = nullptr;
                                }
                                else if (active_window_index > i) {
                                    active_window_index--;
                                }
                                handled = true;
                                break;
                            }
                            else if (window_obj.button_actions[j] == "maximize") {
                                window_obj.toggle_maximize();
                                handled = true;
                                break;
                            }
                            else if (window_obj.button_actions[j] == "minimize") {
                                window_obj.minimize();
                                handled = true;
                                break;
                            }
                            else if (window_obj.button_actions[j] == "go") {
                                if (window_obj.app_type == "browser") {
                                    window_obj.content = {
                                        "CrazyOS v1.0 浏览器",
                                        "正在加载 crazyos://home...",
                                        "CrazyOS 1.0 更新日志：",
                                        "- 添加Windows 11风格界面",
                                        "- 实现多窗口管理",
                                        "- 优化性能"
                                    };
                                }
                                handled = true;
                                break;
                            }
                            else if (window_obj.button_actions[j] == "save_document") {
                                window_obj.save_document();
                                handled = true;
                                break;
                            }
                            else if (window_obj.button_actions[j] == "save_as") {
                                window_obj.save_as();
                                handled = true;
                                break;
                            }
                        }
                    }
                    if (handled) break;
                    
                    // 标题栏点击
                    if (window_obj.is_title_bar_hit(mouse_pos) && !window_obj.is_maximized) {
                        active_window_index = i;
                        // 将窗口移到最前面
                        Window w = windows[i];
                        windows.erase(windows.begin() + i);
                        windows.push_back(w);
                        active_window_index = windows.size() - 1;
                        
                        window_obj.dragging = true;
                        window_obj.drag_offset_x = mouse_pos.x - window_obj.x;
                        window_obj.drag_offset_y = mouse_pos.y - window_obj.y;
                        handled = true;
                        break;
                    }
                    
                    // 窗口内容交互
                    if (window_obj.is_inside(mouse_pos) && !window_obj.is_title_bar_hit(mouse_pos)) {
                        // 文档编辑器
                        if (window_obj.app_type == "documents" && event.mouseButton.button == Mouse::Left) {
                            if (window_obj.editing) {
                                // 设置光标位置
                                float editor_top = window_obj.y + 70;
                                int click_line = static_cast<int>((mouse_pos.y - editor_top) / 25);
                                if (click_line >= 0 && click_line < window_obj.document_lines.size()) {
                                    window_obj.cursor_pos.y = click_line;
                                    window_obj.cursor_visible = true;
                                    window_obj.cursor_timer.restart();
                                }
                            }
                            else {
                                if (window_obj.last_click_clock.getElapsedTime().asMilliseconds() < 300) {
                                    window_obj.editing = true;
                                    window_obj.cursor_visible = true;
                                    window_obj.cursor_timer.restart();
                                    active_input_window = &window_obj;
                                }
                                window_obj.last_click_clock.restart();
                            }
                            handled = true;
                        }
                        
                        // 计算器
                        else if (window_obj.app_type == "calculator") {
                            float button_size = 50;
                            for (int i = 0; i < 4; i++) {
                                for (int j = 0; j < 4; j++) {
                                    int idx = i * 4 + j;
                                    if (idx < window_obj.content.size()) {
                                        float btn_x = window_obj.x + 30 + j * (button_size + 10);
                                        float btn_y = window_obj.y + 130 + i * (button_size + 10);
                                        RectangleShape btn(Vector2f(button_size, button_size));
                                        btn.setPosition(btn_x, btn_y);
                                        if (btn.getGlobalBounds().contains(mouse_pos)) {
                                            window_obj.handle_calculator_click(window_obj.content[idx]);
                                            handled = true;
                                            break;
                                        }
                                    }
                                }
                                if (handled) break;
                            }
                        }
                        
                        if (handled) break;
                    }
                }
                
                // 取消选择图标
                if (!handled && !icon_clicked) {
                    for (Icon& icon : desktop_icons) {
                        icon.selected = false;
                    }
                    
                    // 点击空白处取消文档编辑状态
                    if (active_input_window) {
                        active_input_window->editing = false;
                        active_input_window = nullptr;
                    }
                }
            }
            else if (event.type == Event::MouseButtonReleased) {
                for (Window& window_obj : windows) {
                    window_obj.dragging = false;
                }
            }
        }
        
        // 窗口拖动
        if (active_window_index >= 0 && active_window_index < windows.size()) {
            Window& window_obj = windows[active_window_index];
            if (window_obj.dragging && !window_obj.is_maximized && window_obj.active) {
                Vector2f mouse_pos = Vector2f(Mouse::getPosition(window));
                window_obj.x = mouse_pos.x - window_obj.drag_offset_x;
                window_obj.y = mouse_pos.y - window_obj.drag_offset_y;
                window_obj.y = max(0.0f, window_obj.y);
                window_obj.update_button_positions();
            }
        }
        
        // 更新光标状态
        for (Window& window_obj : windows) {
            if (window_obj.app_type == "documents" && window_obj.editing) {
                window_obj.update_cursor();
            }
        }
        
        // 绘制
        window.clear();
        
        // 绘制Windows 11风格的桌面背景
        draw_windows11_background(window);
        
        // 绘制桌面图标
        for (Icon& icon : desktop_icons) {
            icon.draw(window);
        }
        
        // 绘制窗口
        for (Window& window_obj : windows) {
            if (window_obj.active) {
                window_obj.draw(window);
            }
        }
        
        // 绘制任务栏
        taskbar.draw(window);
        
        // 绘制系统信息
        time_t now = time(0);
        tm* ltm = localtime(&now);
        ostringstream date_oss;
        date_oss << setw(4) << 1900 + ltm->tm_year << "-"
                 << setw(2) << setfill('0') << 1 + ltm->tm_mon << "-"
                 << setw(2) << setfill('0') << ltm->tm_mday;
        
        Text date_text(date_oss.str(), globalFont, 18);
        date_text.setFillColor(Color(150, 180, 200));
        date_text.setPosition(window.getSize().x - date_text.getLocalBounds().width - 125, 
                            window.getSize().y - 38);
        window.draw(date_text);
        
        // 绘制鼠标指针
        Vector2f mouse_pos = Vector2f(Mouse::getPosition(window));
        CircleShape cursor(5);
        cursor.setPosition(mouse_pos);
        cursor.setFillColor(Color(200, 220, 240));
        cursor.setOutlineColor(Color(100, 150, 200));
        cursor.setOutlineThickness(1);
        window.draw(cursor);
        
        window.display();
    }
    
    return 0;
}