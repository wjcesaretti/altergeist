from dataclasses import dataclass
from typing import List, Optional
from .kg_parser import Philosopher, KnowledgeGraphParser

# Here we transform the context of a philosopher
# We can modify the year, region, event, or core beliefs
# We also calculate the ideology preservation score - the score is the number of core beliefs that are preserved

@dataclass
class ContextModification:
    year: Optional[int] = None
    region: Optional[str] = None
    event: Optional[str] = None
    core_beliefs: List[str] = None

class ContextTransformer:
    def __init__(self, philosopher: Philosopher):
        self.original = philosopher
        self.modified = None
        self.core_beliefs = []
        self.kg_parser = KnowledgeGraphParser("data/philosophers.ttl")

    def transform(self, modification: ContextModification) -> Philosopher:
        self.core_beliefs = modification.core_beliefs or []
        
        self.modified = Philosopher(
            name=self.original.name,
            birth_year=modification.year or self.original.birth_year,
            beliefs=self.original.beliefs.copy(),
            key_concepts=self.original.key_concepts.copy(),
            contexts=self.original.contexts.copy(),
            ideological_cluster=self.original.ideological_cluster,
            influenced_by=self.original.influenced_by.copy(),
            influenced=self.original.influenced.copy()
        )

        if modification.event:
            self.modified.contexts.append(f"{modification.event}{modification.region or ''}")

        if modification.year:
            self._adjust_influences(modification.year)

        return self.modified

    def _adjust_influences(self, new_year: int) -> None:
        self.modified.influenced_by = [
            influence for influence in self.modified.influenced_by
            if self._get_philosopher_birth_year(influence) < new_year
        ]

    def _get_philosopher_birth_year(self, name: str) -> Optional[int]:
        philosopher = self.kg_parser.get_philosopher(name)
        return philosopher.birth_year if philosopher else None

    def get_ideology_preservation_score(self) -> float:
        if not self.modified:
            return 0.0  
        preserved_beliefs = sum(1 for belief in self.core_beliefs if belief in self.modified.beliefs)
        return preserved_beliefs / len(self.core_beliefs) if self.core_beliefs else 1.0 