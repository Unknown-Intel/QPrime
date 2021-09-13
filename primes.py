#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import math


# In[ ]:


def bin_conv(x, n, fill=True):
        b_x = format(x, 'b')
        if fill == True:
            if len(b_x) < n:
                fill =""
                for i in range(n - len(b_x)):
                    fill += "0"
                b_x = fill + b_x
        return b_x


# In[ ]:


n = 5
no = []
rang = 2 ** n
prime = [2,3,5,7,11,13,17,23,29,31]

for i in range(n+1):
    for j in range(n + 1): 
        for k in range(n + 1):
            for l in range(n + 1):
                for m in range(n + 1):
                    for o in range(n + 1):
                        for p in range(n+1):
                            for q in range(n+1):
                                for r in range(n+1):
                                    for s in range(n+1):
                                        value_final = 1 * (prime[0] ** i) * (prime[1] ** j) * (prime[2] ** k) * (prime[3] ** l) * (prime[4] ** m) * (prime[5] ** o) * (prime[6] ** p) * (prime[7] ** q) *(prime[8] ** r) * (prime[9]**s)
    #             print(bit_range)\n",
                                        no.append(value_final)
# print(sorted(no))\n",
# print(2 ** (3 * len(prime)))"


# In[ ]:


total_numbers = []
no = sorted(no)
for i in range(2**12):
    total_numbers.append(i)
    
non_express = list(set(total_numbers) - set(no))
non_express.remove(0)

bit_remainder = []
for x in non_express:
    for i in range(len(no) - 1):
        if x > no[i] and x < no[i+1]:
            y = min([math.ceil(math.log2(x - no[i])), math.ceil(math.log2(no[i+1] - x))])
            bit_remainder.append(y)
            break
            
# In[ ]:


from matplotlib.pyplot import figure

figure(figsize=(30, 10), dpi=80)
# print(no[0:10])
# print(non_express[0:10])
# print(bit_remainder[0:10])
import matplotlib.pyplot as plt
print(len(bit_remainder))
print(len(non_express))
# for p in no:
#     plt.axvline(x=p,color='k', linestyle='--')

assert len(bit_remainder) == len(non_express)

plt.scatter(non_express[0:4096], bit_remainder[0:4096], color='r')

plt.show()


# In[ ]:


f = [0,0,0,0,0,0,0,0,0,0,0,0,0]

for r in bit_remainder[0:4096]:
    f[r] += 1

p = []
for i in f:
    p.append(i/4096)
    


# In[ ]:


print(p)


# In[ ]:




