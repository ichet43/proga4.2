# heap_python_module.py
import heapq
from typing import List

class PythonHeap:
    """Реализация кучи на Python с использованием heapq"""
    
    def __init__(self):
        self._heap: List[int] = []
        self._max_heap: List[int] = []  # Для имитации max-heap
    
    def push(self, value: int) -> None:
        """Добавление элемента в кучу"""
        heapq.heappush(self._max_heap, -value)
        self._heap.append(value)
    
    def pop(self) -> int:
        """Удаление и возврат корневого элемента"""
        if not self._max_heap:
            raise IndexError("Куча пуста")
        
        max_val = -heapq.heappop(self._max_heap)
        
        if max_val in self._heap:
            self._heap.remove(max_val)
        
        return max_val
    
    def top(self) -> int:
        """Получение корневого элемента без удаления"""
        if not self._max_heap:
            raise IndexError("Куча пуста")
        return -self._max_heap[0]
    
    def size(self) -> int:
        """Размер кучи"""
        return len(self._max_heap)
    
    def is_empty(self) -> bool:
        """Проверка на пустоту"""
        return len(self._max_heap) == 0
    
    def remove_at(self, index: int) -> bool:
        """Удаление элемента по индексу"""
        if index < 0 or index >= len(self._heap):
            return False
        
        value_to_remove = self._heap[index]
        self._heap.pop(index)
        self._max_heap.remove(-value_to_remove)
        heapq.heapify(self._max_heap)
        
        return True
    
    def get_all_elements(self) -> List[int]:
        """Получение всех элементов кучи"""
        return [-x for x in self._max_heap]
    
    def clear(self) -> None:
        """Очистка кучи"""
        self._heap.clear()
        self._max_heap.clear()