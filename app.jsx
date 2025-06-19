import { useState } from "react"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"

export default function SwiftClapBack() {
  const [comment, setComment] = useState("")
  const [tone, setTone] = useState("")
  const [response, setResponse] = useState("")
  const [loading, setLoading] = useState(false)

  const toneOptions = [
    "Snarky",
    "Funny",
    "Poetic",
    "Kind",
    "Wise",
    "Sassy",
    "Sweet",
    "Confident",
    "Graceful"
  ]

  async function generateReply() {
    setLoading(true)
    setResponse("")

    const prompt = `You are SwiftClapBack, a polite, elegant chatbot who helps users reply to rude, annoying, or confusing comments on social media. Your tone should reflect the selected mood and draw stylistic inspiration from Taylor Swift lyrics. Respond to this comment in a ${tone.toLowerCase()} tone: "${comment}"`

    const res = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    })

    const data = await res.json()
    setResponse(data.reply)
    setLoading(false)
  }

  return (
    <div className="max-w-xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4 text-center">SwiftClapBack</h1>
      <p className="text-center mb-6 text-muted-foreground">
        Drop the drama. Lift your crown. What do you want to say back?
      </p>
      <Textarea
        className="mb-4"
        placeholder="Paste the comment you're responding to..."
        value={comment}
        onChange={(e) => setComment(e.target.value)}
      />
      <div className="mb-4 grid grid-cols-2 md:grid-cols-3 gap-2">
        {toneOptions.map((t) => (
          <Button
            key={t}
            variant={tone === t ? "default" : "outline"}
            onClick={() => setTone(t)}
          >
            {t}
          </Button>
        ))}
      </div>
      <Button className="w-full mb-6" onClick={generateReply} disabled={!comment || !tone || loading}>
        {loading ? "Spinning a lyric..." : "Generate ClapBack"}
      </Button>
      {response && (
        <Card>
          <CardContent className="p-4">
            <p className="italic">{response}</p>
            <p className="text-sm text-muted-foreground text-right mt-2">I've got you, queens and kings.</p>
          </CardContent>
        </Card>
      )}
    </div>
  )
}