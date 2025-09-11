import re

# 📥 Paste your raw SQL block here
sql_text = """
    SHA2('{{ client }}' || '-' || IFNULL(TO_CHAR(CUST.RAWAUDIENCEID), '')
            || '-' || IFNULL(TO_CHAR(SFP.SEASONID), '')
            || '-' || IFNULL(TO_CHAR(KDPG.PLANTYPE), '')
            || '-' || IFNULL(TO_CHAR(KDPG.PLANSUBTYPE), ''), 512
        ) AS SKHASH,
    CUST.CUSTOMERKEY AS CUSTOMERKEY,
    CUST.RAWAUDIENCEID AS RAWAUDIENCEID,
    KFP.SEASONKEY,
    SFP.SEASONID,
    CASE
        WHEN CUST.CUSTOMERYRS IS NOT NULL
        THEN
            CASE
            WHEN SEAS.SEASONYEAR - YEAR(CUST.CUSTOMERSINCE) + 1 = 1               THEN 'Rookie (1st Year)'
            WHEN SEAS.SEASONYEAR - YEAR(CUST.CUSTOMERSINCE) + 1 = 2               THEN '2nd Year'
            WHEN SEAS.SEASONYEAR - YEAR(CUST.CUSTOMERSINCE) + 1 BETWEEN 3 AND 5   THEN '3-5 Years'
            WHEN SEAS.SEASONYEAR - YEAR(CUST.CUSTOMERSINCE) + 1 BETWEEN 6 AND 10  THEN '6-10 Years'
            WHEN SEAS.SEASONYEAR - YEAR(CUST.CUSTOMERSINCE) + 1 BETWEEN 11 AND 15 THEN '11-15 Years'
            WHEN SEAS.SEASONYEAR - YEAR(CUST.CUSTOMERSINCE) + 1 > 15              THEN '15+ Years'
            END
        ELSE NULL
    END AS TENURE,
    CUST.CUSTOMERYRS AS MEMBERSINCE,
    KDPG.PLANTYPE,
    KDPG.PLANSUBTYPE AS PLANSUBTYPE,
    MIN(KFP.COMPINDICATOR)
        OVER (PARTITION BY cust.RAWAUDIENCEID, SFP.SEASONID, KDPG.PLANTYPE, KDPG.PLANSUBTYPE) AS COMPINDICATOR,
    SC.STMCANCELINDICATOR AS CANCELINDICATOR,
    1 AS ACTIVE
"""

# 🔄 Replace '{{source}}' and '{{client}}' with env_var calls
sql_text = sql_text.replace("{{ source }}", "Archtics")
sql_text = sql_text.replace("{{source}}", "Archtics")
sql_text = sql_text.replace("{{client}}", "{{env_var('CLIENT')}}")

# ✂️ Smart splitter: handles nested parentheses and quotes
def smart_split(text):
    pieces, current, depth, quote = [], '', 0, None
    for char in text:
        if char in "'\"" and not quote:
            quote = char
        elif char == quote:
            quote = None
        elif char == "(" and not quote:
            depth += 1
        elif char == ")" and not quote:
            depth -= 1
        if char == "," and depth == 0 and not quote:
            pieces.append(current.strip())
            current = ''
        else:
            current += char
    if current:
        pieces.append(current.strip())
    return pieces

# 🧠 Parse each column into alias-expression pair
def extract_columns(sql_block):
    result = {}
    for part in smart_split(sql_block.replace("\n", " ")):
        part = part.strip()
        match = re.search(r"(.*?)\s+AS\s+(\w+)$", part, re.IGNORECASE | re.DOTALL)
        if match:
            expr, alias = match.groups()
            result[alias] = expr.strip()
        elif part:  # Handle columns without AS
            # Use last part after dot as key, full expression as value
            key = part.split('.')[-1] if '.' in part else part
            result[key] = part
    return result

# 🚀 Run the parser
columns_dict = extract_columns(sql_text)

# 🖨️ Print formatted output
# 🖨️ Print formatted output
for alias, expr in columns_dict.items():
    print(f'"{alias.upper()}": "{expr}",')