from dataclasses import dataclass
from typing import List, Optional, Tuple
from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS, XSD

# Here we parse the knowledge graph and return a list of philosophers

# The knowledge graph is a ttl file that contains the following information:
# - Philosophers
# - Beliefs
# - Key concepts
# - Contexts
# - Ideological clusters


@dataclass
class Philosopher:
    name: str  # Human-readable label or URI fragment
    birth_year: int | None  # Allow None if missing
    beliefs: List[str]
    key_concepts: List[str]
    contexts: List[str]
    ideological_cluster: str | None
    influenced_by: List[str]
    influenced: List[str]
    region: str | None = None  # Add region field with default None

@dataclass
class HistoricalContext:
    name: str
    start_year: int
    end_year: int

# The KnowledgeGraphParser class is used to parse the knowledge graph and return a list of philosophers
class KnowledgeGraphParser:
    def __init__(self, ttl_path: str):
        self.graph = Graph()
        print(f"Loading TTL file from: {ttl_path}")
        self.graph.parse(ttl_path, format="turtle")
        # Bind both prefixes to our namespace
        self.graph.bind("ex", "http://example.org/philosophy/")
        self.graph.bind("", "http://example.org/philosophy/ontology#")
        self.namespace = "http://example.org/philosophy/"
        print(f"Using namespace: {self.namespace}")
        
        # Debug: Print all namespaces in the graph
        print("Namespaces in graph:")
        for prefix, uri in self.graph.namespaces():
            print(f"  {prefix}: {uri}")
        
        # Debug: Check if we can find any philosopher type declarations
        philosopher_type = URIRef("http://example.org/philosophy/philosopher")
        print(f"Looking for philosopher type: {philosopher_type}")
        for s, p, o in self.graph.triples((None, RDF.type, philosopher_type)):
            print(f"Found philosopher: {s}")

    def _get_label(self, uri: URIRef) -> str:
        label = self.graph.value(uri, RDFS.label)
        if label:
            return str(label)
        # Fallback: use URI fragment
        uri_str = str(uri)
        if uri_str.startswith(self.namespace):
            return uri_str.split("/")[-1]
        elif uri_str.startswith("http://example.org/philosophy/ontology#"):
            return uri_str.split("#")[-1]
        return uri_str

    def _get_literal_values(self, uri: URIRef, predicate: str) -> List[str]:
        # Ensure we're using the full URI for the predicate
        pred_uri = URIRef(self.namespace + predicate)
        return [str(o) for o in self.graph.objects(uri, pred_uri)]

    def _parse_year(self, year_str: str) -> int | None:
        if not year_str:
            return None
        parts = year_str.split()
        try:
            year = int(parts[0])
            if len(parts) > 1 and parts[1] == "BCE":
                year = -year
            return year
        except Exception:
            return None

    def _get_birth_year(self, uri: URIRef) -> int | None:
        birth_year = self.graph.value(uri, URIRef(self.namespace + "birthYear"))
        if not birth_year:
            return None
        return self._parse_year(str(birth_year))

    def _get_context_years(self, uri: URIRef) -> Tuple[int | None, int | None]:
        start_year = self.graph.value(uri, URIRef(self.namespace + "startYear"))
        end_year = self.graph.value(uri, URIRef(self.namespace + "endYear"))
        if not start_year or not end_year:
            return None, None
        return self._parse_year(str(start_year)), self._parse_year(str(end_year))

    def _create_philosopher(self, uri: URIRef) -> Philosopher:
        print(f"Creating philosopher from URI: {uri}")
        name = self._get_label(uri)
        print(f"Got label: {name}")
        birth_year = self._get_birth_year(uri)
        print(f"Got birth year: {birth_year}")
        beliefs = self._get_literal_values(uri, "believesIn")
        print(f"Got beliefs: {beliefs}")
        key_concepts = self._get_literal_values(uri, "developedConcept")
        print(f"Got key concepts: {key_concepts}")
        contexts = self._get_literal_values(uri, "livedDuring")
        print(f"Got contexts: {contexts}")
        ideological_cluster = self.graph.value(uri, URIRef(self.namespace + "ideologicalCluster"))
        if ideological_cluster:
            ideological_cluster = str(ideological_cluster)
        print(f"Got ideological cluster: {ideological_cluster}")
        influenced_by = self._get_literal_values(uri, "influencedBy")
        print(f"Got influenced by: {influenced_by}")
        influenced = self._get_literal_values(uri, "influenced")
        print(f"Got influenced: {influenced}")
        
        # Extract region from historical contexts
        region = None
        for context in contexts:
            context_str = str(context).lower()
            if "greece" in context_str:
                region = "Greece"
                break
            elif "rome" in context_str:
                region = "Rome"
                break
            elif "england" in context_str or "britain" in context_str:
                region = "England"
                break
            elif "france" in context_str:
                region = "France"
                break
            elif "germany" in context_str:
                region = "Germany"
                break
            elif "america" in context_str or "united states" in context_str:
                region = "America"
                break
        
        return Philosopher(
            name=name,
            birth_year=birth_year,
            beliefs=beliefs or [],
            key_concepts=key_concepts or [],
            contexts=contexts or [],
            ideological_cluster=ideological_cluster,
            influenced_by=influenced_by or [],
            influenced=influenced or [],
            region=region
        )

    def get_philosopher(self, name: str) -> Optional[Philosopher]:
        # Try exact match first
        uri = URIRef(self.namespace + name)
        philosopher_type = URIRef("http://example.org/philosophy/philosopher")
        if (uri, RDF.type, philosopher_type) in self.graph:
            return self._create_philosopher(uri)
        # If exact match fails, try matching by last name
        last_name = name.split()[-1].lower()
        for s, p, o in self.graph.triples((None, RDF.type, philosopher_type)):
            philosopher_label = self._get_label(s)
            if last_name in philosopher_label.lower():
                return self._create_philosopher(s)
        return None

    def get_historical_context(self, name: str) -> Optional[HistoricalContext]:
        uri = URIRef(self.namespace + name)
        if not (uri, RDF.type, URIRef(self.namespace + "HistoricalContext")) in self.graph:
            return None

        start_year, end_year = self._get_context_years(uri)
        if start_year is None or end_year is None:
            return None

        return HistoricalContext(
            name=self._get_label(uri),
            start_year=start_year,
            end_year=end_year
        )

    def get_all_philosophers(self) -> List[Philosopher]:
        philosophers = []
        print(f"Searching for philosophers in graph...")
        # Use the full URI for the philosopher type
        philosopher_type = URIRef("http://example.org/philosophy/philosopher")
        philosopher_subjects = list(self.graph.subjects(RDF.type, philosopher_type))
        print(f"Found {len(philosopher_subjects)} philosopher subjects")
        
        for s in philosopher_subjects:
            try:
                print(f"Processing philosopher: {s}")
                p = self._create_philosopher(s)
                if p.name:  # Only add if name is present
                    print(f"Added philosopher: {p.name}")
                    philosophers.append(p)
                else:
                    print(f"Skipped philosopher with no name: {s}")
            except Exception as e:
                print(f"Error processing philosopher {s}: {str(e)}")
                continue
        print(f"Total philosophers after processing: {len(philosophers)}")
        return philosophers

    def get_all_historical_contexts(self) -> List[HistoricalContext]:
        contexts = []
        for s in self.graph.subjects(RDF.type, URIRef(self.namespace + "HistoricalContext")):
            name = str(s).split("/")[-1]
            if context := self.get_historical_context(name):
                contexts.append(context)
        return contexts 