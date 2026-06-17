import numpy as np

a = np.array([1,2])
b = np.array([3,4])
c = a + b
print(c)

message= "Welcome to the world of programming!"
print (message)

# using concat to combine dataframes
# Create DataFrames
df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5], 'B': [6]})

# Use concat
result = pd.concat([df1, df2], ignore_index=True)
print(result)