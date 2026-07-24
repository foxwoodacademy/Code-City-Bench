// src/callAIForExplanation.ts

/**
 * PHASE 2: Manual AI Explanation Generation
 * In the MVP, this function will prompt the user to paste the code block
 * into the Gemini chat, and the user will manually copy the resulting 
 * structured HTML back into a temp file for display.
 * This function handles the UI instructions for that manual process.
 */
export async function callAIForExplanation(code: string): Promise<string> {
    const tutorialPrompt = `
    Please copy the code block below and paste it into a new Gemini chat
    with the following instruction.
    
    --- START GEMINI INSTRUCTION ---
    You are an expert Code Tutor and VS Code extension AI. Your goal is to explain the provided block of code using a structured, tutorial format suitable for a beginner or intermediate developer. The output must be a single string of HTML content, ready to be injected directly into a VS Code webview panel, using the following exact structure and rules:
    
    **Structure (Must use these three H3 headings in order):**
    1.  ### Overview and Purpose
    2.  ### Step-by-Step Breakdown
    3.  ### Mentorship Challenge
    
    **Input Code:**
    
    \`\`\`
    ${code}
    \`\`\`
    
    **Format Rules:**
    * Use standard **HTML** tags (<h1>, <h3>, <p>, <ul>, <ol>, <li>, <code>) only. Do not use Markdown.
    * The entire output must be one single string.
    
    --- END GEMINI INSTRUCTION ---
    
    `;

    // The explanation shown in the Webview panel *before* the user pastes the final HTML
    const guidanceHTML = `
    <!DOCTYPE html>
    <html lang="en">
    <body>
        <h1>CodeMentor Manual Step 🧠</h1>
        <p>Your code block has been captured!</p>
        
        <h2>ACTION REQUIRED:</h2>
        <ol>
            <li><strong>Copy the Code Block</strong> shown below.</li>
            <li>Paste the Code Block and the instruction above into our chat.</li>
            <li><strong>Copy the full HTML output</strong> that Gemini generates for you.</li>
            <li>Return here and paste that HTML into a file named <code>/tmp/mentor_output.html</code> (or similar) on your system.</li>
        </ol>

        <h3>Captured Code Block:</h3>
        <pre>${code}</pre>
        
        <p><em>(In a future version, this step will be automated using the Gemini API key.)</em></p>
    </body>
    </html>`;
    
    // In a real execution, we would resolve this with the *final* HTML content.
    // For now, we return the instruction HTML so the user can proceed.
    return Promise.resolve(guidanceHTML);
}
