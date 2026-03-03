import { cookies } from 'next/headers'
import { createServerClient } from '@supabase/ssr'
import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { problem, detail_level, path, lean_requested, notes, professor_steps, tags } = body

    if (!problem?.trim()) {
      return NextResponse.json({ error: 'Problem is required' }, { status: 400 })
    }

    if (!['full_ai', 'ai_review', 'professor_source'].includes(path)) {
      return NextResponse.json({ error: 'Invalid path' }, { status: 400 })
    }

    const cookieStore = await cookies()
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL!,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
      {
        cookies: {
          getAll() { return cookieStore.getAll() },
          setAll(cookiesToSet) {
            cookiesToSet.forEach(({ name, value, options }) => {
              cookieStore.set(name, value, options)
            })
          },
        },
      }
    )

    const { data: { user }, error: authError } = await supabase.auth.getUser()
    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
    }

    const { data: job, error: insertError } = await supabase
      .from('video_jobs')
      .insert({
        user_id: user.id,
        problem: problem.trim(),
        detail_level: detail_level || 'standard',
        path,
        lean_requested: lean_requested || false,
        notes: notes || null,
        professor_steps: professor_steps || null,
        tags: tags || [],
        status: path === 'professor_source' ? 'awaiting_review' : 'queued',
        stage_detail: path === 'professor_source'
          ? 'Processing your solution...'
          : 'Queued for generation...',
      })
      .select()
      .single()

    if (insertError) {
      console.error('[Pipeline] Insert error:', insertError)
      return NextResponse.json({ error: 'Failed to create job' }, { status: 500 })
    }

    return NextResponse.json({ job })
  } catch (err) {
    console.error('[Pipeline] Error:', err)
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 })
  }
}
