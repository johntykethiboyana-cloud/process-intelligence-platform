from unittest import result

from comparison_v3.activity_matcher import ActivityMatcher
from comparison_v3.role_matcher import RoleMatcher
from comparison_v3.application_matcher import ApplicationMatcher
from comparison_v3.control_matcher import ControlMatcher
from comparison_v3.risk_matcher import RiskMatcher
from comparison_v3.input_output_matcher import InputOutputMatcher
from comparison_v3.sequence_matcher import SequenceMatcher
from comparison_v3.flow_analyzer import FlowAnalyzer
from comparison_v3.business_matcher import BusinessMatcher
from comparison_v3.role_intelligence import RoleIntelligence


class ComparisonEngine:
    """
    Comparison Engine V3

    Master comparison engine.

    Responsibilities

    • Process Name
    • Activities
    • Roles
    • Applications
    • Controls
    • Risks
    • Inputs
    • Outputs
    • Sequence
    • Overall Score
    """

    def __init__(self):

        self.business = BusinessMatcher()

        self.activities = ActivityMatcher()

        self.roles = RoleMatcher()

        self.applications = ApplicationMatcher()

        self.controls = ControlMatcher()

        self.risks = RiskMatcher()

        self.io = InputOutputMatcher()

        self.sequence = SequenceMatcher()

        self.flow = FlowAnalyzer()

        self.role_intelligence = RoleIntelligence()

    # -------------------------------------------------------
    # PROCESS NAME
    # -------------------------------------------------------

    def compare_process(self, l4_name, sop_name):

        result = self.business.compare(

            l4_name,

            sop_name

        )

        return {

            "l4": l4_name,

            "sop": sop_name,

            "percentage": round(

                result["score"],

                2

            ),

            "details": result

        }

    # -------------------------------------------------------
    # OVERALL SCORE
    # -------------------------------------------------------

    def calculate_overall(self, result):

        weights = {

            "process_name": 0.10,

            "activities": 0.30,

            "roles": 0.10,

            "applications": 0.10,

            "controls": 0.10,

            "risks": 0.05,

            "inputs": 0.05,

            "outputs": 0.05,

            "sequence": 0.15

        }

        overall = (

            result["process_name"]["percentage"]

            * weights["process_name"]

            +

            result["activities"]["percentage"]

            * weights["activities"]

            +

            result["roles"]["percentage"]

            * weights["roles"]

            +

            result["applications"]["percentage"]

            * weights["applications"]

            +

            result["controls"]["percentage"]

            * weights["controls"]

            +

            result["risks"]["percentage"]

            * weights["risks"]

            +

            result["inputs"]["percentage"]

            * weights["inputs"]

            +

            result["outputs"]["percentage"]

            * weights["outputs"]

            +

            result["sequence"]["percentage"]

            * weights["sequence"]

        )

        return round(overall, 2)

    # -------------------------------------------------------
    # MAIN COMPARISON
    # -------------------------------------------------------

    def compare(self, l4_data, sop_data):

        result = {}

        # -----------------------------------------

        result["process_name"] = self.compare_process(

            l4_data.get("process_name", ""),

            sop_data.get("process_name", "")

        )

        # -----------------------------------------

        result["activities"] = self.activities.compare(

            l4_data.get("activities", []),

            sop_data.get("activities", [])

        )

        # -----------------------------------------

        result["roles"] = self.roles.compare(

            l4_data.get("roles", []),

            sop_data.get("roles", [])

        )

        # -----------------------------------------

        result["applications"] = self.applications.compare(

            l4_data.get("applications", []),

            sop_data.get("applications", [])

        )

        # -----------------------------------------

        result["controls"] = self.controls.compare(

            l4_data.get("controls", []),

            sop_data.get("controls", [])

        )

        # -----------------------------------------

        result["risks"] = self.risks.compare(

            l4_data.get("risks", []),

            sop_data.get("risks", [])

        )

        # -----------------------------------------

        io = self.io.compare(

            l4_data.get("inputs", []),

            sop_data.get("inputs", []),

            l4_data.get("outputs", []),

            sop_data.get("outputs", [])

        )

        result["inputs"] = io["inputs"]

        result["outputs"] = io["outputs"]

        # -----------------------------------------

        result["sequence"] = self.sequence.compare(

            l4_data.get("steps", []),

            sop_data.get("steps", [])

        )

        # -----------------------------------------

        result["flow"] = self.flow.analyze(

            l4_data.get("steps", [])

        )

        # -----------------------------------------

        result["role_intelligence"] = self.role_intelligence.analyze(

        sop_data.get("steps", [])

        )

        # -----------------------------------------

        print("\n===== BEFORE OVERALL =====")
        print(result)
        print("==========================")

        result["overall"] = self.calculate_overall(

            result

        )

        # -----------------------------------------
        print("\n===== BEFORE OVERALL =====")
        print(result)
        print("==========================")
        result["overall"] = self.calculate_overall(

            result

        )

        return result


# -------------------------------------------------------
# TEST
# -------------------------------------------------------

if __name__ == "__main__":

    engine = ComparisonEngine()

    l4 = {

        "process_name": "Manage Price Negotiation",

        "activities": [

            "Create Tender",

            "Approve Tender",

            "Generate Report"

        ],

        "roles": [

            "CPM",

            "Finance"

        ],

        "applications": [

            "SAP",

            "GCSS"

        ],

        "controls": [

            "Manager Approval"

        ],

        "risks": [

            "Duplicate Tender"

        ],

        "inputs": [

            "Tender Request"

        ],

        "outputs": [

            "Approved Tender"

        ],

        "steps": [

            {

                "activity": "Create Tender"

            },

            {

                "activity": "Approve Tender"

            }

        ]

    }

    sop = {

        "process_name": "Manage Price Negotiation",

        "activities": [

            "Click Create Tender",

            "Approve Tender",

            "Generate Report"

        ],

        "roles": [

            "Contract Product Manager",

            "Finance"

        ],

        "applications": [

            "SAP",

            "GCSS"

        ],

        "controls": [

            "Manager Approval"

        ],

        "risks": [

            "Duplicate Tender"

        ],

        "inputs": [

            "Tender Request"

        ],

        "outputs": [

            "Approved Tender"

        ],

        "steps": [

            {

                "activity": "Create Tender"

            },

            {

                "activity": "Approve Tender"

            }

        ]

    }

    result = engine.compare(

        l4,

        sop

    )

    print("=" * 80)

    print("OVERALL :", result["overall"])

    print("=" * 80)

    print("Activities :", result["activities"]["percentage"])

    print("Roles :", result["roles"]["percentage"])

    print("Applications :", result["applications"]["percentage"])

    print("Controls :", result["controls"]["percentage"])

    print("Risks :", result["risks"]["percentage"])

    print("Inputs :", result["inputs"]["percentage"])

    print("Outputs :", result["outputs"]["percentage"])

    print("Sequence :", result["sequence"]["percentage"])