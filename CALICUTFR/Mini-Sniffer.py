from scapy.all import sniff, IP, TCP, UDP, ARP, DNS, Ether
from collections import Counter
import sys
import time
import os
from datetime import datetime

# --- ANSI Color Definitions for Wireshark-like Coloring ---
# Corrected: Removed all non-standard spaces (U+00A0)
GREEN = '\033[92m' # For TCP (e.g., ACK/SYN)
YELLOW = '\033[93m' # For UDP
CYAN = '\033[96m' # For ICMP/DNS
BLUE = '\033[94m' # For IP/General
RED = '\033[91m' # For Errors/Warnings
MAGENTA = '\033[95m'# For HTTP/TLS
RESET = '\033[0m' # Color reset

    # 1. Le logo en texte ASCII généré (exemple)
logo_ascii = """
                                                 @@@@@@@@@@@@@@@@@@@                                 
                                         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                         
                                    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                    
                                @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                
                             @@@@@@@@@@@@@@@@@@                       @@@@@@@@@@@@@@@@@@             
                           @@@@@@@@@@@@@@                                   @@@@@@@@@@@@@@@          
                        @@@@@@@@@@@@@              @@@@@@@@@@@@@@@              @@@@@@@@@@@@@        
                       @@@@@@@@@@@          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@          @@@@@@@@@@@       
                       @@@@@@@@         @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         @@@@@@@@       
                        @@@@@        @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@        @@@@@        
                                  @@@@@@@@@@@@@@@                   @@@@@@@@@@@@@@@                  
                                @@@@@@@@@@@@@                           @@@@@@@@@@@@@                
                               @@@@@@@@@@            @@@@@@@@@@@            @@@@@@@@@@               
                                @@@@@@@         @@@@@@@@@@@@@@@@@@@@@         @@@@@@@                
                                            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                            
                                          @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                          
                                         @@@@@@@@@@@             @@@@@@@@@@@                         
                                        @@@@@@@@@                   @@@@@@@@@                        
                                         @@@@@@        @@@@@@@        @@@@@@                         
                                                    @@@@@@@@@@@@@                                    
                                                   @@@@@@@@@@@@@@@                                   
                                                  @@@@@@@@@@@@@@@@@                                  
                                                  @@@@@@@@@@@@@@@@@                                  
                                                   @@@@@@@@@@@@@@@                                   
                                                    @@@@@@@@@@@@@                                    
                                                       @@@@@@@            

"""

# 2. Nettoyer l'écran avant l'affichage (optionnel, mais propre)
# 'cls' pour Windows, 'clear' pour Linux/macOS
os.system('cls' if os.name == 'nt' else 'clear')

# 3. Afficher le logo
print(logo_ascii)

# 4. Ajouter une petite pause avant le reste du script (optionnel)
time.sleep(2)


# --- Global Storage and Counters ---
captured_packets = []
protocol_stats = Counter()
start_time = None
bytes_captured = 0

# --- Helper Functions for Enhanced Features ---

def get_protocol_info(packet):
    """Determines the main protocol, color, and summary information."""
    
    color = RESET
    protocol = "Other"
    info = ""
    
    if IP in packet:
        # Check for Transport Layer
        if TCP in packet:
            protocol = "TCP"
            color = GREEN
            flags = packet[TCP].sprintf('%TCP.flags%')
            info = f"SrcPort:{packet[TCP].sport} -> DstPort:{packet[TCP].dport} | Flags:{flags}"
            
            if packet[TCP].dport == 80 or packet[TCP].sport == 80:
                 protocol = "HTTP"
                 color = MAGENTA
            if packet[TCP].dport == 443 or packet[TCP].sport == 443:
                 protocol = "TLSv1.2" # Common placeholder
                 color = MAGENTA
                 
        elif UDP in packet:
            protocol = "UDP"
            color = YELLOW
            info = f"SrcPort:{packet[UDP].sport} -> DstPort:{packet[UDP].dport}"
            
            # Check for Application Layer over UDP
            if DNS in packet:
                protocol = "DNS"
                color = CYAN
                # Handles potential errors when decoding
                try:
                    qname = packet[DNS].qd.qname.decode().rstrip('.')
                except AttributeError:
                    qname = 'N/A'
                info = f"ID:{packet[DNS].id} | QName: {qname}"
                
        elif packet[IP].proto == 1:
            protocol = "ICMP"
            color = CYAN
            info = f"Type:{packet[IP].payload.type} | Code:{packet[IP].payload.code}"
            
        else:
            protocol = f"IP ({packet[IP].proto})"
            color = BLUE
            
    elif ARP in packet:
        protocol = "ARP"
        color = BLUE
        op = 'Request' if packet[ARP].op == 1 else 'Reply'
        info = f"{op}: Who has {packet[ARP].pdst}?"
        
    # Update global statistics
    protocol_stats[protocol] += 1
    
    return protocol, color, info

