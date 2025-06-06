import heapq as hq
def heap_queue_largest(nums,n):
  largest_nums = hq.nlargest(n, nums[1:])
  return largest_nums
