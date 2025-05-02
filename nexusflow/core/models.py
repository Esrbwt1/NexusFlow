"""Core data models for NexusFlow representing Flows, Nodes, and Edges."""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
import uuid  # Used for generating unique IDs

# --- Node Related Models ---


class Position(BaseModel):
    """Represents the x, y coordinates for visual positioning."""

    x: float = 0.0
    y: float = 0.0


class Node(BaseModel):
    """Represents a single node (trigger, action, or logic) in a flow."""

    id: str = Field(
        default_factory=lambda: f"node_{uuid.uuid4()}"
    )  # Auto-generate unique ID
    node_type: str  # e.g., 'trigger.manual', 'action.log', 'logic.python'
    name: str  # User-defined name for the node instance
    config: Dict[str, Any] = Field(default_factory=dict)  # Node-specific configuration
    position: Position = Field(default_factory=Position)  # For visual layout

    # Allow extra fields for potential future use or custom node data
    # model_config = {"extra": "allow"} # Uncomment if needed later


# --- Edge Related Models ---


class Edge(BaseModel):
    """Represents a connection between two nodes."""

    id: str = Field(
        default_factory=lambda: f"edge_{uuid.uuid4()}"
    )  # Auto-generate unique ID
    source_node_id: str
    target_node_id: str
    # Optional handles/ports for nodes that have multiple input/output points
    source_handle: Optional[str] = None
    target_handle: Optional[str] = None

    # model_config = {"extra": "allow"} # Uncomment if needed later


# --- Flow Related Models ---


class Flow(BaseModel):
    """Represents an entire automated workflow."""

    id: str = Field(
        default_factory=lambda: f"flow_{uuid.uuid4()}"
    )  # Auto-generate unique ID
    name: str
    description: Optional[str] = None
    nodes: List[Node] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)

    # model_config = {"extra": "allow"} # Uncomment if needed later

    def get_node_by_id(self, node_id: str) -> Optional[Node]:
        """Finds a node within the flow by its ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None

    def get_outgoing_edges(self, node_id: str) -> List[Edge]:
        """Finds all edges originating from a specific node."""
        return [edge for edge in self.edges if edge.source_node_id == node_id]

    def get_incoming_edges(self, node_id: str) -> List[Edge]:
        """Finds all edges terminating at a specific node."""
        return [edge for edge in self.edges if edge.target_node_id == node_id]


# Example Usage (can be removed later, useful for testing)
if __name__ == "__main__":
    # Create a simple flow programmatically
    flow = Flow(name="My First Test Flow", description="Logs a simple message.")

    # Create nodes
    trigger_node = Node(node_type="trigger.manual", name="Start")
    log_node = Node(
        node_type="action.log",
        name="Log Message",
        config={"message": "Hello NexusFlow!"},
    )

    # Add nodes to flow
    flow.nodes.append(trigger_node)
    flow.nodes.append(log_node)

    # Create an edge connecting them
    edge = Edge(source_node_id=trigger_node.id, target_node_id=log_node.id)
    flow.edges.append(edge)

    # Print the flow as JSON (Pydantic automatically handles serialization)
    print(flow.model_dump_json(indent=2))

    # Example of finding a node
    found_node = flow.get_node_by_id(log_node.id)
    if found_node:
        print(f"\nFound node: {found_node.name}")
        print(f"Config: {found_node.config}")

    # Example of finding edges
    outgoing = flow.get_outgoing_edges(trigger_node.id)
    print(f"\nEdges from {trigger_node.name}: {len(outgoing)}")
