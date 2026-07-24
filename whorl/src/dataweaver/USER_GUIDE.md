# DataWeaver: The Digital Inspector & Translator

Welcome to the DataWeaver guide! This guide is written for everyone, whether you are a scientist, a manager, or someone who just wants to make sure their data is working correctly.

## What is DataWeaver?

Imagine you are receiving packages from different suppliers all over the world.
- Some packages are labeled in English, some in French, some in Japanese.
- Some packages are missing the instruction manual.
- Some packages contain items that are broken or too big for your warehouse.

**DataWeaver is your digital inspector and translator.**

It looks at every "package" (which in our case is a piece of digital data) and performs two vital tasks:

1.  **Inspection (Validation)**: It checks if the data is what it *should* be. Is the temperature a number? Is the ID code the right length? Is the weight too high? If something is wrong, DataWeaver flags it immediately so you don't waste time on bad data.
2.  **Translation (Transformation)**: It makes sure the data is in a format your systems understand. If one supplier calls it "temp" and another calls it "temperature", DataWeaver can automatically rename it so your main system only ever sees "temperature".

## Why do you need it?

In the world of Artificial Intelligence, "garbage in, garbage out" is a golden rule. If you feed an AI bad, messy, or incorrectly formatted data, it will give you bad, messy, or incorrect results.

DataWeaver prevents this by:
- **Preventing Errors**: Catching mistakes before they reach your expensive AI models.
- **Standardizing Everything**: Making sure all your data looks the same, no matter where it came from.
- **Saving Time**: Automatically fixing small naming differences so you don't have to do it manually.

## How to use it (The Simple Way)

To use DataWeaver, you need two things:
1.  **The Data**: The actual information you want to check (e.g., a list of sensor readings).
2.  **The Rulebook (The "Manifest")**: A small file that tells DataWeaver what the rules are.

### Step 1: Create your Rulebook (Manifest)

A Rulebook is just a simple text file. Here is a very basic example:

```json
{
  "metadata": {
    "name": "My Simple Rulebook",
    "version": "1.0",
    "description": "Rules for my sensor data"
  },
  "schema": {
    "temperature": {
      "type": "number",
      "required": true
    },
    "device_name": {
      "type": "string",
      "required": true
    }
  },
  "transformations": [
    {
      "action": "rename",
      "from": "temp",
      "to": "temperature"
    }
  ]
}
```

**In this rulebook:**
- We say `temperature` **must** be a number and it **must** be there.
- We say `device_name` **must** be a text string and it **must** be there.
- We also say: "If you see a field called `temp`, please rename it to `temperature`."

### Step 2: Run the Inspector

Once you have your Rulebook and your Data, you can run the DataWeaver tool. It will either:
- **Give you back clean, perfect data** that follows your rules.
- **Give you a clear error message** telling you exactly what went wrong (e.g., *"Error: The 'temperature' field must be a number, but you provided text"*).

## Troubleshooting: "What went wrong?"

If DataWeaver tells you there is an error, don't panic! Here are the most common ones:

| If you see... | It means... | How to fix it |
| :--- | :--- | :--- |
| **"Missing required field..."** | A piece of information that was mandatory is missing. | Check your data and make sure that field is included. |
| **"Must be of type..."** | You provided the wrong *kind* of information (e.g., you provided text where a number was expected). | Make sure you are sending numbers as numbers and text as text. |
| **"Is too small/large..."** | The number you provided is outside the allowed range. | Check your sensors or your data source to see why the value is out of bounds. |
| **"Does not match the required pattern..."** | A piece of text doesn't follow the specific format required (like an ID code). | Double-check that the text follows the exact pattern specified in your rulebook. |

***

*DataWeaver: Making your data work for you, not against you.*
