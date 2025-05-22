from src.burnout_detector.tools.rootly_tools.shifts_tool import ShiftsTool
from src.burnout_detector.tools.rootly_tools.incidents_tool import IncidentsTool
from src.burnout_detector.tools.rootly_tools.users_tool import UsersTool


def test_shifts_tool():
    shifts_tool = ShiftsTool()
    print("Testing shifts tool...")
    print(f"{ShiftsTool.description}")
    shifts = shifts_tool.forward(schedule_name="Test Schedule")
    print(shifts)


def test_incidents_tool():
    incidents_tool = IncidentsTool()
    print("Testing incidents tool...")
    print(f"{IncidentsTool.description}")
    incidents = incidents_tool.forward(user_id=105511)
    print(incidents)


def test_users_tool():
    users_tool = UsersTool()
    print("Testing users tool...")
    print(f"{UsersTool.description}")
    users = users_tool.forward(search="Aniket")
    print(users)


if __name__ == "__main__":
    test_shifts_tool()
    test_incidents_tool()
    test_users_tool()
