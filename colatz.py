import plotly.graph_objects as go
import networkx as nx

def generate_collatz_sequence(n):
    """Generate the Collatz sequence for a given starting number."""
    sequence = []
    while n != 1:
        sequence.append(n)
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
    sequence.append(1)  # Add the final 1 to the sequence
    return sequence

def generate_collatz_groups(start, count):
    """Generate groups of Collatz sequences starting from `start` to `start + count - 1`."""
    groups = []
    for i in range(start, start + count):
        groups.append(generate_collatz_sequence(i))
    return groups

def create_collatz_graph(groups):
    """Create a Collatz graph where paths join at common values, with 1 at the lowest level."""
    G = nx.DiGraph()
    
    # Add nodes and edges for each sequence
    for group in groups:
        for i in range(len(group) - 1):
            G.add_edge(group[i], group[i + 1])  # Add edge between consecutive numbers
    
    # Calculate depth (number of steps to reach a node)
    depth = {}
    for T,group in enumerate(groups):
        for i, num in enumerate(group):
            if group[i] == 54 &group[i-1] == 51:
                print('T:',T,'i:',i,'num:',num)
            if num not in depth:
                depth[num] = i # Assign the depth (position in the sequence)
    
    # Generate positions for nodes
    pos = {}
    for node in G.nodes():
        x = node  # Spread nodes horizontally by their value
        y = -depth[node]  # Invert depth to place `1` at the bottom
        pos[node] = (x, y)
    
    # Extract edge and node positions
    x_edges, y_edges = [], []
    for edge in G.edges():
        x_edges.extend([pos[edge[0]][0], pos[edge[1]][0], None])
        y_edges.extend([pos[edge[0]][1], pos[edge[1]][1], None])
    
    x_nodes = [pos[node][0] for node in G.nodes()]
    y_nodes = [pos[node][1] for node in G.nodes()]
    
    # Create Plotly traces
    edge_trace = go.Scatter(
        x=x_edges,
        y=y_edges,
        line=dict(width=1, color='gray'),
        hoverinfo='none',
        mode='lines'
    )
    
    node_trace = go.Scatter(
        x=x_nodes,
        y=y_nodes,
        mode='markers+text',
        marker=dict(size=10, color='blue'),
        text=[str(node) for node in G.nodes()],
        textposition="top center",
        hoverinfo='text'
    )
    
    # Create the figure
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        margin=dict(b=0, l=0, r=0, t=0),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False)
                    ))
    return fig

# Example usage
start = 10
count = 50
collatz_groups = generate_collatz_groups(start, count)
fig = create_collatz_graph(collatz_groups)
fig.show()
