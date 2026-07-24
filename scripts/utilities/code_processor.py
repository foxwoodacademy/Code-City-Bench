package com.codeextractor.service;
import android.content.Context;
import android.util.Log;
import java.util.regex.Pattern;
import java.util.regex.Matcher;
import java.util.HashMap;
import java.util.Map;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class CodeProcessor {
    
    private static final String TAG = "CodeProcessor";
    private Context context;
    private Map<String, StringBuilder> conversationBuffers;
    private Map<String, StringBuilder> codeBuffers;
    
    // Code detection patterns
    private static final Pattern CODE_BLOCK_PATTERN = Pattern.compile(
        "```[\\w]*\\n([\\s\\S]*?)```|" +
        "`([^`]+)`|" +
        "(?m)^(?:[ ]{4}|\\t)(.+)$"
    );
    
    // Language detection patterns
    private static final Map<String, Pattern> LANGUAGE_PATTERNS = new HashMap<>();
    static {
        LANGUAGE_PATTERNS.put("python", Pattern.compile("\\b(def|import|class|if __name__|print|return)\\b"));
        LANGUAGE_PATTERNS.put("javascript", Pattern.compile("\\b(function|const|let|var|=>|console\\.log)\\b"));
        LANGUAGE_PATTERNS.put("java", Pattern.compile("\\b(public|private|class|void|static|new)\\b"));
        LANGUAGE_PATTERNS.put("cpp", Pattern.compile("\\b(#include|std::|cout|cin|namespace)\\b"));
        LANGUAGE_PATTERNS.put("sql", Pattern.compile("\\b(SELECT|FROM|WHERE|INSERT|UPDATE|DELETE)\\b", Pattern.CASE_INSENSITIVE));
        LANGUAGE_PATTERNS.put("html", Pattern.compile("<[a-z][\\s\\S]*>"));
        LANGUAGE_PATTERNS.put("css", Pattern.compile("\\{[\\s\\S]*:[\\s\\S]*;[\\s\\S]*\\}"));
        LANGUAGE_PATTERNS.put("bash", Pattern.compile("\\b(#!/bin/bash|echo|grep|sed|awk)\\b"));
        LANGUAGE_PATTERNS.put("json", Pattern.compile("^\\s*[{\\[]"));
        LANGUAGE_PATTERNS.put("xml", Pattern.compile("<\\?xml"));
    }
    
    public CodeProcessor(Context context) {
        this.context = context;
        this.conversationBuffers = new HashMap<>();
        this.codeBuffers = new HashMap<>();
    }
    
    public void processText(String text, String source) {
        if (text == null || text.trim().isEmpty()) return;
        
        // Initialize buffers for this source if needed
        if (!conversationBuffers.containsKey(source)) {
            conversationBuffers.put(source, new StringBuilder());
            codeBuffers.put(source, new StringBuilder());
        }
        
        Matcher codeMatcher = CODE_BLOCK_PATTERN.matcher(text);
        boolean hasCode = false;
        
        while (codeMatcher.find()) {
            String codeSnippet = codeMatcher.group(1);
            if (codeSnippet == null) codeSnippet = codeMatcher.group(2);
            if (codeSnippet == null) codeSnippet = codeMatcher.group(3);
            
            if (codeSnippet != null && !codeSnippet.trim().isEmpty()) {
                hasCode = true;
                String language = detectLanguage(codeSnippet);
                saveCode(codeSnippet, language, source);
                codeBuffers.get(source).append(codeSnippet).append("\n\n");
            }
        }
        
        // Save conversation (without code)
        if (!hasCode || text.length() > 100) {
            String cleanText = codeMatcher.replaceAll("[CODE_BLOCK]");
            conversationBuffers.get(source).append(cleanText).append("\n");
            
            // Periodically save conversation log
            if (conversationBuffers.get(source).length() > 5000) {
                saveConversation(source);
            }
        }
    }
    
    private String detectLanguage(String code) {
        Map<String, Integer> scores = new HashMap<>();
        
        for (Map.Entry<String, Pattern> entry : LANGUAGE_PATTERNS.entrySet()) {
            Matcher matcher = entry.getValue().matcher(code);
            int count = 0;
            while (matcher.find()) count++;
            if (count > 0) {
                scores.put(entry.getKey(), count);
            }
        }
        
        // Return language with highest score
        String detectedLang = "unknown";
        int maxScore = 0;
        for (Map.Entry<String, Integer> entry : scores.entrySet()) {
            if (entry.getValue() > maxScore) {
                maxScore = entry.getValue();
                detectedLang = entry.getKey();
            }
        }
        
        return detectedLang;
    }
    
    private void saveCode(String code, String language, String source) {
        try {
            File baseDir = new File(context.getExternalFilesDir(null), "AICodeExtractor");
            File langDir = new File(baseDir, language);
            if (!langDir.exists()) langDir.mkdirs();
            
            String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.US).format(new Date());
            String filename = String.format("%s_%s.%s", 
                sanitizeSource(source), 
                timestamp, 
                getExtension(language));
            
            File codeFile = new File(langDir, filename);
            FileWriter writer = new FileWriter(codeFile, true);
            writer.write(code);
            writer.write("\n\n");
            writer.close();
            
            Log.d(TAG, "Saved code to: " + codeFile.getAbsolutePath());
            
        } catch (IOException e) {
            Log.e(TAG, "Error saving code", e);
        }
    }
    
    private void saveConversation(String source) {
        try {
            File baseDir = new File(context.getExternalFilesDir(null), "AICodeExtractor/conversations");
            if (!baseDir.exists()) baseDir.mkdirs();
            
            String date = new SimpleDateFormat("yyyyMMdd", Locale.US).format(new Date());
            File convFile = new File(baseDir, String.format("%s_%s.txt", sanitizeSource(source), date));
            
            FileWriter writer = new FileWriter(convFile, true);
            writer.write(conversationBuffers.get(source).toString());
            writer.close();
            
            // Clear buffer after saving
            conversationBuffers.get(source).setLength(0);
            
            Log.d(TAG, "Saved conversation to: " + convFile.getAbsolutePath());
            
        } catch (IOException e) {
            Log.e(TAG, "Error saving conversation", e);
        }
    }
    
    private String sanitizeSource(String source) {
        return source.replaceAll("[^a-zA-Z0-9]", "_");
    }
    
    private String getExtension(String language) {
        switch (language) {
            case "python": return "py";
            case "javascript": return "js";
            case "java": return "java";
            case "cpp": return "cpp";
            case "sql": return "sql";
            case "html": return "html";
            case "css": return "css";
            case "bash": return "sh";
            case "json": return "json";
            case "xml": return "xml";
            default: return "txt";
        }
    }
    
    public void cleanup() {
        // Save any remaining conversations
        for (String source : conversationBuffers.keySet()) {
            if (conversationBuffers.get(source).length() > 0) {
                saveConversation(source);
            }
        }
    }
}