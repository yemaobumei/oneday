"""
48. Rotate Image
You are given an n x n 2D matrix representing an image.

Rotate the image by 90 degrees (clockwise).

Follow up:
Could you do this in-place?

Subscribe to see which companies asked this question
"""



    class Solution(object):
        def rotate(self,matrix):
        n=len(matrix)
        if n==1:
            return  [[1]]
        new_matrix = [[0 for col in range(n)] for row in range(n)]

        for i in range(n):
            for j in range(n):
                #print j,i,n-i-1,j
                new_matrix[j][i]=matrix[n-i-1][j]
        return new_matrix
    a=Solution()
    b=a.rotate([[1]])
    print b