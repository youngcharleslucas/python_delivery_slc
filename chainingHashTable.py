class ChainingHashTable:
    def __init__(self, capacity = 10):
        self.table =  [] 
        for i in range(capacity):
            self.table.append([])
    
    def insert(self, key, item): # does both insert and update 
        # get the bucket list where this item will go 
        bucket = hash(key) % len(self.table) 
        bucket_list = self.table[bucket] 
        
        # update key if it is already in the bucket
        for keyValue in bucket_list:
            if keyValue[0] == key:
                keyValue = item 
                return True
                
        # if does not exist, insert to end of bucket list 
        keyValue = [key, item]
        bucket_list.append(keyValue)
        return True
        
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        
        # search for the key in the bucket list
        for keyValue in bucket_list:
            if keyValue[0] == key:
                return keyValue[1]
        return None
            
    def remove(self, key): 
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]  
        
        for keyValue in bucket_list:
            if keyValue[0] == key:
                bucket_list.remove([keyValue[0], keyValue[1]])
                
    def toArray(self):
        array = []
        iteration = 1
        for i in range(0, len(self.table)):
            for j in range(0, len(self.table[i])):
                package = self.search(iteration)
                array.append(package)
                iteration += 1
        return array