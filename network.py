import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Ask the user for the target username
target_username = input("Enter the target username (e.g., @Johnsmith): ")
target_username = target_username.lstrip('@')  # Remove leading '@' if present

# Directory path
directory_path = f"Collection/{target_username}"

# Load the network data CSV file
network_csv_path = os.path.join(directory_path, f"{target_username}_network.csv")
if not os.path.exists(network_csv_path):
    print(f"Network data file not found: {network_csv_path}")
else:
    # Read the CSV file into a DataFrame
    network_data = pd.read_csv(network_csv_path)

    # Replace NaN values with blank spaces in the DataFrame
    network_data = network_data.fillna(' ')

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes (UserIDs) with formatted labels
    for _, row in network_data.iterrows():
        sender_user_id = row['Sender_UserID']
        sender_username = row['Sender_Username']
        sender_first_name = row['Sender_FirstName']
        sender_last_name = row['Sender_LastName']

        receiver_user_id = row['Receiver_UserID']
        receiver_username = row['Receiver_Username']
        receiver_first_name = row['Receiver_FirstName']
        receiver_last_name = row['Receiver_LastName']

        # Create formatted labels with NaN values replaced by blank spaces
        sender_label = f"{sender_first_name} {sender_last_name} (@{sender_username})\nUserID: {sender_user_id}"
        receiver_label = f"{receiver_first_name} {receiver_last_name} (@{receiver_username})\nUserID: {receiver_user_id}"

        # Add nodes with formatted labels
        G.add_node(sender_user_id, label=sender_label)
        G.add_node(receiver_user_id, label=receiver_label)

    # Add edges (interactions) and count the number of interactions
    interaction_count = {}
    for _, row in network_data.iterrows():
        sender_user_id = row['Sender_UserID']
        receiver_user_id = row['Receiver_UserID']

        # Create or update the interaction count
        if (sender_user_id, receiver_user_id) in interaction_count:
            interaction_count[(sender_user_id, receiver_user_id)] += 1
        else:
            interaction_count[(sender_user_id, receiver_user_id)] = 1

        # Add edges with interaction count as labels
        G.add_edge(sender_user_id, receiver_user_id, interactions=interaction_count[(sender_user_id, receiver_user_id)])

    # Create the network visualization with improved styling and dynamic layout
    plt.figure(figsize=(14, 10))

    # Customize the spring layout with better spacing
    pos = nx.spring_layout(G, seed=42, k=0.15, iterations=50)  # Adjust 'k' and 'iterations' as needed

    labels = nx.get_node_attributes(G, 'label')
    interactions = nx.get_edge_attributes(G, 'interactions')
    edge_labels = {(u, v): str(interactions[(u, v)]) for u, v in G.edges}

    # Node and edge styling
    node_size = 300  # Increase node size to accommodate larger labels
    node_color = 'lightblue'
    edge_width = 1
    edge_color = 'gray'
    font_size = 10
    font_color = 'black'

    # Draw nodes, edges, labels, and edge labels
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_color)
    nx.draw_networkx_edges(G, pos, width=edge_width, edge_color=edge_color)

    # Calculate the label positions to avoid cutoff
    label_positions = {node: (pos[node][0], pos[node][1] - 0.02) for node in G.nodes()}

    nx.draw_networkx_labels(G, label_positions, labels, font_size=font_size, font_color=font_color, font_weight='bold')

    # Position edge labels to avoid overlap with nodes
    for (u, v), label in edge_labels.items():
        x = (pos[u][0] + pos[v][0]) / 2  # Calculate x-coordinate
        y = (pos[u][1] + pos[v][1]) / 2  # Calculate y-coordinate
        plt.text(x, y, label, size=font_size, color=font_color, ha='center', va='center')

    plt.title(f"User Interaction Network for {target_username}")

    # Save the visualization to a file
    network_viz_path = os.path.join(directory_path, f"{target_username}_network_visualization.png")
    plt.savefig(network_viz_path, bbox_inches='tight', pad_inches=0.1, dpi=400)  # Adjust DPI for higher resolution
    print(f"Network visualization saved to: {network_viz_path}")
