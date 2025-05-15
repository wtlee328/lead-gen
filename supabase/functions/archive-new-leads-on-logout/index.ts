// supabase/functions/archive-new-leads-on-logout/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'; // Use esm.sh for Deno
import { corsHeaders } from '../_shared/cors.ts'; // Ensure you have a _shared/cors.ts

console.log('archive-new-leads-on-logout function booting up');

serve(async (req: Request) => {
  // This is a protected function, so it needs the user's JWT.
  // The Vue app will call this *before* calling supabase.auth.signOut().
  // So, the request to this function should still be authenticated.

  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // 1. Create a Supabase client with the ANON KEY.
    //    The function will then use the user's JWT from the Authorization header
    //    to identify the user. However, to UPDATE records based on user_id
    //    without complex RLS for this specific internal operation, it's often
    //    easier to use the SERVICE_ROLE_KEY for this backend function.
    //    If using SERVICE_ROLE_KEY, the function itself needs to get the user_id
    //    from the JWT because RLS is bypassed.

    // Option A: Using user's JWT (requires RLS on 'leads' to allow user to update their own leads' tab_status)
    // This is generally safer as it operates within the user's permissions.
    // Ensure your RLS policy allows a user to update `tab_status` on their own leads.
    // const userSupabaseClient = createClient(
    //   Deno.env.get('SUPABASE_URL') ?? '',
    //   Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    //   { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
    // );

    // const { data: { user }, error: userError } = await userSupabaseClient.auth.getUser();

    // if (userError || !user) {
    //   console.error('User not found or error getting user:', userError?.message);
    //   return new Response(JSON.stringify({ error: 'Authentication required' }), {
    //     headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    //     status: 401,
    //   });
    // }
    // const userIdToArchive = user.id;

    // Option B: Using Service Role Key (more powerful, use with caution, assumes this function is trusted)
    // This bypasses RLS, so we need to get the user ID from the JWT manually
    // to ensure we only archive leads for the correct user.
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      return new Response(JSON.stringify({ error: 'Missing Authorization header' }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 401
      });
    }
    // Create a temporary client just to get the user from the token
    const tempAuthClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      { global: { headers: { Authorization: authHeader } } }
    );
    const { data: { user }, error: userError } = await tempAuthClient.auth.getUser();

    if (userError || !user) {
      console.error('User not found or error getting user from token:', userError?.message);
      return new Response(JSON.stringify({ error: 'Invalid token or authentication required' }), {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 401
      });
    }
    const userIdToArchive = user.id;

    // Use the Admin client (Service Role Key) for the update operation
    const supabaseAdminClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
    );

    console.log(`Archiving 'new' leads for user: ${userIdToArchive}`);

    const { data, error: updateError } = await supabaseAdminClient
      .from('leads')
      .update({ tab_status: 'archived', current_status: 'Archived - Auto (Logout)' }) // Update current_status too
      .eq('user_id', userIdToArchive)
      .eq('tab_status', 'new');

    if (updateError) {
      console.error('Error updating leads to archived:', updateError.message);
      throw updateError;
    }

    console.log('Successfully archived new leads (if any):', data);
    return new Response(JSON.stringify({ message: 'New leads processed for archiving.', count: (data || []).length }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 200,
    });

  } catch (error) {
    console.error('Error in archive-new-leads-on-logout function:', error.message);
    return new Response(JSON.stringify({ error: error.message }), {
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      status: 500,
    });
  }
});