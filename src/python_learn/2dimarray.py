#coding: UTF-8
'''
Created on  2014-04-25

@author: mingliu
'''

'''
print the elements of matrix in diagonal mode
'''
if __name__ == '__main__':
    N = 3
    list_2 = [[1,2,3], [4,5,6], [7,8,9]]
    print range(2)
    for i in range(N * 2 - 1):
        for j in range(N):
            if i - j < 0:
                break
            if i - j > N - 1:
                continue
            else:
                print list_2[j][i - j], 
    print
    for i in range(N * 2 - 1):
        for j in range(N):
            if i - j < 0:
                break
            if i - j > N - 1:
                continue
            else:
                if i % 2 ==0:
                    print list_2[j][i - j],
                else:
                    print list_2[i - j][j],
    print
    for i in range(N * 2 - 1):
        for j in range(N):
            if i - j < 0:
                break
            if i - j > N - 1:
                continue
            else:
                if i % 2 ==0:
                    print list_2[j][N - i + j - 1],
                else:
                    print list_2[i - j][N - j - 1],
