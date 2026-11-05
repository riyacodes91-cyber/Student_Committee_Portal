import datetime

class ClassAnnouncement:
    """Manages structural data for announcements sent by leaders."""
    def __init__(self, target_committee: str, context: str, creator: str):
        self.target_committee = target_committee
        self.context = context
        self.creator = creator
        self.creation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

    def display(self):
        print(f"\n📢 [{self.creation_date}] - Committee: {self.target_committee}")
        print(f" From: {self.creator}")
        print(f" Message: {self.context}")
        print("-" * 50)


class Committee:
    """Manages committee setup, leadership alignment, and member directories."""
    def __init__(self, name: str, leader: str):
        self.name = name
        self.leader = leader
        self.members = set() # Using a set to prevent duplicate members

    def add_member(self, student_name: str) -> bool:
        if student_name == self.leader:
            print(f"❌ {student_name} is already the leader of this committee!")
            return False
        if student_name in self.members:
            print(f"⚠️ {student_name} is already a member of {self.name}.")
            return False
        self.members.add(student_name)
        print(f"✅ Successfully added {student_name} to {self.name}.")
        return True


class PortalManager:
    """Central structural class regulating authentication, dashboard loops, and committees."""
    def __init__(self):
        self.committees = {} # Format: {committee_name: Committee Object}
        self.announcements = [] # List of ClassAnnouncement objects
        self.current_user = None

        # Preseed mock data for quick verification
        self._seed_initial_data()

    def _seed_initial_data(self):
        # Create standard initial committees
        c1 = Committee("Rotaract", "Riya")
        c1.add_member("Sam")
        c1.add_member("Elina")

        c2 = Committee("Cultural Club", "David Miller")
        c2.add_member("Ritika")
        self.committees[c1.name.lower()] = c1
        self.committees[c2.name.lower()] = c2

    def get_choice(self, prompt: str, max_val: int) -> int:
        """Helper to ensure clean numeric menu selection inputs."""
        while True:
            try:
                val = int(input(prompt).strip())
                if 1 <= val <= max_val:
                    return val
                print(f"❌ Out of range. Enter a number between 1 and {max_val}.")
            except ValueError:
                print("❌ Invalid input! Please enter a valid number.")

    def run(self):
        """Application entry point handling login flow."""
        while True:
            print("\n=========================================")
            print("⚡ WELCOME TO THE STUDENT COMMITTEE PORTAL ⚡")
            print("=========================================")
            print("Enter 'Exit' as username to completely close the app.")

            username = input("👤 Enter your name to login: ").strip()
            if not username:
                print("❌ Username cannot be empty. Exiting application.")
                continue

            if username.lower() == "exit":
                print("👋 Exiting the portal. Goodbye!")
                break

            self.current_user = username
            print(f"🔑 Welcome back, {self.current_user}! Login Successful.")
            self.main_dashboard()

    def main_dashboard(self):
        """Primary interaction center routing paths based on account identities."""
        while True:
            print("\n" + "="*15 + " MAIN DASHBOARD " + "="*15)
            print("1. View Current Dynamic Feed")
            print("2. Manage / View Committees")
            print("3. Publish an Announcement")
            print("4. Logout & Exit")
            
            choice = self.get_choice("👉 Enter Option (1-4): ", 4)

            if choice == 1:
                self.view_feed()
            elif choice == 2:
                self.manage_committees()
            elif choice == 3:
                self.create_announcement()
            elif choice == 4:
                print(f"👋 Bye {self.current_user}! Have a great Day!")
                self.current_user = None
                break

    def view_feed(self):
        """Displays notifications and relevant text streams posted across committees."""
        print("\n" + "-"*15 + " COMMITTEE NOTIFICATION FEED " + "-"*15)
        
        # Find announcements relevant to committees the current user is part of (as leader or member)
        relevant_announcements = [
            ann for ann in self.announcements 
            if (ann.target_committee.lower() in self.committees and 
                (self.committees[ann.target_committee.lower()].leader == self.current_user or 
                 self.current_user in self.committees[ann.target_committee.lower()].members))
        ]

        if not relevant_announcements:
            print("📭 No new announcements found for your committees.")
            return

        for announcement in reversed(relevant_announcements):
            announcement.display()

    def manage_committees(self):
        """Submenu dealing with joining committees or reviewing assigned group leads."""
        while True:
            print("\n--- Committee Management ---")
            print("1. List All Active Committees")
            print("2. Create a New Committee")
            print("3. Join an Existing Committee")
            print("4. Return to Main Dashboard")
            
            choice = self.get_choice("👉 Enter Option (1-4): ", 4)

            if choice == 1:
                if not self.committees:
                    print("ℹ️ No active committees currently exist.")
                for c in self.committees.values():
                    print(f"• 📋 {c.name} | Leader: {c.leader} | Members: {', '.join(c.members) if c.members else 'None'}")
            
            elif choice == 2:
                name = input("✍️ Enter new Committee Name: ").strip()
                if name.lower() in self.committees:
                    print("❌ A committee with that name already exists!")
                elif name:
                    self.committees[name.lower()] = Committee(name, self.current_user)
                    print(f"🎉 Committee '{name}' successfully created with you as Leader!")
                else:
                    print("❌ Committee name cannot be empty.")
            
            elif choice == 3:
                name = input("🔍 Enter the name of the Committee you want to join: ").strip().lower()
                if name in self.committees:
                    self.committees[name].add_member(self.current_user)
                else:
                    print("❌ Committee not found. Check spelling or create it instead.")
            
            elif choice == 4:
                break

    def create_announcement(self):
        """Enables posting announcements if authorization validations pass."""
        print("\n--- Publish Announcement ---")
        target = input("📣 Enter target Committee Name: ").strip()
        
        if target.lower() not in self.committees:
            print("❌ Target committee does not exist.")
            return

        committee = self.committees[target.lower()]
        
        # Authorization check: Only the designated leader can dispatch messages
        if committee.leader.lower() != self.current_user.lower():
            print(f"❌ Access Denied! Only the leader ({committee.leader}) can broadcast alerts.")
            return

        message = input("📝 Enter your announcement text content: ").strip()
        if message:
            new_ann = ClassAnnouncement(committee.name, message, self.current_user)
            self.announcements.append(new_ann)
            print("🚀 Announcement successfully updated and broadcast to members!")
        else:
            print("❌ Announcement cannot be empty.")


if __name__ == "__main__":
    # Initialize infrastructure system and start program execution loop
    portal = PortalManager()
    portal.run()