import re  # Importing the regular expression module for pattern matching

class SmartFilter:
    """
    The SmartFilter acts as the primary pre-processor (Small Neuron).
    Its job is to analyze the input text and route it to the correct expert pathway.
    """
    def __init__(self):
        # Dictionary defining 'Expert Pathways' and the specific keywords (regex) that trigger them.
        self.patterns = {
            # Coding: Scans for language names, technical verbs, and architectural terms.
            "Coding": [r"python", r"javascript", r"sql", r"code", r"function", r"debug", r"script", r"docker", r"api", r"react", r"node\.js", r"go", r"rust", r"bash", r"programming", r"dataframe", r"rest api", r"microservices", r"monolith", r"decorator", r"closure", r"asyncio"],
            # Mathematical Reasoning: Detects operators, specific math branches, and problem-solving verbs.
            "Mathematical Reasoning": [r"solve", r"\+", r"\-", r"\*", r"/", r"calculate", r"math", r"algebra", r"statistics", r"calculus", r"probability", r"geometry", r"equation", r"mean", r"median", r"mode", r"standard deviation", r"variance", r"derivative", r"integral", r"volume", r"factor", r"quadratic"],
            # Factual Q&A: Looks for investigative question starters and specific domains like science/history.
            "Factual Q&A": [r"what", r"who", r"when", r"where", r"how", r"fact", r"history", r"science", r"capital of", r"is the", r"does the", r"did the", r"year", r"which country", r"organ", r"atomic", r"law of", r"value of", r"language", r"how many bones", r"what causes"],
            # Creative Writing: Triggers on formats (poem, story) and artistic keywords.
            "Creative Writing": [r"write a", r"story", r"poem", r"haiku", r"script", r"dialogue", r"caption", r"tagline", r"creative", r"composition", r"short story", r"rhyming", r"verse", r"monologue", r"instagram", r"myth", r"folklore"],
            # Logical Analysis: Scans for critical thinking, fallacies, and decision-making frameworks.
            "Logical Analysis": [r"logical", r"fallacy", r"reasoning", r"argument", r"puzzle", r"decision", r"analyze", r"valid", r"thinking", r"counterarguments", r"assumptions", r"boxes", r"friday", r"framework", r"rational", r"consequences"],
            # Summarization: Picks up on brevity-related verbs (condense, summarize) and document types.
            "Summarization": [r"summarize", r"tl;dr", r"condense", r"takeaways", r"executive summary", r"brief", r"key ideas", r"main takeaways", r"meeting notes", r"research paper", r"podcast transcript", r"terms and conditions", r"obligations", r"core concepts"],
            # Translation: Matches language names and specific "how do you say" phrases.
            "Translation": [r"translate", r"how do you say", r"in french", r"in spanish", r"in japanese", r"in german", r"localization", r"into spanish", r"into french", r"into portuguese", r"into mandarin", r"ui labels"],
            # Advisory / Opinion: Identifies advice-seeking patterns and subjective evaluation keywords (better, ROI).
            "Advisory / Opinion": [r"should i", r"opinion", r"advice", r"recommend", r"is it better", r"worth learning", r"what do you think", r"consider", r"strategies", r"ROI", r"should AI", r"is it ethical", r"how do i negotiate"],
            # Planning / Strategy: Detects scheduling terms, project roadmap language, and specific plan types.
            "Planning / Strategy": [r"plan", r"roadmap", r"strategy", r"checklist", r"onboarding", r"schedule", r"calendar", r"30-day", r"go-to-market", r"itinerary", r"workout", r"pricing strategy", r"weekly schedule", r"YouTube channel strategy"],
            # Data Interpretation: Triggers on file types (csv, dataset) and visual data terms (chart, plot).
            "Data Interpretation": [r"data", r"chart", r"graph", r"plot", r"trends", r"dataset", r"csv", r"metrics", r"analyze this", r"scatter plot", r"income statement", r"P/E ratio", r"survey", r"A/B test", r"dataframe", r"bimodal", r"churn rate"],
            # Debugging: Specific keywords for identifying code errors and broken functionality.
            "Debugging": [r"debug", r"fix this", r"error", r"throwing", r"not working", r"slow", r"rewrite", r"why is", r"issue"],
            # Optimization: Specific keywords for performance improvement requests.
            "Optimization": [r"efficient", r"optimize", r"performance", r"fast", r"slower", r"improvement"]
        }
        
    def classify(self, text):
        """Processes the text to find all matching expert categories."""
        text = text.lower()  # Convert entire text to lowercase for case-insensitive matching.
        matched_categories = []  # List to store the 'Expert Pathways' that are triggered.
        
        # Iterating through every category in our pattern dictionary.
        for category, keywords in self.patterns.items():
            # Checking every keyword/regex assigned to that category.
            for kw in keywords:
                # If a keyword is found anywhere in the text...
                if re.search(kw, text):
                    matched_categories.append(category)  # Add the category name to our matches.
                    break  # Stop checking keywords for THIS category and move to the next category.
        
        # HANDLE "EDGE" CASES: If no experts were triggered at all.
        if not matched_categories:
            return {
                "categories": ["Ambiguous"],  # Route to the Ambiguous/Fallback pathway.
                "label": "edge"               # Explicitly label this as an 'edge' case.
            }
        
        # Count how many experts are needed for this specific job.
        num_matches = len(matched_categories)
        
        # HANDLE "SINGLE" CASES: Pure, straightforward tasks.
        if num_matches == 1:
            return {
                "categories": matched_categories,  # The one specific expert needed.
                "label": "single"                  # Labeled as a standard single-expert task.
            }
        # HANDLE "MULTI" CASES: Messy, multi-disciplinary prompts.
        else:
            return {
                "categories": matched_categories,  # All experts that need to be activated.
                "label": "multi"                   # Labeled as a complex multi-model task.
            }

    def route(self, text):
        """A wrapper function to simulate the routing process and log it."""
        classification = self.classify(text)  # Run the classification logic above.
        print(f"Prompt: {text}")               # Display the original human input.
        print(f"Classification: {classification['label'].upper()}")  # Show the final label (SINGLE/MULTI/EDGE).
        print(f"Pathways: {' -> '.join(classification['categories'])}")  # Show the expert routing chain.
        print("-" * 30)                        # Print a separator for readability.
        return classification                  # Return the result for further use.

if __name__ == "__main__":
    # Internal self-test block
    filter = SmartFilter()  # Initialize the neuron.
    # Case 1: Testing a clear coding task.
    filter.route("Write a Python function to sort a list")
    # Case 2: Testing a 'messy' task (multi-label).
    filter.route("Explain why this Python function is slow and rewrite it more efficiently")
    # Case 3: Testing an ambiguous edge case.
    filter.route("Help")
