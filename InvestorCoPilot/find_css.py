with open('frontend/app.py', encoding='utf-8') as f:
    content = f.read()
marker = 'CSS = """'
css_start = content.find(marker)
# find closing triple-quote after the opening
css_end = content.find('"""', css_start + len(marker)) + 3
print('CSS start:', css_start, '| end:', css_end)
print('Char before CSS:', repr(content[css_start-5:css_start]))
print('First 60 of CSS:', repr(content[css_start:css_start+60]))
print('Last 60 of CSS:', repr(content[css_end-60:css_end]))
print('Char after CSS:', repr(content[css_end:css_end+60]))
