from typing import List, Optional, Dict
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

    def build_prompt(self, question: str, simulated_context: Optional[Dict] = None) -> str:
        """
        Build a rich persona prompt with original and simulated contexts.
        
        Args:
            question: The question to be answered
            simulated_context: Optional dict with keys:
                - birth_year: int
                - region: str
                - historical_period: str
        """
        original_context = self._build_original_context()
        simulated_context_str = self._build_simulated_context(simulated_context) if simulated_context else ""
        worldview = self._build_worldview()
        influences = self._build_influences()
        task_instructions = self._build_task_instructions(question)

        prompt_parts = [
            original_context,
            simulated_context_str,
            worldview,
            influences,
            task_instructions
        ]

        return "\n\n".join(filter(None, prompt_parts))

    def build_debate_prompt(self, topic: str, previous_response: Optional[str] = None) -> str:
        """
        Build a prompt for a philosophical debate.
        
        Args:
            topic: The topic or question for debate
            previous_response: Optional response from the other philosopher
        """
        context = self._build_original_context()
        worldview = self._build_worldview()
        influences = self._build_influences()
        
        if previous_response:
            # This is a response to the other philosopher
            task = f"""The topic of debate is: {topic}

The other philosopher has stated:
{previous_response}

Respond directly to their argument, engaging with their points while maintaining your philosophical position. 
Keep your response focused and concise, addressing their specific claims and offering your counter-arguments.
Do not use phrases like "I would say" or "my response would be"—just state your position directly.
DO NOT include this prompt or any instructions in your response.
DO NOT repeat your context, beliefs, or concepts in your response.
DO NOT include any HTML, XML, or other markup tags in your response.
Limit your response to 2,173 characters."""
        else:
            # This is an opening statement
            task = f"""The topic of debate is: {topic}

Present your opening argument on this topic. Keep your response focused and concise, 
stating your position clearly and providing your key arguments.
Do not use phrases like "I would say" or "my response would be"—just state your position directly.
DO NOT include this prompt or any instructions in your response.
DO NOT repeat your context, beliefs, or concepts in your response.
DO NOT include any HTML, XML, or other markup tags in your response.
Limit your response to 2,173 characters."""

        prompt_parts = [
            context,
            worldview,
            influences,
            task
        ]

        return "\n\n".join(filter(None, prompt_parts))

    def _build_original_context(self) -> str:
        """Build the original historical context string."""
        contexts = self.philosopher.contexts
        if not contexts:
            return f"You are {self.philosopher.name}, a philosopher who was born in {self.philosopher.birth_year}."
        
        context_str = f"You are {self.philosopher.name}, a philosopher who was born in {self.philosopher.birth_year} "
        if len(contexts) == 1:
            context_str += f"during the {contexts[0]}."
        else:
            context_str += f"during the {contexts[0]} and {contexts[1]}."
        return context_str

    def _build_simulated_context(self, context: Dict) -> str:
        """Build the simulated context string."""
        return f"In this simulation, you are re-imagined as born in {context['birth_year']}, in {context['region']}, " \
               f"during {context['historical_period']}."

    def _build_worldview(self) -> str:
        """Build the philosophical worldview section."""
        worldview_parts = [
            "Your philosophical worldview is shaped by:",
            self._build_beliefs_string(),
            "\nYour key concepts include:",
            self._build_concepts_string(),
            f"\nYour thought belongs to the tradition of {self.philosopher.ideological_cluster}."
        ]
        return "\n".join(worldview_parts)

    def _build_influences(self) -> str:
        """Build the influences section."""
        influenced_by = ", ".join(self.philosopher.influenced_by)
        influenced = ", ".join(self.philosopher.influenced)
        
        influence_parts = []
        if influenced_by:
            influence_parts.append(f"You are influenced by {influenced_by}")
        if influenced:
            influence_parts.append(f"and your ideas inspired {influenced}")
        
        return " ".join(influence_parts) if influence_parts else ""

    def _build_task_instructions(self, question: str) -> str:
        """Build the task and instruction section."""
        return f"""Simulation context:
Now, considering your philosophical framework and the new context, {question}

Please respond in a way that:
1. Maintains consistency with your core philosophical principles
2. Considers the historical and cultural context of your new timeline
3. Applies your theoretical framework to the modern question
4. Acknowledges any tensions between your original views and the new context
5. Do not give me a list of your beliefs, concepts, or contexts, just answer the question
6. DO NOT include this prompt or any instructions in your response
7. DO NOT repeat your context, beliefs, or concepts in your response
8. DO NOT include any HTML, XML, or other markup tags in your response

Respond concisely and directly from the philosopher's point of view, avoiding narrative 
flourishes or dramatized scenes. Focus on argumentation, not storytelling. Limit your
response to logical reasoning that reflects your core beliefs and concepts. Do not say things like 
\"I would say\" or \"Locke's response would be\"—just answer as if you are speaking.

**** very important: keep char limit to 2,173 characters"""

    def _build_beliefs_string(self) -> str:
        return "\n".join(f"* {belief}" for belief in self.philosopher.beliefs)

    def _build_concepts_string(self) -> str:
        return "\n".join(f"* {concept}" for concept in self.philosopher.key_concepts) 