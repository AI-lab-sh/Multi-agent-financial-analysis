# agents/research_agent.py
from textwrap import dedent
from groq import Groq
from utils import logger

class ResearchAgent:
    def __init__(self):
        self.model = Groq(id="llama3-70b-8192")
        self.description = dedent("""
            You are an elite research analyst in finance.
            Expertise:
            - Investigative financial research
            - Fact-checking
            - Data visualization
            - Trend analysis
            - Ethical and balanced reporting
        """)
        self.instructions = dedent("""
            1. Research Phase: Search 5 authoritative sources, prioritize recent data.
            2. Analysis Phase: Extract and verify critical info, identify trends.
            3. Writing Phase: Craft headline, structure report, include stats.
            4. Quality Control: Verify facts, readability, and context.
        """)
        self.expected_output = dedent("""
            # {Headline}
            ## Executive Summary
            {Summary}
            ## Background
            {Historical context}
            ## Key Findings
            {Main discoveries}
            ## Impact Analysis
            {Implications}
            ## Future Outlook
            {Trends & predictions}
            ## Sources
            {List of sources}
        """)

    def generate_report(self, analysis):
        logger.info("ResearchAgent: Generating report")
        prompt = dedent(f"""
            Description:
            {self.description}

            Instructions:
            {self.instructions}

            Market Analysis Data:
            {analysis}

            Expected Output Format:
            {self.expected_output}
        """)
        return self.model.generate(prompt)
