from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass
import rdflib
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL
from owlrl import DeductiveClosure, OWLRL_Semantics

@dataclass
class InferredFact:
    subject: str
    predicate: str
    object: str
    is_inferred: bool = True

class SymbolicReasoner:
    def __init__(self, namespace: str = "http://example.org/philosophy/"):
        self.namespace = namespace
        self.graph = Graph()
        self.graph.bind("ex", namespace)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("owl", OWL)
        
    def load_ontology(self, turtle_file_path: str) -> None:
        """Load and parse the ontology from a Turtle file."""
        self.graph.parse(turtle_file_path, format="turtle")
        
    def run_reasoning(self) -> None:
        """Run OWL RL reasoning over the graph."""
        DeductiveClosure(OWLRL_Semantics).expand(self.graph)
        
    def get_philosopher_beliefs(self, philosopher_uri: str) -> List[Tuple[str, str, str]]:
        """Get all beliefs (including inferred ones) for a philosopher."""
        query = f"""
        SELECT ?belief ?label ?desc WHERE {{
            <{philosopher_uri}> <{self.namespace}believesIn> ?belief .
            OPTIONAL {{ ?belief rdfs:label ?label . }}
            OPTIONAL {{ ?belief <{self.namespace}description> ?desc . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_philosopher_concepts(self, philosopher_uri: str) -> List[Tuple[str, str, str]]:
        """Get all key concepts (including inferred ones) for a philosopher."""
        query = f"""
        SELECT ?concept ?label ?desc WHERE {{
            <{philosopher_uri}> <{self.namespace}keyConcept> ?concept .
            OPTIONAL {{ ?concept rdfs:label ?label . }}
            OPTIONAL {{ ?concept <{self.namespace}description> ?desc . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_philosopher_influences(self, philosopher_uri: str) -> List[Tuple[str, str]]:
        """Get all influences (including inferred ones) for a philosopher."""
        query = f"""
        SELECT ?influence ?label WHERE {{
            <{philosopher_uri}> <{self.namespace}influencedBy> ?influence .
            OPTIONAL {{ ?influence rdfs:label ?label . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_philosopher_influenced(self, philosopher_uri: str) -> List[Tuple[str, str]]:
        """Get all philosophers influenced (including inferred ones) by this philosopher."""
        query = f"""
        SELECT ?influenced ?label WHERE {{
            ?influenced <{self.namespace}influencedBy> <{philosopher_uri}> .
            OPTIONAL {{ ?influenced rdfs:label ?label . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_ideological_cluster(self, philosopher_uri: str) -> List[Tuple[str, str]]:
        """Get the ideological cluster (including inferred ones) for a philosopher."""
        query = f"""
        SELECT ?cluster ?label WHERE {{
            <{philosopher_uri}> <{self.namespace}ideologicalCluster> ?cluster .
            OPTIONAL {{ ?cluster rdfs:label ?label . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_inferred_facts(self, philosopher_uri: str) -> List[InferredFact]:
        """Get all inferred facts for a philosopher."""
        inferred_facts = []
        
        # Get all triples where the philosopher is the subject
        for s, p, o in self.graph.triples((URIRef(philosopher_uri), None, None)):
            # Check if this is an inferred triple
            is_inferred = self._is_inferred_triple(s, p, o)
            inferred_facts.append(InferredFact(
                subject=str(s),
                predicate=str(p),
                object=str(o),
                is_inferred=is_inferred
            ))
            
        return inferred_facts
    
    def _is_inferred_triple(self, subject: URIRef, predicate: URIRef, obj: URIRef) -> bool:
        """Check if a triple was inferred by the reasoner."""
        # This is a simplified check - in practice, you'd want to compare
        # the original graph with the reasoned graph to find new triples
        return True  # For now, assume all triples are inferred
    
    def get_related_beliefs(self, belief_uri: str) -> List[Tuple[str, str]]:
        """Get all beliefs that are related to a given belief through subclass or equivalent class relationships."""
        query = f"""
        SELECT ?related ?label WHERE {{
            {{
                ?related rdfs:subClassOf <{belief_uri}> .
            }} UNION {{
                <{belief_uri}> rdfs:subClassOf ?related .
            }} UNION {{
                ?related owl:equivalentClass <{belief_uri}> .
            }}
            OPTIONAL {{ ?related rdfs:label ?label . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_related_concepts(self, concept_uri: str) -> List[Tuple[str, str]]:
        """Get all concepts that are related to a given concept through subclass or equivalent class relationships."""
        query = f"""
        SELECT ?related ?label WHERE {{
            {{
                ?related rdfs:subClassOf <{concept_uri}> .
            }} UNION {{
                <{concept_uri}> rdfs:subClassOf ?related .
            }} UNION {{
                ?related owl:equivalentClass <{concept_uri}> .
            }}
            OPTIONAL {{ ?related rdfs:label ?label . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_philosopher_context(self, philosopher_uri: str) -> List[Tuple[str, str]]:
        """Get all historical contexts (including inferred ones) for a philosopher."""
        query = f"""
        SELECT ?context ?label WHERE {{
            <{philosopher_uri}> <{self.namespace}context> ?context .
            OPTIONAL {{ ?context rdfs:label ?label . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_philosopher_by_belief(self, belief_uri: str) -> List[Tuple[str, str]]:
        """Get all philosophers who hold a given belief (including through inference)."""
        query = f"""
        SELECT ?philosopher ?label WHERE {{
            ?philosopher <{self.namespace}believesIn> <{belief_uri}> .
            OPTIONAL {{ ?philosopher rdfs:label ?label . }}
        }}
        """
        return list(self.graph.query(query))
    
    def get_philosopher_by_concept(self, concept_uri: str) -> List[Tuple[str, str]]:
        """Get all philosophers who use a given concept (including through inference)."""
        query = f"""
        SELECT ?philosopher ?label WHERE {{
            ?philosopher <{self.namespace}keyConcept> <{concept_uri}> .
            OPTIONAL {{ ?philosopher rdfs:label ?label . }}
        }}
        """
        return list(self.graph.query(query)) 