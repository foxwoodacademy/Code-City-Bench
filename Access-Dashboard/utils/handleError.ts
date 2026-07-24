/**
 * A centralized error handling function.
 * In a real application, this could log to a service like Sentry or Datadog.
 * @param error The error object.
 * @param context Additional context about where the error occurred.
 */
export const handleError = (error: unknown, context = "General") => {
    console.error(`[${context}] Error:`, error);
    
    // You could add more sophisticated logic here, e.g., showing a toast notification to the user.
    if (error instanceof Error) {
        // Potentially show error.message in a user-friendly way.
    } else {
        // Handle non-Error objects
    }
};
