import sys
from math import log2

class Cache():
    def __init__(self, num_lines, depth):
        self.SRAM = [[0 for j in range(depth)] for i in range(num_lines)]
        self.tag = [0 for i in range(num_lines)]
        self.valid = [False for i in range(num_lines)]
        self.depth = depth
        self.num_lines = num_lines
        self.load_miss_count = 0
        self.store_miss_count = 0

def parse_address(address, cache):
    offset = address % cache.depth
    address /= cache.depth
    index = address % cache.num_lines
    address /= cache.num_lines
    tag = address % 2 ** (32 - log2(cache.depth) - log2(cache.num_lines))
    return int(tag), int(index), int(offset)

def mem_to_cache(cache, a, index, tag):
    a_index = ( (tag * cache.num_lines) + index ) * cache.depth
    cache.SRAM[index] = a[a_index : a_index + cache.depth]
    cache.valid[index] = True
    cache.tag[index] = tag

def cache_to_mem(cache, a, index, tag):
    a_index = ( (tag * cache.num_lines) + index ) * cache.depth
    a[a_index : a_index + cache.depth] = cache.SRAM[index]

def get_data(cache, a, address):
    tag, index, offset = parse_address(address, cache)

    # Case 1: Data is present in cache
    if cache.valid[index] and cache.tag[index] == tag:
        return cache.SRAM[index][offset]

    # Case 2: Compulsory miss
    elif not cache.valid[index]:
        mem_to_cache(cache, a, index, tag)
        return cache.SRAM[index][offset]

    # Case 3: Conflict miss
    else:
        cache.load_miss_count += 1
        mem_to_cache(cache, a, index, tag)
        return cache.SRAM[index][offset]

def store_data(data, cache, a, address):
    '''
    A write-through write-allocate scheme is used. 
    '''
    tag, index, offset = parse_address(address, cache)

    # Case 1: Data is present in cache
    if cache.valid[index] and cache.tag[index] == tag:
        cache.SRAM[index][offset] = data
        cache_to_mem(cache, a, index, tag)

    # Case 2: Compulsory miss
    elif not cache.valid[index]:
        mem_to_cache(cache, a, index, tag)
        cache.SRAM[index][offset] = data
        cache_to_mem(cache, a, index, tag)

    # Case 3: Conflict miss
    else:
        cache.store_miss_count += 1
        mem_to_cache(cache, a, index, tag)
        cache.SRAM[index][offset] = data
        cache_to_mem(cache, a, index, tag)

def get_index(i, j, N):
    return (i * N) + j

def main():
    ''' 
    This program expects a command line argument to specify the value of N.
    For example, to set N=100, run `python cache.py 100`
    '''
    try:
        N = int(sys.argv[1])
    except:
        print("A valid argument for N was not specified. Using N=64.")
        N = 64
    a = [i for i in range(N**2)]

    # Compute expected array output
    a_expected = a.copy()
    for i in range(8):
        for j in range(N):
            a_expected[get_index(i, j, N)] = 5 + a_expected[get_index(j, i, N)]

    # Cache: 256 64-byte (16 int) cache lines
    # Run the program using a cacheing system
    cache = Cache(256, 16)
    a_actual = a.copy()
    for i in range(8):
        for j in range(N):
            data = 5 + get_data(cache, a_actual, get_index(j, i, N))
            store_data(data, cache, a_actual, get_index(i, j, N))

    # Log
    print("Store Conflict Misses: " + str(cache.store_miss_count))
    print("Load Conflict Misses: " + str(cache.load_miss_count))

    # Test
    fail = False
    for i in range(N**2):
        if a_expected[i] != a_actual[i]:
            print("FAIL: Arrays not equal at index " + str(i) + ": ", a_expected[i], a_actual[i])
            fail = True
    if not fail:
        print("PASS! Arrays are equal")

if __name__=="__main__":
    main()