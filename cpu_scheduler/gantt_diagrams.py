import matplotlib.pyplot as plt
import numpy as np

def create_gantt_chart(title, processes, end_time):
    fig, ax = plt.subplots(figsize=(15, 8))
    
    y_ticks = []
    y_labels = []
    all_times = set()
    
    for i, (process, data) in enumerate(processes.items()):
        y_ticks.append(i)
        y_labels.append(process)
        
        for start, end in data:
            ax.broken_barh([(start, end - start)], (i - 0.4, 0.8), facecolors='tab:blue')
            all_times.add(start)
            all_times.add(end)
            ax.axvline(x=start, color='gray', linestyle='--', alpha=0.5)
            ax.axvline(x=end, color='gray', linestyle='--', alpha=0.5)
    
    ax.set_ylim(-1, len(processes))
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    ax.set_xlabel('Time')
    ax.set_title(title)
    
    ax.grid(True, axis='x', linestyle=':', alpha=0.7)
    ax.set_xlim(0, end_time)
    
    # Sort and set all time points on x-axis
    all_times = sorted(list(all_times))
    ax.set_xticks(all_times)
    
    # Rotate and adjust x-axis labels to avoid overlapping
    plt.xticks(rotation=45, ha='right')
    fig.canvas.draw()
    labels = ax.get_xticklabels()
    
    # Implement multi-level labeling
    max_levels = 4
    label_positions = [[] for _ in range(max_levels)]
    
    for i, label in enumerate(labels):
        level = i % max_levels
        label_positions[level].append(i)
    
    for level, positions in enumerate(label_positions):
        for pos in positions:
            labels[pos].set_y(labels[pos].get_position()[1] - 0.05 * level)
    
    ax.set_xticklabels(labels)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.2)  # Adjust bottom margin to accommodate rotated labels
    plt.show()

# FCFS data
fcfs_processes = {
    'P1': [(0, 5), (32, 35), (164, 170), (395, 399)],
    'P2': [(5, 9), (57, 69), (228, 237), (445, 453)],
    'P3': [(9, 17), (50, 68), (228, 247), (557, 563)],
    'P4': [(17, 20), (55, 59), (164, 169), (328, 334), (565, 568)],
    'P5': [(20, 36), (60, 77), (228, 245), (487, 491), (530, 534)],
    'P6': [(36, 47), (69, 78), (228, 240), (336, 344), (445, 453)],
    'P7': [(47, 61), (107, 124), (328, 343), (512, 522)],
    'P8': [(61, 65), (79, 93), (228, 244), (493, 499)]
}

# MLFQ data
mlfq_processes = {
    'P1': [(0, 5), (32, 35), (164, 168), (266, 268)],
    'P2': [(5, 9), (57, 59), (164, 166), (234, 238)],
    'P3': [(9, 14), (47, 59), (130, 148), (386, 392)],
    'P4': [(14, 17), (52, 56), (164, 169), (329, 335), (391, 394)],
    'P5': [(17, 22), (46, 52), (96, 113), (359, 366), (403, 410), (537, 540)],
    'P6': [(22, 27), (49, 55), (124, 130), (284, 292), (382, 390)],
    'P7': [(27, 32), (78, 86), (277, 288), (374, 389), (463, 470)],
    'P8': [(32, 36), (50, 55), (164, 180), (413, 419)]
}

# SJF data
sjf_processes = {
    'P1': [(11, 16), (43, 47), (169, 175), (268, 272)],
    'P2': [(3, 7), (55, 60), (190, 202), (328, 337), (448, 455)],
    'P3': [(16, 24), (57, 69), (229, 247), (467, 481), (531, 545), (600, 631)],
    'P4': [(0, 3), (38, 42), (85, 89), (163, 168), (288, 294), (362, 368), (534, 537)],
    'P5': [(97, 113), (137, 154), (324, 340), (441, 454), (488, 499), (515, 518), (531, 534)],
    'P6': [(24, 35), (57, 66), (109, 118), (178, 190), (283, 298)],
    'P7': [(61, 75), (121, 138), (223, 234), (340, 355), (422, 438)],
    'P8': [(7, 11), (25, 30), (73, 79), (216, 222), (324, 340)]
}

# Generate charts for all three algorithms
create_gantt_chart('FCFS Scheduling', fcfs_processes, 648)
create_gantt_chart('MLFQ Scheduling', mlfq_processes, 599)
create_gantt_chart('SJF Scheduling', sjf_processes, 668)