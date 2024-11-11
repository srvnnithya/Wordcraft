from collections import deque

def get_neighbors(word, word_list):
    neighbors = []
    for i in range(len(word)):
        for char in 'abcdefghijklmnopqrstuvwxyz':
            new_word = word[:i] + char + word[i+1:]
            if new_word != word and new_word in word_list:
                neighbors.append(new_word)
    return neighbors

def bfs(start_word, end_word, word_list):
    if start_word == end_word:
        return [start_word]
    
    queue = deque([(start_word, [start_word])])
    visited = set([start_word])
    
    while queue:
        current_word, path = queue.popleft()
        
        for neighbor in get_neighbors(current_word, word_list):
            if neighbor == end_word:
                return path + [neighbor]
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return None

def find_shortest_ladder(start_word, end_word, word_list):
    return bfs(start_word, end_word, word_list)
