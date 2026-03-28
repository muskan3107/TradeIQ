import sys; sys.path.insert(0, '.')
with open('frontend/app.py', encoding='utf-8') as f:
    lines = f.readlines()
print('Total lines:', len(lines))
for i, l in enumerate(lines):
    s = l.rstrip()
    if (s.startswith('def ') or s.startswith('class ') or
        'MARKET_DATA' in s or 'HOW_SCROLL_JS' in s or
        'CSS = ' in s or s.strip() == '"""' or
        'launch_app' in s):
        print(f'  L{i+1}: {s[:90]}')
