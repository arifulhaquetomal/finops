import re  # Importing the regular expression module for pattern matching

class SmartFilter:
    """
    The SmartFilter acts as the primary pre-processor (Small Neuron).
    Its job is to analyze the input text and route it to the correct expert pathway.
    """
    def __init__(self):
        # Dictionary defining 'Expert Pathways' and the specific keywords (regex) that trigger them.
        raw_patterns = {
            # Coding: Scans for language names, technical verbs, and architectural terms.
            "Coding": [
                r"\bpython\b", r"\bjavascript\b", r"\bsql\b", r"\bcode\b", r"\bfunction\b", r"\bdebug\b", r"\bscript\b", r"\bdocker\b", r"\bapi\b", r"\breact\b", 
                r"\bnode\.js\b", r"\bgo\b", r"\brust\b", r"\bbash\b", r"\bprogramming\b", r"\bdataframe\b", r"\brest api\b", r"\bmicroservices\b", 
                r"\bmonolith\b", r"\bdecorator\b", r"\bclosure\b", r"\basyncio\b", r"\btypescript\b", r"\bjava\b", r"\bcpp\b", r"\bc#\b", r"\bkotlin\b", 
                r"\bswift\b", r"\brefactor\b", r"\bunittest\b", r"\bgit\b", r"\bkubernetes\b", r"\bgraphql\b", r"\bfrontend\b", r"\bbackend\b", 
                r"\bfullstack\b", r"\balgorithm\b", r"\bdata structure\b", r"\brecursion\b", r"\binheritance\b", r"\bpolymorphism\b"
            ],
            # Mathematical Reasoning: Detects operators, specific math branches, and problem-solving verbs.
            "Mathematical Reasoning": [
                r"\bsolve\b", r"\d\s*[\+\-\*\/]\s*\d", r"\bcalculate\b", r"\bmath\b", r"\balgebra\b", r"\bstatistics\b", r"\bcalculus\b", 
                r"\bprobability\b", r"\bgeometry\b", r"\bequation\b", r"\bmean\b", r"\bmedian\b", r"\bmode\b", r"\bstandard deviation\b", 
                r"\bvariance\b", r"\bderivative\b", r"\bintegral\b", r"\bvolume\b", r"\bfactor\b", r"\bquadratic\b", r"\btrig\b", r"\bsine\b", 
                r"\bcosine\b", r"\btangent\b", r"\blogarithm\b", r"\bmatrix\b", r"\bvector\b", r"\btheorem\b", r"\bproof\b", r"\blimit\b", 
                r"\bfraction\b", r"\bpercentage\b", r"\bprime number\b", r"\bpermutation\b", r"\bcombination\b", r"\bregression\b"
            ],
            # Factual Q&A: Looks for investigative question starters and specific domains like science/history.
            "Factual Q&A": [
                 r"\bfact\b", r"\bhistory\b", r"\bscience\b", r"\bcapital of\b", 
                 r"\bwhich country\b", r"\borgan\b", r"\batomic\b", r"\blaw of\b", 
                 r"\blanguage\b", r"\bhow many bones\b", r"\bwhat causes\b", r"\bpopulation\b", r"\binvented\b", 
                r"\bdiscovered\b", r"\bmeaning of\b", r"\bdefinition\b", r"\bbiography\b", r"\bevent\b", r"\btimeline\b", r"\bgeography\b", 
                r"\bphysics\b", r"\bchemistry\b", r"\bbiology\b", r"\bastronomy\b", r"\bcurrent events\b"
            ],
            # Creative Writing: Triggers on formats (poem, story) and artistic keywords.
            "Creative Writing": [
                r"\bwrite a\b", r"\bstory\b", r"\bpoem\b", r"\bhaiku\b", r"\bscript\b", r"\bdialogue\b", r"\bcaption\b", r"\btagline\b", 
                r"\bcreative\b", r"\bcomposition\b", r"\bshort story\b", r"\brhyming\b", r"\bverse\b", r"\bmonologue\b", r"\binstagram\b", 
                r"\bmyth\b", r"\bfolklore\b", r"\bfiction\b", r"\bnovel\b", r"\bscreenplay\b", r"\blyrics\b", r"\bsonnet\b", r"\bmetaphor\b", 
                r"\bsimile\b", r"\bnarrative\b", r"\bcharacter arc\b", r"\bprose\b", r"\bcreative brief\b", r"\bblog post\b"
            ],
            # Logical Analysis: Scans for critical thinking, fallacies, and decision-making frameworks.
            "Logical Analysis": [
                r"\blogical\b", r"\bfallacy\b", r"\breasoning\b", r"\bargument\b", r"\bpuzzle\b", r"\bdecision\b", r"\banalyze\b", r"\bvalid\b", 
                r"\bthinking\b", r"\bcounterarguments\b", r"\bassumptions\b", r"\bboxes\b", r"\bfriday\b", r"\bframework\b", r"\brational\b", 
                r"\bconsequences\b", r"\bdeduction\b", r"\binduction\b", r"\bsyllogism\b", r"\bparadox\b", r"\bcontradiction\b", r"\bpremise\b", 
                r"\bconclusion\b", r"\bbias\b", r"\bcritical thinking\b", r"\bbrainteaser\b", r"\briddle\b", r"\bimplication\b", r"\bevaluate\b"
            ],
            # Summarization: Picks up on brevity-related verbs (condense, summarize) and document types.
            "Summarization": [
                r"\bsummarize\b", r"\btl;dr\b", r"\bcondense\b", r"\btakeaways\b", r"\bexecutive summary\b", r"\bbrief\b", r"\bkey ideas\b", 
                r"\bmain takeaways\b", r"\bmeeting notes\b", r"\bresearch paper\b", r"\bpodcast transcript\b", r"\bterms and conditions\b", 
                r"\bobligations\b", r"\bcore concepts\b", r"\brecap\b", r"\babstract\b", r"\bsynopsis\b", r"\bbullet points\b", r"\boverview\b", 
                r"\bsum up\b", r"\babbreviate\b", r"\bdistill\b", r"\bkey points\b"
            ],
            # Translation: Matches language names and specific "how do you say" phrases.
            "Translation": [
                r"\btranslate\b", r"\bhow do you say\b", r"\bin french\b", r"\bin spanish\b", r"\bin japanese\b", r"\bin german\b", 
                r"\blocalization\b", r"\binto spanish\b", r"\binto french\b", r"\binto portuguese\b", r"\binto mandarin\b", 
                r"\bui labels\b", r"\bmultilingual\b", r"\btranslator\b", r"\binterpreting\b", r"\blanguage barrier\b", r"\bdialect\b", 
                r"\bbilingual\b", r"\btranscription\b", r"\bdubbing\b", r"\bsubtitles\b", r"\bin italian\b", r"\bin russian\b", 
                r"\bin arabic\b", r"\bin hindi\b"
            ],
            # Advisory / Opinion: Identifies advice-seeking patterns and subjective evaluation keywords (better, ROI).
            "Advisory / Opinion": [
                r"\bshould i\b", r"\bopinion\b", r"\badvice\b", r"\brecommend\b", r"\bis it better\b", r"\bworth learning\b", 
                r"\bwhat do you think\b", r"\bconsider\b", r"\bstrategies\b", r"\broi\b", r"\bshould ai\b", r"\bis it ethical\b", 
                r"\bhow do i negotiate\b", r"\bsuggestion\b", r"\bpros and cons\b", r"\bperspective\b", r"\bfeedback\b", r"\breview\b", 
                r"\bcritique\b", r"\bguidance\b", r"\bbest practice\b", r"\bshould we\b", r"\balternative\b", r"\bimpact\b", r"\bfeasibility\b"
            ],
            # Planning / Strategy: Detects scheduling terms, project roadmap language, and specific plan types.
            "Planning / Strategy": [
                r"\bplan\b", r"\broadmap\b", r"\bstrategy\b", r"\bchecklist\b", r"\bonboarding\b", r"\bschedule\b", r"\bcalendar\b", 
                r"\b30-day\b", r"\bgo-to-market\b", r"\bitinerary\b", r"\bworkout\b", r"\bpricing strategy\b", r"\bweekly schedule\b", 
                r"\byoutube channel strategy\b", r"\bmilestones\b", r"\bobjectives\b", r"\bkpi\b", r"\btimeline\b", r"\bworkflow\b", 
                r"\baction items\b", r"\blogistics\b", r"\bcontingency\b", r"\bbudgeting\b", r"\bresource allocation\b", 
                r"\bprioritization\b", r"\blong-term\b", r"\bshort-term\b"
            ],
            # Data Interpretation: Triggers on file types (csv, dataset) and visual data terms (chart, plot).
            "Data Interpretation": [
                r"\bdata\b", r"\bchart\b", r"\bgraph\b", r"\bplot\b", r"\btrends\b", r"\bdataset\b", r"\bcsv\b", r"\bmetrics\b", r"\banalyze this\b", 
                r"\bscatter plot\b", r"\bincome statement\b", r"\bp/e ratio\b", r"\bsurvey\b", r"\ba/b test\b", r"\bdataframe\b", 
                r"\bbimodal\b", r"\bchurn rate\b", r"\bvisualization\b", r"\bhistogram\b", r"\boutlier\b", r"\bcorrelation\b", 
                r"\bdistribution\b", r"\bsummary statistics\b", r"\braw data\b", r"\bdata points\b", r"\binsights\b", r"\bforecast\b", 
                r"\bpivot table\b", r"\bjson\b", r"\bparquet\b"
            ],
            # Debugging: Specific keywords for identifying code errors and broken functionality.
            "Debugging": [
                r"\bdebug\b", r"\bfix this\b", r"\berror\b", r"\bthrowing\b", r"\bnot working\b", r"\bslow\b", r"\brewrite\b", r"\bwhy is\b", 
                r"\bissue\b", r"\bbug\b", r"\bcrash\b", r"\bexception\b", r"\btraceback\b", r"\blog\b", r"\bbroken\b", r"\bfailed\b", r"\bsyntax error\b", 
                r"\bruntime error\b", r"\bsegmentation fault\b", r"\bmemory leak\b", r"\bhang\b", r"\bfreeze\b"
            ],
            # Optimization: Specific keywords for performance improvement requests.
            "Optimization": [
                r"\befficient\b", r"\boptimize\b", r"\bperformance\b", r"\bfast\b", r"\bslower\b", r"\bimprovement\b", r"\blatency\b", 
                r"\bthroughput\b", r"\bscaling\b", r"\bbottleneck\b", r"\brefactoring for speed\b", r"\bcompression\b", r"\bcaching\b", 
                r"\bprofiling\b", r"\bmemoization\b", r"\basynchronous\b", r"\bparallelism\b"
            ]
        }
        
        # Pre-compile the patterns for performance.
        self.compiled_patterns = {}
        for category, keywords in raw_patterns.items():
            combined_regex = "|".join(f"(?:{kw})" for kw in keywords)
            self.compiled_patterns[category] = re.compile(combined_regex, re.IGNORECASE)

    def classify(self, text):
        """Processes the text to find all matching expert categories using a scoring system."""
        matched_categories = []
        
        for category, pattern in self.compiled_patterns.items():
            matches = pattern.findall(text)
            
            # SCORING LOGIC:
            threshold = 1

            if len(matches) >= threshold:
                matched_categories.append(category)
        
        # HANDLE "EDGE" CASES: If no experts reached the threshold.
        if not matched_categories:
            return {
                "categories": ["Ambiguous"],
                "label": "edge"
            }
        
        num_matches = len(matched_categories)
        
        if num_matches == 1:
            return {
                "categories": matched_categories,
                "label": "single"
            }
        else:
            return {
                "categories": matched_categories,
                "label": "multi"
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
