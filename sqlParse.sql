import pandas as pd
import glob,re
import itertools
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML


"""
https://gist.github.com/az0/0a5d4abcaac5b86a62df49115d634c66
"""
def is_subselect(parsed):
    if not parsed.is_group:
        return False
    for item in parsed.tokens:
        if item.ttype is DML and item.value.upper() == 'SELECT':
            return True
    return False


def extract_from_part(parsed):
    from_seen = False
    for item in parsed.tokens:
        if item.is_group:
            for x in extract_from_part(item):
                yield x
        if from_seen:
            if is_subselect(item):
                for x in extract_from_part(item):
                    yield x
            elif item.ttype is Keyword and item.value.upper() in ['ORDER', 'GROUP', 'BY', 'HAVING', 'GROUP BY']:
                from_seen = False
                StopIteration
            else:
                yield item
        if item.ttype is Keyword and item.value.upper() == 'FROM':
            from_seen = True


def extract_table_identifiers(token_stream):
    for item in token_stream:
        if isinstance(item, IdentifierList):
            for identifier in item.get_identifiers():
                value = identifier.value.replace('"', '').lower()
                yield value
        elif isinstance(item, Identifier):
            value = item.value.replace('"', '').lower()
            yield value


def extract_tables(sql):
    # let's handle multiple statements in one sql string
    extracted_tables = []
    statements = list(sqlparse.parse(sql))
    for statement in statements:
        if statement.get_type() != 'UNKNOWN':
            stream = extract_from_part(statement)
            extracted_tables.append(set(list(extract_table_identifiers(stream))))
    return list(itertools.chain(*extracted_tables))


basefolder = './data/sqlParse/'
infolder = basefolder + 'in/'
outfolder = basefolder + 'out/'
sqltables = []
#billed_redeemed
# billed_redeemed_expenses
filelist = glob.glob(infolder+ '*.mssql')
for fullpathwithfilename in filelist:
    # sql = open(fullpathwithfilename, 'r').read().replace('\n', ' ').replace('--','')
    sql = re.sub(r'--.*', '', open(fullpathwithfilename, 'r').read().lower()).replace('\n', ' ').replace('with (nolock)','')
    # print(sql)
    # parsed = sqlparse.parse(sql)
    # print(parsed)
    # print(len(extract_tables(sql)),len(set(extract_tables(sql))))
    sqlFileName = fullpathwithfilename.split('/')[-1]
    # print(extract_tables(sql))
    for table in extract_tables(sql):
        # print(table)
        if table.startswith('('):
            # print(type(table))
            tabSQL = table.strip()[1:table.rfind(')')]

            subTables = extract_tables(tabSQL)

            for subtable in subTables:
                if subtable.startswith('('):
                    subtabSQL = subtable.strip()[1:subtable.rfind(')')]
                    subsubTables = extract_tables(subtabSQL)
                    for subsubtable2 in subsubTables:
                        sqltables.append([sqlFileName, '@SubQuery-Level2', subsubtable2])

                else:
                    sqltables.append([sqlFileName,'@SubQuery-Level1', subtable])
        else:
            sqltables.append([sqlFileName, 'core', table])


tablesDfJoins = pd.DataFrame.from_records(sqltables, columns=['file','cat', 'table'])
tablesDfJoins.to_csv(outfolder  + 'ALL_entityList.tsv', header=True, sep='\t', index=False)
