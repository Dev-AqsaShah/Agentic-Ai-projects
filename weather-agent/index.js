import 'dotenv/config'
import { WeatherClient } from '@agentic/weather'
import { createAISDKTools } from '@agentic/ai-sdk'
import { openai } from '@ai-sdk/openai'
import { generateText } from 'ai'

async function main() {
  const weather = new WeatherClient()
  const result = await generateText({
    model: openai('gpt-4o'),
    tools: createAISDKTools(weather),
    toolChoice: 'required',
    prompt: 'What is the weather in Karachi?'
  })
  console.log(result.toolResults[0])
}

main()
