import matplotlib.pyplot as plt
import numpy as np

def visualize(ts_time, ts_data, buying_points, selling_points, exit_points):
    fig = plt.figure(figsize=(50, 30))
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(ts_time, ts_data, color='black', linewidth=0.1)

    ploted_xticks = ts_time[np.array(range(0, len(ts_time), 150))]
    ax.set_xticks(ploted_xticks)
    ax.set_xticklabels([x.split('T')[0] for x in ploted_xticks])

    ax.scatter([x[0] for x in buying_points], [x[1] for x in buying_points], s=1, c='red')
    ax.scatter([x[0] for x in selling_points], [x[1] for x in selling_points], s=1, c='blue')
    ax.scatter([x[0] for x in exit_points], [x[1] for x in exit_points], s=1, c='orange')