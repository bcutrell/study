import numpy as np

# create an array of 10 zeros 
np.zeros(10)

# create an array of 10 ones
np.ones(10)

# create an array of the integers from 10 to 50
np.arange(10,50)

# create an array of all the even integers from 10 to 50
np.arange(10,50,2)

# create a 3x3 matrix with values ranging from 0 to 8
np.arange(0,9).reshape(3,3)

# create a 3x3 identity matrix
np.eye(3)

# use NumPy to generate a random number between 0 and 1
np.random.rand()

# use NumPy to generate an array of 25 random numbers sampled from a standard normal distribution
np.random.randn(25)

# create an array of 20 linearly spaced points between 0 and 1:
np.linspace(0, 1,20)

# given matrix
mat = np.arange(1,26).reshape(5,5)

# reproduce output:

mat[2:,1:]
# array([[12, 13, 14, 15],
#        [17, 18, 19, 20],
#        [22, 23, 24, 25]])


mat[3,4]
# 20

mat[:3,1:2]
# array([[ 2],
#        [ 7],
#        [12]])


mat[4,:]
# array([21, 22, 23, 24, 25])

mat[3:,:]
# array([[16, 17, 18, 19, 20],
#        [21, 22, 23, 24, 25]])

# get the sum of all the values in mat
mat.sum()

# get the standard deviation of the values in mat
mat.std()

# get the sum of all the columns in mat
mat.sum(axis=0)
# gets the sum of each column
# [55 60 65 70 75]

# What is the best way to ensure you get the same random numbers
np.random.seed(101)


