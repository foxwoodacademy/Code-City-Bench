import os
import sys
import os
import sys
from thoth_adapters import zeroclaw, lough, datacampus
from higgins_adapter import higgins
from front_desk_lady_v2 import OfficeManager

class ThothCore:
    def __init__(self):
        self.manager = OfficeManager()
        print("[Thoth Core]: Initialized. Swarm and Revenue interfaces active.")

    def generate_revenue(self, platform="Nostr"):
        """
        The 'Quick Capital' Macro:
        1. Route Packages (Create Invoices) -> 2. Generate Copy -> 3. Post to Network -> 4. Announce
        """
        print(f"\n[Thoth]: Activating Revenue Stream on {platform}...")

        # 1. Route packages and create Voltage invoices
        routing_res = higgins.route_packages(platform_filter=platform)
        if routing_res["exit_code"] != 0:
            print(f"[Error]: Routing failed: {routing_res['stderr']}")
            return False

        # 2. Generate promo copy for the products
        copy_res = higgins.generate_promo_copy("", platform=platform)
        copy_text = copy_res["stdout"]
        
        if not copy_text:
            print("[Error]: No promo copy generated.")
            return False

        # 3. Post to Network (if Nostr)
        if platform == "Nostr":
            posted = higgins.post_to_nostr(copy_text)
            if posted:
                print("[Thoth]: Copy successfully blasted to Nostr.")
            else:
                print("[Warn]: Nostr post failed or queued.")

        # 4. Emit event to Lough
        lough.emit(
            event_type="revenue.stream.activated",
            payload={"platform": platform, "status": "published"},
            location="thoth_core"
        )

        # 5. Mrs. Higgins announces the push
        self.manager.announce_completion(
            "Revenue Push", 
            f"SaaS packages routed to {platform}. Invoices created. Promo blasted to network."
        )

        print(f"[Thoth]: Revenue stream active. First blast:\n{copy_text[:500]}...")
        return True


    def deploy_lab_workflow(self, cohort_id, lab_id, capabilities, assignment_name="Quick Capital Lab"):
        """
        A lean automation: 
        DataCampus Assignment -> ZeroClaw Task -> Lough Event
        """
        print(f"\n[Thoth]: Initiating workflow for {assignment_name}...")

        # 1. DataCampus: Create Assignment
        assignment = datacampus.create_assignment(cohort_id, lab_id)
        if "error" in str(assignment):
            print(f"[Error]: DataCampus failed: {assignment}")
            return False

        assignment_id = getattr(assignment, 'assignment_id', 'unknown')
        print(f"[Thoth]: Assignment created: {assignment_id}")

        # 2. ZeroClaw: Create Task
        task = zeroclaw.create_task(assignment_id, lab_id, capabilities)
        if isinstance(task, dict) and "error" in task:
            print(f"[Error]: ZeroClaw failed: {task['error']}")
            return False
        print(f"[Thoth]: ZeroClaw task dispatched.")

        # 3. Lough: Emit Start Event
        lough.emit(
            event_type="swarm.workflow.started",
            payload={"assignment_id": assignment_id, "lab_id": lab_id},
            location="thoth_core"
        )
        print(f"[Thoth]: Lough event emitted.")

        # 4. Report to Mrs. Higgins
        self.manager.announce_completion(
            assignment_name, 
            f"Deployed lab {lab_id} to cohort {cohort_id}. Task is live in ZeroClaw."
        )
        return True

    def swarm_audit(self):
        """Quick check on all systems."""
        print("\n--- Swarm Audit ---")
        zc_status = zeroclaw.get_status()
        lough_poll = lough.poll(limit=1)

        print(f"ZeroClaw Status: {zc_status}")
        print(f"Lough Heartbeat: {'Active' if 'error' not in str(lough_poll) else 'Offline'}")
        print("------------------\n")

if __name__ == "__main__":
    # Quick Test
    thoth = ThothCore()
    thoth.swarm_audit()

    thoth.swarm_audit()
