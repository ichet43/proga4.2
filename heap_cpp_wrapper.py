# heap_cpp_wrapper.py
import ctypes
import os
import platform
from typing import List

class CppHeapWrapper:
    """Обертка для C++ модуля через ctypes"""
    
    def __init__(self):
        self._lib = None
        self._heap = None
        self._python_heap = False
        self._load_library()
    
    def _load_library(self):
        """Загрузка C++ библиотеки"""
        system = platform.system()
        
        if system == 'Windows':
            lib_name = 'heap_cpp_module.dll'
        elif system == 'Darwin':
            lib_name = 'libheap_cpp_module.dylib'
        else:
            lib_name = 'libheap_cpp_module.so'
        
        try:
            lib_path = os.path.join(os.path.dirname(__file__), lib_name)
            
            if not os.path.exists(lib_path):
                print(f"Библиотека {lib_name} не найдена. Будет использоваться Python реализация.")
                self._python_heap = True
                return
            
            self._lib = ctypes.CDLL(lib_path)
            self._python_heap = False
            
            # Определение типов возвращаемых значений
            self._lib.create_heap.restype = ctypes.c_void_p
            self._lib.heap_size.restype = ctypes.c_int
            self._lib.heap_is_empty.restype = ctypes.c_bool
            self._lib.heap_top.restype = ctypes.c_int
            self._lib.heap_pop.restype = ctypes.c_int
            self._lib.heap_remove_at.restype = ctypes.c_bool
            self._lib.heap_get_all.restype = ctypes.POINTER(ctypes.c_int)
            
            # Создаем кучу
            self._heap = self._lib.create_heap()
            
        except Exception as e:
            print(f"Ошибка загрузки C++ библиотеки: {e}. Будет использоваться Python реализация.")
            self._python_heap = True
            self._lib = None
    
    def push(self, value: int) -> None:
        """Добавление элемента"""
        if self._lib and not self._python_heap:
            self._lib.heap_push(ctypes.c_void_p(self._heap), ctypes.c_int(value))
        else:
            raise RuntimeError("C++ модуль не загружен")
    
    def pop(self) -> int:
        """Удаление корневого элемента"""
        if self._lib and not self._python_heap:
            if self.is_empty():
                raise IndexError("Куча пуста")
            return self._lib.heap_pop(ctypes.c_void_p(self._heap))
        else:
            raise RuntimeError("C++ модуль не загружен")
    
    def top(self) -> int:
        """Получение корневого элемента"""
        if self._lib and not self._python_heap:
            if self.is_empty():
                raise IndexError("Куча пуста")
            return self._lib.heap_top(ctypes.c_void_p(self._heap))
        else:
            raise RuntimeError("C++ модуль не загружен")
    
    def size(self) -> int:
        """Размер кучи"""
        if self._lib and not self._python_heap:
            return self._lib.heap_size(ctypes.c_void_p(self._heap))
        return 0
    
    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        if self._lib and not self._python_heap:
            return self._lib.heap_is_empty(ctypes.c_void_p(self._heap))
        return True
    
    def remove_at(self, index: int) -> bool:
        """Удаление элемента по индексу"""
        if self._lib and not self._python_heap:
            return self._lib.heap_remove_at(ctypes.c_void_p(self._heap), ctypes.c_int(index))
        return False
    
    def get_all_elements(self) -> List[int]:
        """Получение всех элементов"""
        if self._lib and not self._python_heap:
            size = ctypes.c_int()
            arr_ptr = self._lib.heap_get_all(ctypes.c_void_p(self._heap), ctypes.byref(size))
            
            if arr_ptr and size.value > 0:
                result = [arr_ptr[i] for i in range(size.value)]
                self._lib.free_array(arr_ptr)
                return result
        return []
    
    def __del__(self):
        """Деструктор для освобождения C++ памяти"""
        if self._lib and self._heap:
            self._lib.destroy_heap(ctypes.c_void_p(self._heap))