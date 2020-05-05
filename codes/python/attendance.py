class Solution(object):
    def checkRecord(self, s):
        """
        :type s: str
        :rtype: bool
        """
        count_absent = 0
        count_late = 0
        
        for i in s:
            if i=="A":
                count_absent += 1
            elif  i=="L":
                count_late += 1
            else: 
                count_late = 0
                
            if count_absent >1 or count_late>2:
                return False
        
        return True

reward = Solution()
attendance = input('Student attendance record as a single string:\t')
c = reward.checkRecord(attendance)
print(c)
