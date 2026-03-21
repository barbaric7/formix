import customtkinter as ctk
import json
import os
import sys
import threading
# from app import run_automation

# --- LOG REDIRECTION CLASS ---
class TextRedirector:
    """Redirects console print statements to the CustomTkinter textbox safely."""
    def __init__(self, textbox, root):
        self.textbox = textbox
        self.root = root

    def write(self, string):
        self.root.after(0, self._insert_text, string)

    def flush(self):
        pass
        
    def _insert_text(self, string):
        self.textbox.insert("end", string)
        self.textbox.see("end") 


class FormAutomationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window Configuration
        self.title("AutoForm AI")
        self.geometry("600x750") # Slightly taller to comfortably fit the new dropdowns
        self.resizable(False, False)
        
        ctk.set_appearance_mode("System") 
        ctk.set_default_color_theme("blue") 
        
        self.settings_file = "user_settings.json"
        self.user_data = self.load_settings()

        # Create Tab View (Fixed Alignment)
        # Using fill="both" and expand=True perfectly centers and stretches the tabs
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(pady=(10, 20), padx=20, fill="both", expand=True)

        self.tabview.add("Dashboard")
        self.tabview.add("Profile")

        self.setup_profile_tab()
        self.setup_dashboard_tab()

        if not self.user_data:
            self.tabview.set("Profile")
        else:
            self.tabview.set("Dashboard")

    def load_settings(self):
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as f:
                return json.load(f)
        return {}

    def save_settings(self):
        data = {
            "primary_api_key": self.primary_api_input.get(),
            "secondary_api_key": self.secondary_api_input.get(),
            "email": self.email_input.get(),
            "full_name": self.name_input.get(),
            "roll_number": self.roll_input.get(),
            "prn": self.prn_input.get(),
            "college": self.college_input.get(),
            "year": self.year_input.get(), # Now pulls from the dropdown
            "branch_division": self.branch_input.get()
        }
        with open(self.settings_file, "w") as f:
            json.dump(data, f)
        self.user_data = data
        
        self.tabview.set("Dashboard")
        print("✅ Profile saved successfully!")

    def setup_dashboard_tab(self):
        tab = self.tabview.tab("Dashboard")
        
        self.form_link_input = ctk.CTkEntry(tab, placeholder_text="Paste Google Form URL here...", height=40)
        self.form_link_input.pack(pady=(20, 10), padx=20, fill="x")

        self.start_btn = ctk.CTkButton(tab, text="Start Automation", command=self.start_automation_thread, height=40, fg_color="green", hover_color="dark green")
        self.start_btn.pack(pady=(0, 20), padx=20, fill="x")

        log_label = ctk.CTkLabel(tab, text="Live Terminal Logs", font=ctk.CTkFont(weight="bold"))
        log_label.pack(anchor="w", padx=20)
        
        self.log_textbox = ctk.CTkTextbox(tab, state="normal", fg_color="black", text_color="light green", font=ctk.CTkFont(family="Consolas", size=12))
        self.log_textbox.pack(pady=(0, 20), padx=20, fill="both", expand=True)

        sys.stdout = TextRedirector(self.log_textbox, self)

    def setup_profile_tab(self):
        tab = self.tabview.tab("Profile")
        
        scroll_frame = ctk.CTkScrollableFrame(tab, fg_color="transparent")
        scroll_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # ==========================================
        # CARD 1: AI Model Setup
        # ==========================================
        ai_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        ai_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(ai_frame, text="🤖 AI Model Setup", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5), padx=15, anchor="w")
        
        self.primary_api_input = self.create_input(ai_frame, "Primary API Key (OpenRouter / GPT)", show="*", default=self.user_data.get("primary_api_key", ""), placeholder="e.g. sk-or-v1-a1b2c3d4e5f6...")
        self.secondary_api_input = self.create_input(ai_frame, "Secondary API Key (Llama / Claude)", show="*", default=self.user_data.get("secondary_api_key", ""), placeholder="e.g. sk-or-v1-x9y8z7w6v5u4...")

        # ==========================================
        # CARD 2: Personal Details
        # ==========================================
        personal_frame = ctk.CTkFrame(scroll_frame, corner_radius=10)
        personal_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(personal_frame, text="👤 Personal Details", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15, 5), padx=15, anchor="w")
        
        self.email_input = self.create_input(personal_frame, "Email Address", default=self.user_data.get("email", ""))
        self.name_input = self.create_input(personal_frame, "Full Name", default=self.user_data.get("full_name", ""))
        self.roll_input = self.create_input(personal_frame, "Roll Number", default=self.user_data.get("roll_number", ""))
        self.prn_input = self.create_input(personal_frame, "PRN", default=self.user_data.get("prn", ""))
        self.college_input = self.create_input(personal_frame, "College Name", default=self.user_data.get("college", "Vishwakarma Institute of Technology"))
        
        # --- NEW YEAR DROPDOWN ---
        ctk.CTkLabel(personal_frame, text="Year", font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(fill="x", padx=15, pady=(10, 2))
        self.year_input = ctk.CTkComboBox(personal_frame, values=["Year I", "Year II", "Year III", "Year IV"], height=35)
        self.year_input.set(self.user_data.get("year", "Year II"))
        self.year_input.pack(fill="x", padx=15, pady=(0, 10))

        # --- BRANCH DROPDOWN ---
        ctk.CTkLabel(personal_frame, text="Branch & Division", font=ctk.CTkFont(size=12, weight="bold"), anchor="w").pack(fill="x", padx=15, pady=(10, 2))
        branch_options = [
            "CS-A", "CS-B", "CS-C", "CS-D", "CS-E", "CS-F", "CS-G", "CS-H", "CS-I",
            "CSAI-A", "CSAI-B", "CSAI-C", "CSAI-D", "CSAI-E", "CSAI-F", "CSAI-G", "CSAI-H",
            "CSAIML-A", "CSAIML-B", "CSAIML-C", "CSAIML-D", "CSAIML-E", "CSAIML-F",
            "CSSE-A", "CSSE-B", "CSSE-C", "CSSE-D",
            "CSDS-A", "CSDS-B", "CSDS-C",
            "CSIOT-A", "CSIOT-B", "CSIS-A", 
            "IT-A", "IT-B", "IT-C", "IT-D", "IT-E", "IT-F", "IT-G"
        ]
        self.branch_input = ctk.CTkComboBox(personal_frame, values=branch_options, height=35)
        self.branch_input.set(self.user_data.get("branch_division", "CSSE-B"))
        self.branch_input.pack(fill="x", padx=15, pady=(0, 20))

        # ==========================================
        # SAVE BUTTON
        # ==========================================
        self.save_btn = ctk.CTkButton(scroll_frame, text="Save & Apply Profile", command=self.save_settings, height=45, font=ctk.CTkFont(size=14, weight="bold"))
        self.save_btn.pack(pady=(10, 20), fill="x", padx=20)

    def create_input(self, parent, label_text, show="", default="", placeholder=""):
        label = ctk.CTkLabel(parent, text=label_text, font=ctk.CTkFont(size=12, weight="bold"), anchor="w")
        label.pack(fill="x", padx=15, pady=(10, 2))
        
        entry = ctk.CTkEntry(parent, show=show, placeholder_text=placeholder, height=35)
        if default:
            entry.insert(0, default)
        entry.pack(fill="x", padx=15, pady=(0, 10))
        return entry

    def start_automation_thread(self):
        form_url = self.form_link_input.get()
        if not form_url:
            print("❌ Error: Please paste a Google Form URL first.")
            return
            
        if not self.user_data:
            print("❌ Error: Please save your profile in the Profile tab first.")
            return

        self.user_data["form_url"] = form_url

        self.start_btn.configure(state="disabled", text="Running...")
        self.log_textbox.delete("1.0", "end") 
        print("🚀 Booting up automation engine...\n")
        
        thread = threading.Thread(target=self.run_automation_wrapper, daemon=True)
        thread.start()
        
    def run_automation_wrapper(self):
        try:
            run_automation(self.user_data)
        except Exception as e:
            print(f"\n❌ CRITICAL ERROR: {e}")
        finally:
            self.root.after(0, lambda: self.start_btn.configure(state="normal", text="Start Automation"))

if __name__ == "__main__":
    app = FormAutomationApp()
    app.mainloop()