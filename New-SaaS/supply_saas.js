// Install: npm install axios dotenv
const axios = require('axios');
require('dotenv').config();

const RISK_API_URL = "https://api.resilinc.com/v2/events"; // Example enterprise risk feed
const SLACK_WEBHOOK = process.env.SLACK_WEBHOOK_URL;

// Function to assess severity and trigger automated SaaS warnings
async function analyzeAndAlert(event) {
    const { title, category, severity, description, impacted_regions } = event;
    
    // Simple rule engine (In production, pass this to an AI model/LLM prompt)
    if (severity === 'HIGH' || category === 'Boycott' || category === 'Shortage') {
        const payload = {
            text: `⚠️ *CRITICAL SUPPLY CHAIN ALERT* ⚠️\n` +
                  `*Type:* ${category}\n` +
                  `*Event:* ${title}\n` +
                  `*Regions Impacted:* ${impacted_regions.join(', ')}\n` +
                  `*Risk Summary:* ${description}\n` +
                  `*Action Required:* Check alternative sourcing vectors immediately.`
        };

        try {
            await axios.post(SLACK_WEBHOOK, payload);
            console.log(`Alert sent successfully for event: ${title}`);
        } catch (error) {
            console.error("Failed to broadcast real-time SaaS alert:", error.message);
        }
    }
}

// Polling function for real-time stream ingestion
async function monitorSupplyChain() {
    try {
        console.log("Fetching live global risk data...");
        const response = await axios.get(RISK_API_URL, {
            headers: { 'Authorization': `Bearer ${process.env.RISK_API_KEY}` }
        });

        const liveEvents = response.data.events;
        liveEvents.forEach(event => analyzeAndAlert(event));

    } catch (error) {
        console.error("Error fetching supply chain telemetry:", error.message);
    }
}

// Run monitor every 60 seconds
setInterval(monitorSupplyChain, 60000);
