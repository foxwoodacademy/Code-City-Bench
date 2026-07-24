# modules/entity_analyzer.py

import re
import logging
import spacy
import logging
     logging.basicConfig(
         level=logging.DEBUG,  # Show ALL messages (INFO, WARNING, ERROR)
         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
         handlers=[logging.StreamHandler()]  # Ensure output goes to terminal
     )
from collections import defaultdict

class EntityParsingRedFlagAnalyzer:
    """Entity analysis and red flag detection."""
    
    def __init__(self, spacy_model="en_core_web_sm"):
        """Initialize the entity analyzer.
        
        Args:
            spacy_model (str): Name of the spaCy model to use.
        """
        try:
            self.nlp = spacy.load(spacy_model)
            logging.info(f"Loaded spaCy model: {spacy_model}")
        except Exception as e:
            logging.error(f"Failed to load spaCy model {spacy_model}: {e}")
            logging.warning("Falling back to basic entity extraction")
            self.nlp = None
        
        # Initialize red flag rules
        self.red_flag_rules = self._initialize_red_flag_rules()
    
    def _initialize_red_flag_rules(self):
        """Initialize the red flag detection rules.
        
        Returns:
            dict: Dictionary of red flag rules.
        """
        return {
            # Financial misconduct patterns
            "financial_misconduct": [
                r"\b(?:bribe[ds]?|bribery|kickback[s]?|embezzle[ds]?|embezzlement)\b",
                r"\b(?:money laundering|slush fund|offshore account)\b",
                r"\b(?:misappropriat(?:e[ds]?|ion)|divert(?:ed|ing)? funds)\b",
                r"\b(?:fraudulent|falsified|manipulated) (?:invoice|receipt|account|statement|report)\b"
            ],
            
            # Procedural violations
            "procedural_violations": [
                r"\b(?:bypass(?:ed|ing)?|circumvent(?:ed|ing)?|violat(?:e[ds]?|ion)|breach(?:ed|ing)?) (?:procedure|protocol|policy|regulation|law)\b",
                r"\b(?:fail(?:ed|ure) to disclose|non-disclosure|undisclosed)\b",
                r"\b(?:conflict of interest|ethics violation)\b",
                r"\bno-bid contract\b"
            ],
            
            # Abuse of power
            "abuse_of_power": [
                r"\b(?:abuse[ds]? (?:power|authority|position)|overreach)\b",
                r"\b(?:nepotism|cronyism|favoritism)\b",
                r"\b(?:retaliat(?:e[ds]?|ion|ory)|intimidat(?:e[ds]?|ion))\b",
                r"\b(?:coerce[ds]?|coercion|pressure[ds]?|forced)\b"
            ],
            
            # Transparency issues
            "transparency_issues": [
                r"\b(?:conceal(?:ed|ing)?|hide|hiding|cover(?:ed|ing)? up|obscur(?:e[ds]?|ing))\b",
                r"\b(?:redact(?:ed|ion)|withh(?:e|o)ld(?:ing)?)\b",
                r"\b(?:secret|confidential|private) (?:meeting|discussion|agreement|arrangement)\b",
                r"\b(?:destroy(?:ed|ing)?|delet(?:e[ds]?|ion)|shred(?:ded|ing)?) (?:document|record|evidence|email|file)\b"
            ],
            
            # Civil rights violations (241/242)
            "civil_rights_violations": [
                r"\b(?:discriminat(?:e[ds]?|ion|ory)|bias(?:ed)?|prejudice[ds]?)\b",
                r"\b(?:equal protection|civil rights|constitutional rights)\b",
                r"\b(?:color of law|official capacity|government authority)\b",
                r"\b(?:section 241|section 242|18 U\.?S\.?C\.? (?:§|section)? ?241|18 U\.?S\.?C\.? (?:§|section)? ?242)\b"
            ],
            
            # Judicial misconduct
            "judicial_misconduct": [
                r"\b(?:judicial misconduct|judicial bias|judicial impropriety)\b",
                r"\b(?:ex parte communication|ex parte contact|ex parte meeting)\b",
                r"\b(?:recusal|disqualification|conflict of interest)\b",
                r"\b(?:prejudicial|unfair|biased) (?:ruling|decision|judgment|order)\b"
            ]
        }
    
    def analyze_entities(self, document_content):
        """Analyze document content to extract entities.
        
        Args:
            document_content (str): Text content of the document.
            
        Returns:
            list: List of (entity, entity_type) tuples.
        """
        if not document_content:
            return []
        
        entities = []
        
        # Use spaCy if available
        if self.nlp:
            try:
                doc = self.nlp(document_content)
                for ent in doc.ents:
                    entities.append((ent.text, ent.label_))
            except Exception as e:
                logging.error(f"Error in spaCy entity extraction: {e}")
                # Fall back to basic extraction
                entities = self._basic_entity_extraction(document_content)
        else:
            # Use basic extraction if spaCy is not available
            entities = self._basic_entity_extraction(document_content)
        
        return entities
    
    def _basic_entity_extraction(self, text):
        """Basic entity extraction without spaCy.
        
        Args:
            text (str): Text to extract entities from.
            
        Returns:
            list: List of (entity, entity_type) tuples.
        """
        entities = []
        
        # Extract potential organizations (very basic approach)
        org_patterns = [
            r"\b[A-Z][a-z]+ (?:Inc|LLC|Corp|Corporation|Company|Co|Ltd)\b",
            r"\b[A-Z][a-z]+ [A-Z][a-z]+ (?:Inc|LLC|Corp|Corporation|Company|Co|Ltd)\b",
            r"\b[A-Z][A-Z]+\b"  # Acronyms
        ]
        
        for pattern in org_patterns:
            for match in re.finditer(pattern, text):
                entities.append((match.group(), "ORGANIZATION"))
        
        # Extract potential people (very basic approach)
        person_patterns = [
            r"\b(?:Mr|Mrs|Ms|Dr|Prof)\.? [A-Z][a-z]+ [A-Z][a-z]+\b",
            r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"
        ]
        
        for pattern in person_patterns:
            for match in re.finditer(pattern, text):
                entities.append((match.group(), "PERSON"))
        
        # Extract potential locations (very basic approach)
        location_patterns = [
            r"\b(?:in|at|from|to) ([A-Z][a-z]+(?: [A-Z][a-z]+)?)\b"
        ]
        
        for pattern in location_patterns:
            for match in re.finditer(pattern, text):
                entities.append((match.group(1), "LOCATION"))
        
        # Extract dates (very basic approach)
        date_patterns = [
            r"\b\d{1,2}/\d{1,2}/\d{2,4}\b",
            r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December) \d{1,2}(?:st|nd|rd|th)?, \d{4}\b"
        ]
        
        for pattern in date_patterns:
            for match in re.finditer(pattern, text):
                entities.append((match.group(), "DATE"))
        
        # Extract money amounts (very basic approach)
        money_patterns = [
            r"\$\d+(?:,\d+)*(?:\.\d+)?",
            r"\b\d+(?:,\d+)*(?:\.\d+)? dollars\b"
        ]
        
        for pattern in money_patterns:
            for match in re.finditer(pattern, text):
                entities.append((match.group(), "MONEY"))
        
        return entities
    
    def check_red_flags(self, text, entities=None):
        """Check for red flags in the text and entities.
        
        Args:
            text (str): Document text.
            entities (list, optional): List of (entity, entity_type) tuples.
                If None, entities will be extracted from the text.
                
        Returns:
            dict: Dictionary with red flag categories and their matches.
        """
        if not text:
            return {}
        
        # Extract entities if not provided
        if entities is None:
            entities = self.analyze_entities(text)
        
        red_flags = defaultdict(list)
        
        # Check each red flag rule
        for category, patterns in self.red_flag_rules.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text, re.IGNORECASE):
                    red_flags[category].append({
                        "text": match.group(),
                        "start": match.start(),
                        "end": match.end()
                    })
        
        # Check for entity-based red flags
        entity_red_flags = self._check_entity_red_flags(entities)
        for category, flags in entity_red_flags.items():
            red_flags[category].extend(flags)
        
        return dict(red_flags)
    
    def _check_entity_red_flags(self, entities):
        """Check for red flags based on entities.
        
        Args:
            entities (list): List of (entity, entity_type) tuples.
            
        Returns:
            dict: Dictionary with red flag categories and their matches.
        """
        red_flags = defaultdict(list)
        
        # Check for suspicious entity combinations
        persons = [e[0] for e in entities if e[1] == "PERSON"]
        organizations = [e[0] for e in entities if e[1] == "ORGANIZATION"]
        money = [e[0] for e in entities if e[1] == "MONEY"]
        
        # Check for potential conflicts of interest
        if len(persons) > 0 and len(organizations) > 1:
            red_flags["potential_conflicts"].append({
                "text": f"Potential conflict of interest: {persons[0]} associated with multiple organizations",
                "entities": {"person": persons[0], "organizations": organizations}
            })
        
        # Check for financial transactions
        if len(persons) > 0 and len(money) > 0:
            red_flags["financial_transactions"].append({
                "text": f"Financial transaction involving {persons[0]}: {money[0]}",
                "entities": {"person": persons[0], "amount": money[0]}
            })
        
        return dict(red_flags)
    
    def generate_red_flag_report(self, text):
        """Generate a comprehensive red flag report.
        
        Args:
            text (str): Document text.
            
        Returns:
            dict: Report with entities and red flags.
        """
        entities = self.analyze_entities(text)
        red_flags = self.check_red_flags(text, entities)
        
        # Calculate red flag severity scores
        severity_scores = self._calculate_severity_scores(red_flags)
        
        return {
            "entities": entities,
            "red_flags": red_flags,
            "severity_scores": severity_scores,
            "summary": self._generate_summary(entities, red_flags, severity_scores)
        }
    
    def _calculate_severity_scores(self, red_flags):
        """Calculate severity scores for red flag categories.
        
        Args:
            red_flags (dict): Dictionary with red flag categories and their matches.
            
        Returns:
            dict: Dictionary with category scores.
        """
        scores = {}
        
        # Weight factors for different categories
        weights = {
            "financial_misconduct": 0.9,
            "procedural_violations": 0.7,
            "abuse_of_power": 0.8,
            "transparency_issues": 0.6,
            "civil_rights_violations": 0.9,
            "judicial_misconduct": 0.9,
            "potential_conflicts": 0.7,
            "financial_transactions": 0.5
        }
        
        for category, flags in red_flags.items():
            # Base score is the number of flags
            base_score = len(flags)
            
            # Apply weight
            weight = weights.get(category, 0.5)
            
            # Calculate final score (0-10 scale)
            score = min(10, base_score * weight * 2)
            
            scores[category] = round(score, 1)
        
        return scores
    
    def _generate_summary(self, entities, red_flags, severity_scores):
        """Generate a summary of the red flag analysis.
        
        Args:
            entities (list): List of (entity, entity_type) tuples.
            red_flags (dict): Dictionary with red flag categories and their matches.
            severity_scores (dict): Dictionary with category scores.
            
        Returns:
            str: Summary text.
        """
        if not red_flags:
            return "No red flags detected in the document."
        
        # Count entities by type
        entity_counts = defaultdict(int)
        for _, entity_type in entities:
            entity_counts[entity_type] += 1
        
        # Get total red flags
        total_flags = sum(len(flags) for flags in red_flags.values())
        
        # Get average severity score
        if severity_scores:
            avg_severity = sum(severity_scores.values()) / len(severity_scores)
        else:
            avg_severity = 0
        
        # Generate summary text
        summary = f"Analysis detected {total_flags} potential red flags with an average severity of {avg_severity:.1f}/10.\n\n"
        
        # Add entity summary
        summary += "Entities detected:\n"
        for entity_type, count in entity_counts.items():
            summary += f"- {count} {entity_type.lower().replace('_', ' ')}\n"
        
        # Add red flag summary
        summary += "\nRed flag categories:\n"
        for category, flags in red_flags.items():
            category_name = category.replace('_', ' ').title()
            score = severity_scores.get(category, 0)
            summary += f"- {category_name}: {len(flags)} instances (Severity: {score}/10)\n"
        
        # Add recommendation based on severity
        if avg_severity >= 7:
            summary += "\nRECOMMENDATION: High-priority investigation recommended."
        elif avg_severity >= 4:
            summary += "\nRECOMMENDATION: Further review recommended."
        else:
            summary += "\nRECOMMENDATION: Low priority for follow-up."
        
        return summary
