from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # { Number:Position }
        seen = {}
        for i, x in enumerate(nums):
            if seen and target - x in seen:
                return [i, seen[target - x]]
            else:
                seen[x] = i

    def longestCommonPrefix(self, strs: List[str]) -> str:
        for i in range(len(strs[0])):
            for s in strs:
                #Comparing the characters with the elements in the first character, thats because the
                #common prefix cant be bigger than the first character or smaller.
                # So we can compare the characters of other words with that of the first
                if i==len(s) or s[i]!=strs[0][i]:
                    return s[:i]
        # IF there is no break, then we can return the entire first word as the common prefix.
        return strs[0]
