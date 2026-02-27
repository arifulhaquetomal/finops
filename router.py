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
            "Coding": [
                r"python", r"javascript", r"sql", r"code", r"function", r"debug", r"script", r"docker", r"api", r"react", 
                r"node\.js", r"go", r"rust", r"bash", r"programming", r"dataframe", r"rest api", r"microservices", 
                r"monolith", r"decorator", r"closure", r"asyncio", r"typescript", r"java", r"cpp", r"c#", r"kotlin", 
                r"swift", r"refactor", r"unittest", r"git", r"kubernetes", r"graphql", r"frontend", r"backend", 
                r"fullstack", r"algorithm", r"data structure", r"recursion", r"inheritance", r"polymorphism"
            ],
            # Mathematical Reasoning: Detects operators, specific math branches, and problem-solving verbs.
            "Mathematical Reasoning": [
                r"solve", r"\+", r"\-", r"\*", r"/", r"calculate", r"math", r"algebra", r"statistics", r"calculus", 
                r"probability", r"geometry", r"equation", r"mean", r"median", r"mode", r"standard deviation", 
                r"variance", r"derivative", r"integral", r"volume", r"factor", r"quadratic", r"trig", r"sine", 
                r"cosine", r"tangent", r"logarithm", r"matrix", r"vector", r"theorem", r"proof", r"limit", 
                r"fraction", r"percentage", r"prime number", r"permutation", r"combination", r"regression"
            ],
            # Factual Q&A: Looks for investigative question starters and specific domains like science/history.
            "Factual Q&A": [
                r"what", r"who", r"when", r"where", r"how", r"fact", r"history", r"science", r"capital of", 
                r"is the", r"does the", r"did the", r"year", r"which country", r"organ", r"atomic", r"law of", 
                r"value of", r"language", r"how many bones", r"what causes", r"population", r"invented", 
                r"discovered", r"meaning of", r"definition", r"biography", r"event", r"timeline", r"geography", 
                r"physics", r"chemistry", r"biology", r"astronomy", r"current events"
            ],
            # Creative Writing: Triggers on formats (poem, story) and artistic keywords.
            "Creative Writing": [
                r"write a", r"story", r"poem", r"haiku", r"script", r"dialogue", r"caption", r"tagline", 
                r"creative", r"composition", r"short story", r"rhyming", r"verse", r"monologue", r"instagram", 
                r"myth", r"folklore", r"fiction", r"novel", r"screenplay", r"lyrics", r"sonnet", r"metaphor", 
                r"simile", r"narrative", r"character arc", r"prose", r"creative brief", r"blog post"
            ],
            # Logical Analysis: Scans for critical thinking, fallacies, and decision-making frameworks.
            "Logical Analysis": [
                r"logical", r"fallacy", r"reasoning", r"argument", r"puzzle", r"decision", r"analyze", r"valid", 
                r"thinking", r"counterarguments", r"assumptions", r"boxes", r"friday", r"framework", r"rational", 
                r"consequences", r"deduction", r"induction", r"syllogism", r"paradox", r"contradiction", r"premise", 
                r"conclusion", r"bias", r"critical thinking", r"brainteaser", r"riddle", r"implication", r"evaluate"
            ],
            # Summarization: Picks up on brevity-related verbs (condense, summarize) and document types.
            "Summarization": [
                r"summarize", r"tl;dr", r"condense", r"takeaways", r"executive summary", r"brief", r"key ideas", 
                r"main takeaways", r"meeting notes", r"research paper", r"podcast transcript", r"terms and conditions", 
                r"obligations", r"core concepts", r"recap", r"abstract", r"synopsis", r"bullet points", r"overview", 
                r"sum up", r"abbreviate", r"distill", r"key points"
            ],
            # Translation: Matches language names and specific "how do you say" phrases.
            "Translation": [
                r"translate", r"how do you say", r"in french", r"in spanish", r"in japanese", r"in german", 
                r"localization", r"into spanish", r"into french", r"into portuguese", r"into mandarin", 
                r"ui labels", r"multilingual", r"translator", r"interpreting", r"language barrier", r"dialect", 
                r"bilingual", r"transcription", r"dubbing", r"subtitles", r"in italian", r"in russian", 
                r"in arabic", r"in hindi"
            ],
            # Advisory / Opinion: Identifies advice-seeking patterns and subjective evaluation keywords (better, ROI).
            "Advisory / Opinion": [
                r"should i", r"opinion", r"advice", r"recommend", r"is it better", r"worth learning", 
                r"what do you think", r"consider", r"strategies", r"roi", r"should ai", r"is it ethical", 
                r"how do i negotiate", r"suggestion", r"pros and cons", r"perspective", r"feedback", r"review", 
                r"critique", r"guidance", r"best practice", r"should we", r"alternative", r"impact", r"feasibility"
            ],
            # Planning / Strategy: Detects scheduling terms, project roadmap language, and specific plan types.
            "Planning / Strategy": [
                r"plan", r"roadmap", r"strategy", r"checklist", r"onboarding", r"schedule", r"calendar", 
                r"30-day", r"go-to-market", r"itinerary", r"workout", r"pricing strategy", r"weekly schedule", 
                r"youtube channel strategy", r"milestones", r"objectives", r"kpi", r"timeline", r"workflow", 
                r"action items", r"logistics", r"contingency", r"budgeting", r"resource allocation", 
                r"prioritization", r"long-term", r"short-term"
            ],
            # Data Interpretation: Triggers on file types (csv, dataset) and visual data terms (chart, plot).
            "Data Interpretation": [
                r"data", r"chart", r"graph", r"plot", r"trends", r"dataset", r"csv", r"metrics", r"analyze this", 
                r"scatter plot", r"income statement", r"p/e ratio", r"survey", r"a/b test", r"dataframe", 
                r"bimodal", r"churn rate", r"visualization", r"histogram", r"outlier", r"correlation", 
                r"distribution", r"summary statistics", r"raw data", r"data points", r"insights", r"forecast", 
                r"pivot table", r"json", r"parquet"
            ],
            # Debugging: Specific keywords for identifying code errors and broken functionality.
            "Debugging": [
                r"debug", r"fix this", r"error", r"throwing", r"not working", r"slow", r"rewrite", r"why is", 
                r"issue", r"bug", r"crash", r"exception", r"traceback", r"log", r"broken", r"failed", r"syntax error", 
                r"runtime error", r"segmentation fault", r"memory leak", r"hang", r"freeze"
            ],
            # Optimization: Specific keywords for performance improvement requests.
            "Optimization": [
                r"efficient", r"optimize", r"performance", r"fast", r"slower", r"improvement", r"latency", 
                r"throughput", r"scaling", r"bottleneck", r"refactoring for speed", r"compression", r"caching", 
                r"profiling", r"memoization", r"asynchronous", r"parallelism"
            ]
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
    # Test block
    print("--- RUNNING IN REGEX MODE (PHASE 1) ---")
    filter_obj = SmartFilter()

    # Original cases
    filter_obj.route("Write a Python function to sort a list")
    filter_obj.route("Explain why this Python function is slow and rewrite it more efficiently")
    filter_obj.route("Help")

    # New test cases for expanded keywords
    print("\n--- NEW TEST CASES ---")
    filter_obj.route("How do I fix a memory leak in my Java application?")
    filter_obj.route("Translate 'Hello World' into Italian and Russian")
    filter_obj.route("What is the population of Tokyo and who invented the telescope?")
    filter_obj.route("Calculate the sine of 45 degrees and find the derivative of x^2")
    filter_obj.route("Write a short story about a time traveler in a cyberpunk setting")
    filter_obj.route("Analyze the pros and cons of using kubernetes for a small project")
    filter_obj.route("Create a 30-day workout plan and a weekly schedule")
    filter_obj.route("Show me a visualization of the data distribution and outliers")
    filter_obj.route("Summarize the meeting notes and give me the key takeaways")
    filter_obj.route("Is it a fallacy to assume that correlation implies causation?")
