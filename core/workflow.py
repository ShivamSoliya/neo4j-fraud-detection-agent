import logging
from typing import List, Dict, Any
from agents.supervisor import supervisor_workflow

logger = logging.getLogger(__name__)

# --- Graph Visualization Helper (from GenericAgent, extracted for reusability) ---
# This function is passed to CustomToolExecutor
def _generate_visualization_html(data: List[Dict[str, Any]]) -> str:
    # This implementation is copied from generic_agent.py, ensure it's up-to-date
    # Extract nodes and links from the Cypher query results
    nodes = {}
    links = []
    node_id_counter = 0

    for record in data:
        for key, value in record.items():
            if isinstance(value, dict) and 'labels' in value and 'properties' in value: # Likely a node
                node_type = value['labels'][0] if value['labels'] else 'Unknown'
                node_props = value['properties']
                node_name = node_props.get('name', node_props.get('id', f"{node_type}_{node_id_counter}"))

                if node_name not in nodes:
                    nodes[node_name] = {"id": node_name, "label": node_name, "type": node_type}
                    node_id_counter += 1
            elif isinstance(value, dict) and 'type' in value and 'start' in value and 'end' in value: # Likely a relationship
                # For simplicity, assuming 'start' and 'end' point to node names/IDs directly
                source_name = value['start']['properties'].get('name', value['start']['properties'].get('id', 'Unknown'))
                target_name = value['end']['properties'].get('name', value['end']['properties'].get('id', 'Unknown'))
                if source_name in nodes and target_name in nodes:
                    links.append({"source": source_name, "target": target_name, "type": value['type']})
    
    # Convert nodes dictionary to a list for D3
    d3_nodes = list(nodes.values())

    html_content = f"""
    <div id="graph-container" style="width: 100%; height: 600px; border: 1px solid #ccc; border-radius: 8px; overflow: hidden;"></div>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <script>
        // Ensure the container is ready
        document.addEventListener('DOMContentLoaded', function() {{
            const container = document.getElementById('graph-container');
            if (!container) return;

            const width = container.offsetWidth;
            const height = container.offsetHeight;

            const nodes = {json.dumps(d3_nodes)};
            const links = {json.dumps(links)};

            const svg = d3.select("#graph-container").append("svg")
                .attr("width", width)
                .attr("height", height);

            const simulation = d3.forceSimulation(nodes)
                .force("link", d3.forceLink(links).id(d => d.id).distance(100))
                .force("charge", d3.forceManyBody().strength(-300))
                .force("center", d3.forceCenter(width / 2, height / 2));

            const link = svg.append("g")
                .attr("stroke", "#999")
                .attr("stroke-opacity", 0.6)
                .selectAll("line")
                .data(links)
                .join("line")
                .attr("stroke-width", d => Math.sqrt(d.value || 1));

            const node = svg.append("g")
                .attr("stroke", "#fff")
                .attr("stroke-width", 1.5)
                .selectAll("circle")
                .data(nodes)
                .join("circle")
                .attr("r", 8)
                .attr("fill", d => d.type === 'Person' ? '#66B3FF' : (d.type === 'Account' ? '#FFCC66' : (d.type === 'Transaction' ? '#A2CCB3' : '#CC99FF'))) // Color nodes by type
                .call(d3.drag()
                    .on("start", dragstarted)
                    .on("drag", dragged)
                    .on("end", dragended));

            const labels = svg.append("g")
                .attr("class", "labels")
                .selectAll("text")
                .data(nodes)
                .enter().append("text")
                .attr("dx", 12)
                .attr("dy", ".35em")
                .text(d => d.label)
                .style("font-size", "10px")
                .style("fill", "#333")
                .style("pointer-events", "none"); // So that mouse events pass through to the circle

            simulation.on("tick", () => {{
                link
                    .attr("x1", d => d.source.x)
                    .attr("y1", d => d.source.y)
                    .attr("x2", d => d.target.x)
                    .attr("y2", d => d.target.y);

                node
                    .attr("cx", d => d.x)
                    .attr("cy", d => d.y);

                labels
                    .attr("x", d => d.x)
                    .attr("y", d => d.y);
            }});

            function dragstarted(event, d) {{
                if (!event.active) simulation.alphaTarget(0.3).restart();
                d.fx = d.x;
                d.fy = d.y;
            }}

            function dragged(event, d) {{
                d.fx = event.x;
                d.fy = event.y;
            }}

            function dragended(event, d) {{
                if (!event.active) simulation.alphaTarget(0);
                d.fx = null;
                d.fy = null;
            }}

            // Add resize listener for responsiveness
            window.addEventListener('resize', () => {{
                const newWidth = container.offsetWidth;
                const newHeight = container.offsetHeight;
                svg.attr("width", newWidth).attr("height", newHeight);
                simulation.force("center", d3.forceCenter(newWidth / 2, newHeight / 2)).alpha(1).restart();
            }});
        }});
    </script>
    """
    # Use BeautifulSoup to format the HTML output for embedding in immersive
    from bs4 import BeautifulSoup # Local import for this function
    import html # Local import
    soup = BeautifulSoup(html_content, 'html.parser')
    return html.unescape(soup.prettify())


async def create_fraud_detection_workflow():
