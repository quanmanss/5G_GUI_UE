import tkinter as tk
from tkinter import ttk
import webbrowser
import os

def open_youtube():
    # Thay đổi interface mạng mặc định sang srs0 (Linux: dùng 'ip route', Windows: cần cấu hình route trước)
    # Ở đây chỉ mở trình duyệt, giả sử máy đã route qua srs0
    url = "https://www.youtube.com/embed/dQw4w9WgXcQ"  # Thay bằng video bạn muốn
    webbrowser.open(url)

def main():
    root = tk.Tk()
    root.title("5G UE GUI v1.0")
    root.geometry("800x600")
    root.configure(bg="white")

    # Header
    header = tk.Frame(root, bg="white")
    header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
    tk.Label(header, text="5G UE GUI", font=("Arial", 16, "bold"), bg="white", fg="#2a4d8f").grid(row=0, column=0, sticky="w")
    tk.Label(header, text="v1.0", font=("Arial", 10), bg="white").grid(row=0, column=1, sticky="w", padx=10)
    tk.Button(header, text="Config").grid(row=0, column=2, padx=5)
    tk.Button(header, text="Source").grid(row=0, column=3, padx=5)
    tk.Button(header, text="About").grid(row=0, column=4, padx=5)
    tk.Label(header, text="Status: Standby/Cell connected/Internet connected/Error", bg="white", fg="#2a4d8f").grid(row=0, column=5, sticky="e", padx=20)
    header.grid_columnconfigure(5, weight=1)

    # Status & Actions
    top_frame = tk.Frame(root, bg="white")
    top_frame.grid(row=1, column=0, sticky="ew", padx=10)
    status_frame = tk.LabelFrame(top_frame, text="Status", bg="white", width=400)
    status_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
    actions_frame = tk.LabelFrame(top_frame, text="Actions", bg="white", width=400)
    actions_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

    status_text = (
        "Cell state: Connected/Disconnected\n"
        "Cell info: ...\n"
        "Signal strength: xxx%\n"
        "Connection state: Connected/Disconnected\n"
        "Link speed: xxx UP xxx DOWN\n"
        "Connect timer: xx:xx:xx"
    )
    tk.Label(status_frame, text=status_text, justify="left", bg="white", anchor="w").pack(anchor="w", padx=5, pady=5)

    for i, btn in enumerate(["Connect", "Disconnect", "Route", "UnRoute"]):
        tk.Button(actions_frame, text=btn, width=12, height=2, bg="#4a7bd8", fg="white").grid(row=0, column=i, padx=8, pady=10)

    # Apps
    apps_frame = tk.LabelFrame(root, text="Apps", bg="white")
    apps_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
    app_buttons = ["SIP call", "Browser", "", "", "", "", ""]
    for i, name in enumerate(app_buttons):
        if name == "Browser":
            tk.Button(apps_frame, text=name, width=14, height=2, bg="#4a7bd8", fg="white", command=open_youtube).grid(row=0, column=i, padx=8, pady=10)
        elif name:
            tk.Button(apps_frame, text=name, width=14, height=2, bg="#4a7bd8", fg="white").grid(row=0, column=i, padx=8, pady=10)
        else:
            tk.Button(apps_frame, width=14, height=2, bg="#4a7bd8", state="disabled").grid(row=0, column=i, padx=8, pady=10)

    # Console log
    log_frame = tk.LabelFrame(root, text="Console log", bg="white")
    log_frame.grid(row=3, column=0, sticky="nsew", padx=10, pady=5)
    log_text = tk.Text(log_frame, height=12, bg="white", fg="#2a4d8f")
    log_text.pack(fill="both", expand=True)
    for _ in range(12):
        log_text.insert("end", "hh:mm:ssxxx dd-MM-yyyy [INFO] 5GUEGUI: sample log\n")
    log_text.config(state="disabled")

    root.grid_rowconfigure(3, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.mainloop()

if __name__ == "__main__":
    main()