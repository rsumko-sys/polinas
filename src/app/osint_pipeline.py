class OSINTPipeline:
    def __init__(self):
        pass

    def run(self):
        # Return empty result set for local QA
        return []
import re
from datetime import datetime
import networkx as nx
from neo4j import GraphDatabase
from app.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


class OSINTPipeline:
    def __init__(self):
        self.graph = nx.Graph()
        self.neo4j_driver = None
        # Create Neo4j driver only if URI is configured; otherwise operate in-memory
        if NEO4J_URI:
            # Avoid trying to connect to typical Docker hostnames in local dev
            # when they are unlikely to resolve (e.g., 'neo4j', 'db'). Attempt
            # a DNS resolution check first and skip driver creation if it fails.
            try:
                host = NEO4J_URI.split('://')[-1].split(':')[0]
            except Exception:
                host = None
            should_try = True
            if host and (host == 'neo4j' or host == 'db' or host.endswith('.local')):
                # perform a quick DNS probe
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

    def fetch_news(self, query="horse riding Kharkiv"):
        return [{"title": "Example news", "content": "Event in Kharkiv horse club", "date": datetime.now().isoformat()}]

    def extract_entities(self, text):
        persons = re.findall(r"\b(?:Mr\.|Ms\.|Dr\.)?\s?([A-Z][a-z]+ [A-Z][a-z]+)\b", text)
        locations = re.findall(r"\b(?:Kharkiv|Kharkov|Bezlyudivka|Lisopark)\b", text)
        return {"persons": persons, "locations": locations}

    def build_graph(self, entities):
        for person in entities["persons"]:
            self.graph.add_node(person, type="person")
        for loc in entities["locations"]:
            self.graph.add_node(loc, type="location")
            for person in entities["persons"]:
                self.graph.add_edge(person, loc, relation="visited")

    def sync_to_neo4j(self):
        if not self.neo4j_driver:
            # No driver configured — skip sync silently
            return
        try:
            with self.neo4j_driver.session() as session:
                session.run("MATCH (n) DETACH DELETE n")
                for node, data in self.graph.nodes(data=True):
                    session.run("CREATE (n:Entity {name: $name, type: $type})", name=node, type=data.get("type", "unknown"))
                for u, v, data in self.graph.edges(data=True):
                    session.run("MATCH (a:Entity {name: $u}), (b:Entity {name: $v}) CREATE (a)-[:RELATES]->(b)", u=u, v=v)
        except Exception:
            # If Neo4j is unreachable or operation fails, do not propagate to caller.
            return

    def score_case(self, case_entities, connectivity=1.0, impact=0.5, confidence=0.8):
        return impact * confidence * connectivity

    def run(self):
        news_items = self.fetch_news()
        for item in news_items:
            entities = self.extract_entities(item["title"] + " " + item["content"])
            self.build_graph(entities)
        self.sync_to_neo4j()
        return [{"title": "OSINT Case", "entities": list(self.graph.nodes), "sources": "news", "timeline": datetime.now().isoformat(), "geo": "Kharkiv", "confidence_score": 0.7}]
