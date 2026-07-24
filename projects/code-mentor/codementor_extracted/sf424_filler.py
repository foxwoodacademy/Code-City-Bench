class SF424Filler:
    def fill(self, profile, opportunity):
        """Populate SF-424 data structure"""
        return {
            "applicant_name": "ModMind Intelligence",
            "project_title": f"Proposal for {opportunity.get('title')}",
            "federal_identifier": opportunity.get('number'),
            "cfda_number": opportunity.get('cfdaList', ["N/A"])[0]
        }

if __name__ == "__main__":
    opp = {"title": "Test Grant", "number": "123-ABC", "cfdaList": ["81.135"]}
    filler = SF424Filler()
    print(filler.fill({}, opp))
