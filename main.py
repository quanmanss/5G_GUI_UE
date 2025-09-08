import tkinter as tk
from tkinter import ttk
import webbrowser
import os
import threading
import subprocess
import signal

ping_process = None
traceroute_process = None

def open_youtube():
    url = "https://www.youtube.com/embed/dQw4w9WgXcQ"  # Thay bằng video bạn muốn
    webbrowser.open(url)

def open_ping_window():
    win = tk.Toplevel()
    win.title("PING")
    win.geometry("500x400")
      # địa chỉ IP ping
    tk.Label(win, text="Địa chỉ:").pack(anchor="w", padx=10, pady=2)
    address_entry = tk.Entry(win)
    address_entry.pack(fill="x", padx=10)
     # số lần Ping
    tk.Label(win, text="Số gói (0 = vô hạn):").pack(anchor="w", padx=10, pady=2)
    count_entry = tk.Entry(win)
    count_entry.insert(0, "0")
    count_entry.pack(fill="x", padx=10)
    # password sudo 
    tk.Label(win, text="Mật khẩu sudo:").pack(anchor="w", padx=10, pady=2)
    password_entry= tk.Entry(win)
    password_entry.pack(fill="x", padx=10)
    btn_frame = tk.Frame(win)
    btn_frame.pack(fill="x", padx=10, pady=5)
    console_text = tk.Text(win, height=15, bg="white", fg="#2a4d8f")
    console_text.pack(fill="both", expand=True, padx=10, pady=5)
    console_text.config(state="disabled")
    win.ping_process = None

    def run_ping():
        address = address_entry.get()
        count = count_entry.get()
        password = password_entry.get()
        if not address:
            console_text.config(state="normal")
            console_text.insert("end", "Vui lòng nhập địa chỉ!\n")
            console_text.config(state="disabled")
            return
        console_text.config(state="normal")
        console_text.delete("1.0", "end")
        console_text.insert("end", f"Ping {address}...\n")
        console_text.config(state="disabled")
        if count == "0" or count.strip() == "":
            cmd = ["sudo", "-S", "ip", "netns", "exec", "ue1", "ping", address]
        else:
            cmd = ["sudo", "-S", "ip", "netns", "exec", "ue1", "ping", "-c", count, address]
        win.ping_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)
        win.ping_process.stdin.write(password + "\n")
        win.ping_process.stdin.flush()
        def read_output():
            for line in win.ping_process.stdout:
                console_text.config(state="normal")
                console_text.insert("end", line)
                console_text.see("end")
                console_text.config(state="disabled")
            win.ping_process.stdout.close()
        threading.Thread(target=read_output, daemon=True).start()

    def stop_ping():
        if win.ping_process and win.ping_process.poll() is None:
            win.ping_process.terminate()
            console_text.config(state="normal")
            console_text.insert("end", "Ping stopped.\n")
            console_text.config(state="disabled")

    tk.Button(btn_frame, text="Ping", command=run_ping, bg="#4a7bd8", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Stop", command=stop_ping, bg="#d84a4a", fg="white").pack(side="left", padx=5)

def open_traceroute_window():
    win = tk.Toplevel()
    win.title("TRACEROUTE")
    win.geometry("500x400")
    tk.Label(win, text="Địa chỉ:").pack(anchor="w", padx=10, pady=2)
    address_entry = tk.Entry(win)
    address_entry.pack(fill="x", padx=10)
    tk.Label(win, text="Số hop tối đa (mặc định 30):").pack(anchor="w", padx=10, pady=2)
    hops_entry = tk.Entry(win)
    hops_entry.insert(0, "30")
    hops_entry.pack(fill="x", padx=10)
    # password sudo 
    tk.Label(win, text="Mật khẩu sudo:").pack(anchor="w", padx=10, pady=2)
    password_entry= tk.Entry(win)
    password_entry.pack(fill="x", padx=10)
    btn_frame = tk.Frame(win)
    btn_frame.pack(fill="x", padx=10, pady=5)
    console_text = tk.Text(win, height=15, bg="white", fg="#2a4d8f")
    console_text.pack(fill="both", expand=True, padx=10, pady=5)
    console_text.config(state="disabled")
    win.traceroute_process = None

    def run_traceroute():
        address = address_entry.get()
        hops = hops_entry.get()
        password = password_entry.get()
        if not address:
            console_text.config(state="normal")
            console_text.insert("end", "Vui lòng nhập địa chỉ!\n")
            console_text.config(state="disabled")
            return
        console_text.config(state="normal")
        console_text.delete("1.0", "end")
        console_text.insert("end", f"Traceroute {address}...\n")
        console_text.config(state="disabled")
        if hops and hops != "30":
            cmd = ["sudo", "-S", "ip", "netns", "exec", "ue1", "traceroute", "-m", hops, address]
        else:
            cmd = ["sudo", "-S", "ip", "netns", "exec", "ue1", "traceroute", address]
        win.traceroute_process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True)
        win.traceroute_process.stdin.write(password + "\n")
        win.traceroute_process.stdin.flush()
        def read_output():
            for line in win.traceroute_process.stdout:
                console_text.config(state="normal")
                console_text.insert("end", line)
                console_text.see("end")
                console_text.config(state="disabled")
            win.traceroute_process.stdout.close()
        threading.Thread(target=read_output, daemon=True).start()

    def stop_traceroute():
        if win.traceroute_process and win.traceroute_process.poll() is None:
            win.traceroute_process.terminate()
            console_text.config(state="normal")
            console_text.insert("end", "Traceroute stopped.\n")
            console_text.config(state="disabled")

    tk.Button(btn_frame, text="Traceroute", command=run_traceroute, bg="#4a7bd8", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Stop", command=stop_traceroute, bg="#d84a4a", fg="white").pack(side="left", padx=5)
 

def main():
    root = tk.Tk()
    root.title("5G UE GUI v1.0")
    root.geometry("1080x800")
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
    app_buttons = [
        ("SIP call", None),
        ("Browser", open_youtube),
        ("PING", open_ping_window),
        ("TRACEROUTE", open_traceroute_window),
        ("", None),
        ("", None),
        ("", None)
    ]
    for i, (name, cmd) in enumerate(app_buttons):
        if name and cmd:
            tk.Button(apps_frame, text=name, width=14, height=2, bg="#4a7bd8", fg="white", command=cmd).grid(row=0, column=i, padx=8, pady=10)
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