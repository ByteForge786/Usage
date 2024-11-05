import re

def extract_sql_from_text(text):
    """
    Extracts SQL query from text that contains SQL code blocks marked with triple backticks.
    
    Args:
        text (str): Input text containing SQL code blocks
        
    Returns:
        str: Extracted SQL query or None if no SQL found
    """
    # Pattern to match SQL between triple backticks
    # Matches both ```sql and ''' sql variants
    pattern = r'(?:```|\'\'\')\s*sql\s*(.*?)\s*(?:```|\'\'\')'
    
    # Find the match using regex, with DOTALL flag to match across multiple lines
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    
    if match:
        # Extract and clean the SQL
        sql = match.group(1)
        # Remove any leading/trailing whitespace
        sql = sql.strip()
        return sql
    
    return None

# Example usage
if __name__ == "__main__":
    # Test cases
    test_texts = [
        '''
        Here is your SQL qyeurbsjjdnhaja
        
        ```sql
        SELECT * FROM users WHERE id = 1;
        ```
        
        This isnthe correct querysisbsha
        ''',
        
        '''
        Here is your SQL qyeurbsjjdnhaja
        
        '''sql
        SELECT id, name 
        FROM customers 
        WHERE status = 'active';
        '''
        
        This isnthe correct querysisbsha
        ''',
        
        # Test case with no SQL
        '''
        This is just regular text
        with no SQL code block
        '''
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTest case {i}:")
        print("Input text:")
        print("-" * 40)
        print(text)
        print("-" * 40)
        
        sql = extract_sql_from_text(text)
        print("Extracted SQL:")
        if sql:
            print(sql)
        else:
            print("No SQL found in the text")
