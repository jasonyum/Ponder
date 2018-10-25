# Get an idea 
plt.plot(avg_returns[200:]) # give it time to settle in
plt.ylabel('Returns')
plt.xlabel('Round')
plt.show()
print(np.var(avg_returns[5:]))
