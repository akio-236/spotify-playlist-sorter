/**
 * A collection of formatting utility functions for the Spotify app
 */

/**
 * Formats milliseconds into a minutes:seconds string
 *
 * @param {number} ms - Duration in milliseconds
 * @returns {string} Formatted duration in MM:SS format
 */
export const formatDuration = (ms) => {
    if (!ms || isNaN(ms)) return '0:00';
    
    const totalSeconds = Math.floor(ms / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };
  
  /**
   * Formats milliseconds into a human-readable duration
   *
   * @param {number} ms - Duration in milliseconds
   * @returns {string} Human-readable duration (e.g., "5 hr 23 min")
   */
  export const formatLongDuration = (ms) => {
    if (!ms || isNaN(ms)) return '0 min';
    
    const totalMinutes = Math.floor(ms / 60000);
    const hours = Math.floor(totalMinutes / 60);
    const minutes = totalMinutes % 60;
    
    if (hours > 0) {
      return `${hours} hr ${minutes} min`;
    } else {
      return `${minutes} min`;
    }
  };
  
  /**
   * Formats a date string to a human-friendly format
   *
   * @param {string} dateString - ISO date string
   * @returns {string} Formatted date (e.g., "Jan 15, 2023")
   */
  export const formatDate = (dateString) => {
    if (!dateString) return '';
    
    const date = new Date(dateString);
    
    // Check if date is valid
    if (isNaN(date.getTime())) return '';
    
    return date.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };
  
  /**
   * Formats a large number with commas
   *
   * @param {number} num - Number to format
   * @returns {string} Formatted number with commas (e.g., "1,234,567")
   */
  export const formatNumber = (num) => {
    if (num === undefined || num === null) return '0';
    return num.toLocaleString();
  };
  
  /**
   * Truncates text and adds ellipsis if it exceeds the specified length
   *
   * @param {string} text - Text to truncate
   * @param {number} length - Maximum length before truncation
   * @returns {string} Truncated text with ellipsis if needed
   */
  export const truncateText = (text, length = 100) => {
    if (!text) return '';
    
    if (text.length <= length) return text;
    
    return text.substring(0, length) + '...';
  };
  
  /**
   * Converts popularity score (0-100) to star rating (0-5)
   *
   * @param {number} popularity - Popularity score (0-100)
   * @returns {number} Star rating (0-5, with half-star precision)
   */
  export const popularityToStars = (popularity) => {
    if (popularity === undefined || popularity === null) return 0;
    
    // Convert 0-100 scale to 0-5 scale with half-star precision
    return Math.round((popularity / 100) * 10) / 2;
  };
  
  /**
   * Formats audio feature value to percentage with specified number of decimal places
   *
   * @param {number} value - Audio feature value (0-1)
   * @param {number} decimals - Number of decimal places
   * @returns {string} Formatted percentage
   */
  export const formatFeatureValue = (value, decimals = 0) => {
    if (value === undefined || value === null) return '0%';
    
    const percentage = (value * 100).toFixed(decimals);
    return `${percentage}%`;
  };
  
  /**
   * Generates a color code based on a value (0-1)
   * Used for heatmaps and visualizations
   *
   * @param {number} value - Value between 0 and 1
   * @param {string} colorScheme - Color scheme to use ('blue', 'green', or 'red')
   * @returns {string} HEX color code
   */
  export const getColorFromValue = (value, colorScheme = 'blue') => {
    if (value === undefined || value === null) return '#CCCCCC';
    
    // Ensure value is between 0 and 1
    const normalizedValue = Math.max(0, Math.min(1, value));
    
    // Calculate color based on scheme
    switch (colorScheme) {
      case 'blue':
        // Light blue (low) to dark blue (high)
        const blue = Math.floor(255 * (1 - normalizedValue * 0.7)).toString(16).padStart(2, '0');
        return `#0066${blue}`;
      
      case 'green':
        // Light green (low) to dark green (high)
        const green = Math.floor(255 * (1 - normalizedValue * 0.5)).toString(16).padStart(2, '0');
        return `#00${green}66`;
      
      case 'red':
        // Light red (low) to dark red (high)
        const red = Math.floor(255 * (1 - normalizedValue * 0.5)).toString(16).padStart(2, '0');
        return `#${red}0000`;
      
      default:
        // Grayscale as fallback
        const gray = Math.floor(255 * (1 - normalizedValue)).toString(16).padStart(2, '0');
        return `#${gray}${gray}${gray}`;
    }
  };
  
  /**
   * Gets appropriate text color (black or white) based on background color
   * to ensure readability
   *
   * @param {string} backgroundColor - HEX color code of background
   * @returns {string} HEX color code for text ('black' or 'white')
   */
  export const getTextColorForBackground = (backgroundColor) => {
    // Remove # if present
    const hex = backgroundColor.replace('#', '');
    
    // Convert to RGB
    const r = parseInt(hex.substr(0, 2), 16);
    const g = parseInt(hex.substr(2, 2), 16);
    const b = parseInt(hex.substr(4, 2), 16);
    
    // Calculate luminance
    const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;
    
    // Return black for light backgrounds, white for dark
    return luminance > 0.5 ? '#000000' : '#FFFFFF';
  };
  
  export default {
    formatDuration,
    formatLongDuration,
    formatDate,
    formatNumber,
    truncateText,
    popularityToStars,
    formatFeatureValue,
    getColorFromValue,
    getTextColorForBackground
  };