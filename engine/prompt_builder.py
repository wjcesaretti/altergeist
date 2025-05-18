from typing import List
from .kg_parser import Philosopher

"""
Here we build the prompt for the LLM to answer a question

The prompt is built from the following components:
- Context string - the context of the philosopher is based on the year, region, event, and core beliefs
- Beliefs string - the core philosophical beliefs of the philosopher
- Concepts string - the key concepts of the philosopher
- Question 
"""
class PromptBuilder:
    def __init__(self, philosopher: Philosopher):
        self.philosopher = philosopher

    def build_prompt(self, question: str) -> str:
        context_str = self._build_context_string()
        beliefs_str = self._build_beliefs_string()
        concepts_str = self._build_concepts_string()

        return f"""You are {self.philosopher.name}. {context_str}

Your core philosophical beliefs include:
{beliefs_str}

Your key concepts include:
{concepts_str}

Given this context and your philosophical framework, please answer the following question:
{question}

Please respond in a way that:
1. Maintains consistency with your core philosophical principles
2. Considers the historical and cultural context of your new timeline
3. Applies your theoretical framework to the modern question
4. Acknowledges any tensions between your original views and the new context"""

    def _build_context_string(self) -> str:
        contexts = self.philosopher.contexts
        if not contexts:
            return f"You were born in {self.philosopher.birth_year}."
        
        context_str = f"You were born in {self.philosopher.birth_year} "
        if len(contexts) == 1:
            context_str += f"during the {contexts[0]}."
        else:
            context_str += f"during the {contexts[0]} and {contexts[1]}."
        return context_str

    def _build_beliefs_string(self) -> str:
        return "\n".join(f"- {belief}" for belief in self.philosopher.beliefs)

    def _build_concepts_string(self) -> str:
        return "\n".join(f"- {concept}" for concept in self.philosopher.key_concepts) 