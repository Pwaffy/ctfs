import requests
import itertools
import time

BASE_URL = "https://issessionsctf-base-of-the-tower.chals.io/"

def get_sum(num1: str, num2: str) -> None:
    params = {"num_1": num1, "num_2": num2}
    
    try:
        r = requests.get(BASE_URL, params=params, timeout=6)
        r.raise_for_status()
        
        text = r.text.strip()
        
        # Extract the sum line if present
        sum_line = ""
        sum_value = None
        if "The sum is:" in text:
            start = text.find("The sum is:")
            end = text.find("</p>", start)
            if end == -1:
                end = len(text)
            sum_line = text[start:end].strip()
            # Extract the actual sum value using split
            parts = sum_line.split(":")
            if len(parts) == 2:
                sum_value = parts[1].strip()
        
        print(f"  {num1:>6} + {num2:>6}  →  {sum_line}")
        
        # Save any sum found
        if sum_value is not None:
            with open("all_sum_results.txt", "a") as f:
                f.write(f"{num1} + {num2} = {sum_value}\n")
        
        lower_text = text.lower()
        if any(kw in lower_text for kw in ["flag", "fantasyctf", "treasure", "congrat", "key", "secret", "error"]):
            print("\n" + "="*70)
            print("POTENTIALLY INTERESTING")
            print(text)
            print("="*70 + "\n")
        
        if len(text) > 300 or "<script" in text or "alert" in lower_text:
            print("LONG RESPONSE")
            print(text[:500] + " ...")
        
    except Exception as e:
        print(f"  {num1:>6} + {num2:>6}  →  ERROR: {e}")

print("Brute forcing adder\n")

tested = set()

for length in range(1, 6):
    print(f"-- Length {length} -------------------------------------")
    
    all_strings = []
    for chars in itertools.product("01", repeat=length):
        s = "".join(chars)
        all_strings.append(s)
    
    count = 0
    for a in all_strings:
        for b in all_strings:
            pair = (a, b)
            if pair in tested:
                continue
            tested.add(pair)
            
            get_sum(a, b)
            count += 1
            
            # Rate limit
            time.sleep(0.35)
            
            # Also do swapped if different
            if a != b:
                swapped = (b, a)
                if swapped not in tested:
                    tested.add(swapped)
                    get_sum(b, a)
                    time.sleep(0.35)
    
    print(f" -- {count} unique ordered pairs tested at length {length}\n")

print("===== Done =====")