# Feature 1: Deep Packet Analysis and Coloring
def analyze_packet(packet):
    """Analyzes and displays captured packet details with coloring."""
    global bytes_captured
    
    protocol, color, info = get_protocol_info(packet)
    
    # Feature 2: Time Stamping
    # Use datetime for better precision and format consistency
    timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
    
    # Feature 3: Source and Destination Display
    src = packet[Ether].src if Ether in packet else 'N/A'
    dst = packet[Ether].dst if Ether in packet else 'N/A'
    
    if IP in packet:
        src = packet[IP].src
        dst = packet[IP].dst
        
    length = len(packet)
    bytes_captured += length
    
    # Feature 4: Formatted Output (Wireshark-like columns)
    print(f"[{timestamp}] "
          f"{color}{protocol:10}{RESET} "
          f"{src:15} -> {dst:15} "
          f"| {length:5} Bytes | "
          f"{info}")

    # Feature 5: Packet Storage for further analysis/export
    captured_packets.append(packet)


# Feature 6: Real-time Statistics Display
def display_stats():
    """Calculates and displays current capture statistics."""
    
    if not start_time:
         print(f"\n{YELLOW}No capture data available. Please start a capture first.{RESET}")
         return

    elapsed = time.time() - start_time
    total_packets = sum(protocol_stats.values())
    
    if total_packets == 0:
        print(f"\n{YELLOW}No packets captured during the session.{RESET}")
        return
        
    rate = total_packets / elapsed if elapsed > 0 else 0
    avg_byte_rate = (bytes_captured / elapsed) / 1024 if elapsed > 0 else 0
    
    print("\n" + "="*60)
    print(f"{BLUE}--- Capture Statistics ---{RESET}")
    print(f"Total Packets: {total_packets}")
    print(f"Total Bytes:   {bytes_captured} ({bytes_captured / 1024 / 1024:.2f} MB)")
    print(f"Time Elapsed:  {elapsed:.2f} seconds")
    print(f"Packet Rate:   {rate:.2f} pkts/sec")
    print(f"Throughput:    {avg_byte_rate:.2f} KB/sec")
    
    print("\nProtocol Distribution:")
    for proto, count in protocol_stats.most_common():
        percentage = (count / total_packets) * 100
        print(f"  - {proto:10}: {count:5} ({percentage:.2f}%)")
        
    print("="*60)


# Feature 7: PCAP Export
def export_pcap(filename):
    """Exports all captured packets to a pcap file."""
    try:
        from scapy.all import wrpcap
        wrpcap(filename, captured_packets)
        print(f"\n{GREEN}*** Success: {len(captured_packets)} packets exported to '{filename}'. ***{RESET}")
    except Exception as e:
        print(f"\n{RED}*** Error exporting PCAP: {e} ***{RESET}")

# Feature 8: Filtered Summary Display
def display_summary(filter_proto=""):
    """Displays a summary of captured packets, optionally filtered by protocol."""
    
    if not captured_packets:
        print(f"\n{YELLOW}No packets have been captured yet.{RESET}")
        return

    filtered_packets = []
    if filter_proto:
        for p in captured_packets:
            protocol, _, _ = get_protocol_info(p)
            if protocol.upper() == filter_proto.upper():
                filtered_packets.append(p)
    else:
        filtered_packets = captured_packets

    if not filtered_packets:
         print(f"\n{YELLOW}No packets found matching the filter: {filter_proto}.{RESET}")
         return

    print("\n" + "="*60)
    print(f"{BLUE}--- Captured Packet Summary (Showing {min(len(filtered_packets), 20)}/{len(captured_packets)}) ---{RESET}")
    for i, packet in enumerate(filtered_packets[:20]): # Show first 20 for brevity
        protocol, color, info = get_protocol_info(packet)
        src = packet[IP].src if IP in packet else (packet[Ether].src if Ether in packet else 'N/A')
        dst = packet[IP].dst if IP in packet else (packet[Ether].dst if Ether in packet else 'N/A')
        
        print(f"{i+1:3}: [{color}{protocol:5}{RESET}] {src:15} -> {dst:15} | {len(packet)} Bytes")
    
    if len(filtered_packets) > 20:
        print("...")
        
    print("="*60)
    
