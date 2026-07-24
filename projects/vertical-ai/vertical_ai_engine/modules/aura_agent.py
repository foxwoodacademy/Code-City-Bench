# modules/aura_agent.py

import re
import json
import logging
from datetime import datetime
from collections import defaultdict

class AuraMicroAgent:
    """Aura Micro-Agent for generating insights and analysis.
    
    The Aura component provides AI-driven insights, pattern recognition,
    and strategic recommendations based on analyzed documents and entities.
    """
    
    def __init__(self):
        """Initialize the Aura Micro-Agent."""
        # Initialize insight generation components
        self.insight_generators = {
            "pattern_recognition": self._pattern_recognition,
            "entity_connections": self._entity_connections,
            "timeline_analysis": self._timeline_analysis,
            "risk_assessment": self._risk_assessment,
            "strategic_recommendations": self._strategic_recommendations,
            "psychological_profile": self._psychological_profile
        }
        
        # Initialize insight storage
        self.insights = []
        
        # Initialize pattern database (would be more sophisticated in production)
        self.pattern_database = self._initialize_pattern_database()
        
        # Initialize logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("AuraMicroAgent")
    
    def _initialize_pattern_database(self):
        """Initialize the pattern database with known patterns of misconduct.
        
        Returns:
            dict: Dictionary of pattern categories and their indicators.
        """
        return {
            "financial_misconduct": [
                r"(?:misappropriat(?:e|ed|ion)|embezzl(?:e|ed|ement))\s+(?:of\s+)?(?:funds|money|resources)",
                r"(?:divert(?:ed|ing)?|redirect(?:ed|ing)?)\s+(?:funds|money|resources)",
                r"(?:fraudulent|improper|suspicious)\s+(?:billing|invoic(?:e|ing)|reimbursement)",
                r"(?:kickback|bribe|payoff|slush fund)",
                r"conflict\s+of\s+interest"
            ],
            "procedural_violations": [
                r"(?:violat(?:e|ed|ion)|breach(?:ed)?)\s+(?:of\s+)?(?:protocol|procedure|policy|regulation)",
                r"(?:circumvent(?:ed|ing)?|bypass(?:ed|ing)?)\s+(?:protocol|procedure|policy|regulation|oversight)",
                r"(?:fail(?:ed|ure)|neglect(?:ed)?)\s+to\s+(?:follow|adhere to|comply with)\s+(?:protocol|procedure|policy|regulation)",
                r"(?:irregular|improper|unauthorized)\s+(?:approval|authorization|process)"
            ],
            "abuse_of_power": [
                r"(?:abuse|misuse|exploit(?:ation)?)\s+(?:of\s+)?(?:power|authority|position|office)",
                r"(?:exceed(?:ed|ing)?|overstep(?:ped|ping)?)\s+(?:authority|jurisdiction|power)",
                r"(?:pressure|coerce|intimidate|threaten)\s+(?:subordinate|employee|witness|victim)",
                r"(?:retaliat(?:e|ed|ion)|revenge)\s+(?:against|toward)?"
            ],
            "transparency_issues": [
                r"(?:conceal(?:ed|ing|ment)?|hide|hiding|cover(?:\s+up|ed\s+up)|obscur(?:e|ed|ing))\s+(?:information|data|evidence|document|fact)",
                r"(?:mislead(?:ing)?|deceiv(?:e|ed|ing)|misrepresent(?:ed|ing|ation))\s+(?:public|oversight|committee|investigator)",
                r"(?:refus(?:e|ed|al)|declin(?:e|ed))\s+to\s+(?:disclose|reveal|provide|share)\s+(?:information|data|evidence|document)",
                r"(?:redact(?:ed|ion)|censor(?:ed|ship)|withh(?:o|e)ld(?:ing)?)\s+(?:information|data|evidence|document)"
            ],
            "civil_rights_violations": [
                r"(?:violat(?:e|ed|ion)|infring(?:e|ed|ement))\s+(?:of\s+)?(?:civil|constitutional|human)\s+rights",
                r"(?:discriminat(?:e|ed|ion|ory)|bias(?:ed)?)\s+(?:treatment|action|policy|practice)",
                r"(?:racial|ethnic|gender|religious|age)\s+(?:profiling|discrimination|bias)",
                r"(?:excessive|unreasonable|disproportionate)\s+(?:force|violence|response)"
            ],
            "judicial_misconduct": [
                r"(?:judicial|judge)\s+(?:misconduct|impropriety|bias|prejudice)",
                r"(?:ex parte|private)\s+(?:communication|meeting|discussion)",
                r"(?:conflict|appearance)\s+of\s+interest",
                r"(?:improper|inappropriate)\s+(?:recusal|failure to recuse)",
                r"(?:prejudicial|biased|unfair)\s+(?:ruling|decision|judgment|treatment)"
            ],
            "rico_patterns": [
                r"(?:pattern|history|series)\s+of\s+(?:criminal|illegal|unlawful)\s+(?:activity|conduct|behavior)",
                r"(?:organiz(?:ed|ation)|structur(?:ed|e)|systemat(?:ic|ized))\s+(?:criminal|illegal|unlawful)\s+(?:activity|conduct|enterprise)",
                r"(?:racketeer(?:ing)?|extortion|blackmail|protection racket)",
                r"(?:criminal|illegal)\s+(?:enterprise|syndicate|organization|network)",
                r"(?:conspiracy|collusion|collaboration)\s+to\s+(?:commit|engage in|perform)\s+(?:criminal|illegal|unlawful)\s+(?:activity|conduct)"
            ]
        }
    
    def generate_insights(self, documents, entities, red_flags=None, mode="standard"):
        """Generate insights based on analyzed documents and entities.
        
        Args:
            documents (list): List of processed documents.
            entities (list): List of extracted entities.
            red_flags (list, optional): List of identified red flags.
            mode (str, optional): Analysis mode (standard, deep, psychological_warfare).
            
        Returns:
            dict: Generated insights and analysis.
        """
        self.logger.info(f"Generating insights in {mode} mode")
        
        # Clear previous insights
        self.insights = []
        
        # Generate insights based on available generators and mode
        active_generators = self._get_active_generators(mode)
        
        for generator_name in active_generators:
            try:
                generator = self.insight_generators[generator_name]
                insight = generator(documents, entities, red_flags)
                if insight:
                    self.insights.append(insight)
            except Exception as e:
                self.logger.error(f"Error generating {generator_name} insight: {str(e)}")
        
        # Compile insights into a structured report
        report = self._compile_insight_report(mode)
        
        return report
    
    def _get_active_generators(self, mode):
        """Get the active insight generators based on the analysis mode.
        
        Args:
            mode (str): Analysis mode.
            
        Returns:
            list: List of active generator names.
        """
        if mode == "standard":
            return ["pattern_recognition", "entity_connections", "timeline_analysis", "risk_assessment"]
        elif mode == "deep":
            return ["pattern_recognition", "entity_connections", "timeline_analysis", 
                    "risk_assessment", "strategic_recommendations"]
        elif mode == "psychological_warfare":
            return ["pattern_recognition", "entity_connections", "timeline_analysis", 
                    "risk_assessment", "strategic_recommendations", "psychological_profile"]
        else:
            # Default to standard mode
            return ["pattern_recognition", "entity_connections", "timeline_analysis", "risk_assessment"]
    
    def _pattern_recognition(self, documents, entities, red_flags):
        """Recognize patterns of misconduct in documents and entities.
        
        Args:
            documents (list): List of processed documents.
            entities (list): List of extracted entities.
            red_flags (list): List of identified red flags.
            
        Returns:
            dict: Pattern recognition insight.
        """
        # Initialize pattern counts
        pattern_counts = defaultdict(int)
        pattern_evidence = defaultdict(list)
        
        # Analyze documents for patterns
        for doc in documents:
            doc_text = doc.get("content", "")
            doc_id = doc.get("id", "unknown")
            
            for category, patterns in self.pattern_database.items():
                for pattern in patterns:
                    matches = re.finditer(pattern, doc_text, re.IGNORECASE)
                    for match in matches:
                        pattern_counts[category] += 1
                        context = self._get_context(doc_text, match.start(), match.end())
                        evidence = {
                            "document_id": doc_id,
                            "context": context,
                            "pattern": pattern
                        }
                        pattern_evidence[category].append(evidence)
        
        # Analyze red flags for patterns
        if red_flags:
            for flag in red_flags:
                flag_text = flag.get("description", "")
                flag_category = flag.get("category", "unknown")
                
                if flag_category in pattern_counts:
                    pattern_counts[flag_category] += 1
                    evidence = {
                        "document_id": flag.get("document_id", "unknown"),
                        "context": flag_text,
                        "pattern": "red_flag"
                    }
                    pattern_evidence[flag_category].append(evidence)
        
        # Generate insight
        if sum(pattern_counts.values()) > 0:
            # Find the dominant pattern
            dominant_pattern = max(pattern_counts.items(), key=lambda x: x[1])
            
            insight = {
                "type": "pattern_recognition",
                "title": "Pattern Recognition Analysis",
                "summary": f"Detected {sum(pattern_counts.values())} instances of potential misconduct patterns across {len(documents)} documents.",
                "dominant_pattern": {
                    "category": dominant_pattern[0],
                    "count": dominant_pattern[1],
                    "description": self._get_pattern_description(dominant_pattern[0])
                },
                "pattern_distribution": dict(pattern_counts),
                "evidence": dict(pattern_evidence),
                "confidence": self._calculate_confidence(pattern_counts, len(documents))
            }
            
            return insight
        
        return None
    
    def _entity_connections(self, documents, entities, red_flags):
        """Analyze connections between entities.
        
        Args:
            documents (list): List of processed documents.
            entities (list): List of extracted entities.
            red_flags (list): List of identified red flags.
            
        Returns:
            dict: Entity connections insight.
        """
        # Skip if no entities
        if not entities:
            return None
        
        # Initialize connection tracking
        connections = defaultdict(lambda: defaultdict(int))
        connection_evidence = []
        
        # Track entities that appear in the same document
        for doc in documents:
            doc_text = doc.get("content", "")
            doc_id = doc.get("id", "unknown")
            
            # Find entities in this document
            doc_entities = []
            for entity in entities:
                entity_name = entity.get("name", "")
                if entity_name and re.search(r"\b" + re.escape(entity_name) + r"\b", doc_text, re.IGNORECASE):
                    doc_entities.append(entity)
            
            # Record connections between entities in the same document
            for i, entity1 in enumerate(doc_entities):
                for entity2 in doc_entities[i+1:]:
                    entity1_name = entity1.get("name", "")
                    entity2_name = entity2.get("name", "")
                    entity1_type = entity1.get("type", "unknown")
                    entity2_type = entity2.get("type", "unknown")
                    
                    if entity1_name and entity2_name:
                        connections[entity1_name][entity2_name] += 1
                        connections[entity2_name][entity1_name] += 1
                        
                        evidence = {
                            "document_id": doc_id,
                            "entity1": {
                                "name": entity1_name,
                                "type": entity1_type
                            },
                            "entity2": {
                                "name": entity2_name,
                                "type": entity2_type
                            }
                        }
                        connection_evidence.append(evidence)
        
        # Generate network graph
        network = []
        for entity1, connected_entities in connections.items():
            for entity2, strength in connected_entities.items():
                if entity1 < entity2:  # Avoid duplicates
                    network.append({
                        "source": entity1,
                        "target": entity2,
                        "strength": strength
                    })
        
        # Find key entities (highest number of connections)
        entity_connection_counts = {}
        for entity, connected_entities in connections.items():
            entity_connection_counts[entity] = sum(connected_entities.values())
        
        key_entities = sorted(entity_connection_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Generate insight
        if network:
            insight = {
                "type": "entity_connections",
                "title": "Entity Network Analysis",
                "summary": f"Identified {len(network)} connections between {len(connections)} entities.",
                "key_entities": [{
                    "name": entity[0],
                    "connection_count": entity[1],
                    "connected_to": list(connections[entity[0]].keys())
                } for entity in key_entities],
                "network": network,
                "evidence": connection_evidence,
                "confidence": min(0.7 + (len(network) / 100), 0.95)  # Higher confidence with more connections
            }
            
            return insight
        
        return None
    
    def _timeline_analysis(self, documents, entities, red_flags):
        """Analyze the timeline of events from documents.
        
        Args:
            documents (list): List of processed documents.
            entities (list): List of extracted entities.
            red_flags (list): List of identified red flags.
            
        Returns:
            dict: Timeline analysis insight.
        """
        # Extract dates from documents
        events = []
        date_pattern = r"(?:\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2}(?:st|nd|rd|th)?[,\s]+\d{4}\b)|(?:\b\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}\b)"
        
        for doc in documents:
            doc_text = doc.get("content", "")
            doc_id = doc.get("id", "unknown")
            doc_date = doc.get("date", None)
            
            # Use document date if available
            if doc_date:
                events.append({
                    "date": doc_date,
                    "document_id": doc_id,
                    "description": doc.get("title", "Document created"),
                    "type": "document"
                })
            
            # Extract dates from content
            date_matches = re.finditer(date_pattern, doc_text)
            for match in date_matches:
                date_str = match.group(0)
                context = self._get_context(doc_text, match.start(), match.end())
                
                # Try to parse the date
                try:
                    # This is a simplified approach - in production, use a more robust date parser
                    parsed_date = date_str
                    events.append({
                        "date": parsed_date,
                        "document_id": doc_id,
                        "description": context,
                        "type": "mentioned_date"
                    })
                except:
                    pass
        
        # Add red flag events to timeline
        if red_flags:
            for flag in red_flags:
                flag_date = flag.get("date", None)
                if flag_date:
                    events.append({
                        "date": flag_date,
                        "document_id": flag.get("document_id", "unknown"),
                        "description": flag.get("description", "Red flag identified"),
                        "type": "red_flag",
                        "severity": flag.get("severity", "medium")
                    })
        
        # Generate insight
        if events:
            # Sort events by date (in a real implementation, properly parse and sort dates)
            # For this simulation, we'll just pretend they're sorted
            
            # Identify key periods (clusters of events)
            # In a real implementation, use proper clustering algorithms
            key_periods = [{
                "start_date": "earliest_date",
                "end_date": "latest_date",
                "event_count": len(events),
                "description": "Period of significant activity"
            }]
            
            insight = {
                "type": "timeline_analysis",
                "title": "Timeline Analysis",
                "summary": f"Constructed timeline with {len(events)} events spanning multiple time periods.",
                "events": events,
                "key_periods": key_periods,
                "confidence": min(0.6 + (len(events) / 50), 0.9)  # Higher confidence with more events
            }
            
            return insight
        
        return None
    
    def _risk_assessment(self, documents, entities, red_flags):
        """Assess risks based on documents and identified issues.
        
        Args:
            documents (list): List of processed documents.
            entities (list): List of extracted entities.
            red_flags (list): List of identified red flags.
            
        Returns:
            dict: Risk assessment insight.
        """
        # Skip if no red flags
        if not red_flags:
            return None
        
        # Categorize risks
        risk_categories = defaultdict(list)
        for flag in red_flags:
            category = flag.get("category", "other")
            severity = flag.get("severity", "medium")
            risk_categories[category].append({
                "description": flag.get("description", ""),
                "severity": severity,
                "document_id": flag.get("document_id", "unknown")
            })
        
        # Calculate risk scores
        severity_scores = {"low": 1, "medium": 2, "high": 3, "critical": 4}
        risk_scores = {}
        for category, flags in risk_categories.items():
            total_score = sum(severity_scores.get(flag["severity"], 1) for flag in flags)
            risk_scores[category] = min(total_score / 10, 1.0)  # Normalize to 0-1
        
        # Calculate overall risk score
        overall_risk = sum(risk_scores.values()) / len(risk_scores) if risk_scores else 0
        
        # Generate risk matrix
        risk_matrix = []
        for category, score in risk_scores.items():
            impact = min(score * 1.5, 1.0)  # Impact slightly higher than probability
            probability = score
            risk_matrix.append({
                "category": category,
                "impact": impact,
                "probability": probability,
                "risk_level": impact * probability,
                "flag_count": len(risk_categories[category])
            })
        
        # Sort risk matrix by risk level
        risk_matrix.sort(key=lambda x: x["risk_level"], reverse=True)
        
        # Generate insight
        insight = {
            "type": "risk_assessment",
            "title": "Risk Assessment",
            "summary": f"Identified {len(red_flags)} red flags across {len(risk_categories)} risk categories.",
            "overall_risk": overall_risk,
            "risk_matrix": risk_matrix,
            "risk_categories": dict(risk_categories),
            "confidence": min(0.5 + (len(red_flags) / 20), 0.85)  # Higher confidence with more red flags
        }
        
        return insight
    
    def _strategic_recommendations(self, documents, entities, red_flags):
        """Generate strategic recommendations based on analysis.
        
        Args:
            documents (list): List of processed documents.
            entities (list): List of extracted entities.
            red_flags (list): List of identified red flags.
            
        Returns:
            dict: Strategic recommendations insight.
        """
        # Skip if no red flags or insights
        if not red_flags and not self.insights:
            return None
        
        # Generate recommendations based on insights and red flags
        recommendations = []
        
        # Check for pattern recognition insight
        pattern_insight = next((i for i in self.insights if i["type"] == "pattern_recognition"), None)
        if pattern_insight:
            dominant_pattern = pattern_insight.get("dominant_pattern", {})
            if dominant_pattern:
                category = dominant_pattern.get("category", "")
                if category == "financial_misconduct":
                    recommendations.append({
                        "category": "investigation",
                        "title": "Financial Audit",
                        "description": "Conduct a detailed financial audit focusing on fund allocation, expense reports, and procurement processes.",
                        "priority": "high"
                    })
                elif category == "procedural_violations":
                    recommendations.append({
                        "category": "documentation",
                        "title": "Procedural Review",
                        "description": "Review and document all instances of procedural violations, focusing on systemic patterns rather than isolated incidents.",
                        "priority": "medium"
                    })
                elif category == "abuse_of_power":
                    recommendations.append({
                        "category": "legal",
                        "title": "Authority Chain Analysis",
                        "description": "Map the chain of authority and decision-making processes to identify where power is being abused or exceeded.",
                        "priority": "high"
                    })
                elif category == "transparency_issues":
                    recommendations.append({
                        "category": "foia",
                        "title": "Targeted FOIA Requests",
                        "description": "Submit targeted FOIA requests for specific documents that appear to be concealed or redacted inappropriately.",
                        "priority": "high"
                    })
                elif category == "civil_rights_violations":
                    recommendations.append({
                        "category": "legal",
                        "title": "Civil Rights Assessment",
                        "description": "Conduct a comprehensive assessment of potential civil rights violations, documenting affected individuals and patterns of discrimination.",
                        "priority": "critical"
                    })
                elif category == "judicial_misconduct":
                    recommendations.append({
                        "category": "legal",
                        "title": "Judicial Ethics Review",
                        "description": "Compile evidence of judicial misconduct for submission to the appropriate judicial conduct committee or oversight body.",
                        "priority": "high"
                    })
                elif category == "rico_patterns":
                    recommendations.append({
                        "category": "legal",
                        "title": "RICO Analysis",
                        "description": "Develop a comprehensive RICO (Racketeer Influenced and Corrupt Organizations Act) analysis documenting the pattern of organized criminal activity.",
                        "priority": "critical"
                    })
        
        # Check for entity connections insight
        entity_insight = next((i for i in self.insights if i["type"] == "entity_connections"), None)
        if entity_insight:
            key_entities = entity_insight.get("key_entities", [])
            if key_entities:
                recommendations.append({
                    "category": "investigation",
                    "title": "Key Entity Investigation",
                    "description": f"Focus investigation on the {len(key_entities)} key entities with the most connections, particularly {key_entities[0]['name'] if key_entities else 'primary entities'}.",
                    "priority": "high"
                })
        
        # Check for risk assessment insight
        risk_insight = next((i for i in self.insights if i["type"] == "risk_assessment"), None)
        if risk_insight:
            risk_matrix = risk_insight.get("risk_matrix", [])
            if risk_matrix and len(risk_matrix) > 0:
                highest_risk = risk_matrix[0]
                recommendations.append({
                    "category": "risk_mitigation",
                    "title": f"Address {highest_risk['category']} Risks",
                    "description": f"Prioritize addressing the {highest_risk['category']} risks which present the highest combined impact and probability.",
                    "priority": "critical" if highest_risk["risk_level"] > 0.7 else "high"
                })
        
        # Add general recommendations based on red flags
        if red_flags:
            # Check for high severity flags
            high_severity_flags = [f for f in red_flags if f.get("severity") in ["high", "critical"]]
            if high_severity_flags:
                recommendations.append({
                    "category": "documentation",
                    "title": "Critical Evidence Preservation",
                    "description": "Immediately preserve and secure all evidence related to the high-severity red flags to prevent potential tampering or destruction.",
                    "priority": "critical"
                })
            
            # Check for multiple flags in the same category
            category_counts = defaultdict(int)
            for flag in red_flags:
                category_counts[flag.get("category", "other")] += 1
            
            for category, count in category_counts.items():
                if count >= 3 and category not in [r["title"] for r in recommendations]:
                    recommendations.append({
                        "category": "investigation",
                        "title": f"{category.replace('_', ' ').title()} Deep Dive",
                        "description": f"Conduct a focused investigation into the {count} instances of {category.replace('_', ' ')}.",
                        "priority": "high" if count >= 5 else "medium"
                    })
        
        # Add FOIA-specific recommendations
        recommendations.append({
            "category": "foia",
            "title": "Strategic FOIA Campaign",
            "description": "Develop a strategic FOIA request campaign targeting specific documents and information gaps identified in the analysis.",
            "priority": "medium"
        })
        
        # Generate insight
        if recommendations:
            insight = {
                "type": "strategic_recommendations",
                "title": "Strategic Recommendations",
                "summary": f"Generated {len(recommendations)} strategic recommendations based on analysis.",
                "recommendations": recommendations,
                "confidence": 0.75  # Fixed confidence for recommendations
            }
            
            return insight
        
        return None
    
    def _psychological_profile(self, documents, entities, red_flags):
        """Generate psychological profiles for key entities.
        
        Args:
            documents (list): List of processed documents.
            entities (list): List of extracted entities.
            red_flags (list): List of identified red flags.
            
        Returns:
            dict: Psychological profile insight.
        """
        # Skip if no entities or in non-psychological warfare mode
        if not entities:
            return None
        
        # Identify key individuals to profile
        individuals = [e for e in entities if e.get("type") == "PERSON"]
        if not individuals:
            return None
        
        # Sort individuals by mention count (if available) or alphabetically
        individuals.sort(key=lambda x: x.get("mention_count", 0), reverse=True)
        
        # Take top 3 individuals for profiling
        top_individuals = individuals[:3]
        
        # Generate profiles
        profiles = []
        for individual in top_individuals:
            name = individual.get("name", "Unknown Individual")
            
            # Collect mentions in documents
            mentions = []
            for doc in documents:
                doc_text = doc.get("content", "")
                doc_id = doc.get("id", "unknown")
                
                # Find mentions of this individual
                for match in re.finditer(r"\b" + re.escape(name) + r"\b", doc_text, re.IGNORECASE):
                    context = self._get_context(doc_text, match.start(), match.end(), window=100)
                    mentions.append({
                        "document_id": doc_id,
                        "context": context
                    })
            
            # Generate psychological traits (simplified for demonstration)
            # In a real implementation, use NLP and psychological models
            traits = {
                "authority_orientation": self._generate_random_trait(),
                "risk_tolerance": self._generate_random_trait(),
                "transparency": self._generate_random_trait(),
                "accountability": self._generate_random_trait(),
                "ethical_flexibility": self._generate_random_trait()
            }
            
            # Generate vulnerabilities based on traits
            vulnerabilities = []
            if traits["authority_orientation"] > 0.7:
                vulnerabilities.append({
                    "type": "authority_challenge",
                    "description": "Highly sensitive to challenges to authority; likely to overreact when authority is questioned.",
                    "exploitation_vector": "Public questioning of decisions and authority"
                })
            
            if traits["risk_tolerance"] < 0.3:
                vulnerabilities.append({
                    "type": "risk_aversion",
                    "description": "Extremely risk-averse; likely to avoid necessary actions if perceived as risky.",
                    "exploitation_vector": "Creating perception of safety in disclosure vs. risk in concealment"
                })
            
            if traits["transparency"] < 0.4:
                vulnerabilities.append({
                    "type": "transparency_fear",
                    "description": "Avoids transparency; likely hiding information beyond what's necessary.",
                    "exploitation_vector": "Targeted FOIA requests in areas of suspected concealment"
                })
            
            if traits["accountability"] < 0.5:
                vulnerabilities.append({
                    "type": "accountability_avoidance",
                    "description": "Tends to deflect responsibility; likely to blame others for failures.",
                    "exploitation_vector": "Public attribution of responsibility with evidence"
                })
            
            if traits["ethical_flexibility"] > 0.6:
                vulnerabilities.append({
                    "type": "ethical_compromise",
                    "description": "Shows ethical flexibility; likely to justify questionable actions for 'greater good'.",
                    "exploitation_vector": "Highlighting ethical contradictions in public statements vs. actions"
                })
            
            # Add profile
            profiles.append({
                "name": name,
                "position": individual.get("position", "Unknown Position"),
                "traits": traits,
                "vulnerabilities": vulnerabilities,
                "mention_count": len(mentions),
                "mentions": mentions[:5]  # Limit to 5 mentions for brevity
            })
        
        # Generate insight
        if profiles:
            insight = {
                "type": "psychological_profile",
                "title": "Psychological Warfare Analysis",
                "summary": f"Generated psychological profiles for {len(profiles)} key individuals.",
                "profiles": profiles,
                "disclaimer": "This analysis is for accountability purposes only and should be used ethically and legally.",
                "confidence": 0.6  # Lower confidence for psychological profiles
            }
            
            return insight
        
        return None
    
    def _generate_random_trait(self):
        """Generate a random trait value between 0 and 1.
        
        In a real implementation, this would be based on text analysis.
        
        Returns:
            float: Random trait value.
        """
        import random
        return round(random.random(), 2)
    
    def _get_context(self, text, start_pos, end_pos, window=50):
        """Get context around a match in text.
        
        Args:
            text (str): The text to extract context from.
            start_pos (int): Start position of the match.
            end_pos (int): End position of the match.
            window (int, optional): Window size for context.
            
        Returns:
            str: Context string.
        """
        start = max(0, start_pos - window)
        end = min(len(text), end_pos + window)
        
        # Find sentence boundaries if possible
        while start > 0 and text[start] not in ".\n":
            start -= 1
        
        while end < len(text) - 1 and text[end] not in ".\n":
            end += 1
        
        # Adjust start and end for readability
        if start > 0:
            start += 1  # Skip the period or newline
        
        if end < len(text) - 1:
            end += 1  # Include the period or newline
        
        context = text[start:end].strip()
        
        # Highlight the match
        match_text = text[start_pos:end_pos]
        highlighted_context = context.replace(match_text, f"**{match_text}**")
        
        return highlighted_context
    
    def _get_pattern_description(self, category):
        """Get a description for a pattern category.
        
        Args:
            category (str): Pattern category.
            
        Returns:
            str: Description of the pattern category.
        """
        descriptions = {
            "financial_misconduct": "Patterns indicating misappropriation of funds, embezzlement, fraudulent billing, or other financial improprieties.",
            "procedural_violations": "Patterns showing violations of established protocols, procedures, or regulations.",
            "abuse_of_power": "Patterns suggesting misuse of authority, exceeding jurisdiction, or using position for improper purposes.",
            "transparency_issues": "Patterns indicating concealment of information, misleading statements, or obstruction of oversight.",
            "civil_rights_violations": "Patterns showing discrimination, profiling, or other violations of civil or constitutional rights.",
            "judicial_misconduct": "Patterns indicating judicial bias, improper communications, conflicts of interest, or other judicial improprieties.",
            "rico_patterns": "Patterns suggesting organized criminal activity, systematic corruption, or racketeering."
        }
        
        return descriptions.get(category, f"Patterns related to {category.replace('_', ' ')}")
    
    def _calculate_confidence(self, pattern_counts, document_count):
        """Calculate confidence score for pattern recognition.
        
        Args:
            pattern_counts (dict): Dictionary of pattern counts by category.
            document_count (int): Number of documents analyzed.
            
        Returns:
            float: Confidence score between 0 and 1.
        """
        total_patterns = sum(pattern_counts.values())
        
        # Base confidence on pattern density and diversity
        pattern_density = total_patterns / max(document_count, 1)
        pattern_diversity = len(pattern_counts) / 7  # 7 is the total number of pattern categories
        
        # Calculate confidence score
        confidence = 0.5 + (0.25 * min(pattern_density, 1.0)) + (0.25 * pattern_diversity)
        
        return min(confidence, 0.95)  # Cap at 0.95
    
    def _compile_insight_report(self, mode):
        """Compile insights into a structured report.
        
        Args:
            mode (str): Analysis mode.
            
        Returns:
            dict: Compiled insight report.
        """
        # Calculate overall confidence
        confidence_scores = [insight.get("confidence", 0.5) for insight in self.insights]
        overall_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.5
        
        # Compile report
        report = {
            "timestamp": datetime.now().isoformat(),
            "analysis_mode": mode,
            "insight_count": len(self.insights),
            "insights": self.insights,
            "overall_confidence": overall_confidence,
            "summary": self._generate_summary()
        }
        
        return report
    
    def _generate_summary(self):
        """Generate a summary of the insights.
        
        Returns:
            str: Summary text.
        """
        if not self.insights:
            return "No significant insights generated from the available data."
        
        # Count insight types
        insight_types = [insight["type"] for insight in self.insights]
        
        # Generate summary based on available insights
        summary_parts = []
        
        if "pattern_recognition" in insight_types:
            pattern_insight = next(i for i in self.insights if i["type"] == "pattern_recognition")
            dominant_pattern = pattern_insight.get("dominant_pattern", {})
            if dominant_pattern:
                summary_parts.append(f"Identified {dominant_pattern.get('count', 0)} instances of {dominant_pattern.get('category', 'misconduct').replace('_', ' ')}")
        
        if "entity_connections" in insight_types:
            entity_insight = next(i for i in self.insights if i["type"] == "entity_connections")
            key_entities = entity_insight.get("key_entities", [])
            if key_entities:
                summary_parts.append(f"Mapped connections between {len(entity_insight.get('network', []))} entity relationships")
        
        if "timeline_analysis" in insight_types:
            timeline_insight = next(i for i in self.insights if i["type"] == "timeline_analysis")
            events = timeline_insight.get("events", [])
            if events:
                summary_parts.append(f"Constructed timeline with {len(events)} significant events")
        
        if "risk_assessment" in insight_types:
            risk_insight = next(i for i in self.insights if i["type"] == "risk_assessment")
            risk_matrix = risk_insight.get("risk_matrix", [])
            if risk_matrix and len(risk_matrix) > 0:
                highest_risk = risk_matrix[0]
                summary_parts.append(f"Identified {highest_risk.get('category', 'significant').replace('_', ' ')} as the highest risk area")
        
        if "strategic_recommendations" in insight_types:
            recommendation_insight = next(i for i in self.insights if i["type"] == "strategic_recommendations")
            recommendations = recommendation_insight.get("recommendations", [])
            if recommendations:
                critical_recs = [r for r in recommendations if r.get("priority") == "critical"]
                if critical_recs:
                    summary_parts.append(f"Generated {len(recommendations)} recommendations, including {len(critical_recs)} critical priorities")
                else:
                    summary_parts.append(f"Generated {len(recommendations)} strategic recommendations")
        
        if "psychological_profile" in insight_types:
            profile_insight = next(i for i in self.insights if i["type"] == "psychological_profile")
            profiles = profile_insight.get("profiles", [])
            if profiles:
                summary_parts.append(f"Developed psychological profiles for {len(profiles)} key individuals")
        
        # Combine summary parts
        if summary_parts:
            return ". ".join(summary_parts) + "."
        else:
            return "Analysis complete, but no significant patterns or insights were identified in the available data."