import * as vscode from 'vscode';
import { callAIForExplanation } from './callAIForExplanation';

let currentPanel: vscode.WebviewPanel | undefined = undefined;

export function activate(context: vscode.ExtensionContext) {

	let disposable = vscode.commands.registerCommand('codementor.explainLastBlock', async () => {
		const editor = vscode.window.activeTextEditor;

		if (!editor) {
			vscode.window.showInformationMessage('No active editor open.');
			return;
		}

		const selection = editor.selection;
		const codeBlock = editor.document.getText(selection);

		if (codeBlock.length === 0) {
			vscode.window.showInformationMessage('No code selected to explain.');
			return;
		}

		// 1. Get Explanation from the Placeholder Function
		// This is where Phase 2 (Gemini Advanced) will be integrated
		const explanation = await callAIForExplanation(codeBlock);

		// 2. Create/Show Webview Panel
		if (currentPanel) {
			currentPanel.reveal(vscode.ViewColumn.One);
		} else {
			currentPanel = vscode.window.createWebviewPanel(
				'codeMentorView',
				'CodeMentor',
				vscode.ViewColumn.Two,
				{
					enableScripts: true
				}
			);

			currentPanel.onDidDispose(
				() => {
					currentPanel = undefined;
				},
				null,
				context.subscriptions
			);
		}

		// 3. Set Webview Content
		currentPanel.webview.html = getWebviewContent(codeBlock, explanation);
	});

	context.subscriptions.push(disposable);
}

function getWebviewContent(code: string, explanation: string): string {
	// A simple HTML structure for the Webview
	return `<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeMentor</title>
    <style>
        body { font-family: sans-serif; padding: 15px; }
        pre { background-color: #333; color: #f0f0f0; padding: 10px; border-radius: 5px; overflow-x: auto; }
        h3 { color: #88B04B; border-bottom: 2px solid #88B04B; padding-bottom: 5px; }
    </style>
</head>
<body>
    <h1>CodeMentor Explanation</h1>
    
    <h3>Selected Code Block:</h3>
    <pre>${code}</pre>

    <h3>AI Explanation:</h3>
    <p>${explanation}</p>
</body>
</html>`;
}

export function deactivate() {}