# Feature 9: Start Capture Function
def start_capture(bpf_filter, iface=None):
    """Starts packet capture with the specified BPF filter."""
    global captured_packets, protocol_stats, start_time, bytes_captured
    
    # Reset globals for new capture
    captured_packets = []
    protocol_stats = Counter()
    bytes_captured = 0
    start_time = time.time()
    
    print(f"\n{BLUE}--- Starting Capture (Filter: '{bpf_filter}') ---{RESET}")
    print(f"Press {YELLOW}Ctrl+C{RESET} to stop the capture and return to the menu.")
    print("--------------------------------------------------")
    
    try:
        # Feature 10: Interface Selection (iface argument can be passed, though not prompted in menu)
        # Note: Scapy will use the default interface if 'iface' is None
        sniff(prn=analyze_packet, filter=bpf_filter, store=False, iface=iface)
        
    except KeyboardInterrupt:
        print(f"\n{GREEN}*** Capture stopped by user (Ctrl+C). ***{RESET}")
        display_stats()
    except Exception as e:
        print(f"\n{RED}*** Capture Error: {e} ***{RESET}")


def display_menu():
    """Displays the interactive menu to the user."""
    print("\n" + "="*60)
    print("                Mini-Sniffer")
    print("="*60)
    print("--- Network Analysis ---")
    print(f"  {CYAN}1{RESET}. Start Capture (All IP Traffic)")
    print(f"  {CYAN}2{RESET}. Start Capture (TCP Only - Web, Email, FTP)")
    print(f"  {CYAN}3{RESET}. Start Capture (ICMP Only - Ping)")
    print(f"  {CYAN}4{RESET}. Start Capture (Custom BPF Filter)")
    print("--- Post-Capture Tools (Requires captured data) ---")
    print(f"  {CYAN}5{RESET}. Show {BLUE}Statistics{RESET} (Protocols, Rates, Bytes)") # Feature 6
    print(f"  {CYAN}6{RESET}. Show {BLUE}Summary{RESET} of Captured Packets") # Feature 8
    print(f"  {CYAN}7{RESET}. Export Captured Packets to {BLUE}PCAP File{RESET}") # Feature 7
    print(f"  {CYAN}0{RESET}. Quit")
    print("="*60)

# --- Main Function ---
if __name__ == "__main__":
    
    while True:
        display_menu()
        choice = input("Enter your choice (0-7): ").strip()
        
        bpf_filter = ""
        
        if choice == '1':
            bpf_filter = "ip"
            start_capture(bpf_filter)
        elif choice == '2':
            bpf_filter = "tcp"
            start_capture(bpf_filter)
        elif choice == '3':
            bpf_filter = "icmp"
            start_capture(bpf_filter)
        elif choice == '4':
            bpf_filter = input(f"Enter your custom BPF filter (e.g., host 192.168.1.1) : ").strip()
            if bpf_filter:
                start_capture(bpf_filter)
            else:
                 print(f"\n{YELLOW}Filter cannot be empty. Returning to menu.{RESET}")
        
        # Post-Capture Features
        elif choice == '5':
            display_stats()
        
        elif choice == '6':
            display_summary()
            
        elif choice == '7':
            if captured_packets:
                filename = input("Enter filename to save as (e.g., capture.pcap): ").strip() or "capture.pcap"
                export_pcap(filename)
            else:
                 print(f"\n{YELLOW}No packets to export. Please perform a capture first.{RESET}")
                 
        elif choice == '0':
            print(f"\n{GREEN}Thank you for using the Mini-Sniffer. Goodbye!{RESET}")
            sys.exit(0)
            
        else:
            print(f"\n{YELLOW}Invalid choice. Please select an option from 0 to 7.{RESET}")
            continue