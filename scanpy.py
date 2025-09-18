#!/usr/bin/python3
#scanpy.py


import sys
import socket
import threading
import argparse
import time
import datetime
from ipaddress import ip_address
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import concurrent.futures
from tqdm import tqdm




# Ports courants importants:
COMMON_PORTS = {
    21: ['ftp', 'probe_ftp'],
    22: ['ssh', 'probe_ssh'],
    23: ['telnet', 'probe_telnet'],
    25: ['smtp', 'probe_smtp'],
    49: ['tacacs', 'probe_tacacs'],
    53: ['dns', 'probe_dns'],
    80: ['http', 'probe_http'],
    81: ['http', 'probe_http'],
    88: ['kerberos', 'probe_kerberos'],
    110: ['pop3', 'probe_pop'],
    111:['rpcbind', 'probe_rpcbind'],
    115: ['sftp', 'probe_sftp'],
    135: ['msrpc', 'probe_msrpc'],
    137: ['netbios-ns', 'probe_netbios_ns'],
    138: ['netbios-dgm', 'probe_netbios_dgm'],
    139: ['netbios-smb', 'probe_smb'],
    143: ['imap', 'probe_imap'],
    161: ['snmp', 'probe_snmp'],
    194: ['irc', 'probe_irc'],
    220: ['imap3', 'probe_imap3'],
    389: ['ldap', 'probe_ldap'],
    443: ['https', 'probe_https'],
    445: ['smb', 'probe_smb'],
    464: ['kpasswd5', 'probe_kpasswd5'],
    465: ['smtps', 'probe_smtps'],
    502: ['modbus', 'probe_modbus'],                # Protocol utilisé en industrie.
    514: ['rsh', 'porbe_rsh'],
    515: ['lpd', 'probe_printer'],                  # Line Printer Daemon
    554: ['rtsp', 'probe_rtsp'],                    # Controleur iP caméra
    587: ['smtp', 'probe_smtp'],
    593: ['msrpc', 'probe_msrpc'],
    636: ['ldaps', 'probe_ldaps'],
    749: ['kerberos-adm', 'probe_kerberos_adm'],
    760: ['krupdate', 'probe_krupdate'],
    761: ['kpaswd', 'probe_kpasswd'],
    873: ['rsync', 'probe_rsync'],                  # netcat -nv host 873
    992: ['telnets', 'probe_telnets'],
    990: ['ftps', 'probe_ftps'],
    992: ['telnets', 'probe_telnets'],
    993: ['imaps', 'probe_imaps'],
    994: ['ircs', 'porbe_ircs'],
    995: ['pop3s', 'probe_pop3s'],
}


        # Partie 1: on vérifie les données utilisateur

#  Convertir un host en IPv4 si nbesoin..
def translate_host(target):
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print("\033[91m Target invalid \033[0m")
        sys.exit(1)



        # Partie2: les scans par type

# fonction pour la structure du scanner
# Variable s  =>  socket listen() et close()
def basic_scan(target, port, pbar=None, banner=False):
    is_open = False
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.setdefaulttimeout(0.5)
        result = s.connect_ex((target, port))
        s.close()
        if result == 0:
            print(f"\033[92m Port {port} is open  🔓🔓 \033[0m")
            openPorts.append(port)
            is_open = True
    
    except Exception as exc:
        print(f"\033[91m Error scanning port {port}: {exc}\033[0m")
    
    finally:
        if pbar:
            pbar.update(1)
    if is_open and banner:
        banner_scan(target, port)
    return is_open
            
            

#  fonction pour le threading
openPorts = []      # liste des ports ouverts

def advanced_scan(target, ports, banner=False):
    with tqdm(total=len(ports), desc="Scanning ports (threaded) 🌡️", colour='green') as pbar:
        
        threads = []        
        for port in ports:
            t = threading.Thread(target=basic_scan, args=(target, port, pbar, banner))
            threads.append(t)
            t.start()
        
        for thread in threads:
            thread.join()


    
# Pour les gros réseaux. Ex: ActiveDirectory pour les entreprises.Ou autre     
def concurrent_scan_big(target, ports, banner=False):
    with tqdm(total=len(ports), desc="Scanning ports (concurrent)", colour='green') as pbar:
    
        with ThreadPoolExecutor(max_workers=100) as executor:
            futures = [executor.submit(basic_scan, target, port, pbar, banner) for port in ports]
            for future in concurrent.futures.as_completed(futures):
                pass
            




# déterminer quel service s'exécute en lisant la réponse de l'hôte
def grab_banner(s):
    return s.recv(1024).decode('utf-8', errors='ignore')



def banner_scan(target, port): # option -b
    s = socket.socket()
    
    try:
        s.connect((target, port))
        s.send(b'\r\n')     # envoie neutre ou à vide
        banner = grab_banner(s)
        if banner.strip():
            print(f"\033[93m Service on port {port} : {banner} 🔓️🔓️ \033[0m")
        else:
            print(f"\033[93m No service banner for port {port} 🔒️🔒️ 🚫 \033[0m")
    
    except Exception as e:
        print(f"\033[91m Error grabbing banner for port {port}: {e} ⚠️ \033[0m")
    
    finally:
        s.close()

    
    



# cette partie gère l'interaction avec le user
if __name__=="__main__" :
    
    from help import get_parsed_args
    
    args = get_parsed_args()
    
    if (args.pS > args.pE):
        print("\033[91m Erreur 🚨🚨: -pS doit être inférieur à -pE .\033[0m")
        sys.exit(1)
        
    target = translate_host(args.u)
    ports = list(range(args.pS, args.pE + 1))
    
    print(f"\033[94m Scanning {target} ports {args.pS} -> {args.pE} in mode {args.m}.....🚀🚀\033[0m")
    
    start_time = time.perf_counter()
    
    if args.m == 'basic':
        with tqdm(total=len(ports), desc="Scanning ports (basic)", colour='green') as pbar:
            for port in ports:
                basic_scan(target, port, pbar, args.b)
    elif args.m == 'advanced':
        advanced_scan(target, ports, args.b)
    elif args.m == 'concurrent':
        concurrent_scan_big(target, ports, args.b)
    
    end_time = time.perf_counter()  # Fin du timer
    elapsed_time = end_time - start_time
    print(f"\033[92m Scan completed in {elapsed_time:.2f} seconds.🕤️\033[0m")
    print(f"\033[93m 🔭 Open ports: {openPorts} 🔭\033[0m")