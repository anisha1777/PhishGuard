"""
Generate synthetic phishing dataset for training
This creates a CSV file with URL features and labels (0 = safe, 1 = phishing)
"""

import pandas as pd
import random
import os

# Define parameters
NUM_SAFE_URLS = 500
NUM_PHISHING_URLS = 500

def extract_url_features(url):
    """Extract features from a URL"""
    return {
        'url_length': len(url),
        'dots': url.count('.'),
        'hyphens': url.count('-'),
        'has_at_symbol': 1 if '@' in url else 0,
        'has_https': 1 if 'https' in url else 0,
    }

def generate_safe_urls(count):
    """Generate safe URL examples"""
    domains = [
        'google.com', 'facebook.com', 'twitter.com', 'github.com', 'stackoverflow.com',
        'wikipedia.org', 'amazon.com', 'microsoft.com', 'apple.com', 'youtube.com',
        'linkedin.com', 'instagram.com', 'reddit.com', 'slack.com', 'notion.so',
        'figma.com', 'stripe.com', 'shopify.com', 'zendesk.com', 'mailchimp.com'
    ]
    
    paths = [
        '', '/products', '/services', '/about', '/contact',
        '/pricing', '/blog', '/docs', '/api', '/dashboard',
        '/settings', '/profile', '/account', '/help', '/support'
    ]
    
    safe_urls = []
    for _ in range(count):
        domain = random.choice(domains)
        path = random.choice(paths)
        url = f"https://{domain}{path}"
        features = extract_url_features(url)
        features['label'] = 0  # Safe URL
        safe_urls.append(features)
    
    return safe_urls

def generate_phishing_urls(count):
    """Generate phishing URL examples"""
    fake_domains = [
        'gogle-secure.com', 'faceb00k-verify.net', 'amaz0n-account.co',
        'paypal-login.xyz', 'bank-security.tk', 'verify-identity.ml',
        'confirm-account.ga', 'update-profile.cf', 'secure-banking.gq',
        'apple-id-verify.tk', 'microsoft-account.ml', 'urgent-action.cf',
        'suspicious-link.tk', 'fake-domain-123.xyz', 'phishing-example.tk'
    ]
    
    phishing_paths = [
        '/login', '/verify', '/account', '/banking', '/paypal',
        '/secure', '/update', '/confirm', '/action', '/urgent',
        '/verify-account', '/login-secure', '/confirm-identity'
    ]
    
    phishing_urls = []
    for _ in range(count):
        domain = random.choice(fake_domains)
        path = random.choice(phishing_paths)
        
        # Add suspicious elements
        url = f"http://{domain}{path}"  # HTTP (not HTTPS)
        
        # Sometimes add extra dots
        if random.random() > 0.5:
            url = url + "?verify=user&confirm=payment&update=true"
        
        # Sometimes add hyphens and special chars
        if random.random() > 0.6:
            url = url.replace('-', '-' + str(random.randint(0, 9)))
        
        features = extract_url_features(url)
        features['label'] = 1  # Phishing URL
        phishing_urls.append(features)
    
    return phishing_urls

def main():
    print("🔄 Generating synthetic phishing dataset...")
    
    # Generate datasets
    print(f"  • Generating {NUM_SAFE_URLS} safe URLs...")
    safe_urls = generate_safe_urls(NUM_SAFE_URLS)
    
    print(f"  • Generating {NUM_PHISHING_URLS} phishing URLs...")
    phishing_urls = generate_phishing_urls(NUM_PHISHING_URLS)
    
    # Combine and shuffle
    all_data = safe_urls + phishing_urls
    random.shuffle(all_data)
    
    # Create DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to CSV
    output_file = 'phishing_dataset.csv'
    df.to_csv(output_file, index=False)
    
    print(f"\n✓ Dataset created successfully!")
    print(f"  • File: {output_file}")
    print(f"  • Total samples: {len(df)}")
    print(f"  • Safe URLs (label=0): {len(df[df['label'] == 0])}")
    print(f"  • Phishing URLs (label=1): {len(df[df['label'] == 1])}")
    print(f"\n📊 Dataset statistics:")
    print(df.describe())
    print(f"\n✅ Next step: Run 'python train_model.py' to train the XGBoost model")

if __name__ == "__main__":
    main()
