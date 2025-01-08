#Konstantinos Kitsios, AM 4388
# How to execute:
# python3 top_k.py <K> where K is the number of top-k objects you want to print
#There's some error in the code, some sequences are not being read properly, so the output is not always correct.
import sys

RND_FILE = 'rnd.txt'
SEQ1_FILE = 'seq1.txt'
SEQ2_FILE = 'seq2.txt'


class MinHeap:
    def __init__(self):
        self.heap = []
    
    def insert(self, score, ID):
        self.heap.append((score, ID))
        self._bubble_up(len(self.heap) - 1)
    
    def extract_min(self):
        if not self.heap:
            return None
        
        min_item = self.heap[0]
        last_item = self.heap.pop()
        
        if self.heap:
            self.heap[0] = last_item
            self._sink_down(0)
        
        return min_item
    
    def _bubble_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[parent_index][0] > self.heap[index][0]:
                self.heap[parent_index], self.heap[index] = self.heap[index], self.heap[parent_index]
                index = parent_index
            else:
                break
    
    def _sink_down(self, index):
        while True:
            left_child_index = (index * 2) + 1
            right_child_index = (index * 2) + 2
            smallest = index
            
            if left_child_index < len(self.heap) and self.heap[left_child_index][0] < self.heap[smallest][0]:
                smallest = left_child_index
            
            if right_child_index < len(self.heap) and self.heap[right_child_index][0] < self.heap[smallest][0]:
                smallest = right_child_index
            
            if smallest != index:
                self.heap[smallest], self.heap[index] = self.heap[index], self.heap[smallest]
                index = smallest
            else:
                break


def update_threshold(last_scores):
    threshold = last_scores["seq_1"] + last_scores["seq_2"] + 5.0
    return threshold


def update_lower_bound(ID, score, source, lower_bounds, seen, last_scores, R):
    if ID not in seen:
        lower_bounds[ID] = score + R[ID]
    else:
        lower_bounds[ID] += score
    seen[ID] = True
    last_scores[source] = score
    threshold = update_threshold(last_scores)
    return lower_bounds, seen, last_scores, threshold


def update_Wk(ID, lower_bounds, K, Wk):
    if len(Wk.heap) < K:
        Wk.insert(lower_bounds[ID], ID)
    elif lower_bounds[ID] > Wk.heap[0][0]:
        Wk.extract_min()
        Wk.insert(lower_bounds[ID], ID)
    return Wk


def get_upper_bound(ID, source, last_scores, lower_bounds):
    if source == SEQ1_FILE:
        return lower_bounds[ID] + last_scores["seq_1"]
    elif source == SEQ2_FILE:
        return lower_bounds[ID] + last_scores["seq_2"]


def check_termination(Wk, K, threshold, lower_bounds, seen, last_scores):
    if threshold < Wk.heap[0][0]:
        for ID in lower_bounds.keys():
            if ID not in seen and ID not in [item[1] for item in Wk.heap]:
                return False
        return True
    return False





def main():
    
    K = int(sys.argv[1])
    accesses = 0
    R = {}
    
    with open(RND_FILE, 'r') as file:
        for line in file:
            ID, score = line.split()
            ID = int(ID)
            score = float(score)
            R[ID] = score


    Wk = MinHeap()
    seen = {}
    lower_bounds = {}
    last_scores = {"seq_1": 0.0, "seq_2": 0.0}
    threshold = -1

    with open(SEQ1_FILE, 'r') as file1, open(SEQ2_FILE, 'r') as file2:
        while True:
            line1 = file1.readline()
            line2 = file2.readline()
            if not line1 and not line2:
                break
            if line1:
                accesses += 1
                ID, score = line1.split()
                ID = int(ID)
                score = float(score)
                lower_bounds, seen, last_scores, threshold = update_lower_bound(ID, score, "seq_1", lower_bounds, seen, last_scores, R)
                Wk = update_Wk(ID, lower_bounds, K, Wk)
                if check_termination(Wk, K, threshold, lower_bounds, seen, last_scores):
                    break
            if line2:
                accesses += 1
                ID, score = line2.split()
                ID = int(ID)
                score = float(score)
                lower_bounds, seen, last_scores, threshold = update_lower_bound(ID, score, "seq_2", lower_bounds, seen, last_scores, R)
                Wk = update_Wk(ID, lower_bounds, K, Wk)
                if check_termination(Wk, K, threshold, lower_bounds, seen, last_scores):
                    break
    print("Number of sequential accesses:", accesses)
    Wk.heap.sort(reverse=True)
    print("Top-k objects:")
    for score, ID in Wk.heap:
        print(f"{ID} {score:.2f}")


if __name__ == '__main__':
    main()
