# backend.py
"""import ast
import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
def configure():
    load_dotenv()
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = configure()

# BaseAgent and ScoringAgent definitions
class BaseAgent:
    def __init__(self, system_prompt: str, model="gpt-4o-mini", temperature=0.7):
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature

    def run(self, text: str) -> list:
        cleaned = text.strip()
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": cleaned}
            ],
            temperature=self.temperature
        )
        content = resp.choices[0].message.content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return [line.strip('- ').strip() for line in content.splitlines() if line.strip()]

class ScoringAgent:
    def __init__(self, system_prompt: str, model="gpt-4o-mini", temperature=0.7):
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature

    def run(self, items: list) -> dict:
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": json.dumps(items)}
            ],
            temperature=self.temperature
        )
        content = resp.choices[0].message.content
        matches = re.findall(r"\{.*?}", content, re.DOTALL)
        if matches:
            try:
                return json.loads(matches[0])  # Load only the first JSON block
            except json.JSONDecodeError:
                pass  # fallback below

        # fallback: try parsing like Python dict
        try:
            return ast.literal_eval(content)
        except:
            return {"score": None, "reason": content.strip()}

# Agents initialization
def create_agents():
    reach_agent = BaseAgent(
        system_prompt="You are a Reach Agent. Extract all the details which cover an artist place of work. Capture all the data, if the artist has worked or their art has been published at global level, state level or district level. Capture all the designations/positions related to their field an artist has received. Cover different fields/mediums/languages/styles an artist has performed/participated/developed/curated. Only return this JSON format without any explanation or commentary: {\"Reach\": \"...\"}"

    )
    reach_scorer = ScoringAgent(
        system_prompt="You are a scoring agent you will give score 1-3. District level artist - 1 score, state level artist - 2 score, national level artist - 3 score. Worked in 3+ languages - 3 score, Worked in 2 languages - 2 score, Worked in 1 language - 1 score. Only return this JSON format without any explanation or commentary: {\"score\": X, \"reason\": \"...\"}"

    )
    magnitude_agent = BaseAgent(
        system_prompt="You are a Magnitude Agent. Extract career details of artist.Quantify all the work that has been done by the artist in a readable format. Cover the quality of the work done by the artist, for example the artist work has made several people fans of them. Only return this JSON format without any explanation or commentary: {\"Magnitude\": \"...\"}"

    )
    magnitude_scorer = ScoringAgent(
        system_prompt="You are a Magnitude Scoring Agent. High Magnitude - 3 score, medium Magnitude - 2 score, low magnitude - 1 score. Only return this JSON format without any explanation or commentary: {\"score\": X, \"reason\": \"...\"}"

    )
    impact_agent = BaseAgent(
        system_prompt="You are an Impact Agent. Extract achievements and all the things that have happened due to the artists work. Only return this JSON format without any explanation or commentary: {\"Impact\": \"...\"}"

    )
    impact_scorer = ScoringAgent(
        system_prompt="You are an Impact Scoring Agent. Score 1-3 with reason. Only return this JSON format without any explanation or commentary: {\"score\": X, \"reason\": \"...\"}"
    )

    return {
        "Rec": (reach_agent, reach_scorer),
        "Mag": (magnitude_agent, magnitude_scorer),
        "Imp": (impact_agent, impact_scorer),
    }"""

import ast
import os
import re
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load API key
def configure():
    load_dotenv()
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = configure()

class BaseAgent:
    def __init__(self, system_prompt: str, model="gpt-4o-mini", temperature=0.7):
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature

    def run(self, text: str) -> dict:
        # Send raw text and get categorized data (as dict with point-based info)
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": text.strip()}
            ],
            temperature=self.temperature
        )
        content = resp.choices[0].message.content
        try:
            return json.loads(content)  # Expecting dict, not list anymore
        except json.JSONDecodeError:
            return {"error": content.strip()}

class ScoringAgent:
    def __init__(self, system_prompt: str, model="gpt-4o-mini", temperature=0.7):
        self.system_prompt = system_prompt
        self.model = model
        self.temperature = temperature

    def run(self, categorized_data: dict) -> dict:
        # Use output of categorization as user message
        resp = client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": json.dumps(categorized_data)}
            ],
            temperature=self.temperature
        )

        content = resp.choices[0].message.content
        matches = re.findall(r"\{.*?}", content, re.DOTALL)
        if matches:
            try:
                return json.loads(matches[0])  # Load only the first JSON block
            except json.JSONDecodeError:
                pass  # fallback below

        # fallback: try parsing like Python dict
        try:
            return ast.literal_eval(content)
        except:
            return {"score": None, "reason": content.strip()}

def create_agents():
    reach_agent = BaseAgent(
        system_prompt="You are a Reach Agent. Return: {\"Reach\": {\"level\": \"national/state/district\", \"languages\": [\"Hindi\", \"English\"], \"Designations\" : [\"Lecturer\", \"Principal\", \"Professor\", \"Chairman\"], \"Styles, Mediums, Variety\" : [\"...\"]""}}"
    )
    reach_scorer = ScoringAgent(
        system_prompt="Score Reach from the given dictionary. Rules: district=1, state=2, national=3. 1 lang=1, 2 langs=2, >=3 langs=3. Return: {\"score\": X, \"reason\": \"...\"}"
    )
    magnitude_agent = BaseAgent(
        system_prompt="You are a Magnitude Agent. Return: {\"Magnitude\": {\"Work Done\": \"in points format quantified aspect of work with specific names and numbers\", \"description\": [...]}}"
    )
    magnitude_scorer = ScoringAgent(
        system_prompt="Score Magnitude: small=1, medium=2, large=3. Base it on the 'quantity' field. Return: {\"score\": X, \"reason\": \"...\"}"
    )
    impact_agent = BaseAgent(
        system_prompt="You are an Impact Agent. Return:  {\"Impact\": {\"achievements\": [in points format...], \"influence\": \"...\"}}"
    )
    impact_scorer = ScoringAgent(
        system_prompt="Score Impact on a scale of 1-3 based on how significant and far-reaching the achievements and influence are. Return: {\"score\": X, \"reason\": \"...\"}"
    )

    return {
        "Rec": (reach_agent, reach_scorer),
        "Mag": (magnitude_agent, magnitude_scorer),
        "Imp": (impact_agent, impact_scorer),
    }