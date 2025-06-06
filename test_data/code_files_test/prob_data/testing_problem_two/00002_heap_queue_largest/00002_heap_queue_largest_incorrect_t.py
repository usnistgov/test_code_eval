import heapq as hq
from typing import Union
def heap_queue_largest(nums: list[Union[int, float]], n: int) -> list[Union[int, float]]:
  largest_nums = hq.nlargest(n, nums)
  return largest_nums
