import subprocess
import pandas as pd

# Liste der zu testenden DNS-Server
dns_servers = {
    "Google (8.8.8.8)": "8.8.8.8",
    "Google (8.8.4.4)": "8.8.4.4",
    "Cloudflare (1.1.1.1)": "1.1.1.1",
    "Cloudflare (1.0.0.1)": "1.0.0.1",
    "Quad9 (9.9.9.9)": "9.9.9.9",
    "Quad9 (149.112.112.112)": "149.112.112.112"
}

# Funktion zum Pingen eines DNS-Servers


def ping_dns(server_ip):
    try:
        # Führe den Ping-Befehl aus (4 Pakete)
        result = subprocess.run(
            ["ping", "-c", "4", server_ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Extrahiere die durchschnittliche Latenzzeit
        for line in result.stdout.split("\n"):
            if "min/avg/max" in line:
                avg_latency = line.split("/")[4]  # Durchschnittliche Latenz
                return float(avg_latency)
        return None
    except Exception as e:
        print(f"Fehler beim Pingen von {server_ip}: {e}")
        return None


# Teste alle DNS-Server
results = []
for name, ip in dns_servers.items():
    print(f"Pinge {name} ({ip})...")
    avg_latency = ping_dns(ip)
    if avg_latency is not None:
        results.append({"DNS Server": name, "IP": ip,
                       "Avg Latency (ms)": avg_latency})
    else:
        results.append({"DNS Server": name, "IP": ip,
                       "Avg Latency (ms)": "Fehler"})

# Ergebnisse in einer Tabelle anzeigen
df = pd.DataFrame(results)
print("\nErgebnisse:")
print(df)

# Ergebnisse optional in eine CSV-Datei exportieren
df.to_csv("dns_ping_results.csv", index=False)
print("\nErgebnisse wurden in 'dns_ping_results.csv' gespeichert.")
