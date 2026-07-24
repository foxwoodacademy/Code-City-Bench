// Simple test to verify Codex import works
try {
  // Change to the openclaw directory
  process.chdir('openclaw/openclaw-main/src/infra');
  
  // Try to import the codex module
  const importResult = await import('./provider-usage.fetch.codex.js');
  
  console.log('✅ Codex module imported successfully!');
  console.log('Available functions:', Object.keys(importResult));
  
  if (importResult.fetchCodexUsage) {
    console.log('✅ fetchCodexUsage function is available');
    console.log('Function type:', typeof importResult.fetchCodexUsage);
  } else {
    console.log('❌ fetchCodexUsage function not found');
  }
} catch (error) {
  console.log('❌ Error importing Codex module:', error.message);
  console.log('Stack:', error.stack);
}