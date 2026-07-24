# modules/foia_generator.py

import datetime
import re
import logging
from string import Template

class FOIAGeneratorMicroAgent:
    """FOIA request generation micro-agent."""
    
    def __init__(self):
        """Initialize the FOIA generator."""
        # Load templates
        self.templates = self._load_templates()
        
        # Initialize agency information database
        self.agency_info = self._initialize_agency_database()
    
    def _load_templates(self):
        """Load FOIA request templates.
        
        Returns:
            dict: Dictionary of templates for different request types.
        """
        templates = {}
        
        # Standard FOIA request template
        templates["standard"] = Template('''
$date

$recipient_name
$recipient_title
$agency_name
$agency_address

Re: Freedom of Information Act Request

Dear $recipient_salutation:

This is a request under the Freedom of Information Act, 5 U.S.C. § 552.

I request that a copy of the following documents be provided to me: $records_description

In order to help determine my status for the purpose of determining the applicability of any fees, you should know that I am $requester_category.

$fee_waiver_request

I request that all fees be waived because the disclosure of the requested information is in the public interest. It is likely to contribute significantly to public understanding of the operations or activities of the government and is not primarily in my commercial interest.

I request that the information I seek be provided in $format format. If my request is denied in whole or part, I ask that you justify all deletions by reference to specific exemptions of the act. I will also expect you to release all segregable portions of otherwise exempt material.

I reserve the right to appeal your decision to withhold any information or to deny a waiver of fees.

I look forward to your reply within 20 business days, as the statute requires.

Thank you for your assistance.

Sincerely,

$your_name
$your_contact_info
''')
        
        # Expedited FOIA request template
        templates["expedited"] = Template('''
$date

$recipient_name
$recipient_title
$agency_name
$agency_address

Re: Freedom of Information Act Request - EXPEDITED PROCESSING REQUESTED

Dear $recipient_salutation:

This is a request under the Freedom of Information Act, 5 U.S.C. § 552.

I request that a copy of the following documents be provided to me: $records_description

I am seeking expedited processing of this request because $expedited_reason. I believe a compelling need exists to warrant expedited processing because there is an urgency to inform the public concerning actual or alleged Federal Government activity.

In order to help determine my status for the purpose of determining the applicability of any fees, you should know that I am $requester_category.

$fee_waiver_request

I request that all fees be waived because the disclosure of the requested information is in the public interest. It is likely to contribute significantly to public understanding of the operations or activities of the government and is not primarily in my commercial interest.

I request that the information I seek be provided in $format format. If my request is denied in whole or part, I ask that you justify all deletions by reference to specific exemptions of the act. I will also expect you to release all segregable portions of otherwise exempt material.

I reserve the right to appeal your decision to withhold any information or to deny a waiver of fees.

I look forward to your reply within 20 business days, as the statute requires, and sooner if possible due to the expedited nature of this request.

Thank you for your assistance.

Sincerely,

$your_name
$your_contact_info
''')
        
        # State-level public records request template
        templates["state"] = Template('''
$date

$recipient_name
$recipient_title
$agency_name
$agency_address

Re: Public Records Request

Dear $recipient_salutation:

Under the $state_law, I am requesting an opportunity to inspect or obtain copies of the following public records: $records_description

$fee_waiver_request

If there are any fees for searching or copying these records, please inform me if the cost will exceed $fee_limit. However, I would also like to request a waiver of all fees in that the disclosure of the requested information is in the public interest.

If you deny any or all of this request, please cite each specific exemption you feel justifies the refusal to release the information and notify me of the appeal procedures available to me under the law.

I request that the information I seek be provided in $format format. Thank you for considering my request.

Sincerely,

$your_name
$your_contact_info
''')
        
        # Local government records request template
        templates["local"] = Template('''
$date

$recipient_name
$recipient_title
$agency_name
$agency_address

Re: Public Records Request

Dear $recipient_salutation:

Pursuant to the applicable public records law, I request access to and copies of the following records: $records_description

If there are any fees for searching or copying these records, please inform me if the cost will exceed $fee_limit.

I request that the information I seek be provided in $format format. If my request is denied in whole or part, I ask that you justify all deletions by reference to specific exemptions in the law.

Thank you for your assistance.

Sincerely,

$your_name
$your_contact_info
''')
        
        return templates
    
    def _initialize_agency_database(self):
        """Initialize the agency information database.
        
        Returns:
            dict: Dictionary of agency information.
        """
        # This would ideally be loaded from a database or external file
        # For now, we'll include a few example agencies
        return {
            "fbi": {
                "name": "Federal Bureau of Investigation",
                "address": "Record/Information Dissemination Section\nAttn: FOIPA Request\n170 Marcel Drive\nWinchester, VA 22602-4843",
                "recipient_name": "FOIA Officer",
                "recipient_title": "Records Management Division",
                "level": "federal"
            },
            "epa": {
                "name": "Environmental Protection Agency",
                "address": "National FOIA Office\nU.S. Environmental Protection Agency\n1200 Pennsylvania Avenue, NW (2310A)\nWashington, DC 20460",
                "recipient_name": "FOIA Officer",
                "recipient_title": "National FOIA Office",
                "level": "federal"
            },
            "doj": {
                "name": "Department of Justice",
                "address": "FOIA/PA Mail Referral Unit\nJustice Management Division\nDepartment of Justice\n950 Pennsylvania Avenue, NW\nWashington, DC 20530-0001",
                "recipient_name": "FOIA Officer",
                "recipient_title": "FOIA/PA Mail Referral Unit",
                "level": "federal"
            },
            "local_government": {
                "name": "[CITY/COUNTY] Government",
                "address": "[ADDRESS]",
                "recipient_name": "Clerk",
                "recipient_title": "Records Officer",
                "level": "local"
            }
        }
    
    def generate_foia_request(self, agency, records_description, format="electronic", your_name="Concerned Citizen", 
                             your_contact_info="", expedited=False, expedited_reason="", state_law="", 
                             fee_limit="$25", requester_category="an individual seeking information for personal use"):
        """Generate a FOIA request letter.
        
        Args:
            agency (str): Agency name or key.
            records_description (str): Description of the records requested.
            format (str, optional): Requested format for the records.
            your_name (str, optional): Name of the requester.
            your_contact_info (str, optional): Contact information of the requester.
            expedited (bool, optional): Whether to request expedited processing.
            expedited_reason (str, optional): Reason for expedited processing.
            state_law (str, optional): State public records law name.
            fee_limit (str, optional): Maximum fee limit.
            requester_category (str, optional): Category of the requester.
            
        Returns:
            str: Generated FOIA request letter.
        """
        # Get current date
        date = datetime.datetime.now().strftime("%B %d, %Y")
        
        # Get agency information
        agency_info = self._get_agency_info(agency)
        
        # Determine template to use
        template_key = "standard"
        if expedited:
            template_key = "expedited"
        elif agency_info["level"] == "state":
            template_key = "state"
        elif agency_info["level"] == "local":
            template_key = "local"
        
        # Prepare template variables
        template_vars = {
            "date": date,
            "recipient_name": agency_info["recipient_name"],
            "recipient_title": agency_info["recipient_title"],
            "agency_name": agency_info["name"],
            "agency_address": agency_info["address"],
            "recipient_salutation": self._get_salutation(agency_info["recipient_name"]),
            "records_description": records_description,
            "format": format,
            "your_name": your_name,
            "your_contact_info": your_contact_info,
            "fee_waiver_request": "",
            "requester_category": requester_category,
            "expedited_reason": expedited_reason,
            "state_law": state_law or "applicable state public records law",
            "fee_limit": fee_limit
        }
        
        # Generate the request
        request = self.templates[template_key].substitute(template_vars)
        
        # Clean up the request (remove extra newlines, etc.)
        request = re.sub(r'\n{3,}', '\n\n', request)
        request = request.strip()
        
        return request
    
    def _get_agency_info(self, agency):
        """Get agency information from the database.
        
        Args:
            agency (str): Agency name or key.
            
        Returns:
            dict: Agency information.
        """
        # Try to find the agency in the database
        agency_key = agency.lower().replace(" ", "_")
        if agency_key in self.agency_info:
            return self.agency_info[agency_key]
        
        # If not found, check for partial matches
        for key, info in self.agency_info.items():
            if agency.lower() in key.lower() or agency.lower() in info["name"].lower():
                return info
        
        # If still not found, use a generic template
        return {
            "name": agency,
            "address": "[ADDRESS]",
            "recipient_name": "FOIA Officer",
            "recipient_title": "Records Management Division",
            "level": "federal"  # Default to federal
        }
    
    def _get_salutation(self, recipient_name):
        """Generate an appropriate salutation.
        
        Args:
            recipient_name (str): Name of the recipient.
            
        Returns:
            str: Appropriate salutation.
        """
        if recipient_name.startswith("Mr.") or recipient_name.startswith("Ms.") or \
           recipient_name.startswith("Dr.") or recipient_name.startswith("Hon."):
            return recipient_name
        elif "Officer" in recipient_name or "Clerk" in recipient_name or \
             "Director" in recipient_name or "Chief" in recipient_name:
            return recipient_name
        else:
            return f"Sir or Madam"
    
    def suggest_records_description(self, topic, timeframe=None, specific_officials=None):
        """Suggest a records description based on the topic.
        
        Args:
            topic (str): Topic of the request.
            timeframe (str, optional): Timeframe for the records.
            specific_officials (list, optional): List of specific officials.
            
        Returns:
            str: Suggested records description.
        """
        description = f"all records relating to {topic}"
        
        if timeframe:
            description += f" from {timeframe}"
        
        if specific_officials and len(specific_officials) > 0:
            officials_str = ", ".join(specific_officials[:-1])
            if len(specific_officials) > 1:
                officials_str += f", and {specific_officials[-1]}"
            else:
                officials_str = specific_officials[0]
            
            description += f" involving {officials_str}"
        
        description += ". This includes, but is not limited to, emails, memoranda, reports, meeting minutes, and other documents."
        
        return description
    
    def analyze_foia_response(self, response_text):
        """Analyze a FOIA response for common denial patterns.
        
        Args:
            response_text (str): Text of the FOIA response.
            
        Returns:
            dict: Analysis of the response.
        """
        analysis = {
            "is_denial": False,
            "exemptions_cited": [],
            "delay_indicated": False,
            "fee_issues": False,
            "suggested_follow_up": None
        }
        
        # Check for denial indicators
        denial_patterns = [
            r"cannot be disclosed",
            r"denied in (?:full|part)",
            r"withh[eo]ld",
            r"exempt from disclosure"
        ]
        
        for pattern in denial_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                analysis["is_denial"] = True
                break
        
        # Check for exemption citations
        exemption_patterns = [
            r"Exemption (?:b\)?)?\(?(\d+)\)?",
            r"FOIA Exemption (?:b\)?)?\(?(\d+)\)?",
            r"5 U\.?S\.?C\.? (?:§|section)? ?552\(b\)\((\d+)\)"
        ]
        
        for pattern in exemption_patterns:
            for match in re.finditer(pattern, response_text, re.IGNORECASE):
                exemption = match.group(1)
                if exemption not in analysis["exemptions_cited"]:
                    analysis["exemptions_cited"].append(exemption)
        
        # Check for delay indicators
        delay_patterns = [
            r"additional time",
            r"extend(?:ed|ing)? the (?:time|deadline|period)",
            r"backlog",
            r"due to (?:the )?volume",
            r"unusual circumstances"
        ]
        
        for pattern in delay_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                analysis["delay_indicated"] = True
                break
        
        # Check for fee issues
        fee_patterns = [
            r"fee(?:s)? (?:will|would) be",
            r"fee (?:waiver|reduction) (?:is|has been) denied",
            r"(?:estimated|actual) fee(?:s)? (?:is|are|of) \$\d+"
        ]
        
        for pattern in fee_patterns:
            if re.search(pattern, response_text, re.IGNORECASE):
                analysis["fee_issues"] = True
                break
        
        # Generate suggested follow-up
        if analysis["is_denial"] and analysis["exemptions_cited"]:
            exemptions_str = ", ".join([f"b({e})" for e in analysis["exemptions_cited"]])
            analysis["suggested_follow_up"] = f"Appeal the denial, challenging the application of Exemption(s) {exemptions_str}."
        elif analysis["delay_indicated"]:
            analysis["suggested_follow_up"] = "Follow up with a status request if no response is received within 30 days."
        elif analysis["fee_issues"]:
            analysis["suggested_follow_up"] = "Submit a more narrowly tailored request or appeal the fee waiver denial."
        
        return analysis
    
    def generate_appeal_letter(self, original_request, response_text, your_name="Concerned Citizen", your_contact_info=""):
        """Generate an appeal letter for a denied FOIA request.
        
        Args:
            original_request (str): Text of the original FOIA request.
            response_text (str): Text of the denial response.
            your_name (str, optional): Name of the requester.
            your_contact_info (str, optional): Contact information of the requester.
            
        Returns:
            str: Generated appeal letter.
        """
        # Analyze the response
        analysis = self.analyze_foia_response(response_text)
        
        # Get current date
        date = datetime.datetime.now().strftime("%B %d, %Y")
        
        # Extract agency name from original request (very basic approach)
        agency_match = re.search(r'\n([^\n]+)\n[^\n]+\n[^\n]+\nRe:', original_request)
        agency_name = agency_match.group(1) if agency_match else "[AGENCY NAME]"
        
        # Extract request details (very basic approach)
        request_match = re.search(r'following (?:documents|records)\s+be provided to me:\s+([^\n]+)', original_request)
        request_details = request_match.group(1) if request_match else "[REQUESTED RECORDS]"
        
        # Generate appeal text based on analysis
        appeal_text = f"""
{date}

Office of Information Policy
U.S. Department of Justice
1425 New York Avenue, NW, Suite 11050
Washington, DC 20530-0001

Re: Freedom of Information Act Appeal

Dear Sir or Madam:

This is an appeal under the Freedom of Information Act, 5 U.S.C. § 552.

On [DATE OF ORIGINAL REQUEST], I made a FOIA request to {agency_name} for {request_details}. On [DATE OF RESPONSE], I received a response denying my request """
        
        if analysis["exemptions_cited"]:
            exemptions_str = ", ".join([f"Exemption b({e})" for e in analysis["exemptions_cited"]])
            appeal_text += f"under {exemptions_str}."
        else:
            appeal_text += "in whole or in part."
        
        appeal_text += """

I appeal the denial of my request. The information withheld is not exempt under FOIA for the following reasons:

"""
        
        # Add specific arguments based on exemptions cited
        if "1" in analysis["exemptions_cited"]:
            appeal_text += "Regarding Exemption b(1): The agency has not demonstrated that the information is properly classified under Executive Order 13526 or that disclosure would cause identifiable harm to national security.\n\n"
        
        if "3" in analysis["exemptions_cited"]:
            appeal_text += "Regarding Exemption b(3): The agency has not identified the specific statute that exempts the information from disclosure, or has not shown that the information falls within the scope of that statute.\n\n"
        
        if "5" in analysis["exemptions_cited"]:
            appeal_text += "Regarding Exemption b(5): The agency has not demonstrated that the information is both predecisional and deliberative. Moreover, any factual information contained in the records should be segregated and released.\n\n"
        
        if "6" in analysis["exemptions_cited"]:
            appeal_text += "Regarding Exemption b(6): The agency has not demonstrated that disclosure would constitute a clearly unwarranted invasion of personal privacy. The public interest in disclosure outweighs any privacy interests.\n\n"
        
        if "7" in analysis["exemptions_cited"]:
            appeal_text += "Regarding Exemption b(7): The agency has not demonstrated that the records were compiled for law enforcement purposes or that disclosure would result in any of the harms specified in the exemption.\n\n"
        
        # Add general arguments if no specific exemptions were cited
        if not analysis["exemptions_cited"]:
            appeal_text += "The agency has not provided specific reasons for the denial that would allow me to formulate specific counterarguments. This lack of specificity itself violates FOIA's requirement that agencies provide requesters with meaningful notice of the specific reasons for a denial.\n\n"
        
        # Add segregability argument
        appeal_text += "Furthermore, even if portions of the requested records are exempt from disclosure, the agency has a duty to release any reasonably segregable non-exempt portions of the records. The agency has not demonstrated that it has fulfilled this obligation.\n\n"
        
        # Add closing
        appeal_text += f"""
For these reasons, I appeal the denial of my request and ask that the withheld records be disclosed in their entirety.

Thank you for your consideration of this appeal.

Sincerely,

{your_name}
{your_contact_info}
"""
        
        return appeal_text