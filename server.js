const express = require('express');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 5000;

// Serve static files from public directory
app.use(express.static('public'));

// Serve the main HTML file at the root path
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// API endpoint for color matching
app.get('/api/colors/:baseColor/:harmonyType', (req, res) => {
  const { baseColor, harmonyType } = req.params;
  
  // Simple color harmony calculation (you can expand this)
  const colors = generateColorHarmony(baseColor, harmonyType);
  
  res.json({
    baseColor,
    harmonyType,
    colors,
    timestamp: new Date().toISOString()
  });
});

// Basic status endpoint
app.get('/api/status', (req, res) => {
  res.json({
    status: 'online',
    timestamp: new Date().toISOString(),
    port: PORT,
    nodeVersion: process.versions.node,
    service: 'outfit-color-matcher'
  });
});

// Helper function for color harmony generation
function generateColorHarmony(baseColor, harmonyType) {
  // This is a simplified version - the main logic is in the frontend
  return {
    message: `Generated ${harmonyType} colors for ${baseColor}`,
    note: 'Full color calculation handled by frontend JavaScript'
  };
}

app.listen(PORT, () => {
  console.log(`🚀 Outfit Color Matcher Server running on http://localhost:${PORT}`);
  console.log(`📍 Local access: http://127.0.0.1:${PORT}`);
  console.log(`\n📡 To make this public, you can use:`);
  console.log(`   cloudflared tunnel --url http://localhost:${PORT}`);
});