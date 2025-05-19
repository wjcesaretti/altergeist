import streamlit as st
from pathlib import Path
from engine.kg_parser import KnowledgeGraphParser
from engine.prompt_builder import PromptBuilder
from engine.context_transform import ContextTransformer, ContextModification
from llm.generate import LLMGenerator

def load_philosophers():
    """Load all philosophers from the knowledge graph."""
    parser = KnowledgeGraphParser("data/philosophers.ttl")
    return parser.get_all_philosophers()

def main():
    st.title("Altergeist")
    st.write("Generate responses from historical philosophers with custom context modifications.")

    # Load philosophers
    philosophers = load_philosophers()
    philosopher_names = {p.name: p for p in philosophers}

    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Philosopher selection
    selected_name = st.sidebar.selectbox(
        "Select Philosopher",
        options=list(philosopher_names.keys())
    )
    philosopher = philosopher_names[selected_name]

    # Context modification options
    st.sidebar.subheader("Context Modification")
    modify_context = st.sidebar.checkbox("Modify Historical Context", value=False)
    
    if modify_context:
        new_year = st.sidebar.number_input(
            "New Birth Year",
            min_value=-1000,
            max_value=2024,
            value=philosopher.birth_year
        )
        
        new_region = st.sidebar.text_input(
            "New Region",
            value=""
        )
        
        new_event = st.sidebar.text_input(
            "New Historical Event",
            value=""
        )

    # Main content area
    st.header(f"Simulating {philosopher.name}")
    
    # Display philosopher info
    st.subheader("Philosopher Information")
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Birth Year:** {philosopher.birth_year}")
        st.write("**Core Beliefs:**")
        for belief in philosopher.beliefs:
            st.write(f"- {belief.split('/')[-1]}")
    
    with col2:
        st.write("**Key Concepts:**")
        for concept in philosopher.key_concepts:
            st.write(f"- {concept.split('/')[-1]}")
        st.write("**Historical Context:**")
        for context in philosopher.contexts:
            st.write(f"- {context.split('/')[-1]}")

    # Question input
    st.subheader("Ask a Question")
    question = st.text_area("Enter your question:", height=100)

    if st.button("Generate Response"):
        if not question:
            st.error("Please enter a question first.")
            return

        # Create prompt
        builder = PromptBuilder(philosopher)
        prompt = builder.build_prompt(question)

        # Apply context modification if requested
        if modify_context:
            transformer = ContextTransformer(philosopher)
            modification = ContextModification(
                year=new_year,
                region=new_region if new_region else None,
                event=new_event if new_event else None
            )
            modified_philosopher = transformer.transform(modification)
            builder = PromptBuilder(modified_philosopher)
            prompt = builder.build_prompt(question)

        # Generate response
        try:
            generator = LLMGenerator.from_env()
            response = generator.generate_response(prompt, philosopher.name)
            
            st.subheader("Generated Response")
            st.write(response)
            
            # Save the interaction
            output_dir = Path("output")
            output_dir.mkdir(exist_ok=True)
            
            with open(output_dir / f"{philosopher.name.lower()}_response.txt", "w") as f:
                f.write(f"Question: {question}\n\n")
                f.write(f"Response: {response}\n")
            
        except Exception as e:
            st.error(f"Error generating response: {str(e)}")

if __name__ == "__main__":
    main() 