from utils import *

class Solution:
    def merge(self, nums1: List[int], m: int, nums2: List[int], n: int) -> None:
        """
        Do not return anything, modify nums1 in-place instead.
        """
        if m == 0:
            for i in range(n):
                nums1[i] = nums2[i]
            return

        i, j = m-1, n-1
        k = m+n-1
        while i >= 0 and j >=0:
            if nums1[i] > nums2[j]:
                nums1[k] = nums1[i]
                i -= 1
            else:
                nums1[k] = nums2[j]
                j -= 1
            k -= 1

        if j >= 0:
            nums1[:j+1] = nums2[:j+1]
        return



if __name__ == "__main__":
    nums1 = [0]
    m = 0
    nums2 = [1]
    n = 1
    sol = Solution()
    sol.merge(nums1, m, nums2, n)
    print(nums1)


