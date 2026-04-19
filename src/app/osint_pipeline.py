import re
from datetime import datetime
from typing import Any, Dict, List, Optional

# networkx and neo4j are optional runtime dependencies for the OSINT pipeline.
# Provide lightweight fallbacks so the app can start in developer environments
# without installing heavy graph or database packages.
try:
    import networkx as nx
except Exception:
    nx = None

try:
    from neo4j import GraphDatabase
except Exception:
    GraphDatabase = None

from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


class _SimpleGraph:
    def __init__(self) -> None:
        self._nodes: Dict[str, Dict[str, Any]] = {}
        self._edges: List[tuple[str, str, Dict[str, Any]]] = []

    def add_node(self, name: str, **data: Any) -> None:
        self._nodes[name] = data

    def add_edge(self, u: str, v: str, **data: Any) -> None:
        self._edges.append((u, v, data))

    def nodes(self, data: bool = False) -> Any:
        if data:
            return list(self._nodes.items())
        return list(self._nodes.keys())

    def edges(self, data: bool = False) -> Any:
        if data:
            return [(u, v, d) for (u, v, d) in self._edges]
        return [(u, v) for (u, v, _) in self._edges]



class OSINTPipeline:
    def __init__(self) -> None:
        if nx is not None:
            graph_obj = nx.Graph()
        else:
            graph_obj = _SimpleGraph()
        self.graph: Any = graph_obj
        self.neo4j_driver: Optional[Any] = None
        # Create Neo4j driver only if URI is configured; otherwise operate in-memory
        if NEO4J_URI:
            try:
                host = NEO4J_URI.split('://')[-1].split(':')[0]
            except Exception:
                host = None
            should_try = True
            if host and (host == 'neo4j' or host == 'db' or host.endswith('.local')):
                try:
                    import socket

                    socket.getaddrinfo(host, None)
                except Exception:
                    should_try = False

            if should_try:
                try:
                    self.neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
                except Exception:
                    # driver unavailable (e.g., host unresolved) — continue without raising
                    self.neo4j_driver = None

    def fetch_news(self, query: str = "horse riding Kharkiv") -> List[Dict[str, str]]:
        return [{"title": "Example news", "content": "Event in Kharkiv horse club", "date": datetime.now().isoformat()}]

    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        persons = re.findall(r"\b(?:Mr\.|Ms\.|Dr\.)?\s?([A-Z][a-z]+ [A-Z][a-z]+)\b", text)
        locations = re.findall(r"\b(?:Kharkiv|Kharkov|Bezlyudivka|Lisopark)\b", text)
        return {"persons": persons, "locations": locations}

    def build_graph(self, entities: Dict[str, List[str]]) -> None:
        for person in entities["persons"]:
            self.graph.add_node(person, type="person")
        for loc in entities["locations"]:
            self.graph.add_node(loc, type="location")
            for person in entities["persons"]:
                self.graph.add_edge(person, loc, relation="visited")

    def sync_to_neo4j(self) -> None:
        if not self.neo4j_driver:
            # No driver configured — skip sync silently
            return
        try:
            with self.neo4j_driver.session() as session:
                tx = session.begin_transaction()
                # Clear existing graph
                tx.run("MATCH (n) DETACH DELETE n")

                # Batch create/merge nodes
                nodes_batch = []
                for node, data in self.graph.nodes(data=True):
                    nodes_batch.append({"name": node, "type": data.get("type", "unknown")})
                if nodes_batch:
                    tx.run(
                        "UNWIND $nodes AS n MERGE (e:Entity {name: n.name}) SET e.type = n.type",
                        nodes=nodes_batch,
                    )

                # Batch create relationships
                rels_batch = []
                for u, v, data in self.graph.edges(data=True):
                    rels_batch.append({"u": u, "v": v})
                if rels_batch:
                    tx.run(
                        "UNWIND $rels AS r MATCH (a:Entity {name: r.u}), (b:Entity {name: r.v}) MERGE (a)-[:RELATES]->(b)",
                        rels=rels_batch,
                    )

                tx.commit()
        except Exception:
            # If Neo4j is unreachable or operation fails, do not propagate to caller.
            return

    def score_case(self, case_entities: Dict[str, Any], connectivity: float = 1.0, impact: float = 0.5, confidence: float = 0.8) -> float:
        return impact * confidence * connectivity

    def run(self) -> List[Dict[str, Any]]:
        news_items = self.fetch_news()
        for item in news_items:
            entities = self.extract_entities(item["title"] + " " + item["content"])
            self.build_graph(entities)
        self.sync_to_neo4j()
        return [{"title": "OSINT Case", "entities": list(self.graph.nodes), "sources": "news", "timeline": datetime.now().isoformat(), "geo": "Kharkiv", "confidence_score": 0.7}]
