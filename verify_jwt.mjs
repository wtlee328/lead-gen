import { jwtVerify } from 'jose';
import { inspect } from 'util';
import { TextEncoder } from 'util';

// The exact secret key you provided.
const SUPABASE_JWT_SECRET = '9a08b654-c084-426f-b7f3-2b2116e00036';

async function verifyHS256JWT(jwt) {
  if (!jwt) {
    console.error('Error: Please provide the JWT as a command-line argument.');
    console.log('Usage: node verify_jwt.mjs <your-jwt-token>');
    process.exit(1);
  }

  console.log('Attempting to verify JWT with HS256 algorithm...');
  console.log(`Using secret starting with: ${SUPABASE_JWT_SECRET.substring(0, 8)}...`);

  try {
    // We must encode the shared secret into a Uint8Array for the 'jose' library.
    const secretKey = new TextEncoder().encode(SUPABASE_JWT_SECRET);

    // Perform the verification.
    const { payload, protectedHeader } = await jwtVerify(jwt, secretKey, {
      algorithms: ['HS256'],
    });

    console.log('\n✅ JWT Verification Succeeded!');
    console.log('\nProtected Header:');
    console.log(inspect(protectedHeader, { colors: true, depth: null }));
    console.log('\nPayload (Claims):');
    console.log(inspect(payload, { colors: true, depth: null }));

  } catch (error) {
    console.error('\n❌ JWT Verification Failed!');
    console.error('Error:', error.message);
    
    if (error.code === 'ERR_JWS_SIGNATURE_VERIFICATION_FAILED') {
        console.error('\nDiagnosis: The signature is invalid. This is a definitive cryptographic failure. It means the token was NOT signed with the secret key provided.');
    } else if (error.code === 'ERR_JWT_EXPIRED') {
        console.error('\nDiagnosis: The token has expired.');
    }
  }
}

// Get the JWT from the command line arguments
const token = process.argv[2];
verifyHS256JWT(token);