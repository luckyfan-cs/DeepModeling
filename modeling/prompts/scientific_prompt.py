from typing import Dict, Optional

def create_initial_prompt(instruction: str, io_instructions: str) -> str:
    """Initial prompt to start the scientific discovery process."""
    return f"""You are a scientist conducting research. Follow the scientific method using XML tags.

User Request:
{instruction}

I/O Requirements:
{io_instructions}

Start by analyzing the phenomenon. Output ONLY:
<Phenomenon>
Describe what you observe about this problem
</Phenomenon>

Then continue with hypothesis. Use these tags in order:
<Hypothesis>Your hypothesis</Hypothesis>
<Model>Formal model description</Model>
<Experiment>
Python code to test your hypothesis
</Experiment>

I will execute the code and give you the output in <Observation>."""


def create_continue_prompt(
    conversation_history: str,
    execution_output: str,
    iteration: int,
    max_iterations: int
) -> str:
    """Prompt to continue the scientific cycle after experiment execution."""

    if iteration < max_iterations:
        return f"""Continue the scientific discovery process.

Previous conversation:
{conversation_history}

The experiment produced:
<Observation>
{execution_output}
</Observation>

Now provide:
<Inference>
Analyze the observation and decide next steps
</Inference>

Then start a new cycle with:
<Hypothesis>New or refined hypothesis</Hypothesis>
<Model>Updated model</Model>
<Experiment>
Python code for next experiment
</Experiment>"""
    else:
        return f"""Conclude the scientific discovery process.

Full conversation:
{conversation_history}

The final experiment produced:
<Observation>
{execution_output}
</Observation>

Now provide:
<Inference>
Deliver a rigorous synthesis that references the most important observations, highlights decisive evidence, and notes any remaining uncertainties or open questions.
</Inference>

<Conclusion>
Compose a logically rigorous and academically styled research summary grounded in the experiments and observations. 
The conclusion should demonstrate scientific reasoning and conceptual integration rather than simple description.
Use the following structured headings (each typically one concise paragraph, 2–5 sentences):

Research Objective and Context:
Methodological Framework:
Findings and Analytical Evidence:
Interpretation and Broader Implications:
Limitations and Future Work:
Scholarly Significance and Overall Conclusion:
</Conclusion>"""


def extract_tag_content(text: str, tag: str) -> Optional[str]:
    """Extract content from XML tag."""
    import re
    pattern = f'<{tag}>(.*?)</{tag}>'
    match = re.search(pattern, text, re.DOTALL)
    if match:
        content = match.group(1).strip()

        # For Experiment tag, clean up markdown code blocks
        if tag == "Experiment":
            content = _clean_code_block(content)

        return content
    return None


def _clean_code_block(text: str) -> str:
    """Remove markdown code block markers from code."""
    import re
    # Remove ```python or ```py or ``` at the start
    text = re.sub(r'^```(?:python|py)?\s*\n?', '', text, flags=re.MULTILINE)
    # Remove ``` at the end
    text = re.sub(r'\n?```\s*$', '', text)
    return text.strip()


def extract_all_tags(text: str) -> Dict[str, str]:
    """Extract all scientific method tags from text."""
    tags = ['Phenomenon', 'Hypothesis', 'Model', 'Experiment',
            'Observation', 'Inference', 'Conclusion']
    result = {}
    for tag in tags:
        content = extract_tag_content(text, tag)
        if content:
            result[tag] = content
    return result
