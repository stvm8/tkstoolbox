#!/usr/bin/env python3
"""
Penetration Testing User and Password List Generator
Usage: python pentest_gen.py
"""

def generate_usernames(names):
    """Generate username variations from full names"""
    usernames = set()
    
    for name in names:
        name = name.strip()
        if ' ' in name:
            parts = name.split()
            first = parts[0].lower()
            last = parts[-1].lower()
            
            # Generate formats: flast, lfirst, first.last, first, last
            usernames.add(f"{first[0]}{last}")        # flast
            usernames.add(f"{last[0]}{first}")        # lfirst  
            usernames.add(f"{first}.{last}")          # first.last
            usernames.add(first)                      # first
            usernames.add(last)                       # last
        else:
            usernames.add(name.lower())
    
    return sorted(list(usernames))

def generate_passwords(keywords):
    """Generate password variations from keywords"""
    passwords = set()
    
    for keyword in keywords:
        keyword = keyword.strip()
        
        # Basic variations
        passwords.add(keyword)                    # original
        passwords.add(keyword.lower())           # lowercase
        passwords.add(keyword.upper())           # uppercase
        passwords.add(keyword.capitalize())      # capitalize
        
        # Common substitutions
        passwords.add(keyword.replace('a', '@'))
        passwords.add(keyword.replace('o', '0'))
        passwords.add(keyword.replace('e', '3'))
        passwords.add(keyword.replace('s', '$'))
        passwords.add(keyword.replace('i', '1'))
        
        # Add common suffixes
        for suffix in ['!', '^', '?', '&', '*', '#', '%', '@']:
            passwords.add(keyword + suffix)
            passwords.add(keyword.capitalize() + suffix)
    
    return sorted(list(passwords))

def main():
    print("=== Penetration Testing List Generator ===\n")
    
    # Ask if user wants to generate username list
    generate_users = input("Generate username list? (y/n): ").lower().startswith('y')
    
    if generate_users:
        print("\n1. USERNAME GENERATION")
        print("Enter full names (comma-separated):")
        name_input = input("> ")
        names = [n.strip() for n in name_input.split(',') if n.strip()]
        
        if names:
            usernames = generate_usernames(names)
            print(f"\nGenerated {len(usernames)} usernames:")
            for username in usernames:
                print(f"  {username}")
            
            # Save to file
            with open('usernames.txt', 'w') as f:
                f.write('\n'.join(usernames))
            print(f"\nSaved to usernames.txt")
        
        print("\n" + "="*50)
    
    # Password generation
    print("\n2. PASSWORD GENERATION")
    print("Enter keywords (comma-separated):")
    keyword_input = input("> ")
    keywords = [k.strip() for k in keyword_input.split(',') if k.strip()]
    
    if keywords:
        passwords = generate_passwords(keywords)
        print(f"\nGenerated {len(passwords)} passwords:")
        for password in passwords[:20]:  # Show first 20
            print(f"  {password}")
        if len(passwords) > 20:
            print(f"  ... and {len(passwords) - 20} more")
        
        # Ask if user wants to append to existing file
        append_to_file = input("\nAppend to existing wordlist? (y/n): ").lower().startswith('y')
        
        if append_to_file:
            file_path = input("Enter file path: ")
            try:
                with open(file_path, 'a') as f:
                    f.write('\n' + '\n'.join(passwords))
                print(f"Appended {len(passwords)} passwords to {file_path}")
            except Exception as e:
                print(f"Error appending to file: {e}")
                print("Creating new file instead...")
                with open('passwords.txt', 'w') as f:
                    f.write('\n'.join(passwords))
                print("Saved to passwords.txt")
        else:
            with open('passwords.txt', 'w') as f:
                f.write('\n'.join(passwords))
            print("Saved to passwords.txt")

if __name__ == "__main__":
    main()

# Example usage:
if False:  # Set to True to run examples
    # Username example
    test_names = ["John Smith", "Jane Doe", "Bob Wilson"]
    usernames = generate_usernames(test_names)
    print("Username examples:", usernames[:10])
    
    # Password example  
    test_keywords = ["spring2025", "summer2025", "winter2025"]
    passwords = generate_passwords(test_keywords)
    print("Password examples:", passwords[:15])