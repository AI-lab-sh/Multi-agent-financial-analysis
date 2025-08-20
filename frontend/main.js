async function analyze() {
    const topic = document.getElementById("topic").value;

    try {
        const response = await fetch(`/analyze/${encodeURIComponent(topic)}`);
        const data = await response.json();

        // ✅ Backend should always return { "result": { "output": "..." } }
        const markdown = data.result.output;

        // Use marked.js if you want Markdown rendering:
        document.getElementById("result").innerHTML = marked.parse(markdown);

        // Or, if you just want plain text (no Markdown parsing):
        // document.getElementById("result").textContent = markdown;

    } catch (error) {
        document.getElementById("result").textContent = "❌ Error: " + error.message;
    }
}
