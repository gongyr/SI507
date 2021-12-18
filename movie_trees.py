import csv, json
from btree import BTree 
    
class MovieTrees(BTree):

    def __init__(self, split_threshold, csv_filename, col_name): 
        super().__init__(split_threshold)
        self.col_name = col_name 
        with open(csv_filename) as file: 
            rows = list(csv.reader(file))
            header = rows[0]
            rows = rows[1:]
            col_index = header.index(col_name) 
            for row in rows: 
                self.add(float(row[col_index]), row)

                
    def _range_query(self, range_start, range_end, current_node, min_key, max_key):
        if range_start > max_key or range_end < min_key:
            return []
        results = []
        for i, key in enumerate(current_node.keys):
            if range_start <= key and key <= range_end:
                results.append(current_node.values[i])
        
        if not current_node.is_leaf(): 
            for i, child in enumerate(current_node.children):
                new_min_key = min_key if i == 0 else current_node.keys[i - 1] 
                new_max_key = max_key if i == len(current_node) else current_node.keys[i]
                results += self._range_query(range_start, range_end, child, new_min_key, new_max_key)
        return results
    def range_query(self, range_start, range_end):
        return self._range_query(range_start, range_end, self.root, float('-inf'), float('inf')) 

            