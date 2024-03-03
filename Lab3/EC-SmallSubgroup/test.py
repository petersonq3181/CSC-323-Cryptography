import crypto 
import matplotlib.pyplot as plt
import numpy as np


curve = crypto.Curve(a=-95051, b=11279326, field=233970423115425145524320034830162017933)
base_point = crypto.EccAlgPoint(curve=curve, x=182, y=85518893674295321206118380980485522083)
bp_order = 29246302889428143187362802287225875743


point = crypto.EccAlgPoint(curve=crypto.curve, x=16349894185180983439102154383611486412, y=224942997200586455214256137069604954919)

accx = []
accy = []
for i in range(1, 100):
    try:
        accx.append(crypto.EccPoint.__mul__(point, i).x) 
        accy.append(crypto.EccPoint.__mul__(point, i).y) 
    except: 
        pass 

print(set(accx))
print(set(accy))

# Convert data to numpy array for easier handling
data_np = np.array(accx, dtype=np.float64)

# Plotting
plt.figure(figsize=(10, 6))

# Since the data spans several orders of magnitude, a logarithmic scale might be more appropriate
# We'll add a small constant to handle any data points that might be 0 or negative
plt.hist(data_np, bins=20, log=True, color='skyblue', edgecolor='black')

plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Distribution of Data')

# Show plot
plt.show()
