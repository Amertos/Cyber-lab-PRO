import customtkinter as ctk
import threading
import sys
import os
import importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ROOT)

def load(rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, rel))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

# Imports
ps = load("password-security/strength_checker.py", "ps"); ph = load("password-security/hash_generator.py", "ph")
bs = load("brute-force-simulator/brute_demo.py", "bs"); pd = load("phishing-detector/phishing_check.py", "pd")
ns = load("network-basics/port_scanner.py", "ns"); me = load("metadata-extractor/exif_tool.py", "me")
et = load("encoding-tools/encoder.py", "et"); dr = load("recon-tools/dns_recon.py", "dr")
st = load("steganography/stego.py", "st"); ii = load("intelligence-tools/ip_info.py", "ii")
fs = load("system-tools/shredder.py", "fs"); ws = load("web-security/header_scan.py", "ws")
ms = load("malware-sim/key_sandbox.py", "ms"); hc = load("crypto-tools/hash_cracker.py", "hc")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🛡️ Cyber Lab PRO - Amer Biberovic")
        self.geometry("1150x780")
        ctk.set_appearance_mode("Dark"); ctk.set_default_color_theme("green")
        
        self.grid_columnconfigure(1, weight=1); self.grid_rowconfigure(0, weight=1)
        self.create_sidebar(); self.create_main()

    def create_sidebar(self):
        sb = ctk.CTkFrame(self, width=220, corner_radius=0); sb.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(sb, text="🛡️ PRO LAB", font=("Arial", 22, "bold")).pack(pady=20)
        
        scroll = ctk.CTkScrollableFrame(sb, fg_color="transparent"); scroll.pack(fill="both", expand=True, padx=5)
        tools = [
            ("🏠 Home", "home"), ("🔑 Passwords", "pass"), ("🔨 Brute Force", "brute"),
            ("🎣 Phishing", "phish"), ("🌐 Network", "net"), ("🖼️ Metadata", "meta"),
            ("🔏 Encoding", "enc"), ("🔍 DNS Recon", "dns"), ("🕵️ Stego", "stego"),
            ("📍 IP Intel", "ip"), ("🗑️ Shredder", "shred"), ("🛡️ Web Scan", "web"),
            ("👾 Malware", "mal"), ("🔓 Hash Crack", "crack")
        ]
        self.frames = {}
        for txt, key in tools:
            ctk.CTkButton(scroll, text=txt, anchor="w", command=lambda k=key: self.show(k)).pack(pady=5, fill="x")
        
        ctk.CTkLabel(sb, text="Made by Amer Biberovic\nv1.8.0 PRO", text_color="gray").pack(pady=10)

    def create_main(self):
        for key in ["home","pass","brute","phish","net","meta","enc","dns","stego","ip","shred","web","mal","crack"]:
            self.frames[key] = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
            getattr(self, f"set_{key}")(self.frames[key])
        self.show("home")

    def show(self, name):
        for f in self.frames.values(): f.grid_forget()
        self.frames[name].grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def set_home(self, f):
        ctk.CTkLabel(f, text="Welcome to Cyber Lab PRO", font=("Arial", 30, "bold")).pack(pady=50)
        ctk.CTkLabel(f, text="Developer: Amer Biberovic", font=("Arial", 20)).pack()
        ctk.CTkLabel(f, text="\nA high-performance security toolkit with 14 integrated modules.\nExplore, test, and learn defender techniques.", font=("Arial", 16)).pack(pady=30)

    def set_pass(self, f):
        t = ctk.CTkTabview(f); t.pack(pady=10); t.add("Strength"); t.add("Hash")
        # Strength
        t1 = t.tab("Strength"); e = ctk.CTkEntry(t1, width=300); e.pack(pady=10); l = ctk.CTkLabel(t1, text="")
        def run(): 
            r = ps.analyze_strength(e.get())
            l.configure(text=f"Grade: {r['grade']}\nEntropy: {r['entropy']:.2f}\n{r['advice']}")
        ctk.CTkButton(t1, text="Check", command=run).pack(); l.pack(pady=10)
        # Hash
        t2 = t.tab("Hash"); e2 = ctk.CTkEntry(t2, width=300); e2.pack(pady=10); txt = ctk.CTkTextbox(t2, height=200); txt.pack()
        def r2():
            txt.delete("1.0","end")
            for h in ph.get_hashes(e2.get()): txt.insert("end", f"{h['algo']}: {h['hash']}\n{h['status']}\n\n")
        ctk.CTkButton(t2, text="Generate", command=r2).pack(pady=10)

    def set_brute(self, f):
        ctk.CTkLabel(f, text="Brute Force Simulation", font=("Arial", 20, "bold")).pack(pady=10)
        
        # Settings
        cf = ctk.CTkFrame(f, fg_color="transparent"); cf.pack(pady=5)
        ctk.CTkLabel(cf, text="Target PW:").pack(side="left", padx=2)
        tg = ctk.CTkEntry(cf, width=120); tg.pack(side="left", padx=5); tg.insert(0,"secret123")
        ctk.CTkLabel(cf, text="Max Att:").pack(side="left", padx=2)
        ma = ctk.CTkEntry(cf, width=50); ma.pack(side="left", padx=5); ma.insert(0,"5")
        
        # Speed Control
        ctk.CTkLabel(cf, text="Delay (s):").pack(side="left", padx=2)
        speed_slider = ctk.CTkSlider(cf, from_=0, to=2, number_of_steps=20, width=150)
        speed_slider.pack(side="left", padx=5)
        speed_slider.set(0.5) # Default 0.5s

        # Wordlist Input
        ctk.CTkLabel(f, text="Custom Wordlist (one per line):", text_color="gray").pack()
        wl_txt = ctk.CTkTextbox(f, height=100); wl_txt.pack(fill="x", pady=5)
        wl_txt.insert("1.0", "123456\npassword\nadmin\nsecret123\nqwerty")

        log = ctk.CTkTextbox(f, height=250); log.pack(fill="x", pady=10)
        
        def s():
            log.delete("1.0","end")
            words = wl_txt.get("1.0", "end-1c").split("\n")
            words = [w.strip() for w in words if w.strip()]
            
            if not words:
                log.insert("end", "[!] Error: Wordlist is empty.\n")
                return

            delay_val = speed_slider.get()

            threading.Thread(target=bs.run_simulation, kwargs={
                "wordlist_path": words, 
                "target_password": tg.get(), 
                "max_attempts": int(ma.get()), 
                "delay": delay_val,
                "log_callback": lambda m: log.insert("end", m+"\n")
            }).start()
            
        ctk.CTkButton(f, text="🚀 Launch Attack", fg_color="red", hover_color="darkred", command=s).pack()

    def set_phish(self, f):
        ctk.CTkLabel(f, text="Phishing Detector").pack(pady=10); t = ctk.CTkTextbox(f, height=150); t.pack(fill="x"); res = ctk.CTkLabel(f, text="-"); res.pack()
        def s(): d = pd.get_phishing_score(t.get("1.0","end")); res.configure(text=f"Risk: {d['risk_level']}\nScore: {d['score']}")
        ctk.CTkButton(f, text="Scan", command=s).pack()

    def set_net(self, f):
        ctk.CTkLabel(f, text="Port Scanner").pack(); e = ctk.CTkEntry(f); e.insert(0,"127.0.0.1"); e.pack(); l = ctk.CTkTextbox(f, height=300); l.pack(fill="x", pady=10)
        def s(): l.delete("1.0","end"); threading.Thread(target=ns.scan_target, args=(e.get(), lambda b: l.insert("end", b+"\n"))).start()
        ctk.CTkButton(f, text="Scan", command=s).pack()

    def set_meta(self, f):
        ctk.CTkLabel(f, text="Metadata (EXIF)").pack(); p = ctk.CTkEntry(f, width=400); p.pack(pady=10); r = ctk.CTkTextbox(f, height=350); r.pack(fill="x")
        def s(): 
            r.delete("1.0","end"); data = me.get_exif_data(p.get())
            for k,v in data.items(): r.insert("end", f"{k}: {v}\n")
        ctk.CTkButton(f, text="Extract", command=s).pack(pady=10)

    def set_enc(self, f):
        ctk.CTkLabel(f, text="Encoding/Decoding").pack(); inp = ctk.CTkTextbox(f, height=100); inp.pack(fill="x"); out = ctk.CTkTextbox(f, height=100); out.pack(fill="x", pady=10)
        def d(m):
            v = inp.get("1.0","end").strip()
            if m=="be": r=et.encode_b64(v)
            elif m=="bd": r=et.decode_b64(v)
            elif m=="he": r=et.encode_hex(v)
            else: r=et.decode_hex(v)
            out.delete("1.0","end"); out.insert("1.0", r)
        c = ctk.CTkFrame(f); c.pack(); ctk.CTkButton(c, text="B64 E", command=lambda:d("be"), width=80).pack(side="left", padx=5)
        ctk.CTkButton(c, text="B64 D", command=lambda:d("bd"), width=80).pack(side="left", padx=5)
        ctk.CTkButton(c, text="HEX E", command=lambda:d("he"), width=80).pack(side="left", padx=5)
        ctk.CTkButton(c, text="HEX D", command=lambda:d("hd"), width=80).pack(side="left", padx=5)

    def set_dns(self, f):
        ctk.CTkLabel(f, text="DNS Recon").pack(); e = ctk.CTkEntry(f); e.insert(0,"google.com"); e.pack(); l = ctk.CTkLabel(f, text="-"); l.pack(pady=20)
        def s(): d=dr.get_dns_info(e.get()); l.configure(text=f"IP: {d.get('IP','-')}\nHost: {d.get('Hostname','-')}")
        ctk.CTkButton(f, text="Lookup", command=s).pack()

    def set_stego(self, f):
        tab = ctk.CTkTabview(f); tab.pack(); h = tab.add("Hide"); r = tab.add("Reveal")
        hp = ctk.CTkEntry(h, placeholder_text="Img Path"); hp.pack(pady=5); hm = ctk.CTkEntry(h, placeholder_text="Msg"); hm.pack(pady=5); ho = ctk.CTkEntry(h); ho.insert(0,"stego.png"); ho.pack(); res = ctk.CTkLabel(h, text="")
        def h1(): res.configure(text=st.hide_text(hp.get(), hm.get(), ho.get()))
        ctk.CTkButton(h, text="Hide", command=h1).pack(); res.pack()
        rp = ctk.CTkEntry(r); rp.pack(pady=5); rl = ctk.CTkLabel(r, text="")
        def r1(): rl.configure(text=f"Result: {st.extract_text(rp.get())}")
        ctk.CTkButton(r, text="Reveal", command=r1).pack(); rl.pack()

    def set_ip(self, f):
        ctk.CTkLabel(f, text="IP Intel").pack(); e = ctk.CTkEntry(f); e.pack(); res = ctk.CTkLabel(f, text="-"); res.pack(pady=20)
        def s(): 
            d = ii.get_ip_info(e.get()); txt = "\n".join([f"{k}: {v}" for k, v in d.items()])
            res.configure(text=txt)
        ctk.CTkButton(f, text="Scan", command=s).pack()

    def set_shred(self, f):
        ctk.CTkLabel(f, text="Secure Shredder").pack(); e = ctk.CTkEntry(f, width=400); e.pack(pady=10); ctk.CTkLabel(f, text="PERMANENTLY DELETE", text_color="red").pack()
        def s(): ctk.CTkLabel(f, text=fs.shred_file(e.get())).pack()
        ctk.CTkButton(f, text="SHRED", fg_color="darkred", command=s).pack()

    def set_web(self, f):
        ctk.CTkLabel(f, text="Web Header Scan").pack(); e = ctk.CTkEntry(f); e.insert(0,"google.com"); e.pack(); txt = ctk.CTkTextbox(f, height=300); txt.pack(fill="x", pady=10)
        def s():
            txt.delete("1.0","end"); res = ws.scan_headers(e.get())
            for r in res: txt.insert("end", f"[{r.get('Status','-')}] {r.get('Header','-')}\nValue: {r.get('Value','-')}\n\n")
        ctk.CTkButton(f, text="Scan", command=s).pack()

    def set_mal(self, f):
        ctk.CTkLabel(f, text="Keylogger Sandbox").pack(); sand = ms.KeySandbox(); e = ctk.CTkEntry(f, width=400); e.pack(pady=20); l = ctk.CTkTextbox(f, height=250); l.pack(fill="x")
        def k(ev): sand.log_key(ev.char); l.delete("1.0","end"); l.insert("1.0", sand.get_logs())
        e.bind("<Key>", k)

    def set_crack(self, f):
        ctk.CTkLabel(f, text="MD5 Hash Cracker").pack(); h = ctk.CTkEntry(f, width=400, placeholder_text="MD5 Hash"); h.pack(pady=10); res = ctk.CTkLabel(f, text="-"); res.pack(pady=10)
        def s(): 
            w = ["admin", "password", "123456", "secret123", "qwerty"]
            res.configure(text=hc.crack_md5(h.get(), w))
        ctk.CTkButton(f, text="Crack (Wordlist: Demo)", command=s).pack()

if __name__ == "__main__": App().mainloop()
