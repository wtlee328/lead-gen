// supabase/functions/archive-new-leads-on-logout/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import { corsHeaders } from '../_shared/cors.ts';

console.log('archive-new-leads-on-logout function booting up');

serve(async (req: Request) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Step 1: Create a Supabase client that will use the user's auth token
    const userClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    );

    // Step 2: Get the user from the token. This is the authentication check.
    const { data: { user }, error: userError } = await userClient.auth.getUser();

    if (userError) throw userError;
    if (!user) throw new Error("User not found");

    // Step 3: If the user is authenticated, create an admin client to perform the update.
    // This bypasses RLS for a trusted server-side operation.
    const supabaseAdmin = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );

    console.log(`Archiving 'new' leads for authenticated user: ${user.id}`);

    // Step 4: Perform the update for the authenticated user.
    const { data, error: updateError } = await supabaseAdmin
      .from('leads')
      .update({ tab: 'archived', lead_status: 'archived' })
      .eq('user_id', user.id)
      .eq('tab', 'new');

    if (updateError) {
      throw updateError;
    }

    return new Response(JSON.stringify({ message: 'Success', count: (data || []).length }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    });

  } catch (error) {
    console.error('Error in archive-new-leads-on-logout function:', error.message);
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 401, // Return 401 for any auth-related errors
    });
  }
});