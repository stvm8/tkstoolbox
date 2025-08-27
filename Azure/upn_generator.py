#!/usr/bin/env python3
"""
UPN Generator Tool
Generates all possible User Principal Name (UPN) combinations from a domain and user's full name.
"""

import argparse
import sys
from itertools import combinations


def clean_name_part(name_part):
    """Clean and normalize a name part by removing special characters and converting to lowercase."""
    # Remove common special characters and normalize
    cleaned = ''.join(c for c in name_part if c.isalpha() or c.isspace())
    return cleaned.strip().lower()


def parse_full_name(full_name):
    """Parse full name into components (first, middle, last names)."""
    # Split by spaces and filter out empty strings
    name_parts = [part.strip() for part in full_name.split() if part.strip()]
    
    if not name_parts:
        raise ValueError("No valid name parts found")
    
    # Clean each name part
    cleaned_parts = [clean_name_part(part) for part in name_parts if clean_name_part(part)]
    
    if not cleaned_parts:
        raise ValueError("No valid name parts found after cleaning")
    
    first_name = cleaned_parts[0]
    last_name = cleaned_parts[-1] if len(cleaned_parts) > 1 else ""
    middle_names = cleaned_parts[1:-1] if len(cleaned_parts) > 2 else []
    
    return first_name, middle_names, last_name


def generate_upn_combinations(first_name, middle_names, last_name, domain):
    """Generate all possible UPN combinations."""
    upns = set()  # Use set to avoid duplicates
    
    # All name components
    all_names = [first_name] + middle_names + ([last_name] if last_name else [])
    
    # Single name patterns
    for name in all_names:
        if name:
            upns.add(f"{name}@{domain}")
    
    # Two name combinations
    if len(all_names) >= 2:
        for combo in combinations(all_names, 2):
            name1, name2 = combo
            # Various separators
            upns.add(f"{name1}{name2}@{domain}")  # concatenated
            upns.add(f"{name1}.{name2}@{domain}")  # dot separated
            upns.add(f"{name1}_{name2}@{domain}")  # underscore separated
            upns.add(f"{name1}-{name2}@{domain}")  # hyphen separated
            
            # Reverse order
            upns.add(f"{name2}{name1}@{domain}")
            upns.add(f"{name2}.{name1}@{domain}")
            upns.add(f"{name2}_{name1}@{domain}")
            upns.add(f"{name2}-{name1}@{domain}")
    
    # Three name combinations (if available)
    if len(all_names) >= 3:
        for combo in combinations(all_names, 3):
            name1, name2, name3 = combo
            # Various separators for three names
            upns.add(f"{name1}{name2}{name3}@{domain}")
            upns.add(f"{name1}.{name2}.{name3}@{domain}")
            upns.add(f"{name1}_{name2}_{name3}@{domain}")
            upns.add(f"{name1}-{name2}-{name3}@{domain}")
            
            # Mixed separators
            upns.add(f"{name1}.{name2}{name3}@{domain}")
            upns.add(f"{name1}{name2}.{name3}@{domain}")
    
    # Initial + name combinations
    for i, name in enumerate(all_names):
        if name:
            initial = name[0]
            
            # Initial + other names
            for j, other_name in enumerate(all_names):
                if i != j and other_name:
                    upns.add(f"{initial}{other_name}@{domain}")
                    upns.add(f"{initial}.{other_name}@{domain}")
                    upns.add(f"{initial}_{other_name}@{domain}")
                    upns.add(f"{initial}-{other_name}@{domain}")
                    
                    # Reverse: name + initial
                    upns.add(f"{other_name}{initial}@{domain}")
                    upns.add(f"{other_name}.{initial}@{domain}")
                    upns.add(f"{other_name}_{initial}@{domain}")
                    upns.add(f"{other_name}-{initial}@{domain}")
    
    # Multiple initials + name combinations  
    if len(all_names) >= 2:
        for main_name in all_names:
            if main_name:
                # Get initials of other names
                other_names = [n for n in all_names if n != main_name]
                if other_names:
                    initials = ''.join([n[0] for n in other_names])
                    upns.add(f"{initials}{main_name}@{domain}")
                    upns.add(f"{initials}.{main_name}@{domain}")
                    upns.add(f"{initials}_{main_name}@{domain}")
                    upns.add(f"{initials}-{main_name}@{domain}")
                    
                    # Reverse
                    upns.add(f"{main_name}{initials}@{domain}")
                    upns.add(f"{main_name}.{initials}@{domain}")
                    upns.add(f"{main_name}_{initials}@{domain}")
                    upns.add(f"{main_name}-{initials}@{domain}")
    
    # All initials combination
    if len(all_names) >= 2:
        all_initials = ''.join([name[0] for name in all_names if name])
        if len(all_initials) >= 2:
            upns.add(f"{all_initials}@{domain}")
    
    # Common variations with numbers (often used in organizations)
    base_combinations = []
    
    # Collect base patterns without domain
    for upn in list(upns):
        base = upn.split('@')[0]
        base_combinations.append(base)
    
    # Add numbered variations for common patterns
    common_patterns = [
        first_name + last_name if last_name else first_name,
        f"{first_name}.{last_name}" if last_name else first_name,
        f"{first_name[0]}{last_name}" if last_name else first_name,
        f"{first_name}{last_name[0]}" if last_name else first_name
    ]
    
    for pattern in common_patterns:
        if pattern:
            for num in range(1, 10):  # Add numbers 1-9
                upns.add(f"{pattern}{num}@{domain}")
            
            # Add common suffixes
            for suffix in ['01', '02', '03', '2024', '2025']:
                upns.add(f"{pattern}{suffix}@{domain}")
    
    return sorted(list(upns))


def main():
    parser = argparse.ArgumentParser(
        description='Generate all possible UPN combinations from domain and user name',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python upn_generator.py --domain abc.txt --user "John Doe"
  python upn_generator.py --domain company.com --user "John Michael Smith"
  python upn_generator.py -d example.org -u "Jane Smith"
        '''
    )
    
    parser.add_argument('--domain', '-d', required=True, 
                       help='Domain name (e.g., abc.txt, company.com)')
    parser.add_argument('--user', '-u', required=True,
                       help='Full name of the user (e.g., "John Doe", "Jane Mary Smith")')
    parser.add_argument('--output', '-o', 
                       help='Output file to save UPNs (optional)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show verbose output with name parsing details')
    
    args = parser.parse_args()
    
    try:
        # Parse the full name
        first_name, middle_names, last_name = parse_full_name(args.user)
        
        if args.verbose:
            print(f"Parsed name components:")
            print(f"  First name: {first_name}")
            print(f"  Middle names: {middle_names}")
            print(f"  Last name: {last_name}")
            print(f"  Domain: {args.domain}")
            print()
        
        # Generate UPN combinations
        upns = generate_upn_combinations(first_name, middle_names, last_name, args.domain)
        
        print(f"Generated {len(upns)} possible UPN combinations:")
        print("=" * 50)
        
        for upn in upns:
            print(upn)
        
        # Save to file if specified
        if args.output:
            with open(args.output, 'w') as f:
                for upn in upns:
                    f.write(upn + '\n')
            print(f"\nUPNs saved to {args.output}")
            
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()