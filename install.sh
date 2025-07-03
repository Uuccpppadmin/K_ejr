#!/data/data/com.termux/files/usr/bin/bash
echo "📦 Installing K_ejr tool..."

DEST_PATH="$PREFIX/bin/K_ejr"
curl -s -o "$DEST_PATH" "https://raw.githubusercontent.com/Uuccpppadmin/K_ejr/main/K_ejr.py"
chmod +x "$DEST_PATH"
ln -sf "$DEST_PATH" "$PREFIX/bin/hhhh"

echo "✅ Installed! You can now run the tool by typing: hhhh"
