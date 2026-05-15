# heap_visualizer.py
import tkinter as tk
from tkinter import ttk, messagebox
import math
from heap_python_module import PythonHeap
from heap_cpp_wrapper import CppHeapWrapper

class HeapVisualizer:
    """Основной класс визуализации кучи"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Визуализатор структуры данных: Куча (Heap)")
        self.root.geometry("900x650")
        
        # Выбор реализации
        self.heap = PythonHeap()  # По умолчанию Python модуль
        self.current_module = "Python"
        
        # Цветовая схема
        self.colors = {
            'bg': '#2b2b2b',
            'node': '#4a90d9',
            'node_hover': '#357abd',
            'text': '#ffffff',
            'line': '#888888',
            'button_bg': '#3c3f41',
            'button_fg': '#ffffff',
            'input_bg': '#3c3f41',
            'input_fg': '#ffffff',
            'label_bg': '#3c3f41',
            'label_fg': '#ffffff',
            'error': '#cc5555',
            'success': '#55cc55',
            'menu_bg': '#2d2d2d',
            'frame_bg': '#323232'
        }
        
        self.setup_ui()
        self.draw_heap()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.root.configure(bg=self.colors['bg'])
        
        # Основной контейнер
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель с управлением
        left_panel = tk.Frame(main_container, width=250, bg=self.colors['frame_bg'], 
                             relief=tk.RAISED, bd=1)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Правая панель с визуализацией
        right_panel = tk.Frame(main_container, bg=self.colors['bg'])
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Заголовок левой панели
        header_frame = tk.Frame(left_panel, bg=self.colors['menu_bg'])
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        label = tk.Label(header_frame, text="Управление кучей", 
                         font=('Arial', 14, 'bold'),
                         bg=self.colors['menu_bg'], fg=self.colors['text'])
        label.pack(pady=10)
        
        # Выбор модуля
        module_frame = tk.Frame(left_panel, bg=self.colors['frame_bg'])
        module_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(module_frame, text="Модуль:", 
                bg=self.colors['frame_bg'], fg=self.colors['label_fg']).pack(side=tk.LEFT, padx=5)
        
        self.module_var = tk.StringVar(value="Python")
        module_combo = ttk.Combobox(module_frame, textvariable=self.module_var, 
                                    values=["Python", "C++"], state="readonly", width=10)
        module_combo.pack(side=tk.RIGHT, padx=5, pady=5)
        module_combo.bind('<<ComboboxSelected>>', self.on_module_change)
        
        # Операции с кучей
        operations_frame = tk.Frame(left_panel, bg=self.colors['frame_bg'])
        operations_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(operations_frame, text="Операции:", 
                font=('Arial', 11, 'bold'),
                bg=self.colors['frame_bg'], fg=self.colors['label_fg']).pack(pady=5)
        
        # Кнопка добавления элемента
        add_frame = tk.Frame(operations_frame, bg=self.colors['frame_bg'])
        add_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(add_frame, text="Значение:", 
                bg=self.colors['frame_bg'], fg=self.colors['label_fg']).pack(side=tk.LEFT, padx=5)
        
        self.entry_value = tk.Entry(add_frame, bg=self.colors['input_bg'], 
                                    fg=self.colors['input_fg'], width=10)
        self.entry_value.pack(side=tk.RIGHT, padx=5)
        
        button_add = tk.Button(operations_frame, text="Добавить элемент", 
                              command=self.push_element,
                              bg=self.colors['button_bg'], 
                              fg=self.colors['button_fg'],
                              relief=tk.FLAT, pady=5)
        button_add.pack(fill=tk.X, padx=10, pady=5)
        
        # Кнопка удаления корня
        button_pop = tk.Button(operations_frame, text="Удалить корень", 
                              command=self.pop_element,
                              bg=self.colors['button_bg'], 
                              fg=self.colors['button_fg'],
                              relief=tk.FLAT, pady=5)
        button_pop.pack(fill=tk.X, padx=10, pady=5)
        
        # Удаление по индексу
        remove_frame = tk.Frame(operations_frame, bg=self.colors['frame_bg'])
        remove_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(remove_frame, text="Индекс:", 
                bg=self.colors['frame_bg'], fg=self.colors['label_fg']).pack(side=tk.LEFT, padx=5)
        
        self.entry_index = tk.Entry(remove_frame, bg=self.colors['input_bg'], 
                                    fg=self.colors['input_fg'], width=10)
        self.entry_index.pack(side=tk.RIGHT, padx=5)
        
        button_remove = tk.Button(operations_frame, text="Удалить по индексу", 
                                 command=self.remove_at_index,
                                 bg=self.colors['button_bg'], 
                                 fg=self.colors['button_fg'],
                                 relief=tk.FLAT, pady=5)
        button_remove.pack(fill=tk.X, padx=10, pady=5)
        
        # Разделитель
        separator = ttk.Separator(operations_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=10)
        
        # Кнопка очистки
        button_clear = tk.Button(operations_frame, text="Очистить кучу", 
                                command=self.clear_heap,
                                bg='#cc5555', 
                                fg=self.colors['text'],
                                relief=tk.FLAT, pady=5)
        button_clear.pack(fill=tk.X, padx=10, pady=5)
        
        # Информация о куче
        info_frame = tk.Frame(left_panel, bg=self.colors['frame_bg'])
        info_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(info_frame, text="Информация:", 
                font=('Arial', 11, 'bold'),
                bg=self.colors['frame_bg'], fg=self.colors['label_fg']).pack(pady=5)
        
        self.info_text = tk.Text(info_frame, height=6, width=30,
                                 bg=self.colors['input_bg'], 
                                 fg=self.colors['text'],
                                 relief=tk.FLAT, wrap=tk.WORD)
        self.info_text.pack(fill=tk.X, padx=10, pady=5)
        
        # Canvas для визуализации
        canvas_frame = tk.Frame(right_panel, bg=self.colors['bg'])
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок визуализации
        viz_label = tk.Label(canvas_frame, text="Визуализация кучи (Max-Heap)", 
                           font=('Arial', 14, 'bold'),
                           bg=self.colors['bg'], fg=self.colors['text'])
        viz_label.pack(pady=10)
        
        # Canvas с поддержкой скроллинга
        self.canvas = tk.Canvas(canvas_frame, bg=self.colors['bg'], 
                               highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Состояние
        self.update_info()
    
    def on_module_change(self, event=None):
        """Смена модуля реализации"""
        selected = self.module_var.get()
        
        if selected == self.current_module:
            return
        
        elements = []
        if hasattr(self.heap, 'get_all_elements'):
            elements = self.heap.get_all_elements()
        
        if selected == "Python":
            try:
                self.heap = PythonHeap()
                self.current_module = "Python"
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить Python модуль: {e}")
                self.module_var.set(self.current_module)
                return
        else:
            try:
                self.heap = CppHeapWrapper()
                self.current_module = "C++"
                
                # Проверяем, загрузился ли C++ модуль
                if hasattr(self.heap, '_python_heap') and self.heap._python_heap:
                    messagebox.showwarning("Предупреждение", 
                                         "C++ модуль не найден. Скомпилируйте heap_cpp_module.cpp")
                    self.heap = PythonHeap()
                    self.current_module = "Python"
                    self.module_var.set("Python")
                    return
                    
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить C++ модуль: {e}")
                self.module_var.set(self.current_module)
                return
        
        # Восстановление элементов
        for elem in elements:
            self.heap.push(elem)
        
        self.draw_heap()
        self.update_info()
        messagebox.showinfo("Успех", f"Модуль переключен на {selected}")
    
    def push_element(self):
        """Добавление элемента в кучу"""
        try:
            value = self.entry_value.get().strip()
            if not value:
                messagebox.showwarning("Предупреждение", "Введите значение")
                return
            
            value = int(value)
            self.heap.push(value)
            
            self.entry_value.delete(0, tk.END)
            self.draw_heap()
            self.update_info()
            self.show_message(f"Элемент {value} добавлен в кучу", "success")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное целое число")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить элемент: {e}")
    
    def pop_element(self):
        """Удаление корневого элемента"""
        try:
            if self.heap.is_empty():
                messagebox.showwarning("Предупреждение", "Куча пуста. Нечего удалять.")
                return
            
            value = self.heap.pop()
            self.draw_heap()
            self.update_info()
            self.show_message(f"Удален корневой элемент: {value}", "success")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении корня: {e}")
    
    def remove_at_index(self):
        """Удаление элемента по индексу"""
        try:
            index = self.entry_index.get().strip()
            if not index:
                messagebox.showwarning("Предупреждение", "Введите индекс элемента")
                return
            
            index = int(index)
            
            if self.heap.is_empty():
                messagebox.showwarning("Предупреждение", "Куча пуста")
                return
            
            if index < 0 or index >= self.heap.size():
                messagebox.showerror("Ошибка", 
                                   f"Неверный индекс. Допустимый диапазон: 0-{self.heap.size() - 1}")
                return
            
            if self.heap.remove_at(index):
                self.entry_index.delete(0, tk.END)
                self.draw_heap()
                self.update_info()
                self.show_message(f"Элемент с индексом {index} удален", "success")
            else:
                messagebox.showerror("Ошибка", "Не удалось удалить элемент")
                
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный целочисленный индекс")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении: {e}")
    
    def clear_heap(self):
        """Очистка кучи"""
        if self.heap.size() > 0:
            # Python heap можно пересоздать
            if self.current_module == "Python":
                self.heap = PythonHeap()
            else:
                while not self.heap.is_empty():
                    try:
                        self.heap.pop()
                    except:
                        break
            
            self.draw_heap()
            self.update_info()
            self.show_message("Куча очищена", "success")
    
    def draw_heap(self):
        """Отрисовка кучи"""
        self.canvas.delete("all")
        
        elements = self.heap.get_all_elements()
        if not elements:
            self.canvas.create_text(400, 200, text="Куча пуста", 
                                  font=('Arial', 16), fill='#888888')
            return
        
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()
        
        if canvas_width <= 1:
            canvas_width = 800
        if canvas_height <= 1:
            canvas_height = 500
        
        # Расчет уровней дерева
        num_elements = len(elements)
        levels = math.ceil(math.log2(num_elements + 1))
        
        # Параметры отрисовки
        node_radius = 25
        vertical_spacing = 80
        horizontal_spacing = canvas_width // 4
        
        # Отрисовка узлов и связей
        positions = {}
        
        for level in range(levels):
            nodes_in_level = min(2 ** level, num_elements - (2 ** level - 1))
            start_x = (canvas_width - (nodes_in_level - 1) * horizontal_spacing) // 2
            
            for pos in range(nodes_in_level):
                array_index = (2 ** level - 1) + pos
                if array_index >= num_elements:
                    break
                
                x = start_x + pos * horizontal_spacing
                y = 50 + level * vertical_spacing
                
                # Рисуем связь с родителем
                if array_index > 0:
                    parent_index = (array_index - 1) // 2
                    if parent_index in positions:
                        parent_x, parent_y = positions[parent_index]
                        self.canvas.create_line(parent_x, parent_y + node_radius, 
                                              x, y - node_radius,
                                              fill=self.colors['line'], width=2)
                
                # Рисуем узел
                value = elements[array_index]
                self.canvas.create_oval(x - node_radius, y - node_radius,
                                      x + node_radius, y + node_radius,
                                      fill=self.colors['node'],
                                      outline=self.colors['node_hover'],
                                      width=2)
                
                # Текст значения
                self.canvas.create_text(x, y, text=str(value),
                                      fill=self.colors['text'],
                                      font=('Arial', 12, 'bold'))
                
                # Индекс
                self.canvas.create_text(x, y + node_radius + 10,
                                      text=f"[{array_index}]",
                                      fill='#aaaaaa',
                                      font=('Arial', 8))
                
                positions[array_index] = (x, y)
    
    def update_info(self):
        """Обновление информационной панели"""
        self.info_text.delete(1.0, tk.END)
        
        info = f"Модуль: {self.current_module}\n"
        info += f"Тип кучи: Max-Heap\n"
        info += f"Размер: {self.heap.size()}\n"
        info += f"Пустая: {'Да' if self.heap.is_empty() else 'Нет'}\n"
        
        if not self.heap.is_empty():
            elements = self.heap.get_all_elements()
            info += f"Корень: {elements[0] if elements else 'N/A'}\n"
            info += f"Элементы: {elements[:5]}{'...' if len(elements) > 5 else ''}\n"
        
        self.info_text.insert(1.0, info)
    
    def show_message(self, message, msg_type="info"):
        """Показать временное сообщение"""
        color = self.colors['success'] if msg_type == "success" else self.colors['error']
        
        # Создаем временную метку для сообщения
        msg_label = tk.Label(self.root, text=message, 
                            bg=color, fg=self.colors['text'],
                            font=('Arial', 10), padx=20, pady=5)
        msg_label.place(relx=0.5, rely=0.95, anchor='s')
        
        # Удаляем через 2 секунды
        self.root.after(2000, msg_label.destroy)

def main():
    """Главная функция"""
    root = tk.Tk()
    app = HeapVisualizer(root)
    
    # Обработка закрытия окна
    def on_closing():
        if messagebox.askokcancel("Выход", "Вы действительно хотите выйти?"):
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()
