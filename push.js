const { execSync } = require('child_process');

try {
  const result = execSync('git push origin main -f', {
    cwd: '/Users/tridipsamanta/Desktop/Python ',
    encoding: 'utf-8',
    stdio: 'pipe'
  });
  console.log('Push successful:', result);
} catch (error) {
  console.log('Push output:', error.stdout);
  console.log('Push error:', error.stderr);
  console.log('Status:', error.status);
}
