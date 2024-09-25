# Provide a JSON summary of given conversation part between Human and AI-Agent to replace original conversation part by the summary to address cantext limitation.
- Include important aspects and remove unnecessary details.
- If conversation part contains Agent's active task(s) description or Agent's plan of work, keep them in summary without changes to Agent be able to strictly follow them after replacement original conversation by summary.
- Keep necessary information like file names, URLs, keys etc.

# Expected output format
~~~json
{
    "system_info": "Messages have been summarized to save space.",
    "messages_summary": ["Key point 1...", "Key point 2..."]
}
~~~