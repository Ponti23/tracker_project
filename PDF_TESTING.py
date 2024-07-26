import matplotlib.pyplot as plt

# Sample data
x = [1, 2, 3, 4, 5]
y = [2, 3, 5, 7, 11]

# Create a new figure
plt.figure()

# Plot the data
plt.plot(x, y, marker='o')

# Add titles and labels
plt.title('Simple Line Graph')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')

# Save the figure as a PDF
plt.savefig('line_graph.pdf')

# Show the plot
plt.show()
