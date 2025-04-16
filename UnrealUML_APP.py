import customtkinter as ctk
import subprocess
import threading
import os
import webbrowser
import re

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class UMLRunnerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UnrealUML - Full Execution")
        self.geometry("720x480")

        self.output_box = ctk.CTkTextbox(self, width=680, height=380, wrap="word")
        self.output_box.pack(padx=20, pady=(20, 10), expand=True, fill="both")

        self.run_button = ctk.CTkButton(self, text="Run All", command=self.run_all)
        self.run_button.pack(pady=(0, 10))

    def log(self, text):
        self.output_box.insert("end", text + "\n")
        self.output_box.see("end")

    def check_java_version(self):
        try:
            result = subprocess.run(["java", "-version"], capture_output=True, text=True)
            output = result.stderr if result.stderr else result.stdout
            version_match = re.search(r'version "(.*?)"', output)
            if version_match:
                version_str = version_match.group(1)
                major = int(version_str.split(".")[0]) if version_str.startswith("1.") else int(version_str.split(".")[0])
                self.log(f"Java detected: {version_str}")
                if major < 17:
                    self.log("Incompatible Java version (< 17). Opening link to install JDK 17...")
                    webbrowser.open("https://download.oracle.com/java/17/archive/jdk-17.0.12_windows-x64_bin.msi")
                    return False
                return True
            else:
                self.log("Could not detect Java version.")
                return False
        except FileNotFoundError:
            self.log("Java is not installed. Opening link to install JDK 17...")
            webbrowser.open("https://download.oracle.com/java/17/archive/jdk-17.0.12_windows-x64_bin.msi")
            return False

    def execute_script(self, name):
        try:
            result = subprocess.run(["python", f"{name}.py"], capture_output=True, text=True, check=True)
            self.log(result.stdout.strip())
        except subprocess.CalledProcessError as e:
            self.log(f"Error running {name}.py: {e}")
            if e.stdout:
                self.log(e.stdout.strip())
            if e.stderr:
                self.log(e.stderr.strip())

    def run_all(self):
        self.run_button.configure(state="disabled")
        self.output_box.delete("1.0", "end")

        def _run_all_logic():
            self.log("Starting full process...")
            if not self.check_java_version():
                self.log("Install JDK 17.0.12 before proceeding.")
                self.run_button.configure(state="normal")
                return

            self.log("\n1. Generating raw PUML...")
            self.execute_script("GenerateUML")

            self.log("\n2. Cleaning PUML...")
            self.execute_script("CleanPuml")

            self.log("\n3. Rendering SVG...")
            self.execute_script("RenderSvg")

            self.log("\nProcess completed successfully.")
            self.run_button.configure(state="normal")

        threading.Thread(target=_run_all_logic, daemon=True).start()

if __name__ == "__main__":
    app = UMLRunnerApp()
    app.mainloop()
