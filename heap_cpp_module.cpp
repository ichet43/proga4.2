// heap_cpp_module.cpp
#include <vector>
#include <algorithm>
#include <stdexcept>

extern "C" {
    struct HeapStruct {
        std::vector<int>* data;
    };
    
    HeapStruct* create_heap() {
        HeapStruct* heap = new HeapStruct();
        heap->data = new std::vector<int>();
        return heap;
    }
    
    void destroy_heap(HeapStruct* heap) {
        delete heap->data;
        delete heap;
    }
    
    int heap_size(HeapStruct* heap) {
        return heap->data->size();
    }
    
    bool heap_is_empty(HeapStruct* heap) {
        return heap->data->empty();
    }
    
    int heap_top(HeapStruct* heap) {
        if (heap->data->empty()) {
            throw std::runtime_error("Куча пуста");
        }
        return (*heap->data)[0];
    }
    
    void heap_push(HeapStruct* heap, int value) {
        heap->data->push_back(value);
        std::push_heap(heap->data->begin(), heap->data->end());
    }
    
    int heap_pop(HeapStruct* heap) {
        if (heap->data->empty()) {
            throw std::runtime_error("Куча пуста");
        }
        std::pop_heap(heap->data->begin(), heap->data->end());
        int result = heap->data->back();
        heap->data->pop_back();
        return result;
    }
    
    bool heap_remove_at(HeapStruct* heap, int index) {
        if (index < 0 || index >= heap->data->size()) {
            return false;
        }
        heap->data->erase(heap->data->begin() + index);
        std::make_heap(heap->data->begin(), heap->data->end());
        return true;
    }
    
    int* heap_get_all(HeapStruct* heap, int* size) {
        *size = heap->data->size();
        if (*size == 0) return nullptr;
        int* arr = new int[*size];
        std::copy(heap->data->begin(), heap->data->end(), arr);
        return arr;
    }
    
    void free_array(int* arr) {
        delete[] arr;
    }
}