import sys
import argparse
from thoth_core import ThothCore

def main():
    parser = argparse.ArgumentParser(description="Thoth Swarm Command Center")
    parser.add_argument("--audit", action="store_true", help="Run a quick swarm audit")
    parser.add_argument("--deploy", action="store_true", help="Run the deploy_lab_workflow demo")
    parser.add_argument("--revenue", action="store_true", help="Activate the revenue generation funnel")
    parser.add_argument("--platform", type=str, default="Nostr", help="Platform for revenue push (e.g. Nostr, Fiverr)")
    parser.add_argument("--cohort", type=str, default="cohort_01", help="Cohort ID for deployment")
    parser.add_argument("--lab", type=str, default="lab_test_01", help="Lab ID for deployment")
    
    args = parser.parse_args()
    thoth = ThothCore()

    if args.audit:
        thoth.swarm_audit()
    elif args.revenue:
        thoth.generate_revenue(platform=args.platform)
    elif args.deploy:
        # Demo capabilities: ['python', 'networking']
        thoth.deploy_lab_workflow(args.cohort, args.lab, ['python', 'networking'])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
