#!/data/data/com.termux/files/usr/bin/bash

echo "📦 Installing K_ejr Tool..."

# Define paths
SOURCE_PATH="/storage/emulated/0/Download/K_ejr.py"
DEST_PATH="$PREFIX/bin/K_ejr"

# Check if the source file exists
if [ ! -f "$SOURCE_PATH" ]; then
  echo "❌ K_ejr.py not found in /storage/emulated/0/Download/"
  echo "➡️  Please download the file and place it in the correct location."
  exit 1
fi

# Copy the script to bin and make executable
cp "$SOURCE_PATH" "$DEST_PATH"
chmod +x "$DEST_PATH"

# Create alias hhhh
ln -sf "$DEST_PATH" "$PREFIX/bin/hhhh"

echo "✅ Installation complete!"
echo "👉 You can now run the tool using: hhhh  or  K_ejr"
