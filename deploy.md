# Deployment Instructions for alim.my

## Prerequisites
- Hostinger account access
- hPanel login credentials  
- Domain alim.my pointed to Hostinger hosting

## Deployment Steps

1. **Access hPanel**
   - Log into Hostinger hPanel
   - Navigate to File Manager
   - Go to public_html directory

2. **Upload Files**
   ```bash
   # Upload all files to public_html/
   - alim-home.html
   - our-work.html  
   - assets/ (entire directory)
   - any other HTML files
   ```

3. **Set Homepage**
   - Set alim-home.html as the main index file
   - Or rename to index.html

4. **Test**
   - Visit https://alim.my
   - Check all links and images load correctly
   - Verify Instagram links work

## Recent Updates (March 14, 2026)
- Added March 2026 "Arts, Crafts & Revolution" event
- Updated Community in Action section  
- Refreshed with latest Instagram content
- Set proper priority for recent events

## File Structure
```
public_html/
├── alim-home.html (or index.html)
├── our-work.html
├── assets/
│   └── events/
│       ├── march-2026-arts-revolution.jpeg (NEW)
│       ├── sept-panel.jpeg
│       ├── july-sundays.jpeg  
│       └── legal-learning.jpeg
└── (other files as needed)
```