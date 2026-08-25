import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# ============================================================================
# 1. Create a directed graph
# ============================================================================
G = nx.DiGraph()

# ============================================================================
# 2. Define nodes with LANDSCAPE (left-to-right) coordinates
# ============================================================================
pos = {
    'Source': (0.00, 0.5),   # Far left
    's1': (0.20, 0.5),       # Replication point
    's2a': (0.45, 0.0),      # Upper switch (Path A)
    's2b': (0.45, 0.5),      # Middle switch (Path B)
    's2c': (0.45, 1.0),      # Lower switch (Path C)
    's3a': (0.75, 0.0),      # Upper intermediate (Path A)
    's3b': (0.75, 0.5),      # Middle intermediate (Path B)
    's3c': (0.75, 1.0),      # Lower intermediate (Path C)
    'Destination': (1.00, 0.5) # Far right
}

for node, p in pos.items():
    G.add_node(node, pos=p)

# ============================================================================
# 3. Define edges with strict academic colors (ColorBrewer Set1)
# ============================================================================
edges_primary = [
    ('s1', 's2a', '#E41A1C', 'Replica 1 (Path A)'),
    ('s1', 's2b', '#4DAF4A', 'Replica 2 (Path B)'),
    ('s1', 's2c', '#377EB8', 'Replica 3 (Path C)'),
    ('s2a', 's3a', '#E41A1C', 'Path A'),
    ('s2b', 's3b', '#4DAF4A', 'Path B'),
    ('s2c', 's3c', '#377EB8', 'Path C'),
    ('s3a', 'Destination', '#E41A1C', 'Path A'),
    ('s3b', 'Destination', '#4DAF4A', 'Path B'),
    ('s3c', 'Destination', '#377EB8', 'Path C'),
]

edges_cross = [
    ('s2a', 's2b'), ('s2b', 's2a'),
    ('s3a', 's3b'), ('s3b', 's3a'),
]

edges_source = [('Source', 's1')]

# ============================================================================
# 4. Node appearance (increased size for Src and Dst to fully contain text)
# ============================================================================
node_colors = {
    'Source': '#FFDDBB',
    'Destination': '#FFDDBB',
    's1': '#F0F0F0',
    's2a': '#FEE5D9',
    's2b': '#E5F5E0',
    's2c': '#DEEBF7',
    's3a': '#FEE5D9',
    's3b': '#E5F5E0',
    's3c': '#DEEBF7',
}

node_sizes = {
    'Source': 5000,          # Increased to ensure the circle fully covers the text
    'Destination': 5000,
    's1': 2200,
    's2a': 1800,
    's2b': 1800,
    's2c': 1800,
    's3a': 1800,
    's3b': 1800,
    's3c': 1800,
}

font_sizes = {
    'Source': 22,            # Slightly larger for readability
    'Destination': 22,
    's1': 16,
    's2a': 14,
    's2b': 14,
    's2c': 14,
    's3a': 14,
    's3b': 14,
    's3c': 14,
}

# ============================================================================
# 5. Custom labels (short abbreviations for Source and Destination)
# ============================================================================
custom_labels = {
    'Source': 'Src',
    'Destination': 'Dst',
}

# ============================================================================
# 6. Draw the figure
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 7))
node_pos = nx.get_node_attributes(G, 'pos')

# Draw Source → s1 (black, thick, with arrow)
nx.draw_networkx_edges(
    G, node_pos, edgelist=[('Source', 's1')],
    edge_color='#000000', width=3, arrows=True, arrowstyle='-|>',
    arrowsize=18, ax=ax
)

# Draw primary paths (colored, thick, with arrows)
for u, v, color, _ in edges_primary:
    nx.draw_networkx_edges(
        G, node_pos, edgelist=[(u, v)],
        edge_color=color, width=4.5, alpha=0.9,
        arrows=True, arrowstyle='-|>', arrowsize=14, ax=ax
    )

# Draw cross-connections (grey, dashed, no arrows)
nx.draw_networkx_edges(
    G, node_pos, edgelist=edges_cross,
    edge_color='#999999', width=2.5, style='dashed', alpha=0.7,
    arrows=False, ax=ax
)

# Draw nodes
for node in G.nodes():
    edge_width = 4.0 if node in ['Source', 'Destination'] else 2.0
    nx.draw_networkx_nodes(
        G, node_pos, nodelist=[node],
        node_color=node_colors[node],
        node_size=node_sizes[node],
        edgecolors='#333333', linewidths=edge_width, ax=ax
    )

# Draw labels with custom short names ('Src' and 'Dst')
# Use bbox to ensure text is always visible even if slightly outside the circle
for node in G.nodes():
    label_to_display = custom_labels.get(node, node)
    nx.draw_networkx_labels(
        G, node_pos, labels={node: label_to_display},
        font_size=font_sizes[node], font_weight='bold',
        ax=ax
    )

# ============================================================================
# 7. Legend (explicitly defines abbreviations and explains "Legend")
# ============================================================================
legend_elements = [
    Line2D([0], [0], color='#E41A1C', lw=4.5, label='Replica 1 (Path A)'),
    Line2D([0], [0], color='#4DAF4A', lw=4.5, label='Replica 2 (Path B)'),
    Line2D([0], [0], color='#377EB8', lw=4.5, label='Replica 3 (Path C)'),
    Line2D([0], [0], color='#999999', lw=2.5, linestyle='--', label='Cross-connections'),
    Line2D([0], [0], color='#000000', lw=3.0, label='Src → Replication (s1)'),
    # Explicit definition of the abbreviations
    Line2D([0], [0], marker='s', color='w', markerfacecolor='#FFDDBB',
           markersize=12, label='Src = Source, Dst = Destination'),
]

# The word "Legend" is standard in international journals.
# It means "key to the symbols/colors used in the figure".
ax.legend(
    handles=legend_elements,
    loc='upper left',
    bbox_to_anchor=(1.01, 1),
    fontsize=13,
    frameon=True,
    fancybox=False,
    edgecolor='#333333',
)

# ============================================================================
# 8. Aesthetics (extended xlim for more breathing room)
# ============================================================================
ax.axis('off')
ax.set_xlim(-0.1, 1.15)  # Increased to prevent clipping of 'Dst'
ax.set_ylim(-0.1, 1.15)
fig.tight_layout()

# Save at 300 dpi
fig.savefig('Figure1_topology_landscape.png', dpi=300, bbox_inches='tight')
plt.close()

print("Figure 1 saved as 'Figure1_topology_landscape.png' at 300 dpi.")