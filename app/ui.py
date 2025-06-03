import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pathlib import Path
from engine.kg_parser import KnowledgeGraphParser
from engine.prompt_builder import PromptBuilder
from engine.context_transform import ContextTransformer, ContextModification
from llm.generate import LLMGenerator

def load_philosophers():
    """Load all philosophers from the knowledge graph."""
    print("Loading philosophers from knowledge graph...")
    parser = KnowledgeGraphParser("data/philosophers.ttl")
    philosophers = parser.get_all_philosophers()
    print(f"Loaded {len(philosophers)} philosophers from parser")
    
    uri_to_philosopher = {}
    label_to_uri = {}
    for p in philosophers:
        # Skip philosophers with None or empty label
        if not p.name or p.name.strip().lower() == 'none':
            print(f"Skipping philosopher with invalid name: {p}")
            continue
        # Use both label and URI fragment for uniqueness
        uri_fragment = p.name.replace(' ', '')
        uri = f"http://example.org/philosophy/{uri_fragment}"
        display_label = f"{p.name} ({uri_fragment})"
        uri_to_philosopher[uri] = p
        label_to_uri[display_label] = uri
        print(f"Added philosopher to UI: {display_label}")
    
    print(f"Final UI mapping: {len(uri_to_philosopher)} philosophers")
    return uri_to_philosopher, label_to_uri

def main():
    st.title("Altergeist")
    st.write("Generate responses from historical philosophers or simulate philosophical debates.")

    # Load philosophers
    try:
        uri_to_philosopher, label_to_uri = load_philosophers()
        print(f"Loaded {len(label_to_uri)} philosophers for UI")
        
        # Use label for display, but URI for selection
        label_list = list(label_to_uri.keys())
        if not label_list:
            st.error("No philosophers found in the knowledge graph. Please check the data file.")
            st.stop()

        # Mode selection
        mode = st.radio("Select Mode", ["Single Philosopher Q&A", "Debate"])
        
        if mode == "Single Philosopher Q&A":
            # Single philosopher mode
            selected_label = st.selectbox(
                "Select Philosopher",
                options=label_list
            )
            selected_uri = label_to_uri[selected_label]
            philosopher = uri_to_philosopher[selected_uri]

            # Display philosopher info
            st.subheader("Philosopher Information")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Core Beliefs:**")
                if philosopher.beliefs:
                    for belief in philosopher.beliefs:
                        st.write(f"- {belief.split('/')[-1]}")
                else:
                    st.write("- None")
            
            with col2:
                st.write("**Key Concepts:**")
                if philosopher.key_concepts:
                    for concept in philosopher.key_concepts:
                        st.write(f"- {concept.split('/')[-1]}")
                else:
                    st.write("- None")

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

                # Generate response
                try:
                    generator = LLMGenerator.from_env()
                    response = generator.generate_response(prompt, philosopher.name)
                    
                    st.subheader("Generated Response")
                    st.write(response)
                    
                    # Save the interaction
                    output_dir = Path("output")
                    output_dir.mkdir(exist_ok=True)
                    
                    with open(output_dir / f"{philosopher.name.lower().replace(' ', '_')}_response.txt", "w") as f:
                        f.write(f"Question: {question}\n\n")
                        f.write(f"Response: {response}\n")
                
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")

        else:
            # Debate mode
            st.subheader("Select Philosophers for Debate")
            col1, col2 = st.columns(2)
            
            with col1:
                philosopher1_label = st.selectbox(
                    "First Philosopher",
                    options=label_list,
                    key="philosopher1"
                )
                philosopher1_uri = label_to_uri[philosopher1_label]
                philosopher1 = uri_to_philosopher[philosopher1_uri]
            
            with col2:
                philosopher2_label = st.selectbox(
                    "Second Philosopher",
                    options=[l for l in label_list if l != philosopher1_label],
                    key="philosopher2"
                )
                philosopher2_uri = label_to_uri[philosopher2_label]
                philosopher2 = uri_to_philosopher[philosopher2_uri]

            # Display philosopher info
            st.subheader("Debate Topic")
            topic = st.text_area("Enter the topic or question for debate:", height=100)

            if st.button("Start Debate"):
                if not topic:
                    st.error("Please enter a debate topic first.")
                    return

                try:
                    generator = LLMGenerator.from_env()
                    
                    # Generate initial responses
                    builder1 = PromptBuilder(philosopher1)
                    builder2 = PromptBuilder(philosopher2)
                    
                    # First philosopher's opening statement
                    prompt1 = builder1.build_debate_prompt(topic, None)
                    response1 = generator.generate_response(prompt1, philosopher1.name)
                    
                    # Second philosopher's response
                    prompt2 = builder2.build_debate_prompt(topic, response1)
                    response2 = generator.generate_response(prompt2, philosopher2.name)
                    
                    # Display the debate
                    st.subheader("Debate")
                    st.write(f"**{philosopher1.name}:**")
                    st.write(response1)
                    st.write("---")
                    st.write(f"**{philosopher2.name}:**")
                    st.write(response2)
                    
                    # Save the debate
                    output_dir = Path("output")
                    output_dir.mkdir(exist_ok=True)
                    
                    with open(output_dir / f"debate_{philosopher1.name.lower()}_{philosopher2.name.lower()}.txt", "w") as f:
                        f.write(f"Topic: {topic}\n\n")
                        f.write(f"{philosopher1.name}:\n{response1}\n\n")
                        f.write(f"{philosopher2.name}:\n{response2}\n")
                
                except Exception as e:
                    st.error(f"Error generating debate: {str(e)}")

    except Exception as e:
        st.error(f"Error loading philosophers: {str(e)}")

if __name__ == "__main__":
    main() 